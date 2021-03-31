# DIETERpy is electricity market model developed by the research group
# Transformation of the Energy Economy at DIW Berlin (German Institute of Economic Research)
# copyright 2021, Carlos Gaete-Morales, Martin Kittel, Alexander Roth,
# Wolf-Peter Schill, Alexander Zerrahn
"""

"""
import os
import re
import csv
import glob
import time
import gzip
import yaml
import pickle
import secrets
import pandas as pd
from multiprocessing import Lock, Process, Queue, Manager, cpu_count
from gams import GamsWorkspace, GamsOptions, DebugLevel

from .gdx_handler import (
    gdx_get_set_coords,
    gdx_get_symb_info,
    gdx_get_symb_list,
    gdx_get_symb_recordnr,
    gdx_get_symb_recordnr_from_list,
    gdx_get_summary,
)

from ..config import settings


def get_solver_status(file):
    pattern = re.compile("LP status", re.IGNORECASE)  # Compile a case-insensitive regex
    with open(file, "rt") as myfile:
        for line in myfile:
            if pattern.search(line) != None:  # If a match is found
                return line.rstrip("\n")


def solver_status_summary(method=None, input=None):
    df = pd.DataFrame()
    firstones = ["run", "long_id"]
    lastones = ["System Costs [bn €]", "solver_msg"]
    ommit = firstones + lastones
    if method == "direct":
        for run_dc in input["RUNS"]:
            ndf = pd.DataFrame([{"run": run_dc["run_orig"]}])
            for k, v in run_dc["config"].items():
                ndf[k] = v
            ndf["System Costs [bn €]"] = round(run_dc["system_costs"] * 1e-9, 4)
            df = df.append(ndf)
        df = df.sort_values("run")
        df = df[firstones + [col for col in df.columns if col not in ommit] + lastones]
        df.to_csv(
            os.path.join(
                input["RESULTS_DIR_ABS"], input["unique"] + "_model_status.csv"
            ),
            index=False,
        )
    return df


def read_iteration_symbols(csvpath=None):
    """
    Read csv file with the modified symbols for the iteration.
    csvpath: string absolute file path
    it returns a list with dictionaries, each dictionary contains the required data to execute one run.
    Example: {SymbolA: {dims element : value}, SymbolB: {dims element : value}}
    """
    rawcsvdata = pd.read_csv(csvpath, header=[0, 1])
    # print(rawcsvdata)
    d = dict(
        zip(
            rawcsvdata.columns.levels[1],
            [i if "Unnamed" not in i else "." for i in rawcsvdata.columns.levels[1]],
        )
    )
    renameddata = rawcsvdata.rename(columns=d, level=1)
    symbgroup = renameddata.groupby(axis=1, level=0)
    datalist = []
    for symb, df in symbgroup:
        datalist.append(df.dropna(how="all"))
    dataproduct = pd.DataFrame(columns=pd.MultiIndex.from_product([["."], ["."]]))
    for df in datalist:
        df = df.join(
            pd.DataFrame(
                [0] * len(df),
                index=df.index,
                columns=pd.MultiIndex.from_product([["."], ["."]]),
            )
        )
        dataproduct = pd.merge(dataproduct, df, how="outer")
    data = dataproduct.drop((".", "."), axis=1)
    dc = data.T.to_dict()
    iterationlist = []
    for i, j in dc.items():
        tmp = {}
        for k, v in j.items():
            if k[0] in tmp.keys():
                tmp[k[0]].update({tuple(k[1].split(",")): v})
            else:
                tmp[k[0]] = {}
                tmp[k[0]].update({tuple(k[1].split(",")): v})
        iterationlist.append(tmp)
    return iterationlist


def get_symb_from_features(feat_ingdx, symbfile):
    df = pd.read_csv(symbfile)
    basicsymbset_plus_features = ["basic"] + feat_ingdx
    symbols_from_features = []
    for column in df.columns:
        if column in basicsymbset_plus_features:
            symbols_from_features = (
                symbols_from_features + df.loc[df[column].notna(), column].to_list()
            )
    return symbols_from_features


