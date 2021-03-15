.. _prog_options:

************************
Command line interface
************************

In this section we present the comamnd line interface (CLI) to run our project and make use of useful functions for processing and visualization of results. 
The functions are ``create_project``, ``run``, ``gdxconvert``, ``create_report`` and ``web``. To execute all functions we have to call first ``dieterpy`` as shown below.


Create new project or copy a template
-------------------------------------

This function has been already introduced :ref:`here <start-create-project>`. By using the terminal you can navigate to the location you want to create your project folder, type the following command (*firstproject* will be the name of the new project and the new folder)::

    dieterpy create_project --name firstproject

We have used an argument in its two forms ``--name`` or ``-n`` to provide a directory name to our project folder. This argument is mandatory. 
There is another argument that can optionaly be provided whenever we want to copy a preset project.
we call it ``template`` and the argument is ``--template`` or ``-t``. This argument is followed by the name of the desired template. To get the list of available templates you can type instead ``--template_list`` or ``-tl``.

To get the templates' list:

.. code-block:: bash

    $ dieterpy create_project --template_list

To copy a template project:

.. code-block:: bash

    $ dieterpy create_project --name firstproject --template example1

An example is described :ref:`here <example1>`.


Run a model
----------------------

As described in previous :ref:`Model <model_options>` section. After the creation of a project folder and the customization of the model run by altering the configuration files, the optimization can be executed with the function ``run`` as follows:

.. code-block:: bash

    $ dieterpy run

The ``run`` function upmost target is run the optimization, but depending on the :ref:`project variables <project_variables>` selected, it would trigger subroutines in the following oder:

+ Data input conversion: Excel and CSV files that contain sets and parameters are converted to GDX file format.
+ Optimization with GAMS: Scenario iteration can run sequentialy, and with GUSS tool activated runs may carry out in parallel.
+ Data output conversion: For every scenario run, GAMS generates a GDX file that constains all symbols (sets, parameters, variables and equations), each GDX file can be converted to CSV, Pickle or Vaex file formats.
+ Reporting file creation: It collects all output files (pickle files only) and generates a new pickle file for every symbol (parameters, variables and equations) containing the respective symbol for each scenario result.

The function ``gdxconvert`` and ``create_report`` can be executed independently of the ``run`` function as described below.

.. hint:: The resulting files of a scenario run are hosted in the data_output folder within a dedicated scenario directory. The GDX files contain all symbols of the model and are kept for further access.


Convert output files
---------------------

The function ``gdxconvert`` can convert the GDX files hosted in the data_output folder to the CSV, Pickle or VAEX (hdf5) files. This function requires three arguments: ``--method``, ``--output`` and ``--cores``.

The argument ``--method`` or ``-m`` is mandatory. Two options can be selected: `global` or `custom`. The `global` option consists of searching on every child folder of the data_output folder and read the `.yml`. Such files contain relevant information about the respective scenario and the GDX files. Then it converts all scenarios' GDX files to the selected format. On the other hand, the `custom` option will request to provide the ID (scenario name = folder name) after hitting enter. This option is useful to convert only a few scenarios.

The argument ``--output`` or ``-o`` is optional, and three options can be selected. The options are `csv`, `pickle` and `vaex`. If we do not provide the ``--output`` argument, by default, the GDX files are converted to `pickle` as is the required format for the next function ``create_report``. If more than one option is required, then a hyphen must connect them, e.g. `vaex-csv`.

The argument ``--cores`` or ``-c`` is optional, and must be followed by an integer. It represent the number of cores we want to use to convert the files by processing every symbol in parallel and to speed up the conversion. If this argument is not provided then the function will choose the maximum number of cores available.

Example:

.. code-block:: bash

    $ dieterpy gdxconvert --method global --output csv-pickle --cores 1

In this example we want to convert all scenarios' results from GDX to CSV and Pickle file format, and using only one core for the conversion of every symbol in each GDX file.


Each format has a particular way to store the symbols that are contained in the GDX files:

+ CSV: Each symbol will be converted to a CSV file. All CSV files are then hosted in a dedicated directory within the scenario directory in the data_output folder.
+ Pickle: A dictionary is created where every pair key, value consists of symbol name and a pandas dataframe of the symbol respectively. The dictionary is saved into a pickle file.
+ Vaex: Each symbol will be converted to a vaex dataframe and saved in a temporal folder with extension `.hdf5`. Then all vaex dataframe contained in hdf5 files are concatenated to generate a large hdf5 file.

Vaex is a python package that enable large datasets to be manipulated without loading the data to the memory RAM. According to the authors, this library vaex is based on streaming algorithms, memory mapped files and a zero memory copy policy to allow exploration of datasets larger than memory (see `reference link`_).

.. _reference link: https://arxiv.org/abs/1801.02638

.. warning:: To generate VAEX data frames and save them with hdf5 format, the package must be installed beforehand. This can be done by typing :title:`>> pip install vaex`.

Create output report
----------------------

The function ``create_report`` consists of extracting from each scenario's pickle file a symbol at a time to create a new pickle file per symbol that contains all scenarios' symbol. This function does not have aditional arguments. The function generates an instance of a CollectScenariosPerSymbol class, this class looks through all pickle files in data_output folder. Each new pickle file is saved in a new directory named report_files.

To generate reporting files:

.. code-block:: bash

    $ dieterpy create_report

The default configuration is defined as follow:

.. code-block:: python

    >> Data = CollectScenariosPerSymbol()
    >> Data.collectinfo()
    >> Data.join_all_symbols("v", False)
    >> Data.join_scens_by_symbol("con1a_bal", "m", False, False)


From the above code snippet, the collectinfo method looks through all pickle files in the data_output folder to identify symbols in each file. The method join_all_symbols will use the information collected to extract symbol by symbol across all scenarios. The first argument can opt for two alternatives: ``v`` or ``m``. The option ``v`` stands for value for parameters or level for variables and equations, and ``m`` for marginal in variables and equations. We can infer from this piece of code that the function ``create_report`` collects all values or level from all symbols by default. From the equation `con1a_bal` representing the energy balance, the pickle file is generated with marginal values.

The default configuration enables us to generate the required data for visualization by using the browser interface described below.


Start graphical user interface
--------------------------------

To run the graphical user interface (GUI) for visualization of the results, the report_files folder must contain the pickle files of symbols.

To run the browser interface type as follows:

.. code-block:: bash

    $ dieterpy web

.. warning:: To be able to run a local server the package streamlit must be installed beforehand as well as plotly and matplotlib. This can be done by typing :title:`>> pip install streamlit; pip install plotly; pip install matplotlib==3.1.3`.

Once the browser has open, activate the report section in the left-hand side panel and click in load data. Different visualization alternatives will be available to iterpret and study the results. To see the list of symbols required for loadding properly the data, see the function ``get_results`` in the ``web_interface.py`` in the API, and then compare if the symbols are in the report_files folder.

.. warning:: Make sure to call ``dieterpy`` within the main project folder and ensure that the file manage.py is hosted there. This applies for all functions described here with the exception of ``create_project`` function.
