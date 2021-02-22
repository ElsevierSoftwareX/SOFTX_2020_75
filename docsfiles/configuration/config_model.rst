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
    Select ``yes`` to activate the "Gather-Update-Solve-Scatter" (GUSS) tool. The GUSS tool uses a `"GAMSCheckpoint" <https://www.gams.com/latest/docs/API_PY_TUTORIAL.html#PY_INIT_CHECKPOINT_RUNNING_JOB>` as a basis for solving several scenario runs. If several scenario runs are sufficiently similar (only single parameter or variable values varied), using the GUSS tool decrease the overall time to solve all scenarios because the model has to compiled only once. 

GUSS_parallel: *yes/no*
    If the *GUSS* is activated (see above), selection ``yes`` for this option will solve several scenario runs in parallel. Every scenario run is solved on single CPU thread, yet several at the same time in parallel. However, be aware that this option demands a high amount of RAM. If insufficient RAM is provided, the optimization can abort.

GUSS_parallel_threads: choose an integer, e.g. *4*
    This option defines the number of threads used to solve scenario runs in parallel. If ``0`` is chosen and *GUSS parallel* is ``yes``, then all available CPU threads are used. To avoid running out of RAM, you can either choose to reduce the number of threads used (hence smaller number) runs or deactivate the options *GUSS parallel* altogether.

data_input_file: filename e.g. *data_input.xlsx*
    Name of the file (in the folder ``data_input``) that contains the time-invariant data. If empty, the import of data is skipped.

time_series_file: filename e.g. *time_series.xlsx*
    Name of the file (in the folder ``data_input``) that contains the time-varying data. If empty, the import of data is skipped.

iteration_data_file: filename e.g. *iteration_data.xlsx*
    Defines the file that contains the data for iteration (if data will be varied in different scenario runs). If empty, the import of data is skipped.

gdx_convert_parallel_threads: choose an integer, e.g. *4*
    Defines the number of CPU threads used to convert the output GDX files to other files. If ``0`` is chosen, the maximum number of CPU threads will be used.

gdx_convert_to_csv: *yes/no*
    Select ``yes`` to convert the GDX output files to CSV files. For every symbol (variables, parameter, equation), a separate CSV file will be created. The files are saved in folder named ``CSV`` within the output folder of each scenario run.

gdx_convert_to_pickle: *yes/no*
    Select ``yes`` to convert the GDX output files to PICKLE files. For every scenario run, a separate PICKLE file is created that stores all symbols (variables, parameter, equation) and their values. Important: these PICKLE files are required to created the *reporting files*.

gdx_convert_to_vaex: *yes/no*
    Select ``yes`` to convert the GDX output files to HDF5 files. For every scenario run, a separate HDF5 file is created that stores all symbols (variables, parameter, equation) and their values. HDF5 files are large but can be used out of RAM. IMPORTANT: the *vaex* package has to be installed before and separately for a successful conversion of files.

report_data: *yes/no*
    Select ``yes`` to create *report files* that contain the same symbols of all scenario runs. These files are saved in ``report`` folder and are used for the web interface to plot the results. To choose the symbols to be reported, you have to edit the file ``reporting_symbols.csv``. 

Features in nodes
--------------------------------------------------------------------------------------
``features_node_selection.csv``: In this file, you can switch on and off several submodules of the model for different nodes (countries).

The files looks as following (the comment column is not shown).

.. csv-table:: features_node_selection.csv
   :header: "feature","DE","FR","DK","BE","NL","PL","CZ","AT","CH","ES","IT","PT"

    "dsm",0,0,0,0,0,0,0,0,0,0,0,0
    "ev_endogenous",0,0,0,0,0,0,0,0,0,0,0,0
    "ev_exogenous",0,0,0,0,0,0,0,0,0,0,0,0
    "reserves",0,0,0,0,0,0,0,0,0,0,0,0
    "prosumage",0,0,0,0,0,0,0,0,0,0,0,0
    "heat",0,0,0,0,0,0,0,0,0,0,0,0

If a ``0`` is set in the respective cell, that particular module is not activated in that country. A ``1`` on the other side will activate that module in that country.

A brief description of the modules below:

dsm: Demand sight management
    Add brief description here.

ev_endogenous: Endogenous electric vehicles
    Add brief description here.

ev_exogenous: Exogenous electric vehicles
    Add brief description here.

reserves: Reserves
    Add brief description here.

prosumage: Prosumage
    Add brief description here.

heat: Heat provision
    Add brief description here.

