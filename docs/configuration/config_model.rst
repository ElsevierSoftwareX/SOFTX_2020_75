.. _model_options:

********************
Model
********************

Overview files
---------------

Before running DIETERpy, you are able to change several options regarding computational aspects as well as the size and features of the model. DIETERpy requires a specific folder structure in order to run properly which you see below.

.. code-block:: bash

    ├── firstproject
    │   ├── manage.py
    │   └── project_files
    │       ├── iterationfiles
    │       │   ├── iteration_table.csv
    │       │   └── iteration_data.xlsx
    │       ├── data_input
    │       │   ├── data_input.xlsx
    │       │   └── time_series.xlsx
    │       ├── model
    │       │   └── model.gms
    │       └── settings
    │           ├── project_variables.csv
    │           ├── features_node_selection.csv
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
|``iteration_table.csv``          | yes        | Stores information on the different scenario runs                                             |
+---------------------------------+------------+-----------------------------------------------------------------------------------------------+
|``iteration_data.xlsx``          | no         | Data to be changed over several model runs                                                    |
+---------------------------------+------------+-----------------------------------------------------------------------------------------------+
|``static_input.xlsx``            | yes        | Contains static (non time-varying) input data for the model                                   |
+---------------------------------+------------+-----------------------------------------------------------------------------------------------+
|``timeseries_input.xlsx``        | yes        | Contains time-varying input data for the model                                                |
+---------------------------------+------------+-----------------------------------------------------------------------------------------------+
|``model.gms``                    | yes        | Contains the model itself (equations etc.), written in GAMS                                   |
+---------------------------------+------------+-----------------------------------------------------------------------------------------------+
|``constraints_list.csv``         | ?          | List of optional constraints that can be chosen in different scenario runs                    |
+---------------------------------+------------+-----------------------------------------------------------------------------------------------+
|``reporting_symbols.csv``        | ?          | List of symbols (parameters, variables and equations) to be considered in the data report     |
+---------------------------------+------------+-----------------------------------------------------------------------------------------------+

.. toctree::
   :maxdepth: 1

   files/project_variables
   files/features_nodes
   files/iteration.rst
   files/constraints.rst
   files/reporting.rst