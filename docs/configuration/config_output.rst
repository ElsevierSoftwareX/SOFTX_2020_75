.. _data_output:


.. |br| raw:: html

    <br>

******************
Output data
******************

GAMS generates GDX files that contains all symbols (GAMS nomenclature for parameters, variables and equations) 
of the model after finishing a scenario run. DIETERpy can generate two different output data types. The first 
option is to convert the GDX files to three file formats: Pickle, CSV and VAEX (HD5f). As each GDX file represents 
an scenario data, the generated files will also contain the same estructure. We call this files as `scenario files`. 
The second option consist of making a compilation of each symbol through all scenarios. What DIETERpy does in this 
case is to take scenario pickle files and generate a new pickle file for each symbol and put in there the symbol's 
data for each scenario. We call this kind of files as `reporting files`. |br|
CSV files can simply be open by text editor, but also with many other tools. As VAEX and pickle are python libraries, 
the HDf5 and pickle files can be open with any python interpreter. For the reporting files, DIETERpy provides two 
python classes that deal with the reporting files. They are called `SymbolHandler` and `Symbol`. `SymbolHandler` 
collects and read all reporting files and store relevant information from each file, such as, file path, symbol 
name, dimensions, sets names, etc. `Symbol` open/load the requested symbol and enables operations 
between them to generate new symbols by taking care of the dimensions and scenarios. For all the mentioned options it 
is recommended to use Jupyter notebooks or Spyder since they allow querying the data while we navigate in the data. 

GDX files
------------------

The number of GDX generated per scenario depends on the solving method either with or without GUSS tool 
(`Gather-Update-Solve-Scatter <https://new.gams.com/latest/docs/S_GUSS.html>`_). If we opt for the option to run our 
project without GUSS tool, DIETERpy will generate only one file, otherwise the tool will generate two files. DIETERpy 
save the scenario files in the `data_output` folder. In this folder the scenarios have their own folder, where the 
files are hosted. the name of the folder is the same as the scenario name. Here are also hosted the CSV files, pickle 
and HDf5 (VAEX). |br|
For end users who want to open the GDX files using the GAMS viewer. If the project run without GUSS tool, the GDX file 
will contain the name of the scenario. Otherwise, two files will be generated. GUSS tool only reports the variables 
and equation, and also provides the values of such symbols that are not present in the original configuration - the 
check point (CP) file - this file ends with ``_tmp.gdx``. Sometimes in our GAMS model we instanciate some variables 
with fixed values (VAR.fx), these ones are also included in the CP file. In order to get the variables in one piece, 
we use the GAMS tool ``diff`` to create a file that concatenate the variables and equation comparing two GDX files, 
file ends with ``_diff``.

.. hint:: The GDX file whose name ends with ``CP`` it stands for Check Point and contains only sets and parameters, 
    while variables and equation remain empty, with zeros or with the fixed values preset in the model.

Scenario files
------------------

DIETERpy handels the extraction of symbols in either case - one file for runs without GUSS tool or two files 
otherwise - with the help of the config file. The config file (scenario name + _config.yml) is also created for 
each scenario. It indicates the location of the GDX files and a boolean indicating the use of GUSS tool.

CSV
 The symbols are converted to CSV files that will be hosted in a folder called CSV in the scenario folder. |br|
Pickle
 The Python object structure can be serialized and de-serialized using the Pickle module that implements binary 
 protocols. Pickle files are compresed the gzip library. It Contains a python dictionary whose key is the symbol name and 
 the value is also a dictionary. This dictionary contains name of the symbol again, description, number of 
 dimentions, the dimensions in a lists, and a pandas dataframe with the symbol data. |br|
VAEX (HDf5)
 HDF5 is the binary data format used by the VAEX library to save VAEX dataframes objects. This library helps to 
 efficiently manipulate large datasets that are larger than the memory. It is beneficial if several scenario runs 
 are executed, and if their results are to be accessed at once. This is only one big file per scenario.


**Open files** |br|
Pickle:

.. code-block:: python

    import pickle
    import gzip
    with gzip.open('path_to_pickle_file') as file:
        scenario_dict = pickle.load(file)

VAEX (see `tutorial <https://vaex.readthedocs.io/en/docs/example_io.html#Binary-file-formats>`_):

.. code-block:: python

    import vaex
    df_names = vaex.open('path_to_hdf5_file')


Reporting files
------------------

.. so if you converted the GDX files to CSV or HDf5 this is not possible.


SymbolHandler and Symbol classes
-------------------------------------




Other files
------------------

Status
config
collection
stdout