Iteration Main File
--------------------------------------------------------------------------------------
``iteration_main_file.csv``: This file is central to define scenario runs. If only a single run is wished, this file can be left untouched.

The only required column is *run* as well as the respective number of each run (1, 2, 3, ...). To change data, countries, values, etc. between runs, the column headers of that file have to be changed accordingly which will be explained briefly in the following. 

Countries
^^^^^^^^^^^^^^^^^^^^^^^^^^

To vary the set of nodes between the different scenario runs, add the column ``country_set`` to the ``iteration_main_file.csv``. The row values of that column define the nodes to be considered for the respective run. No value means that all available nodes are included.

.. csv-table:: Example nodes
   :header: "run","country_set"

   1, 
   2, "DE"
   3, "DE,FR"

In this example, the first scenario run uses all available nodes (as provided ``data_input.xlsx``), the second run only Germany (``DE``), the third Germany and France (``"DE,FR"``). You will notice that the optimization time will be drastically lower for the 2nd and 3rd run. However, the model has to be recompiled between all three runs.

Data
^^^^^^^^^^^^^^^^^^^^^^^^^^

to be explained (time_series_scen)

Constrains
^^^^^^^^^^^^^^^^^^^^^^^^^^

to be explained.


Variables & parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^

Values of parameter and variables can be set by adding the name of that symbol as a column header to the ``iteration_main_file.csv``. You have to check in the ``model.gms`` file how exactly the symbol is called and defined. In the following, we provide some examples for better understanding.

Setting a value of a variable 
***************************************************

Let's assume you want to set the generation capacity of solar power in Germany to 25 GW in one run and to 50 GW in another run. First, you need to find the correct symbol for generation capacity in the GAMS model (``N_TECH(n,tech)``), then the identifier for solar power (``pv``), then the identifier for Germany (``DE``). In order to fix a variable to a specific value, you need to append ``.fx`` to the respective symbol name (before the brackets though). Then add the country and technology identifier with '' in the right place within the bracket. As ``N_TECH`` is defined in MV, you need to adjust your values accordingly.

In the first run, the PV capacity in Germany could be set freely (yet check possible limits in the ``data_input.xlsx`` file), set to 25 GW in the 2nd, and 50GW in the 3rd run:

.. csv-table:: Example variables
   :header: "run","country_set", "N_TECH.fx('DE','pv')"

   1, , 
   2, , 25000
   3, , 50000

Let's assume that you want to set these limits not only for Germany, but for all countries. Then your sheet has to look like the following. Note that ``'DE'`` has been replace by ``n`` (without ''), so it applies to the entire set ``n``:

.. csv-table:: Example variables
   :header: "run","country_set", "N_TECH.fx(n,'pv')"

   1, , 
   2, , 25000
   3, , 50000

Setting a (lower/upper) limit of variable value
***************************************************

Setting an lower or upper limit for a value of variable follows the same logic as fixing a value. Instead of appending ``.fx``, you append ``.lo`` for lower value and ``.up`` for upper value. Let's assume you want to set an lower limit for the generation capacity of PV in Germany (25 GW and 50 GW) and an upper limit to the generaetion capacity of nuclear power (10 GW and 5 GW). As reference, the first run does not define any limits:

.. csv-table:: Example variables
   :header: "run","country_set", "N_TECH.lo('DE,'pv')", "N_TECH.up('DE,'nuc')"

   1, , 
   2, , 25000, 10000
   3, , 50000, 5000

Setting a value of a parameter 
***************************************************

Setting a value of a parameter has the same logic as for a variable, except that you can leave out the suffices ``.fx .lo .up``. Let's assume you want to run a two-country scenario (DE & FR) and you want to set the share of renewable energy (``phi_min_res_exog(n)``) of Germany to 50% in the 1st, and to 75% in the 2nd run. In the 3rd and 4th run these values should apply to both countries. Whenever you leave a cell empty, the default value will be taken:

.. csv-table:: Example variables
   :header: "run","country_set", "phi_min_res_exog('DE')",  "phi_min_res_exog(n)"

   1,"DE,FR",0.50, 
   2,"DE,FR",0.75, 
   3,"DE,FR",    , 0.50
   4,"DE,FR",    , 0.75

In that same logic, you can vary the value of every parameter and variable in the entire model.

Constrains
--------------------------------------------------------------------------------------

``constraints_list.csv``: explanations will be added


Reporting
--------------------------------------------------------------------------------------

``reporting_symbols.csv``: explanations will be added




