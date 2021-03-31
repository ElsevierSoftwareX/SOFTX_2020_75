# DIETERpy is electricity market model developed by the research group
# Transformation of the Energy Economy at DIW Berlin (German Institute of Economic Research)
# copyright 2021, Carlos Gaete-Morales, Martin Kittel, Alexander Roth,
# Wolf-Peter Schill, Alexander Zerrahn
"""

"""
import os
import yaml
import time
import pandas as pd
import shutil
from multiprocessing import Lock, Process, Queue, Manager, cpu_count

from .input_data import (
    getConfigVariables,
    getGlobalFeatures,
    generateInputGDX,
    prepareGAMSAPI,
    defineGAMSOptions,
    writeCountryOpt,
    writeConstraintOpt,
    getIterableDataDict,
    genStringOptData,
    genIterationDict,
    convert_par_var_dict,
    getGussVariables,
    setCountryIteration,
    setDataIteration,
    createModelCheckpoint,
    getConstraintsdata,
    getTopographydata,
    getGDXoutputOptions,
)

from .solve import scen_solve, guss_solve, guss_parallel
from .output_data import GDXpostprocessing, solver_status_summary
from .report import CollectScenariosPerSymbol
from ..config import settings

try:
    import streamlit as st

    st_installed = True
except ImportError:
    st_installed = False


