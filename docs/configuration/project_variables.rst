Project variables 
-------------------

``project_variables.csv``: This file is the main option file. The file has three columns, ``feature``, which holds the variable name, ``value`` the value assigned, and ``comment``, which gives explanations. In the following, we briefly present all variables and their configuration options.

scenarios_iteration: *yes/no*
    If ``yes``, DIETERpy uses ``iteration_table.csv`` to run multiple scenario runs, which have to be configured properly prior to running the model. If ``no``, a single run is performed.

skip_input: *yes/no*
    Allows for skipping the generation of the necessary input gdx files from the input excel files. If ``yes``, the generation is skipped. Be aware, if skipped, the ``gdx_input folder`` must already contain the correct gdx files. This can be useful to reduce computation time if you want to run the model again using the same the input data. If ``no``, input excel files are transformed to input gdx files.

skip_iteration_data_file: *yes/no*
    If the ``iteration_data_file.xlsx`` sheet has not been changed between runs, you can use ``yes`` to reduce computation time and skip the creation of gdx files from excel files. If data have been changed, make sure to use ``no`` so that changes in the data are imported to the model.

base_year: e.g. *2030*
    Choose the year of the time series data. Only relevant if several years are provided in the input data. Verify this in ``timeseries_input.xlsx``.

end_hour: e.g. *h336*
    For testing purposes, the model can run from h1 to *end_hour*. Default value is ``h8760`` which represents an entire year.

dispatch_only: *yes/no*
    If you select ``yes``, the model will run in *dispatch only* mode, which means that power plant and storage capacities are fixed. Verify in the ``static_input.xlsx`` sheet that fixed values are provided. To run DIETERpy as an *investment and dispatch model*, select ``no``.

network_transfer: *yes/no*
    Select ``yes`` to allow for electricity flows between nodes. Select ``no`` to set cross-nodal electricity flows to zero.

no_crossover: *yes/no*
    Select ``yes`` to switch off *crossover* of the solver CPLEX. This settings is relevant when CPLEX uses the *Barrier Optimizer* to solve an LP.

infeasibility: *yes/no*
    Select ``yes`` to activate a slack variable in the energy balance of the model representing an unspecified generator. If demand cannot be met in a certain timestep, this generator will catch the missing generation, thus avoiding infeasibility of the optimization problem. Check the variable when debugging. Select ``no`` to deactivate this variable.

GUSS: *yes/no*
    Select ``yes`` to activate the "Gather-Update-Solve-Scatter" (GUSS) tool. The GUSS tool uses a `GAMSCheckpoint <https://www.gams.com/latest/docs/API_PY_TUTORIAL.html#PY_INIT_CHECKPOINT_RUNNING_JOB>`__ as a basis for solving several scenario runs. If several scenario runs are sufficiently similar (only single parameter or variable values varied), using the GUSS tool decrease the overall computation time to solve all scenarios because the model has to compiled only once. 

GUSS_parallel: *yes/no*
    If the *GUSS* is activated (see above), selection ``yes`` for this option will solve several scenario runs in parallel. Every scenario run is solved on single CPU thread, yet several scenarios at the same time in parallel. However, be aware that this option demands a high amount of RAM. If insufficient RAM is provided, the optimization can abort.

GUSS_parallel_threads: choose an integer, e.g. *4*
    This option defines the number of threads used to solve scenario runs in parallel. If ``0`` is chosen and *GUSS parallel* is ``yes``, then all available CPU threads are used. To avoid running out of RAM, you can either choose to reduce the number of threads used (hence smaller number) or deactivate the options *GUSS parallel* altogether.

static_input_file: filename e.g. *static_input.xlsx*
    Name of the file (in the folder ``data_input``) that contains the time-invariant data. If empty, the import of data is skipped.

timeseries_input_file: filename e.g. *timeseries_input.xlsx*
    Name of the file (in the folder ``data_input``) that contains the time-varying data. If empty, the import of data is skipped.

iteration_data_file: filename e.g. *iteration_data.xlsx*
    Defines the file name of the file that contains the data for scenario iteration (if data will be varied in different scenario runs). If empty, the import of data is skipped.

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