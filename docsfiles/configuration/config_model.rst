.. _model_options:

********************
Model
********************

Files
------

Before running DIETERpy, you are able to change several options regarding computational aspects as well as the size and features of the model. DIETERpy requires a specific folder structure in order to run properly which you see below.

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


Below there is a short description for every file. A more detailed description as well as further configurations and options are provided further down.

+---------------------------------+------------+-----------------------------------------------------------------------------------------------+
| File name                       | Mandatory? |  Explanation                                                                                  |
+=================================+============+===============================================================================================+
|``manage.py``                    | yes        | Essential script to run the program or to convert gdx file to csv and other formats           |
+---------------------------------+------------+-----------------------------------------------------------------------------------------------+
|``project_variables.csv``        | yes        | Main options file                                                                             |
+---------------------------------+------------+-----------------------------------------------------------------------------------------------+
|``features_node_selection.csv``  | yes        | Enables to (de-) activate certain features in certain nodes                                   |
+---------------------------------+------------+-----------------------------------------------------------------------------------------------+
|``iteration_main_file.csv``      | yes        | Stores information on the different scenario runs                                             |
+---------------------------------+------------+-----------------------------------------------------------------------------------------------+
|``iteration_data.xlsx``          | no         | Data to be changed over several model runs                                                    |
+---------------------------------+------------+-----------------------------------------------------------------------------------------------+
|``data_input.xlsx``              | yes        | Contains data on parameters                                                                   |
+---------------------------------+------------+-----------------------------------------------------------------------------------------------+
|``time_series.xlsx``             | yes        | Contains data on time-series                                                                  |
+---------------------------------+------------+-----------------------------------------------------------------------------------------------+
|``model.gms``                    | yes        | Contains the model itself (equations etc.), written in GAMS                                   |
+---------------------------------+------------+-----------------------------------------------------------------------------------------------+
|``constraints_list.csv``         | ?          | List of optional contraints that can be choosen in different scenario runs                    |
+---------------------------------+------------+-----------------------------------------------------------------------------------------------+
|``reporting_symbols.csv``        | ?          | List of symbols (parameters, variables and equations) to be considered in the data report     |
+---------------------------------+------------+-----------------------------------------------------------------------------------------------+

Project variables 
--------------------------------------------------------------------------------------

``project_variables.csv``: This file is the main option file. The file has three columns, ``feature``, which holds the variable name, ``value`` the value assigned, and ``comment`` which serves as an explanation. In the following, we present quickly all variables as well as their possible options.

scenarios_iteration: *yes/no*
    If ``yes``, DIETERpy uses ``iteration_main_file.csv`` to run multiple scenario runs, which has to be configured properly. If ``no``, a single run occurs.

skip_input: *yes/no*
    Generates the necessary input gdx files from the input excel files. If ``yes``, this generation is skipped, and the ``gdx_input folder`` must already contain the correct gdx files. This can be useful to save time if only the model has been changed without the data. If ``no``, input excel files are transformed to input gdx files.

skip_iteration_data_file: *yes/no*
    If the ``iteration_data_file.xlsx`` sheet has not been changed between runs, you can use ``yes`` to save time and skip the creation of gdx files from excel files. If data has been changed, make sure to use ``no`` so that changes in the data are imported to the model.

base_year: e.g. *2030*
    Choose the year of the time series data. Only relevant if several years are provided in the input data. Verify this in ``time_series.xlsx``.

end_hour: e.g. *h336*
    For testing purposes, the model can run from h1 to *end_hour*. Default value is ``h8760`` which represents an entire year.

dispatch_only: *yes/no*
    If you select ``yes``, the model will run in *dispatch only*, which means that power plant and storage capacities are fixed. Verify in the ``data_input.xlsx`` sheet that fixed values are provided. To run DIETERpy as an *investment and dispatch model*, select ``no``.

network_transfer: *yes/no*
    Select ``yes`` to allow for electricity flows between nodes. Select ``no`` to set cross-nodal electricity flows to zero.

no_crossover: *yes/no*
    Select ``yes`` to switch off *crossover* of the solver CPLEX. This settings is relevant when CPLEX uses the *Barrier Optimizer* to solve an LP.

infeasibility: *yes/no*
    Select ``yes`` to activate the infeasibility variable within the model. Select ``no`` to deactivate this variable. This variable can be useful to debug model runs. 

GUSS: *yes/no*
    ,no,"select 'yes' to activate GUSS tool"

GUSS_parallel: *yes/no*
    ,no,"select 'yes' to run parallel scenarios with GUSS tool, where every thread compiles only once, it helps speed up the optimization, although for complex problems     it may demand large RAM use"

GUSS_parallel_threads: *yes/no*
    ,0,"if zero and GUSS parallel is yes, then the model makes parallel runs using all available cores. When the model is too large, to avoid running out of     RAM, you can either choose, to reduce the number of parallel runs or deactivate GUSS parallel"

data_input_file: filename e.g. *data_input.xlsx*
    ,data_input.xlsx,"enter a file name. If empty, then import of time-invariant data is skipped"

time_series_file: filename e.g. *time_series.xlsx*
    ,time_series.xlsx,"enter a file name. If empty then import of time-variant data is skipped"

iteration_data_file: filename e.g. *iteration_data.xlsx*
    ,iteration_data.xlsx,"enter a file name. Holds time series data for iteration"

gdx_convert_parallel_threads
    ,0,"if zero then a maximum number of CPU cores will be in use"

gdx_convert_to_csv
    ,no,"select 'yes' to create a CSV file for each symbol. Files are hosted in folder 'CSV'"

gdx_convert_to_pickle
    ,yes,"select 'yes' to create a pickle file for each run. It contains a dictionary where keys are symbol names and values are symbol's pandas dataframe, this     pickle file is required for reporting files"

gdx_convert_to_vaex
    ,no,"select 'yes' to creates an hdf5 file for each run. A vaex dataframe contains all symbols. Files are larger but can be handled out of the RAM. Vaex     package has to be installed separately"

report_data
    ,yes,"select 'yes' to group symbols through scenarios. Files are saved in 'report' folder. These files are used for the web interface to plot the results"

Features in nodes (``features_node_selection.csv``)
--------------------------------------------------------------------------------------


Iteration Main File (``iteration_main_file.csv``)
--------------------------------------------------------------------------------------


Constrains (``constraints_list.csv``)
--------------------------------------------------------------------------------------


Reporting (``reporting_symbols.csv``)
--------------------------------------------------------------------------------------