def main():
    if st_installed:
        activate_st = st._is_running_with_streamlit
    else:
        activate_st = False
    if activate_st:
        show_bar_text = st.empty()
        bar = st.progress(0)
    print("::::::::::::::::::::::::::::")
    print("Start DIETER prepartion.")
    print("::::::::::::::::::::::::::::")

    ##### BASIC CONFIGURATION
    BASE = {}
    start_time_global = time.time()
    start_time_global_gm = time.gmtime()
    # String time part of unique name of scenarios. Files will contain this string at the beginning
    BASE["unique"] = time.strftime("%Y%m%d%H%M%S", start_time_global_gm)

    # create location paths
    BASE[
        "BASE_DIR_ABS"
    ] = settings.BASE_DIR_ABS  # absolute path to child folder of project directory
    BASE[
        "INPUT_DIR_ABS"
    ] = (
        settings.INPUT_DIR_ABS
    )  # absolute path to folder where input_data.xlsx and timeseries.xlsx are hosted
    BASE[
        "SETTINGS_DIR_ABS"
    ] = settings.SETTINGS_DIR_ABS  # absolute path to folder where
    BASE[
        "ITERATION_DIR_ABS"
    ] = (
        settings.ITERATION_DIR_ABS
    )  # absolute path to folder where constraints_list.csv and symbols.csv are hosted
    BASE[
        "RUN_DIR_ABS"
    ] = (
        settings.RUN_DIR_ABS
    )  # absolute path to folder where gams runs "ws.working_directory"
    BASE[
        "GDX_INPUT_ABS"
    ] = (
        settings.GDX_INPUT_ABS
    )  # absolute path to folder where inputs gdx files are hosted. 'RUN_DIR_ABS'  is its parent folder
    BASE[
        "RESULTS_DIR_ABS"
    ] = (
        settings.RESULTS_DIR_ABS
    )  # absolute path to folder where model output files are hosted
    BASE[
        "MODEL_DIR_ABS"
    ] = settings.MODEL_DIR_ABS  # absolute path to folder where model.gms is hosted
    BASE[
        "TMP_DIR_ABS"
    ] = settings.TMP_DIR_ABS  # absolute path to the folder for temp files

    # import control and scenario variables from config folder
    convar_dc = getConfigVariables(BASE["SETTINGS_DIR_ABS"])

    # generate input gdx files s.t. control variable skip_import
    active_gf, gdx_abspaths_dc = generateInputGDX(
        BASE["INPUT_DIR_ABS"],
        BASE["SETTINGS_DIR_ABS"],
        BASE["GDX_INPUT_ABS"],
        convar_dc,
    )

    # get switch values for all global features
    glob_feat_dc = getGlobalFeatures(BASE["SETTINGS_DIR_ABS"], active_gf)

    # Read list of constraints
    itercon_dc = getConstraintsdata(BASE["SETTINGS_DIR_ABS"])

    # Read in topology
    topography = getTopographydata(BASE["INPUT_DIR_ABS"], convar_dc)

    # Get iterable data
    data_it_dc, data_it_gdx = getIterableDataDict(
        BASE["ITERATION_DIR_ABS"], BASE["GDX_INPUT_ABS"], convar_dc
    )

    # Add data_it_gdx to gdx_abspaths_dc
    gdx_abspaths_dc["data_it_gdx"] = data_it_gdx

    ##### ITERATION CONFIG
    iteration_main_dict, list_constraints = genIterationDict(
        convar_dc, BASE["ITERATION_DIR_ABS"]
    )

    # Get guss tool configuration
    guss, parallel, guss_threads = getGussVariables(convar_dc)
    # save into BASE
    BASE["guss_tool"], BASE["guss_parallel"], BASE["guss_threads"] = (
        guss,
        parallel,
        guss_threads,
    )

    csv_bool, pickle_bool, vaex_bool, convert_cores = getGDXoutputOptions(convar_dc)

    # Get cpu cores
    cores = cpu_count()

    # # Save iteration_main_dict
    # os.makedirs(BASE['RESULTS_DIR_ABS'], exist_ok=True)
    # with open(os.path.join(BASE['RESULTS_DIR_ABS'], 'iteration_main_dict.yml'),'w') as f:
    #     yaml.dump(iteration_main_dict, f)
    if activate_st:
        show_bar_text.text(f"DIETER preparation finished")
        bar.progress(10 / 100)
    print(
        "DIETER preparation finished. It took %s minutes"
        % (round((time.time() - start_time_global) / 60, 1))
    )

    ###########################################################################
    # START LOOPING
    ###########################################################################

    print("::::::::::::::::::::::::::::")
    print("START DIETER solving")
    print("::::::::::::::::::::::::::::")

    BASE["RUNS"] = []
    BASE["tmp"] = {}
    barmax = len(iteration_main_dict.keys())
    for block, block_iter_dc in iteration_main_dict.items():
        print("----------------------------")
        print("Block run %s started" % block)
        print("----------------------------")
        # save temp BASE to be used later to contruct relevant BASE of each run
        BASE["tmp"][block] = {}
        BASE["tmp"][block]["str_block"] = "_b" + str(block).zfill(
            2
        )  # e.g. block=21 then after zfill(5) results 00021, five digits
        BASE["tmp"][block]["runs"] = block_iter_dc

        ############################
        # prepare GAMS API
        ############################

        ws, cp, opt = prepareGAMSAPI(BASE["RUN_DIR_ABS"])

        ############################
        # GLOBAL OPTIONS
        ############################

        opt = defineGAMSOptions(opt, glob_feat_dc, convar_dc, gdx_abspaths_dc)

        ############################
        # SET ITERATION
        ############################

        opt, countries, lines = setCountryIteration(opt, block_iter_dc, topography)

        ############################
        # CONSTRAINT ITERATION
        ############################

        # For every constraint, write GAMS option
        choosen_constraints = writeConstraintOpt(
            opt, block_iter_dc, list_constraints, itercon_dc
        )

        ###############################
        # DATA (TIME SERIES) ITERATION
        ###############################

        opt, data_scen_key = setDataIteration(opt, block_iter_dc)

        ###############################
        # Model Checkpoint and GDX
        ###############################

        cp_file, main_gdx_file = createModelCheckpoint(
            ws, opt, cp, BASE["MODEL_DIR_ABS"], data_it_dc, data_scen_key
        )

        BASE["tmp"][block]["cp_file"] = cp_file
        BASE["tmp"][block]["main_gdx_file"] = main_gdx_file

        ############################
        # PARAMETER
        ############################

        # Create parameter dict that will be used in this block
        dict_parameters_block = block_iter_dc["par_var"]

        #######################################################################
        # RUN MODEL
        #######################################################################

        # Collect information of used options for pass-through to gdx file name

        # used_constraints = list()
        # for con in list_constraints:
        #     used_constraints.append(block_iter_dc[con])
        # BASE['tmp'][block]['used_constraints'] = '-'.join(used_constraints)

        BASE["tmp"][block]["runs"].update(choosen_constraints)
        BASE["tmp"][block]["used_constraints"] = "-".join(
            list(choosen_constraints.values())
        )
        BASE["tmp"][block]["used_countries"] = countries.replace(",", "-")
        # BASE['tmp'][block]['used_lines']       = lines.replace(",", "-")
        BASE["tmp"][block]["used_data"] = data_scen_key

        # run several parameter/variable configurations per block
        if guss:
            guss_symbol_block, symbs = convert_par_var_dict(
                symbols_dict=dict_parameters_block
            )
            if parallel:
                with Manager() as manager:
                    block_results = manager.list()
                    queue = Queue()
                    for run, dc in guss_symbol_block.items():
                        queue.put((run, dc))
                    count = len(guss_symbol_block)
                    if guss_threads == 0:
                        nr_workers = min(count, cores)
                    elif guss_threads <= min(count, cores):
                        nr_workers = guss_threads
                    else:
                        print(
                            "GUSS_parallel_threads:",
                            guss_threads,
                            "is greater than ",
                            min(count, cores),
                            ". Minimum value is selected",
                        )
                        nr_workers = min(count, cores)
                    print("nr_workers", nr_workers)
                    queue_lock = Lock()
                    print_lock = Lock()
                    processes = {}
                    for i in range(nr_workers):
                        processes[i] = Process(
                            target=guss_parallel,
                            args=(
                                block_results,
                                queue,
                                queue_lock,
                                print_lock,
                                symbs,
                                BASE,
                                block,
                            ),
                        )
                        processes[i].start()
                    for i in range(nr_workers):
                        processes[i].join()
                    scenario_collection = list(block_results)
                BASE["RUNS"] += scenario_collection
            else:
                scenario_collection = guss_solve(guss_symbol_block, symbs, BASE, block)
                BASE["RUNS"] += scenario_collection
        # no guss tool then sequential model solve
        else:
            scenario_collection = []
            for run, dc in dict_parameters_block.items():
                # Solve DIETER model
                scenario_collection += scen_solve(dc, BASE, run, block)
            BASE["RUNS"] += scenario_collection
        if activate_st:
            show_bar_text.text(f"Problem block {block+1} of {barmax} finished")
            bar.progress((10 + (70 / barmax) * (block + 1)) / 100)

    summary_status = solver_status_summary("direct", BASE)
    print(summary_status)
    time.sleep(2)

    if not pickle_bool:
        with open(
            os.path.join(
                BASE["RESULTS_DIR_ABS"], BASE["unique"] + "_scenario_collection.yml"
            ),
            "w",
        ) as f:
            yaml.dump(BASE, f)

    elapsed_time_global = time.time() - start_time_global

    print("::::::::::::::::::::::::::::::::::::")
    print("ALL RUNS FINISHED")
    print("::::::::::::::::::::::::::::::::::::")
    print("Total calculation time:")
    print("Seconds: %s" % (round((elapsed_time_global), 2)))
    print("Minutes: %s" % (round((elapsed_time_global) / 60, 1)))
    print("Hours:   %s" % (round((elapsed_time_global) / 3600, 1)))
    print("::::::::::::::::::::::::::::::::::::")

    if activate_st:
        st.write("Optimization Status")
        st.dataframe(summary_status)

    print("GDX FILES CONVERSION")
    print("::::::::::::::::::::::::::::::::::::::")
    GDXpostprocessing(
        method="direct",
        input=BASE["RUNS"],
        csv_bool=csv_bool,
        pickle_bool=pickle_bool,
        vaex_bool=vaex_bool,
        cores_data=convert_cores,
        base=BASE,
    )
    settings.RESULT_CONFIG = BASE

    if pickle_bool:
        with open(
            os.path.join(
                BASE["RESULTS_DIR_ABS"], BASE["unique"] + "_scenario_collection.yml"
            ),
            "w",
        ) as f:
            yaml.dump(BASE, f)

    print("::::::::::::::::::::::::::::::::::::::")
    print("")
    if activate_st:
        show_bar_text.text(f"GDX files conversion finished")
        bar.progress(85 / 100)

    if convar_dc["report_data"] == "yes":
        print("REPORTING FILES")
        print("::::::::::::::::::::::::::::::::::::::")
        paths = [rundc["PKL_path"] for rundc in BASE["RUNS"]]
        Data = CollectScenariosPerSymbol(paths=paths, cores=convert_cores)
        Data.collectinfo()
        Data.join_all_symbols("v", False, False)
        Data.join_scens_by_symbol("con1a_bal", "m", False, False)
        if activate_st:
            show_bar_text.text(f"Reporting files created")
            bar.progress(95 / 100)
    if activate_st:
        time.sleep(2)
        show_bar_text.text(f"Program finished successfully")
        bar.progress(100 / 100)

    # Delete tmp folder
    shutil.rmtree(BASE["TMP_DIR_ABS"])

    print("::::::::::::::::::::::::::::::::::::::")
    print(":::::::::::::::FINISHED:::::::::::::::")
    return None


if __name__ == "__main__":
    main()
