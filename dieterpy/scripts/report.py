# DIETERpy is electricity market model developed by the research group
# Transformation of the Energy Economy at DIW Berlin (German Institute of Economic Research)
# copyright 2021, Carlos Gaete-Morales, Martin Kittel, Alexander Roth,
# Wolf-Peter Schill, Alexander Zerrahn
"""

"""
import re
import sys
import glob
import os
import copy
import time

import gzip
import mgzip
import pickle
import numpy as np
import pandas as pd
import ntpath

from multiprocessing import Lock, Process, Queue, Manager, cpu_count
from ..config import settings


def parallel_func(dc, queue=None, queue_lock=None, function=None, kargs={}):
    while True:
        queue_lock.acquire()
        if queue.empty():
            queue_lock.release()
            return None
        key, item = queue.get()
        queue_lock.release()
        obj = function(item, **kargs)
        dc[key] = obj
        # sys.exit()
    return None


def parallelize(function=None, inputdict=None, nr_workers=1, **kargs):
    """
    input is a dictionary that contains numbered keys and as value any object
    the queue contains tuples of keys and objects, the function must be consistent when getting data from queue
    """
    with Manager() as manager:
        dc = manager.dict()
        queue = Queue()
        for key, item in inputdict.items():
            queue.put((key, item))
        queue_lock = Lock()
        processes = {}
        for i in range(nr_workers):
            if kargs:
                processes[i] = Process(
                    target=parallel_func, args=(dc, queue, queue_lock, function, kargs,)
                )
            else:
                processes[i] = Process(
                    target=parallel_func, args=(dc, queue, queue_lock, function,)
                )
            processes[i].start()
        for i in range(nr_workers):
            # print('   ', processes[i], processes[i].is_alive())
            processes[i].join()
            # print('   ', processes[i], processes[i].is_alive())
        outputdict = dict(dc)
    return outputdict


def open_file(path):

    # use parallel proc to open file
    # with mgzip.open(path, thread=cpu_count()) as pk:
    with gzip.open(path) as pk:
        dc = pickle.load(pk)
    return dc


