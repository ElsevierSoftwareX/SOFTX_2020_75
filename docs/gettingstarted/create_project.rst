******************************
Creating a project
******************************

Before running DIETERpy, you need first to create a new project. "Creating a new project" means setting up a folder structure that DIETERpy is able to read and process. You can either manually download a project from our Gitlab repository or use DIETERpy to create it. For a detailed description of the functionalities of DIETERpy and how to configure the model, please check out the next section configuration_.

.. _configuration: https://diw-evu.gitlab.io/dieter_public/dieterpy/gettingstarted/configuration

In our example, we want to create a new project called *firstproject* and use the console to create the project folder. Thus either open the console in the folder, where you want to create the project folder (e.g. in Windows by right-clicking and shift and choosing *Open Windows Terminal here*), or navigate to the desired folder within the console. Before creating the new project, activate your conda environment as described in the last section.

Once you are in the right folder, type the following command::

    dieterpy create_project -n firstproject

or::

    dieterpy create_project --name firstproject

.. warning:: We recommend to avoid blank spaces in the path that point to the project. Some GAMS versions do not recognize blanks spaces in paths (as documented `here <https://support.gams.com/platform:spaces_in_directory_or_file_name>`_) and could come back with an error.

This command creates a folder structure which looks like the following and has the following folders and files.

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

For now, you do not have to worry about all these files. A detailed description is provided HERE.

.. _link: https://gitlab.com/diw-evu/dieter_public/dieterpy/-/tree/master/dieterpy/templates/base
.. _repository: https://gitlab.com/diw-evu/dieter_public/dieterpy/