def gams_gdxdiff(gams_dir=None, maingdx=None, scengdx=None, newfile=None, base=None):
    start = time.time()

    tmp_path = base["TMP_DIR_ABS"]
    rnd = secrets.token_hex(8)
    tmp_path_unique = os.path.join(tmp_path, rnd)

    # Create tmp folder
    try:
        os.makedirs(tmp_path_unique)
        # print("Directory " , tmp_path_unique ,  " Created ")
    except FileExistsError:
        print("Directory ", tmp_path_unique, " already exists")

    ws = GamsWorkspace(
        system_directory=gams_dir,
        # debug=DebugLevel.KeepFiles,
        working_directory=tmp_path_unique,
    )
    jobs = ws.add_job_from_string(
        "execute 'gdxdiff %maingdx% %scengdx% %newfile% > %system.nullfile%'"
    )
    opt = GamsOptions(ws)
    opt.defines["newfile"] = f'"{newfile}"'
    opt.defines["maingdx"] = f'"{maingdx}"'
    opt.defines["scengdx"] = f'"{scengdx}"'
    jobs.run(gams_options=opt)
    # print(f'{scenario_dir} -> {symbname}: Elapsed time {round(time.time() - start, 3)} sec.')
    return None


def gams_gdxdumptocsv(gams_dir, scenario_dir_abspath, gdxfilename, symbname, base):
    start = time.time()

    tmp_path = base["TMP_DIR_ABS"]
    rnd = secrets.token_hex(8)
    tmp_path_unique = os.path.join(tmp_path, rnd)

    # Create tmp folder
    try:
        os.makedirs(tmp_path_unique)
        # print("Directory " , tmp_path_unique ,  " Created ")
    except FileExistsError:
        print("Directory ", tmp_path_unique, " already exists")

    ws = GamsWorkspace(system_directory=gams_dir, working_directory=tmp_path_unique)
    jobs = ws.add_job_from_string(
        "execute 'gdxdump %gdxfile% output=%dir%%syn%.csv symb=%syn% CSVAllFields format=csv EpsOut=0'"
    )
    opt = GamsOptions(ws)
    opt.defines["dir"] = f'"{scenario_dir_abspath}/"'
    opt.defines["syn"] = f'"{symbname}"'
    opt.defines["gdxfile"] = f'"{gdxfilename}"'
    jobs.run(gams_options=opt)
    # print(f'{scenario_dir} -> {symbname}: Elapsed time {round(time.time() - start, 3)} sec.')
    return None


def gams_gdxdumptocsv_parallel(queue, queue_lock, gams_dir, csv_dir, gdxfilelist, base):
    while True:
        queue_lock.acquire()
        if queue.empty():
            queue_lock.release()
            return None
        symbname = queue.get()
        queue_lock.release()
        for file in gdxfilelist:
            ret, _ = gdx_get_symb_info(
                gams_dir=gams_dir, filename=file, symbol=symbname
            )
            if ret:
                gams_gdxdumptocsv(gams_dir, csv_dir, file, symbname, base)
                break
            else:
                continue
    return None


