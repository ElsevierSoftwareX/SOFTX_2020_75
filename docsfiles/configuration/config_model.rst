.. _model_options:

********************
Model options
********************

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


As an alternative, you could also download the folder ``base`` (link_) in ``dieterpy/dieterpy/templates`` from our repository_ and place the folder ``basicmodeldata`` within ``base``. Of course, you are free to rename ``base``. This manual procedure equals the command ``$ dieterpy create_project -n firstproject``.


