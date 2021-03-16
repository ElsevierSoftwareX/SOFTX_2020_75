****************
Running a model
****************

After having created a project folder (last section), you are ready to run the model. There are several ways to run the model, which are presented shortly here.

Method 1: from console (simple)
================================

Activate the conda environment in which you have installed DIETER. The active path in your console has to point the projected folder (make sure that the *manage.py* file is present).

You can start the optimization by typing::

    $ dieterpy run

Once the optimization has finished, you can analyze the output data. You find the output (depending on your configuration) in ``project_files/data_output`` and ``project_files/report_files``.

Method 2: from Python with installation (advanced)
===================================================

You can also run DIETERpy directly from the Python console. However, you have to provide some additional information in order to run the model successfully. 

Open a Python console (make sure that the correct conda environment is activated) and import the DIETERpy package:

.. code-block:: python

    >>> import dieterpy
    >>> from dieterpy.scripts import runopt
    >>> from dieterpy.config import settings

Then set the correct path so that DIETERpy finds your project folder:

.. code-block:: python

    >>> settings.PROJECT_DIR_ABS = "<here the absolute path to the project directory as string>"
    >>> settings.update_changes()

Run the model:

.. code-block:: python

    >>> runopt.main()

The runopt.main() function reads the configuration files and executes the optimization. Depending on the caracterisitcs the project and which features we (de-) activated,  the program generates a dictionary object with the location of generated files and also with additional information that is required by other functions. We can store such dictionary in a variable as follows:

.. code-block:: python

    >>> result_configuration_dict = settings.RESULT_CONFIG

There are functions that are called on runopt.main(). We can use such functions again in the python interpreter for a customized implementation. Some relevant are, for instance, `GDXpostprocessing` to convert GDX files or the class `CollectScenariosPerSymbol` to create reporting files. See the the functions :ref:`here <tool_api>`.

Method 3: from Python without installation (advanced)
=====================================================

It is also possible to run DIETERpy without installing the package. For that, you need to install the entire repository and ran the following commands from the Python console making sure that you are in the folder of DIETERpy:

.. code-block:: python

    >>> import dieterpy
    >>> from dieterpy.scripts import runopt
    >>> from dieterpy.config import settings

Then, you need to create a project *firstproject*, hence a structure of folders, of the following form and place the required files in the right folders.

.. Hint:: Setting up this folder structure and placing the files inside is what is done by the command ``dieterpy create_project`` as explained before.

.. code-block:: bash

    ├── firstproject
    │   ├── manage.py
    │   └── project_files
    │       ├── iterationfiles
    │       │   ├── iteration_table.csv
    │       │   └── iteration_data.xlsx
    │       ├── data_input
    │       │   ├── static_input.xlsx
    │       │   └── timeseries_input.xlsx
    │       ├── model
    │       │   └── model.gms
    │       └── settings
    │           ├── project_variables.csv
    │           ├── features_node_selection.csv
    │           ├── constraints_list.csv
    │           └── reporting_symbols.csv

Then set the correct path so that DIETERpy finds your project folder where *firstproject* is located in:

.. code-block:: python

    >>> settings.PROJECT_DIR_ABS = "<here the absolute path to the project directory as string>"
    >>> settings.update_changes()

Finally, run the model:

.. code-block:: python

    >>> runopt.main()

.. warning:: It could happen that the last command returns an error because of missing packages. If so, make sure to install the missing packages with PIP or Conda.