def gams_csvtovaex_parallel(
    L,
    queue,
    queue_lock,
    list_lock,
    scen_name,
    block,
    gams_dir,
    csv_bool,
    pickle_bool,
    vaex_bool,
    main_gdx,
    diffgdxfile=None,
):
    """
    This function makes several actions to convert properly csv files that contain symbols.
    1. when the gdx file is created from GUSS Tool, it contains only symbols that were modified from the original model.
    In this case, this fuction compares the original gdx (before GUSS tool scenario) with the resulting gdx.
    It opens symbol csv files and also read the original gdx. Then it compares the headers if they are identical or not.
    a. When they are identical, it converts the csv file to pandas dataframes and vaex (eventually).
    b. When the headers are different. It makes two steps, first compares the columns and second ...
    """
    selected = ["Val", "Marginal", "Lower", "Upper"]
    common = ["Val", "Marginal", "Lower", "Upper", "Scale"]
    while True:
        queue_lock.acquire()
        if queue.empty():
            queue_lock.release()
            return None
        csvpath = queue.get()
        queue_lock.release()
        with open(csvpath) as csvFile:
            reader = csv.reader(csvFile)
            csv_header_list = next(reader)
        name = os.path.basename(csvpath).split(".")[0]
        if name[-6:] == "_Fixed":
            print(
                f"Symbol {name} has been ommited. It is created to handel {name[:-6]} variable for GUSS tool dict"
            )
            continue

        summary = gdx_get_summary(filename=main_gdx)
        sets_list = []
        for item in summary:
            if item["type"] == "set":
                flag = False
                for omited in ["headers", "map_", "*", "SameAs"]:
                    if item["name"].startswith(omited):
                        flag = True
                        break
                if not flag:
                    sets_list.append(item["name"])
        # print(*sets_list,sep='\n')

        dims_in_csv = [
            dim for dim in csv_header_list if dim not in common
        ]  # see the csv headers and select headers apart of Val, Marginal ...
        csv_header_set = set(dims_in_csv)

        _, maingdx_info = gdx_get_symb_info(
            gams_dir=gams_dir, filename=main_gdx, symbol=name
        )
        gdx_dims_set = set(maingdx_info["dims"])
        if csv_header_set.issubset(gdx_dims_set):
            common_header = csv_header_list[
                maingdx_info["nrdims"] :
            ]  # Val marginal and so on
            headers = maingdx_info["dims"] + [
                hd for hd in common_header if hd in selected
            ]
            df_pandas = pd.read_csv(csvpath, usecols=headers)
            if csv_bool:
                df_pandas.to_csv(csvpath, index=False)
            else:
                os.remove(csvpath)
            if pickle_bool:
                maingdx_info["data"] = df_pandas
            else:
                maingdx_info["data"] = None
            if vaex_bool:
                try:
                    import vaex

                    df_pandas = df_pandas.reindex(
                        columns=sets_list + selected + ["Symbol", "Block", "ID"]
                    )
                    df_pandas["Symbol"] = name
                    df_pandas["Block"] = block
                    df_pandas["ID"] = scen_name
                    df = vaex.from_pandas(df_pandas, copy_index=False)
                    df.export_hdf5(csvpath[:-4] + ".hdf5")
                except ImportError:
                    raise Exception('vaex is not installed. "pip install vaex"')
        else:
            if diffgdxfile is None:
                raise Exception(
                    f"Symbol {name} in csv has different headers than the file {main_gdx}. You must provide diffgdxfile"
                )
            else:
                _, diffgdx_info = gdx_get_symb_info(
                    gams_dir=gams_dir, filename=diffgdxfile, symbol=name
                )
                # print(name,'maingdx_info:',maingdx_info['nrdims'])
                # print(name,'diffgdx_info:',diffgdx_info['nrdims'])
            if maingdx_info["nrdims"] == diffgdx_info["nrdims"]:
                common_header = csv_header_list[
                    maingdx_info["nrdims"] :
                ]  # Val marginal and so on
                headers = maingdx_info["dims"] + [
                    hd for hd in common_header if hd in selected
                ]
                df_pandas = pd.read_csv(csvpath, usecols=list(range(len(headers))))
                df_pandas.columns = headers
                if csv_bool:
                    df_pandas.to_csv(csvpath, index=False)
                else:
                    os.remove(csvpath)
                if pickle_bool:
                    maingdx_info["data"] = df_pandas
                else:
                    maingdx_info["data"] = None
                if vaex_bool:
                    try:
                        import vaex

                        df_pandas = df_pandas.reindex(
                            columns=sets_list + selected + ["Symbol", "Block", "ID"]
                        )
                        df_pandas["Symbol"] = name
                        df_pandas["Block"] = block
                        df_pandas["ID"] = scen_name
                        df = vaex.from_pandas(df_pandas, copy_index=False)
                        df.export_hdf5(csvpath[:-4] + ".hdf5")
                    except ImportError:
                        raise Exception('vaex is not installed. "pip install vaex"')
            else:  # we assume that there is a new column in the diffgdx and hence in csv. In this case will will remove dif1 in this new column if exists
                common_header = csv_header_list[
                    diffgdx_info["nrdims"] :
                ]  # Val marginal and so on
                headers = csv_header_list[: diffgdx_info["nrdims"]] + [
                    hd for hd in common_header if hd in selected
                ]
                new_headers = maingdx_info["dims"] + [
                    hd for hd in common_header if hd in selected
                ]
                col_filter = csv_header_list[diffgdx_info["nrdims"] - 1]
                df_pandas = pd.read_csv(csvpath, usecols=headers)
                # print(name, col_filter, list(set(df_pandas[col_filter].to_list())))
                df_pandas = df_pandas[df_pandas[col_filter] != "dif1"]
                df_pandas = df_pandas.drop(col_filter, axis=1)
                df_pandas.columns = new_headers
                if csv_bool:
                    df_pandas.to_csv(csvpath, index=False)
                else:
                    os.remove(csvpath)
                if pickle_bool:
                    maingdx_info["data"] = df_pandas
                else:
                    maingdx_info["data"] = None
                if vaex_bool:
                    try:
                        import vaex

                        df_pandas = df_pandas.reindex(
                            columns=sets_list + selected + ["Symbol", "Block", "ID"]
                        )
                        df_pandas["Symbol"] = name
                        df_pandas["Block"] = block
                        df_pandas["ID"] = scen_name
                        df = vaex.from_pandas(df_pandas, copy_index=False)
                        df.export_hdf5(csvpath[:-4] + ".hdf5")
                    except ImportError:
                        raise Exception('vaex is not installed. "pip install vaex"')
        del df_pandas
        # maingdx_info['data'] = df_pandas
        list_lock.acquire()
        L.append(maingdx_info)
        list_lock.release()
    return None


