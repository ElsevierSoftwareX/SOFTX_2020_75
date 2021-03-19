.. _data_output:

.. |br| raw:: html

    <br>

******************
Output data
******************

GAMS generates GDX files that contains all symbols (GAMS nomenclature for parameters, variables and equations) of the model after finishing a scenario run. DIETERpy can generate two different output data types: (1) The first option is to convert the GDX files to three file formats: Pickle, CSV and VAEX (HDF5). As each GDX file represents data of scenario run, the generated files also contain the same structure. These files are called `scenario files`. (2) The second option consist of making a compilation of each symbol over all scenarios. DIETERpy takes the pickle files of the individual scenario runs and generates a new pickle file for each symbol and joins the symbol's data of all scenario runs. These files are called `reporting files`.

CSV files can simply be opened by any text editor, but also with many other tools. As VAEX and pickle are Python libraries, the HDf5 and pickle files can be opened with any Python interpreter. For the reporting files, DIETERpy provides two specific Python classes that deal with the reporting files. They are called `SymbolHandler` and `Symbol`. `SymbolHandler` collects and reads all reporting files and stores relevant information from each file, such as, file path, symbol 
name, dimensions, sets names, etc. `Symbol` opens/loads the requested symbol and enables operations to generate new symbols by taking care of the dimensions and scenarios. For all the mentioned options it is recommended to use Jupyter notebooks or Spyder since they allow querying the data while navigating through the data. 

GDX files
------------------

DIETERpy the scenario files in the `data_output` folder. In this folder, every scenario has its own folder, in which the output files are saved. The name of the folder is the same as the scenario name. In this same folder, CSV files, pickle and HDF5 (VAEX) files are saved. The number of GDX files generated per scenario depends whether the solving is done with or without the GUSS tool (`Gather-Update-Solve-Scatter <https://new.gams.com/latest/docs/S_GUSS.html>`_). If the GUSS tool is not activated, DIETERpy will generate only one output GDX file; with the GUSS tool activated, two files output GDX files are generated. If the project is run without the GUSS tool, the GDX file will contain the name of the scenario. Th GUSS tool only reports the variables and equations and also provides the values of those symbols that are not present in the original configuration - the check point (CP) file - this file ends with ``_tmp.gdx``. In can happen that some variables with fixed values (VAR.fx) are defined, these ones are also included in the CP file. In order to have all variables in one file, we use the GAMS tool ``diff`` to create a file that concatenates the variables and equations comparing two GDX files. This file ends with ``_diff``.

.. hint:: The GDX file whose name ends with ``CP`` stands for *Check Point* and contains only sets and parameters. Variables and equations remain empty, with zeros or with the fixed values preset in the model.

Scenario files
------------------

DIETERpy handles the extraction of symbols - one file for runs without GUSS tool or two files otherwise - with the help of the config file. The config file (scenario name + _config.yml) is created for each scenario. It indicates the location of the GDX files and a boolean indicating the use of GUSS tool. The tool uses a GAMS function that converts all symbols in a GDX file to CSV files `gdxdump <https://www.gams.com/33/docs/T_GDXDUMP.html>`_. These files are stored temporary, as the tool requires them to process further in case the GUSS tool was used.

CSV
    Symbols are converted to CSV files that will be hosted in a folder called CSV in the scenario folder.

Pickle
    The Python object structure can be serialized and de-serialized using the Pickle module that implements binary protocols. Pickle files are compressed with the gzip library. It contains a Python dictionary whose key is the symbol name and the value is also a dictionary. This dictionary contains name of the symbol again, description, number of dimensions, the dimensions in a lists, and a pandas dataframe with the symbol data.

.. code-block:: python

    import pickle
    import gzip
    with gzip.open('path_to_pickle_file') as file:
        scenario_dict = pickle.load(file)

See the notebook below (:download:`Download <./open_scenario_files.ipynb>`)

.. include:: ./open_scenario_files.html

VAEX (HDF5)
    HDF5 is the binary data format used by the VAEX library to save VAEX dataframes objects. This library helps to efficiently manipulate large datasets that are larger than the available RAM of the computer. It is beneficial if several scenario runs are executed and if their results are to be accessed at once. Only one big file per scenario is created (see `tutorial <https://vaex.readthedocs.io/en/docs/example_io.html#Binary-file-formats>`_).

.. code-block:: python

    import vaex
    df_names = vaex.open('path_to_hdf5_file')

Reporting files
------------------

The reporting files consist of getting one to four files per symbol. These files are pickle files compressed with gzip. These kinds of files store a Python dictionary that contains as key the name of the scenario and as value another dictionary that contains symbol name, type of symbol, symbol description, dimensions, data, and three more elements that are useful for the functions and classes developed to manage the data. These three elements are `loop`, `scen`, and `modifiers`. To generate these reporting files, DIETERpy uses the `scenario files` by collecting the pickle files in the `data_output` folder. For doing this it uses the class `CollectScenariosPerSymbol` as described `here <create_report>`_.

.. _create_report: ../configuration/config_prog.html#create-output-report

.. warning:: To create reporting files, you need first to convert the GDX files to pickle files (CSV or HDF5 cannot be used as input to the reporting files).

See the notebook below (:download:`Download <./open_reporting_files.ipynb>`)

.. include:: ./open_reporting_files.html

CollectScenariosPerSymbol class
------------------------------------

*Explanations will be added soon*.

SymbolHandler and Symbol classes
-------------------------------------

*Explanations will be added soon*.

Other files
------------------

*Explanations will be added soon*.

Status

config

collection

stdout