class CollectScenariosPerSymbol:
    def __init__(self, paths=None, rng=None, cores = 0):
        self.cores = cores
        self.fixed = ["scenario", "loop", "scen_desc", "path"]
        if rng is None and paths is None:
            self.pkls = glob.glob("project_files/data_output/*/*.pkl.gz")
        elif paths is None:
            self.pkls = glob.glob("project_files/data_output/*/*.pkl.gz")[
                rng[0] : rng[1]
            ]
        elif rng is None:
            self.pkls = paths
        else:
            raise Exception("paths and rng can not be provided simultaneously")
        self.config = []
        inpdc = {}
        for i, v in enumerate(self.pkls):
            inpdc[i] = v
        if self.cores == 0:
            nr_workers = min(len(inpdc), cpu_count())
        else:
            nr_workers = min(len(inpdc), self.cores)

        outpdc = parallelize(function=self.from_pkl_remove_df, inputdict=inpdc, nr_workers = nr_workers)
        for ix in sorted(list(outpdc.keys())):
            self.config.append(outpdc[ix])

        self.convertiontable = {
            "v": "Val",
            "m": "Marginal",
            "up": "Upper",
            "lo": "Lower",
        }

    def from_pkl_remove_df(self, path):

        ## use parallel proc to open file
        # with mgzip.open(path, thread=cpu_count()) as pk:

        with gzip.open(path) as pk:
            dc = pickle.load(pk)
        for key in list(dc.keys()):
            if key not in self.fixed:
                dc[key].pop("data")
                dc["path"] = path
        return dc

    def scen_load(self, path, symbol):

        # with mgzip.open(path, thread=cpu_count()) as pk:
        with gzip.open(path) as pk:
            dc = pickle.load(pk)
            symbdc = dc[symbol]
        return symbdc

    def collectinfo(self, symbols=[]):
        data = copy.deepcopy(self.config)
        if symbols:
            symblist = self.fixed + symbols
            for idx, scen in enumerate(self.config):
                for ky in scen.keys():
                    if ky not in symblist:
                        data[idx].pop(ky)

        self.data = data
        self.symbols = [
            sy for sy in self.showsymbols(self.data) if sy not in self.fixed
        ]
        self.shortscennames = self.scenario_name_shortener(self.data)
        self.loopitems = self.get_loopitems(self.data)
        self.pathsbook = dict()
        print("Collecting scenarios data finished")
        print(
            "Now choose a method of a CollectScenariosPerSymbol instance by doing \neg.  instance.join_scens_by_symbol(symbol, result_col, loopinclude, warningshow), or\n     instance.join_all_symbols(result_col, loopinclude, warningshow)"
        )

    @staticmethod
    def ts(df):
        df.loc[:, "h"] = df.h.str.extract(r"(\d+)", expand=False).astype("int16")
        return df

    @staticmethod
    def showsymbols(data):
        ks = list()
        for sc in data:
            ks += list(sc.keys())
        return sorted(list(set(ks)))

    @staticmethod
    def scenario_name_shortener(data):
        flag = False
        pattern = re.compile(r"(\d+)", re.IGNORECASE)
        names = list()
        numbs = list()
        shortnames = dict()
        for scen in data:
            name = scen["scenario"]
            names.append(name)
            if pattern.search(name) != None:
                numbs.append(pattern.search(name)[0])
            else:
                flag = True
        names = sorted(names)
        if not flag:
            names_set = list(set(names))
            if len(names) == len(names_set):
                if len(names) == len(set(numbs)):
                    for name in names:
                        shortname = "S" + pattern.search(name)[0]
                        shortnames[name] = shortname
                        shortnames[shortname] = name
                else:
                    flag = True
            else:
                flag = True
        if flag:
            print(
                "New short names for scenarios. To know the corresponding \
                    scenario names type object.shortscennames"
            )
            for n in enumerate(names):
                shortname = "S" + str(n).zfill(3)
                shortnames[name] = shortname
                shortnames[shortname] = name
        return shortnames

    @staticmethod
    def get_loopitems(data):
        loopkeys = list()
        for scen in data:
            loopkeys += list(scen["loop"].keys())
        loopset = list(set(loopkeys))
        loopitems = dict()
        for loop in loopset:
            vals = list()
            for scen in data:
                if loop in scen["loop"].keys():
                    val = type(scen["loop"][loop]).__name__
                    if val in ["int"]:
                        bit = scen["loop"][loop].bit_length()
                        if bit < 16:
                            val = val + "16"
                        elif bit < 32:
                            val = val + "32"
                        else:
                            val = val + "64"
                    elif val == "float":
                        val = val + "16"
                    elif val == "str":
                        val = "category"
                    else:
                        raise Exception(
                            f"the iteration values in scenario {scen['scenario']} for the symbol '{loop}' is {scen['loop']}, not recognized as int,float or str"
                        )
                    vals.append(val)
            typ = sorted(list(set(vals)))[-1]  # the higest bit for all values
            loopitems[loop] = typ
        return loopitems

    @staticmethod
    def get_modifiers(scen, loopitems):
        loops = dict()
        for key, value in loopitems.items():
            if key in scen["loop"].keys():
                loops[key] = scen["loop"][key]
            else:
                if value == "category":
                    loops[key] = "NaN"
                elif "int" in value:
                    loops[key] = np.nan
                elif "float" in value:
                    loops[key] = np.nan
                else:
                    raise Exception("loop must contain int, float or string")
        return loops

    @staticmethod
    def add_scencols(
        scen, symbol, symbscen, shortscennames, loopitems, val_col, loopinclude
    ):
        df = symbscen["data"]
        scenname = scen["scenario"]
        shortn = shortscennames[scenname]
        dims = scen[symbol]["dims"]
        # write into df
        df.loc[:, "symbol"] = symbol
        df.loc[:, "id"] = shortn

        if loopinclude:
            loops = self.get_modifiers(scen, loopitems)
            for k in loopitems.keys():
                df.loc[:, k] = loops[k]
            return df[["id", *list(loopitems.keys()), "symbol", *dims, val_col]].copy()
        else:
            return df[["id", "symbol", *dims, val_col]].copy()

    def concatenation(self, symbol, flag, loopinclude, result_col, symblist):
        savefile = False

        symbdict = self.data[flag][symbol]

        if loopinclude:
            if len(symblist) > 1:
                savefile = True
                symbdict[result_col] = (
                    pd.concat(symblist)
                    .astype({k: typ for k, typ in self.loopitems.items()})
                    .astype(
                        {
                            k: "int16" if k == "h" else "category"
                            for k in symbdict["dims"]
                        }
                    )
                    .astype({k: "category" for k in ["id", "symbol"]})
                )
            elif len(symblist) == 1:
                savefile = True
                symbdict[result_col] = (
                    symblist[0]
                    .astype({k: typ for k, typ in self.loopitems.items()})
                    .astype(
                        {
                            k: "int16" if k == "h" else "category"
                            for k in symbdict["dims"]
                        }
                    )
                    .astype({k: "category" for k in ["id", "symbol"]})
                )
            else:
                print(f"   {symbol} does not have data in any scenarios provided")
        else:
            if len(symblist) > 1:
                savefile = True
                symbdict[result_col] = (
                    pd.concat(symblist)
                    .astype(
                        {
                            k: "int16" if k == "h" else "category"
                            for k in symbdict["dims"]
                        }
                    )
                    .astype({k: "category" for k in ["id", "symbol"]})
                )
            elif len(symblist) == 1:
                savefile = True
                symbdict[result_col] = (
                    symblist[0]
                    .astype(
                        {
                            k: "int16" if k == "h" else "category"
                            for k in symbdict["dims"]
                        }
                    )
                    .astype({k: "category" for k in ["id", "symbol"]})
                )
            else:
                print(f"   {symbol} does not have data in any scenarios provided")

        # queue.put((symbdict, savefile))
        return (symbdict, savefile)

    def symbol_dataframe_ready(self, scen, scenload_file_func, add_scencols_func, ts_func, shortscennames, loopitems, loopinclude, val_col, symbol):
        symb_scendict = scenload_file_func(scen["path"], symbol)
        dframe = add_scencols_func(
            scen,
            symbol,
            symb_scendict,
            shortscennames,
            loopitems,
            val_col,
            loopinclude,
        )
        if "h" in scen[symbol]["dims"]:
            dframe = ts_func(dframe)
        return dframe

    def join_scens_by_symbol(
        self, symbol, result_col="v", loopinclude=False, warningshow=True,
    ):
        """
        result_col: marginal or val
        self.data
        symbol
        """
        tmi = time.time()
        print(f"{symbol}.{result_col} --> Starting...")
        print(f"   Loading pkl files of scenario data")
        if result_col in self.convertiontable.keys():
            val_col = self.convertiontable[result_col]
        else:
            raise Exception(
                f"result_col is {result_col}, it must be one of the following: {list(self.convertiontable.keys())}"
            )
        sceninfo_dict = dict()
        for indx, scen in enumerate(self.data):
            if symbol in scen.keys():
                sceninfo_dict[indx] = scen
        # if self.cores == 0:
        #     nr_workers = min(len(sceninfo_dict), cpu_count())
        # else:
        #     nr_workers = min(len(sceninfo_dict), self.cores)

        # outputdict = parallelize(function = self.symbol_dataframe_ready,
        #                         inputdict = sceninfo_dict,
        #                         nr_workers = nr_workers,
        #                         scenload_file_func = self.scen_load, 
        #                         add_scencols_func = self.add_scencols, 
        #                         ts_func = self.ts, 
        #                         shortscennames = self.shortscennames, 
        #                         loopitems = self.loopitems, 
        #                         loopinclude = loopinclude, 
        #                         val_col = val_col, 
        #                         symbol = symbol)

        outputdict = {}
        for idx, scenario in sceninfo_dict.items():

            symbdf = self.symbol_dataframe_ready(scen = scenario,
                                    scenload_file_func = self.scen_load,
                                    add_scencols_func = self.add_scencols,
                                    ts_func = self.ts,
                                    shortscennames = self.shortscennames,
                                    loopitems = self.loopitems,
                                    loopinclude = loopinclude,
                                    val_col = val_col,
                                    symbol = symbol)
            outputdict[idx] = symbdf

        symblist = [v for v in outputdict.values()]

        flag = -1
        modifiers = dict()
        for ix, scen in enumerate(self.data):
            if symbol in scen.keys():
                modifiers[self.shortscennames[scen["scenario"]]] = self.get_modifiers(
                    scen, self.loopitems
                )
                flag = ix
            else:
                print(f'   Symbol "{symbol}" is not in {scen["scenario"]}')
        tmm = time.time()
        print(f"   Starting concatenation of dataframes. (Loading time {round(tmm-tmi)} s)")

        if flag > -1:
            symbdict, savefile = self.concatenation(symbol, flag, loopinclude, result_col, symblist)
            symbdict["scen"] = self.shortscennames
            symbdict["loop"] = list(self.loopitems.keys())
            symbdict["modifiers"] = modifiers

        else:
            savefile = False
            print(f'Symbol "{symbol}" does not exist in any scenario')

        if savefile:
            dest_dir = settings.REPORT_DIR_ABS
            dest_path = os.path.join(dest_dir, symbol + "." + result_col + ".pkl.gz")

            if symbol not in self.pathsbook.keys():
                self.pathsbook[symbol] = {}
            self.pathsbook[symbol][result_col] = dest_path
            tmc = time.time()
            print(f"   Saving file... (Concat time {round(tmc-tmm)} s)")
            self.to_pickle(dest_path, symbdict)
            print(f"   Final file size {round(os.path.getsize(dest_path)/10**6, 2)} mb. Saving time {round(time.time() - tmc)} s")
        print()

        if warningshow:
            print(
                'The info can be accessed by instance.pathsbook[symbol][result_col], result_col can be "v" for value or "m" for marginal'
            )
        return None

    def join_all_symbols(self, result_col, loopinclude=False, warningshow=True):
        for symb in self.symbols:
            self.join_scens_by_symbol(symb, result_col, loopinclude, False)
        if warningshow:
            print(
                'The info can be accessed by instance.pathsbook[symbol][result_col], result_col can be "v" for value or "m" for marginal'
            )

    def to_pickle(self, path, obj):

        pickleobj = pickle.dumps(obj, protocol=min(3, pickle.HIGHEST_PROTOCOL))

        if path.endswith(".pkl.gz"):
            folder = os.path.dirname(path)
            os.makedirs(folder, exist_ok=True)

            # use parallel proc to open file
            # define block size per cpu
            cpu_nr = max(cpu_count() - 1, 1)
            filesize = len(pickleobj)
            size_per_cpu = int(filesize/cpu_nr)
            if size_per_cpu > 3*10**6: # 3mb
                size_selected = 3*10**6
            elif size_per_cpu < 1*10**5: # 100kb
                size_selected = 1*10**5
            else:
                size_selected = size_per_cpu
            print(f'   Uncompressed file {round(filesize/10**6, 2)} mb. Chunk {round(size_selected/10**3, 1)} kb.')

            # with gzip.open(path, "wb") as datei:
            with mgzip.open(path, "wb", thread=0, blocksize=size_selected) as datei:
                datei.write(pickleobj)
            print(f"   File saved: {path}")
        else:
            print(f'   File {path} not saved. It does not have ".pkl.gz" extension')