def GDXpostprocessing(
    method="direct",
    input=None,
    cores_data=0,
    sysdir=None,
    csv_bool=True,
    pickle_bool=True,
    vaex_bool=True,
    base=None,
):
    if not any([csv_bool, pickle_bool, vaex_bool]):
        print("All formats are set to False. No conversion required.")
    else:
        if method == "direct":
            if input is None:
                raise Exception(
                    f"When method is {method}, input must be a list of dictionaries. Dictionary is an output of solve functions."
                )
            else:
                RUNS_list = input
        elif method == "global":
            if input is None:
                raise Exception(
                    f'When method is {method}, input must be a string path that match glob format. e.g "/user/project1/data_output/*/*_config.yml."'
                )
            else:
                RUNS_list = []
                for yml_path in glob.glob(input):
                    with open(yml_path, "r") as f:
                        RUNS_list.append(yaml.load(f, yaml.FullLoader))
        elif method == "custom":
            if input is None:
                raise Exception(
                    f"When method is {method}, input must be a list of strings. Absolute path to the corresponding scenario file *_config.yml."
                )
            else:
                RUNS_list = []
                for yml_path in input:
                    with open(yml_path, "r") as f:
                        RUNS_list.append(yaml.load(f, yaml.FullLoader))

        if vaex_bool:
            try:
                import vaex
            except ImportError:
                print('vaex is not installed. "pip install vaex"')
                vaex_bool = False
                print("vaex_bool has been set to False in scripts.GDXpostprocessing.")
        else:
            pass

        print("Generating temporal csv files of symbols per scenario...")
        cores = cpu_count()
        all_symb_count = 0
        start_csv = time.time()

        for resultdc in RUNS_list:
            start = time.time()
            symbfile = os.path.join(
                settings.BASE_DIR_ABS,
                resultdc["reporting_symbols_file"].rpartition(resultdc["BASE_DIR_ABS"])[
                    -1
                ][1:],
            )
            scen_name = resultdc["id"]
            scen_dir_abspath = os.path.join(
                settings.BASE_DIR_ABS,
                resultdc["id_dir"].rpartition(resultdc["BASE_DIR_ABS"])[-1][1:],
            )
            csv_dir_path = os.path.join(
                settings.BASE_DIR_ABS,
                resultdc["csv_dir"].rpartition(resultdc["BASE_DIR_ABS"])[-1][1:],
            )
            os.makedirs(csv_dir_path, exist_ok=True)

            if resultdc["guss_tool"]:
                gdxfilepath_tmp = os.path.join(
                    settings.BASE_DIR_ABS,
                    resultdc["tmp_gdx"].rpartition(resultdc["BASE_DIR_ABS"])[-1][1:],
                )
                main_gdx_file = os.path.join(
                    settings.BASE_DIR_ABS,
                    resultdc["checkpoint_gdx"].rpartition(resultdc["BASE_DIR_ABS"])[-1][
                        1:
                    ],
                )
                gdxfilepath = os.path.join(
                    settings.BASE_DIR_ABS,
                    resultdc["diff_gdx"].rpartition(resultdc["BASE_DIR_ABS"])[-1][1:],
                )
                # merge maingdx with gdx from guss
                gams_gdxdiff(
                    gams_dir=sysdir,
                    maingdx=main_gdx_file,
                    scengdx=gdxfilepath_tmp,
                    newfile=gdxfilepath,
                    base=base,
                )
            else:
                gdxfilepath = os.path.join(
                    settings.BASE_DIR_ABS,
                    resultdc["main_gdx"].rpartition(resultdc["BASE_DIR_ABS"])[-1][1:],
                )
                main_gdx_file = os.path.join(
                    settings.BASE_DIR_ABS,
                    resultdc["main_gdx"].rpartition(resultdc["BASE_DIR_ABS"])[-1][1:],
                )

            symbols_in_the_main_gdx = gdx_get_symb_list(
                gams_dir=sysdir, filename=main_gdx_file
            )  # gdxcc api
            features_in_the_main_gdx = gdx_get_set_coords(
                gams_dir=sysdir, filename=main_gdx_file, setname="feat_included"
            )  # gdxcc api
            preferred_symbols = get_symb_from_features(
                feat_ingdx=features_in_the_main_gdx, symbfile=symbfile
            )  # those symbols indicated in the symbols.csv file
            print(
                os.path.basename(main_gdx_file),
                "Columns from /settings/reporting_symbols.csv:\n",
                ["Basic"] + features_in_the_main_gdx,
            )
            pre_selected_symbols = [
                symb for symb in symbols_in_the_main_gdx if symb in preferred_symbols
            ]
            try:
                records = gdx_get_symb_recordnr_from_list(
                    gams_dir=sysdir,
                    filenamelist=[gdxfilepath, main_gdx_file],
                    symbolnamelist=pre_selected_symbols,
                )
                selected_symbols = [
                    symb for symb, recNr in records.items() if recNr > 0
                ]
            except:
                print("except")
                selected_symbols = pre_selected_symbols
            count_symb = len(selected_symbols)
            if cores_data == 0:
                nr_workers = min(count_symb, cores)
            else:
                nr_workers = cores_data
            # print('  Workers nr:', nr_workers)
            queue = Queue()
            for selected_symb in selected_symbols:
                queue.put(selected_symb)

            queue_lock = Lock()
            processes = {}
            for i in range(nr_workers):
                processes[i] = Process(
                    target=gams_gdxdumptocsv_parallel,
                    args=(
                        queue,
                        queue_lock,
                        sysdir,
                        csv_dir_path,
                        [gdxfilepath, main_gdx_file],
                        base,
                    ),
                )
                processes[i].start()
            for i in range(nr_workers):
                processes[i].join()
            end = time.time() - 1
            difftime = round(end - start, 2)
            print(f"  CSV dump {scen_name} in {difftime} sec...")
            all_symb_count += count_symb
        end_csv = time.time()
        diffcsv = round(end_csv - start_csv / 60, 1)
        ln = str(len(RUNS_list))
        print(
            f"{all_symb_count} symbols through {ln} gdx files finished in {diffcsv} min"
        )

        print("Converting temp csv files of symbols to pickle file per scenario...")
        for resultdc in RUNS_list:
            stime = time.time()
            scen_name = resultdc["id"]
            print(f"{scen_name} starting...")
            scen_dir_abspath = os.path.join(
                settings.BASE_DIR_ABS,
                resultdc["id_dir"].rpartition(resultdc["BASE_DIR_ABS"])[-1][1:],
            )
            csv_dir_path = os.path.join(
                settings.BASE_DIR_ABS,
                resultdc["csv_dir"].rpartition(resultdc["BASE_DIR_ABS"])[-1][1:],
            )
            block = resultdc["block"]
            if resultdc["guss_tool"]:
                main_gdx_file = os.path.join(
                    settings.BASE_DIR_ABS,
                    resultdc["checkpoint_gdx"].rpartition(resultdc["BASE_DIR_ABS"])[-1][
                        1:
                    ],
                )
                gdxfilepath = os.path.join(
                    settings.BASE_DIR_ABS,
                    resultdc["diff_gdx"].rpartition(resultdc["BASE_DIR_ABS"])[-1][1:],
                )
            else:
                main_gdx_file = os.path.join(
                    settings.BASE_DIR_ABS,
                    resultdc["main_gdx"].rpartition(resultdc["BASE_DIR_ABS"])[-1][1:],
                )
                gdxfilepath = os.path.join(
                    settings.BASE_DIR_ABS,
                    resultdc["main_gdx"].rpartition(resultdc["BASE_DIR_ABS"])[-1][1:],
                )

            csvpathlist = glob.glob(os.path.join(csv_dir_path, "*.csv"))
            csvpathlist = sorted(csvpathlist, key=os.path.getsize, reverse=True)
            # for path in csvpathlist:
            # print(path, os.path.getsize(path))
            with Manager() as manager:
                L = manager.list()
                queue = Queue()
                for csvpath in csvpathlist:
                    queue.put(csvpath)
                count = len(csvpathlist)
                if cores_data == 0:
                    nr_workers = min(count, cores)
                else:
                    nr_workers = cores_data
                print("  Workers nr:", nr_workers)
                queue_lock = Lock()
                list_lock = Lock()
                processes = {}
                for i in range(nr_workers):
                    processes[i] = Process(
                        target=gams_csvtovaex_parallel,
                        args=(
                            L,
                            queue,
                            queue_lock,
                            list_lock,
                            scen_name,
                            block,
                            sysdir,
                            csv_bool,
                            pickle_bool,
                            vaex_bool,
                            main_gdx_file,
                            gdxfilepath,
                        ),
                    )
                    processes[i].start()
                for i in range(nr_workers):
                    processes[i].join()
                listofsymbdicts = list(L)
            if pickle_bool:
                symbols_dict = {}
                symbols_dict["scenario"] = scen_name
                symbols_dict["loop"] = resultdc["config"]
                symbols_dict["scen_desc"] = resultdc["summary"]
                for symb_dict in listofsymbdicts:
                    symbols_dict[symb_dict["name"]] = {
                        "data": symb_dict["data"],
                        "dims": symb_dict["dims"],
                        "type": symb_dict["type"],
                        "symb_desc": symb_dict["desc"],
                        "symbol": symb_dict["name"],
                    }

                pkl_file = os.path.join(scen_dir_abspath, scen_name + ".pkl.gz")
                resultdc["PKL_path"] = pkl_file
                with gzip.open(pkl_file, "wb") as datei:
                    pickle.dump(symbols_dict, datei)
                print("  pickle done")
            print(
                " ", scen_name, "time:", str(round(time.time() - stime, 1)), "seconds"
            )

            if len(os.listdir(csv_dir_path)) == 0:  # check if folder csv is empty
                os.rmdir(csv_dir_path)  # Delete..

        if vaex_bool:
            print("Generating a vaex file per scenario...")
            for resultdc in RUNS_list:
                stime = time.time()
                scen_name = resultdc["id"]
                print(f"{scen_name} starting...")
                scen_dir_abspath = os.path.join(
                    settings.BASE_DIR_ABS,
                    resultdc["id_dir"].rpartition(resultdc["BASE_DIR_ABS"])[-1][1:],
                )
                csv_dir_path = os.path.join(
                    settings.BASE_DIR_ABS,
                    resultdc["csv_dir"].rpartition(resultdc["BASE_DIR_ABS"])[-1][1:],
                )
                vaex_file = os.path.join(scen_dir_abspath, scen_name + ".hdf5")
                df = vaex.open_many(glob.glob(os.path.join(csv_dir_path, "*.hdf5")))
                df.export_hdf5(vaex_file)
                for hdf5_path in glob.glob(os.path.join(csv_dir_path, "*.hdf5")):
                    os.remove(hdf5_path)
                if len(os.listdir(csv_dir_path)) == 0:  # check if folder csv is empty
                    os.rmdir(csv_dir_path)  # Delete..
                print(
                    " ",
                    scen_name,
                    "time:",
                    str(round(time.time() - stime, 1)),
                    "seconds",
                )
    return None
