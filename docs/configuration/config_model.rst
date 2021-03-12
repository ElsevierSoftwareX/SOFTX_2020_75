.. _model_options:

********************
Model
********************

Before running DIETERpy, it is possible to configure several options regarding computational aspects as well as the size and features of the model. DIETERpy requires a specific folder structure in order to run properly which you see below. This structure is generated automtically as described :ref:`here <start-create-project>`.

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


Below there is a short description for every file. A more detailed description as well as further configurations and options are provided in the respective submenus.

+---------------------------------+------------+-----------------------------------------------------------------------------------------------+
| File name                       | Mandatory? |  Explanation                                                                                  |
+=================================+============+===============================================================================================+
|``manage.py``                    | yes        | Essential script to run the program or to convert gdx file to csv and other formats           |
+---------------------------------+------------+-----------------------------------------------------------------------------------------------+
|``project_variables.csv``        | yes        | Main options file to configure the project                                                    |
+---------------------------------+------------+-----------------------------------------------------------------------------------------------+
|``features_node_selection.csv``  | yes        | Enables (de-)activation of model features for each model node                                 |
+---------------------------------+------------+-----------------------------------------------------------------------------------------------+
|``iteration_table.csv``          | yes        | Stores information on the different scenario runs                                             |
+---------------------------------+------------+-----------------------------------------------------------------------------------------------+
|``iteration_data.xlsx``          | no         | Data to be changed over several model runs                                                    |
+---------------------------------+------------+-----------------------------------------------------------------------------------------------+
|``static_input.xlsx``            | yes        | Contains static (non time-varying) input parameter for the model                              |
+---------------------------------+------------+-----------------------------------------------------------------------------------------------+
|``timeseries_input.xlsx``        | yes        | Contains time-variant input parameter for the model                                           |
+---------------------------------+------------+-----------------------------------------------------------------------------------------------+
|``model.gms``                    | yes        | Contains the model itself (equations etc.), written in GAMS                                   |
+---------------------------------+------------+-----------------------------------------------------------------------------------------------+
|``constraints_list.csv``         | yes         | List of optional contraints that can be selected in different scenario runs                   |
+---------------------------------+------------+-----------------------------------------------------------------------------------------------+
|``reporting_symbols.csv``        | yes         | List of symbols (parameters, variables and equations) to be considered in the result reporting|
+---------------------------------+------------+-----------------------------------------------------------------------------------------------+

.. toctree::
   :maxdepth: 1

   project_variables
   features_nodes
   constraints.rst
   iteration.rst
   reporting.rst