class SymbolsHandler:
    def __init__(self, method, input=None):
        self.filelocacions = {}
        if method == "object":
            self.from_object(input)
        elif method == "folder":
            self.from_folder(input)
        else:
            raise Exception('A method mus be provided from either "object" or "folder"')
        self.symbol_list = []
        self.get_symbolnames()
        self.loop_list = []
        self.get_loopitems()

    def from_object(self, object):
        self.filelocacions = object.pathsbook

    def from_folder(self, folder_path=None):
        if folder_path is None:
            self.folder_path = settings.REPORT_DIR_ABS
        else:
            self.folder_path = folder_path

        files = glob.glob(os.path.join(self.folder_path, "*.pkl.gz"))
        for file in files:
            self.add_symbolfile(file)

    def get_symbolnames(self):
        for name in self.filelocacions.keys():
            self.symbol_list.append(name)

    def get_loopitems(self):
        looplist = []
        for name in self.symbol_list:
            for k, v in self.filelocacions[name].items():
                looplist = looplist + self.get_data(name, k)["loop"]
                break  # if this name has more than one valuetype 'v', 'm', 'up', 'lo' then takes only one, since it is about the same symbol.
        self.loop_list = list(set(looplist))

    def add_symbolfile(self, path):
        symbol, valuetype = ntpath.basename(path).rstrip(".pkl.gz").split(".")
        if symbol not in self.filelocacions.keys():
            self.filelocacions[symbol] = {}
        self.filelocacions[symbol][valuetype] = path

    def get_data(self, name, valuetype):
        return open_file(self.filelocacions[name][valuetype])


