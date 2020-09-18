Getting started
===============

Installation
++++++++++++

This library works on top of a GAMS model. Therefore, it is required to have installed GAMS with a corresponding license on your computer. GAMS system directory includes a Python API that must be installed. It is also recommended to install dieter in a dedicated conda environment. The following instructions describe how to install Anaconda to create a Python environment, how to install the Python API for GAMS, and after that the installation instructions of dieter that includes also all dependencies.

Installation of Anaconda
------------------------

Download Anaconda *Python 3.7 version* from https://www.anaconda.com/distribution/.

During the installation process of Anaconda, you will be asked for information, here our recommendations::
- Install Anaconda to a custom directory (such as C:/Anaconda or D:/Anaconda); Do not install in the default folder, because this will increase log-in and log-out out time (recommended for permission restricted computers);
- Do not use *C:/Programs/* or *C:/Program Files/* because this will require admin rights (recommended for permission restricted computers);
- During the installation process, select "advanced option" and check both boxes (despite not recommended by the application). This action adds the Conda Python version to the path and enables it as default python.

Create a new environment
------------------------

An environment is an isolated python space; different environments can contain packages of different versions. An environment is useful to have a reproducible and stable “working space”. The python version depends on the python API available in the GAMS directory. Our GAMS version (24.8) includes API_36, therefore we recommend creating an environment with Python 3.6 Version.

There are different ways on how to create a new environment.

*Anaconda navigator*

Start the Anaconda Navigator and go on Environment and click create.

Choose Use Packages Python 3.6.

*Anaconda Powershell (or Anaconda Prompt)*

Create a new environment "yourenvname" by typing into the promt/shell::

    conda create -n "yourenvname" python=3.6

Get an overview over all installed enviroments::

    conda info --envs


Installation of the Python API for GAMS
---------------------------------------

(Instructions come from here:: https://www.gams.com/latest/docs/API_PY_TUTORIAL.html)

Make sure you have activated the correct environment by typing::

    conda activate "yourenvname"

In the console (terminal, command-line or promp/shell), go to the folder which contains the Python 3.6 API files. For instance: `C:\GAMS\win64\24.8\apifiles\Python\api_36`. Hence::

    cd C:\GAMS\win64\24.8\apifiles\Python\api_36

In this folder, execute in the console::

    python setup.py install

Installation of DIETER
----------------------

while having activated the "yourenvname" environment install dieter by typing one of the two options.

*directly from PYPI*::

    pip install dieterpy



Uninstall DIETER
----------------

while having activated the "yourenvname" environment, type the following::

    pip uninstall dieter

Quick start
+++++++++++

Two basic steps are required to run a model or several model scenarios. First, is to create your project directory; and second, customize your scenarios and run.

Create a project directory
--------------------------

By doing this all the configuration files will be created in your desired location. In this example we will create our project directory in `D:\firstproject`. We have to provide a project name, in this case is `firstproject`.

in the console activate the "yourenvname" environment. and type::

    D:

your console will be located in the root of the disc D then type::

    dieter create_project -n firstproject

or::

    dieter create_project --name firstproject


After doing this, you will be able to navegate through `D:/firstproject` folder using the windows file explorer. The file and folder tree looks like the following:

.. code-block:: bash

    ├── firstproject
    │   ├── manage.py
    │   └── project_files
    │       ├── project_variables.csv
    │       ├── features_node_selection.csv
    │       ├── iterationfiles
    │       │   ├── iteration_main_file.csv
    │       │   └── iteration_data.xlsx
    │       ├── basicmodeldata
    │       │   ├── data_input.xlsx
    │       │   └── time_series.xlsx
    │       ├── model
    │       │   └── model.gms
    │       └── settings
    │           ├── constraints_list.csv
    │           └── reporting_symbols.csv


Here we have to explain the relevance of each file.
manage.py contain the script to run the program or to convert gdx file to csv and other formats.

.. csv-table::
   :header: "Filename", "Function"
   :widths: 15, 25

    "project_variables.csv", "control variables (mandatory)"
    "features_node_selection.csv", "indicates the relationship between nodes and features (mandatory)"
    "iteration_main_file.csv", "indicates the nodes, time-variant scenario name (detailed in iteration_data.xlsx), constraints, parameters and variables to modify in each run (mandatory)"
    "iteration_data.xlsx", "time-variant parameters and variables to be changed over several model runs (optional)"
    "data_input.xlsx", "contains the all the default time-independent parameters that are basic to run the model (mandatory)"
    "time_series.xlsx", "contains the all the default time-dependent parameters that are basic to run the model (mandatory)"
    "model.gms", "it has DIETER model script in written in GAMS language"
    "constraints_list.csv", "list of optional contraints based on a main constraint (column header)"
    "reporting_symbols.csv", "list of symbols (parameters, variables and equations) to be considered when converting gdx files to csv or/and pickle files. The symbols are selected for conveting each gdx files depending on the model features used for each scenario (or run, we have to choose which word suit best and be consistent through the document `scenario` or `run`)"


Run model
---------

there are two methods to run the model. From here on, bear in mind that the console must have activated our environment.

*Method 1: dieter (simple)*

locate the console inside the project folder, make sure the manage.py file is present. and type the following::

    dieter run

Once the optimization has finished, you can analyze the output data.

*Method 2: python console (advanced)*

this method can be used from a python console or jupyter notebook. In this case we have to provide some additional configurations associated with providing the absolute path to the project directory and importing dieter module.

Open a python console and type the following script (make sure to have the environment activated):


    >>> import dieter
    >>> from dieter.model import runopt
    >>> from dieter.config import settings

    >>> settings.PROJECT_DIR_ABS = "<here the absolute path to the project directory as string>"
    >>> settings.update_changes()

    >>> runopt.main()
    >>> result_configuration_dict = settings.RESULT_CONFIG


Troubleshooting
+++++++++++++++

pending

- GAMS_DIR env path in windows
- to Write absolute paths in windows, mac, and linux (in windows c:\\folder1\\folder2, mac and linux /home/folder1/folde2)
- run-out of memory for large models (to choose few cores in parallel, or run sequential)
