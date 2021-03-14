.. _start-create-project:

******************************
Creating a project
******************************

Before running DIETERpy, you need first to create a new project. "Creating a new project" means setting up a folder structure that DIETERpy is able to read and process. You can either manually download a project from our Gitlab repository or use DIETERpy to create it. For a detailed description of the functionalities of DIETERpy and how to configure the model, please check out the next section :ref:`configuration <model_options>`.

In our example, we want to create a new project called *firstproject* and use the console to create the project folder. Thus either open the console in the folder, where you want to create the project folder (e.g. in Windows by right-clicking and shift and choosing *Open Windows Terminal here*), or navigate to the desired folder within the console. Before creating the new project, activate your conda environment as described in the last section.

Once you are in the desired folder, type the following command::

    $ dieterpy create_project -n firstproject

or::

    $ dieterpy create_project --name firstproject

.. warning:: We recommend to avoid blank spaces in the path that point to the project. Some GAMS versions do not recognize blanks spaces in paths and could come back with an error.

This command creates a folder and file structure as follows.

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

We describe the functions of these files serve in more detail in the :ref:`model configuration <model_options>` and :ref:`data configuration <data_options>` sections.

.. _link: https://gitlab.com/diw-evu/dieter_public/dieterpy/-/tree/master/dieterpy/templates/base
.. _repository: https://gitlab.com/diw-evu/dieter_public/dieterpy/