# utils
def argmax(l):
    def f(i):
        return l[i]

    return max(range(len(l)), key=f)


def argmin(l):
    def f(i):
        return l[i]

    return min(range(len(l)), key=f)


class Symbol(object):
    def __init__(
        self,
        name,
        value_type,
        unit,
        header_name,
        dims=None,
        symbol_type=None,
        index=["id"],
        symbol_handler=None,
    ):
        self.__dict__["_repo"] = {}
        self.exists_sh = True
        self.name = name
        self.value_type = value_type
        self.unit = unit
        self.header_name = header_name
        self.symbol_type = symbol_type
        self.dims = dims
        self.index = index + ["symbol"]  # must be a list
        self.preferred_index = index  # must be a list
        self.data = None  # represents df
        self.modifiers = None
        self.symbol_handler = symbol_handler
        self.extend_header = ""

        self.check_handler()
        self.check_inputs()
        self._repo["conversion_table"] = {
            "v": "Val",
            "m": "Marginal",
            "up": "Upper",
            "lo": "Lower",
        }
        self._repo["conversion_factors"] = {
            "MWh": {"GWh": 1e-3, "TWh": 1e-6, "MWh": 1},
            "GWh": {"MWh": 1e3, "TWh": 1e-3, "GWh": 1},
            "TWh": {"MWh": 1e6, "GWh": 1e3, "TWh": 1},
            "MW": {"GW": 1e-3, "TW": 1e-6, "MW": 1},
            "GW": {"MW": 1e3, "TW": 1e-3, "GW": 1},
            "TW": {"MW": 1e6, "GW": 1e3, "TW": 1},
            "h": {"h": 1},
            "%": {"": 0.01, "%": 1},
            "": {"%": 100, "": 1},
            "€/MW": {"€/MW": 1},
            "€": {"€": 1},
        }
        self.check_value_type()
        self.get_modifiers()
        # self.get_index_rest()
        # self.id_dict()

    def fill_data(self):
        temp = self.get("symbol_handler").get_data(
            self.get("name"), self.get("value_type")
        )
        self.symbol_type = temp["type"]
        self.dims = temp["dims"]
        self.index = ["id", "symbol"] + temp["loop"]
        del temp

    def check_handler(self):
        if isinstance(self.get("symbol_handler"), SymbolsHandler):
            self.exists_sh = True
            if self.get("name") in self.get("symbol_handler").symbol_list:
                self.fill_data()
            else:
                self.exists_sh = False
        else:
            self.exists_sh = False

    def check_inputs(self):
        if not self.get("exists_sh"):
            if (
                self.get("symbol_type") is None
                or self.get("dims") is None
                or self.get("index") is None
            ):
                raise Exception(
                    "At least one of the following argument is missing 'symbol_type' 'dims' 'index'"
                )

    def check_value_type(self):
        if self.get("value_type") in self._repo["conversion_table"]:
            pass
        else:
            raise Exception(
                "value_type argument must be either 'v', 'm', 'lo', or 'up'"
            )

    def check_index(self):
        if isinstance(self.get("preferred_index"), list):
            for index in self.get("preferred_index"):
                if not index in self.get("index"):
                    raise Exception(
                        f"'{index}' in preferred_index does not exists in the symbols data (columns of dataframe)"
                    )
        else:
            raise Exception("preferred_index must be a list")

    def update_index(self, preferred_index):
        self.preferred_index = preferred_index

    # def get_index_rest(self):
    #     self.index_rest = [x for x in self.get('preferred_index') if x != 'id']

    # def id_dict(self):
    #     if self.get('index_rest'):
    #         smalldf = self.df[self.get('preferred_index')]
    #         id_items = list(smalldf['id'].unique())
    #         id_dict = {}
    #         for id_item in id_items:
    #             dc = {}
    #             for rest in index_rest:
    #                 dc[rest] = list(smalldf[rest].unique())[0]  # it should be only one
    #             id_dict[id_item] = dc
    #         self.index_rest = dc

    # TODO: send a warning when after operation resultin dataframe is empty
    # TODO: Add new index items, for example actual res_share per scenario
    # TODO: Check header_name contains at least one entry of the current unit

    def get_df(self):
        if self.get("exists_sh"):
            df = self.get("symbol_handler").get_data(
                self.get("name"), self.get("value_type")
            )[self.get("value_type")]
            df = df.drop(
                df.columns.difference(
                    self.get("preferred_index")
                    + ["symbol"]
                    + self.get("dims")
                    + [self._repo["conversion_table"][self.get("value_type")]]
                ),
                axis=1,
            )
            df = df.rename(
                columns={
                    self._repo["conversion_table"][self.get("value_type")]: "value"
                }
            )
            return df.reset_index(drop=True)
        else:
            if self.get("data") is None:
                raise Exception("No dataframe has been provided")
            return self.get("data")

    def set_df(self, df):
        if not self.get("exists_sh"):
            self.data = df

    def get_modifiers(self):
        if self.get("exists_sh"):
            loops = self.get("symbol_handler").get_data(
                self.get("name"), self.get("value_type")
            )["modifiers"]
            self.modifiers = pd.DataFrame(loops).transpose().to_dict()

    @property
    def df(self):
        return self.get_df()

    def get(self, name):
        if name == "df":
            return self.get_df()
        else:
            return self._repo[name]

    @property
    def dfm(self):
        dfm = self.get_df()
        for k, v in self.get("modifiers").items():
            dfm[k] = dfm["id"].map(v)
        return dfm

    def dfmdr(self, dim='h', nan = False, aggfunc='sum'):
        '''
        dfmdr stands for dataframe with modifiers and dimension reduction
        dim are the list of dimension to be Reduced with sum(), default 'h'
        nan convert numeric columns, nan to -1 when value is True
        '''
        new_dims = list(set(self.get("dims")).symmetric_difference(set([dim])))
        dfmdr = (
            self.df.set_index(self.get("preferred_index") + self.get("dims"))
            .drop("symbol", axis=1)
            .sort_index()
        )
        if dim in self.get("dims"):
            dfmdr = dfmdr.groupby(self.get("preferred_index") + new_dims).agg({'value':aggfunc}).reset_index()
        else:
            dfmdr = dfmdr.reset_index()
            
        for k, v in self.get("modifiers").items():
            dfmdr[k] = dfmdr["id"].map(v)
        dfmdr.insert(1, "symbol", self.get("name"))
        if nan:
            numeric_columns = dfmdr.select_dtypes(include=['number']).columns
            dfmdr[numeric_columns] = dfmdr[numeric_columns].fillna(-1)
        return dfmdr

    def __setattr__(self, name, value):
        if name == "df":
            self.set_df(value)
        elif name == "header_name":
            if not "header_name" in self._repo:
                self._repo[name] = {}
            self._repo[name].update(value)
        elif name == "preferred_index":
            self._repo[name] = value
            self.check_index()
        elif name == "name":
            if not self.get("exists_sh"):
                self._repo[name] = value
                if self.get("data") is not None:
                    self.get("data").loc[:, "symbol"] = value
            else:
                self._repo[name] = value
        else:
            self._repo[name] = value

    def show(self, unit=None, extend_header=None):
        if unit is None:
            unit = self.get("unit")
        if extend_header is not None:
            self.extend_header = extend_header + " " + self.get("extend_header")
        return self.convert_dataframe(unit)

    def showm(self, unit=None, extend_header=None):
        if unit is None:
            unit = self.get("unit")
        if extend_header is not None:
            self.extend_header = extend_header + " " + self.get("extend_header")
        return self.convert_dataframe(unit, mod=True)

    def convert_dataframe(self, unit, mod=False):
        # TODO: Add new index items, for example actual res_share per scenario
        if mod:
            df = self.dfm
            df = df.set_index(
                self.get("preferred_index") + list(self.get("modifiers").keys())
            )
        else:
            df = self.df
            df = df.set_index(self.get("preferred_index"))
        if unit not in self.get("header_name").keys():
            raise Exception(f"Add first '{unit}' to self.get('header_name')")
        df = df.rename(
            columns={"value": self.get("extend_header") + self.get("header_name")[unit]}
        )
        df = df.drop(
            df.columns.difference(
                self.get("dims")
                + [self.get("extend_header") + self.get("header_name")[unit]]
            ),
            axis=1,
        )

        if self.get("dims"):
            df = self.reorganize(df, self.get("dims"), self.get("name"))
        df = df * self._repo["conversion_factors"][self.get("unit")][unit]
        return df

    def reorganize(self, df, cols, original_name):
        try:
            return df.set_index(cols, append=True).unstack(cols).fillna(0)
        except ValueError as err:
            print(f"Failure while executing: {err}.")
            print(
                "If this transformation involved the merge of two dataframes, make sure Index does not contain duplicate entries."
            )
            print(
                "This issue is solved by calling pivot tables instead of unstack in Pandas Dataframes, where duplicates are added up."
            )
            print(f'Conflictive symbol: "{original_name}"')
            return (
                df.reset_index()
                .pivot_table(
                    index=self.get("preferred_index"),
                    columns=cols,
                    values=df.columns.difference(self.get("preferred_index") + cols),
                    aggfunc=sum,
                )
                .fillna(0)
            )

    def __add__(self, other):
        flag = False
        if set(self.get("dims")) == set(other.get("dims")):
            if self.get("unit") == other.get("unit"):

                new_df = (
                    self.df.set_index(self.get("preferred_index") + self.get("dims"))
                    .drop("symbol", axis=1)
                    .sort_index()
                    + other.df.set_index(
                        other.get("preferred_index") + other.get("dims")
                    )
                    .drop("symbol", axis=1)
                    .sort_index()
                )
                new_object = Symbol(
                    self.get("name") + "+" + other.get("name"),
                    "v",
                    self.get("unit"),
                    self.get("header_name"),
                    self.get("dims"),
                    "expression",
                    self.get("preferred_index"),
                )
                new_df.loc[:, "symbol"] = new_object.get("name")
                new_object.df = new_df.reset_index()
                new_object.modifiers = self.get("modifiers")
                return new_object
            else:
                flag = True
        else:
            flag = True
        if flag:
            raise Exception("dims or/and unit are not equal")

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            new_df = (
                self.df.set_index(self.get("preferred_index") + self.get("dims")).drop(
                    "symbol", axis=1
                )
                * other
            )
            new_object = Symbol(
                "(" + self.get("name") + ")" + "*" + str(other),
                "v",
                self.get("unit"),
                self.get("header_name"),
                self.get("dims"),
                "expression",
                self.get("preferred_index"),
            )
            new_df.loc[:, "symbol"] = new_object.get("name")
            new_object.df = new_df.reset_index()
            new_object.modifiers = self.get("modifiers")
            return new_object
        elif isinstance(other, object):
            diffdims = list(
                set(self.get("dims")).symmetric_difference(set(other.get("dims")))
            )
            lendiff = len(diffdims)
            flag = False
            if set(self.get("dims")) == set(other.get("dims")):
                new_df = (
                    self.df.set_index(self.get("preferred_index") + self.get("dims"))
                    .drop("symbol", axis=1)
                    .sort_index()
                    * other.df.set_index(
                        other.get("preferred_index") + other.get("dims")
                    )
                    .drop("symbol", axis=1)
                    .sort_index()
                )
                new_object = Symbol(
                    "(" + self.get("name") + ")" + "*" + other.get("name"),
                    "v",
                    self.get("unit"),
                    self.get("header_name"),
                    self.get("dims"),
                    "expression",
                    self.get("preferred_index"),
                )
                new_df.loc[:, "symbol"] = new_object.get("name")
                new_object.df = new_df.reset_index()
                new_object.modifiers = self.get("modifiers")
                print(
                    f"Warning: After an operation check allways the 'unit' and 'header_name' attributes of the new object {new_object.get('name')} for consistency."
                )
                return new_object
            elif lendiff == 1:
                dim = diffdims[0]
                save = {}
                save[dim in self.get("dims")] = self
                save[dim in other.get("dims")] = other

                common_dims = list(
                    set(save[True].get("dims")).intersection(save[False].get("dims"))
                )
                # common_items = []
                # for cdim in common_dims:
                #     dim_items = [save[True].df[cdim].unique(), save[False].df[cdim].unique()]
                #     common_items.append(dim_items[argmin([len(dim_items[0]), len(dim_items[1])])])

                # query = ' & '.join([f'''{setname} in {"['" + "','".join(items) + "']"}''' for setname, items in zip(common_dims,common_items)])

                true_df = save[True].df  # .query(query)
                false_df = save[False].df  # .query(query)

                new_df = (
                    true_df.set_index(
                        save[True].get("preferred_index") + save[True].get("dims")
                    )
                    .drop("symbol", axis=1)
                    .unstack(common_dims)
                    .fillna(0)
                    .sort_index()
                    .mul(
                        false_df.set_index(
                            save[False].get("preferred_index") + save[False].get("dims")
                        )
                        .drop("symbol", axis=1)
                        .unstack(common_dims)
                        .fillna(0)
                        .sort_index()
                    )
                )
                new_df = new_df.stack(common_dims)
                new_object = Symbol(
                    "(" + save[False].get("name") + ")" + "*" + save[True].get("name"),
                    "v",
                    save[False].get("unit") + save[True].get("unit"),
                    save[False].get("header_name"),
                    save[True].get("dims"),
                    "expression",
                    save[True].get("preferred_index"),
                )
                new_df.loc[:, "symbol"] = new_object.get("name")
                new_object.df = new_df.reset_index()
                new_object.modifiers = self.get("modifiers")
                print(
                    f"Warning: After an operation check allways the 'unit' and 'header_name' attributes of the new object {new_object.get('name')} for consistency."
                )
                return new_object
            elif lendiff > 1:
                common_dims = list(
                    set(self.get("dims")).intersection(other.get("dims"))
                )
                if len(common_dims) > 0:
                    new_df = (
                        self.df.set_index(
                            self.get("preferred_index") + self.get("dims")
                        )
                        .drop("symbol", axis=1)
                        .sort_index()
                        * other.df.set_index(
                            other.get("preferred_index") + other.get("dims")
                        )
                        .drop("symbol", axis=1)
                        .sort_index()
                    )
                    new_object = Symbol(
                        "(" + self.get("name") + ")" + "*" + other.get("name"),
                        "v",
                        self.get("unit") + other.get("unit"),
                        {
                            self.get("unit")
                            + other.get("unit"): self.get("header_name")[
                                self.get("unit")
                            ]
                        },
                        list(set(self.get("dims") + other.get("dims"))),
                        "expression",
                        self.get("preferred_index"),
                    )
                    new_df.loc[:, "symbol"] = new_object.get("name")
                    new_object.df = new_df.reset_index()
                    new_object.modifiers = self.get("modifiers")
                    return new_object
                else:
                    raise Exception(
                        f"The difference in dimensions is greater than one: '{diffdims}' and has no common dimensions"
                    )
        else:
            raise Exception(
                "The second term is not known, must be a int, float or a Symbol object"
            )

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            new_df = (
                self.df.set_index(self.get("preferred_index") + self.get("dims")).drop(
                    "symbol", axis=1
                )
                / other
            )
            new_object = Symbol(
                "(" + self.get("name") + ")" + "/" + str(other),
                "v",
                self.get("unit"),
                self.get("header_name"),
                self.get("dims"),
                "expression",
                self.get("preferred_index"),
            )
            new_df.loc[:, "symbol"] = new_object.get("name")
            new_object.df = new_df.reset_index()
            new_object.modifiers = self.get("modifiers")
            return new_object
        elif isinstance(other, object):
            diffdims = list(
                set(self.get("dims")).symmetric_difference(set(other.get("dims")))
            )
            lendiff = len(diffdims)
            flag = False
            if set(self.get("dims")) == set(other.get("dims")):
                new_df = (
                    self.df.set_index(self.get("preferred_index") + self.get("dims"))
                    .drop("symbol", axis=1)
                    .sort_index()
                    / other.df.set_index(
                        other.get("preferred_index") + other.get("dims")
                    )
                    .drop("symbol", axis=1)
                    .sort_index()
                )
                new_object = Symbol(
                    "(" + self.get("name") + ")" + "/" + other.get("name"),
                    "v",
                    self.get("unit"),
                    self.get("header_name"),
                    self.get("dims"),
                    "expression",
                    self.get("preferred_index"),
                )
                new_df.loc[:, "symbol"] = new_object.get("name")
                new_object.df = new_df.reset_index()
                new_object.modifiers = self.get("modifiers")
                print(
                    f"Warning: After an operation check allways the 'unit' and 'header_name' attributes of the new object {new_object.get('name')} for consistency."
                )
                return new_object
            elif lendiff == 1:
                dim = diffdims[0]
                save = {}
                save[dim in self.get("dims")] = self
                save[dim in other.get("dims")] = other

                common_dims = list(
                    set(save[True].get("dims")).intersection(save[False].get("dims"))
                )
                # common_items = []
                # for cdim in common_dims:
                #     dim_items = [save[True].df[cdim].unique(), save[False].df[cdim].unique()]
                #     common_items.append(dim_items[argmin([len(dim_items[0]), len(dim_items[1])])])

                # query = ' & '.join([f'''{setname} in {"['" + "','".join(items) + "']"}''' for setname, items in zip(common_dims,common_items)])

                true_df = save[True].df  # .query(query)
                false_df = save[False].df  # .query(query)

                new_df = (
                    true_df.set_index(
                        save[True].get("preferred_index") + save[True].get("dims")
                    )
                    .drop("symbol", axis=1)
                    .unstack(common_dims)
                    .fillna(0)
                    .sort_index()
                    / false_df.set_index(
                        save[False].get("preferred_index") + save[False].get("dims")
                    )
                    .drop("symbol", axis=1)
                    .unstack(common_dims)
                    .fillna(0)
                    .sort_index()
                )
                new_df = new_df.stack(common_dims)
                new_object = Symbol(
                    "(" + save[False].get("name") + ")" + "/" + save[True].get("name"),
                    "v",
                    save[False].get("unit") + save[True].get("unit"),
                    save[False].get("header_name"),
                    save[True].get("dims"),
                    "expression",
                    save[True].get("preferred_index"),
                )
                new_df.loc[:, "symbol"] = new_object.get("name")
                new_object.df = new_df.reset_index()
                new_object.modifiers = self.get("modifiers")
                print(
                    f"Warning: After an operation check allways the 'unit' and 'header_name' attributes of the new object {new_object.get('name')} for consistency."
                )
                return new_object
            elif lendiff > 1:
                raise Exception(
                    f"The difference in dimensions is greater than one: '{diffdims}'"
                )
        else:
            raise Exception(
                "The second term is not known, must be a int, float or a Symbol object"
            )

    def dimreduc(self, dim, aggfunc='sum'):
        new_dims = list(set(self.get("dims")).symmetric_difference(set([dim])))
        new_df = (
            self.df.set_index(self.get("preferred_index") + self.get("dims"))
            .drop("symbol", axis=1)
            .sort_index()
        )
        new_df = new_df.groupby(self.get("preferred_index") + new_dims).agg({'value':aggfunc})
        new_object = Symbol(
            f"({self.get('name')}).dimreduc({dim})",
            "v",
            self.get("unit"),
            self.get("header_name"),
            new_dims,
            "expression",
            self.get("preferred_index"),
        )
        new_df.loc[:, "symbol"] = new_object.get("name")
        new_object.df = new_df.reset_index()
        new_object.modifiers = self.get("modifiers")
        return new_object

    def concat(self, other):
        flag = False
        if set(self.get("dims")) == set(other.get("dims")):
            if self.get("unit") == other.get("unit"):
                new_df = pd.concat(
                    [
                        self.df[
                            self.get("preferred_index")
                            + self.get("dims")
                            + ["symbol", "value"]
                        ],
                        other.df[
                            other.get("preferred_index")
                            + other.get("dims")
                            + ["symbol", "value"]
                        ],
                    ]
                )
                new_object = Symbol(
                    self.get("name") + "-concat-" + other.get("name"),
                    "v",
                    self.get("unit"),
                    self.get("header_name"),
                    self.get("dims"),
                    "expression",
                    self.get("preferred_index"),
                )
                new_df.loc[:, "symbol"] = new_object.get("name")
                new_object.df = new_df
                new_object.modifiers = self.get("modifiers")
                return new_object
            else:
                flag = True
        else:
            flag = True
        if flag:
            raise Exception("dims or/and unit are not equal")

def storagecycling(storage_in: Symbol, storage_out: Symbol) -> Symbol:
    '''
    Symbol whose dataframe in the column 'value' has three possible options 0,1,2.
    Where 2 indicates storage cycling. This function gives a 1 if the flow occurs, 
    otherwise, is 0 for each symbol (input and output flow). The both symbols are added,
    if at certain hour input and output flows have 1, the result will be 2.
    
    Args:
        storage_in (Symbol): Symbol storage input flow
        storage_out (Symbol): Symbol storage output flow
        
    Return:
        sto
    '''
    stoin = storage_in/storage_in
    stoin.df['value'] = stoin.df['value'].fillna(0)
    stoout = storage_out/storage_out
    stoout.df['value'] = stoout.df['value'].fillna(0)
    sto = stoout + stoin
    sto.df['value'] = sto.df['value'].fillna(0)
    unique = sto.df['value'].unique().tolist()
    print(unique)
    if 2.0 in unique:
        print('Storage cycling: True, as 2 in "value" column')
    else:
        print('Storage cycling: False, as 2 is not present in "value" column')
    print('Use .df to get the dataframe')
    return sto
