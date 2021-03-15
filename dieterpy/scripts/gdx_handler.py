# DIETERpy is electricity market model developed by the research group
# Transformation of the Energy Economy at DIW Berlin (German Institute of Economic Research)
# copyright 2021, Carlos Gaete-Morales, Martin Kittel, Alexander Roth,
# Wolf-Peter Schill, Alexander Zerrahn
"""
This module contains functions that enable us to read GDX files and extract GAMS symbols, such as sets, variables, parameters and equations.
"""
from typing import List
from gdxcc import (
    gdxSystemInfo,
    gdxSymbolInfo,
    gdxCreateD,
    gdxOpenRead,
    GMS_SSSIZE,
    gdxDataReadDone,
    new_gdxHandle_tp,
    gdxFindSymbol,
    gdxDataReadStrStart,
    gdxDataReadStr,
    gdxSymbolGetDomainX,
    gdxSymbolInfoX,
    gdxClose,
    gdxFree,
)


def gdx_get_symb_info(gams_dir: str = None, filename: str = None, symbol: str = None):
    """This function provides information of a symbol in a GDX file.

    Args:
        gams_dir (str, optional): GAMS.exe path, if None the API looks at Environment variables. Defaults to None.
        filename (str, optional): GDX filename. Defaults to None.
        symbol (str, optional): name of the symbol in the GDX file. Defaults to None.

    Raises:
        Exception: GDX file does not exist or is failed

    Returns:
        tuple: first position is a bool that indicates if symbol exists. Second position is a dictionary with symbol's name, number of dimensions, dimension's name in a list, type of symbol and description.
    """
    gamstype = {0: "set", 1: "parameter", 2: "variable", 3: "equation", 4: "alias"}
    gdxHandle = new_gdxHandle_tp()
    gdxCreateD(gdxHandle, gams_dir, GMS_SSSIZE)
    try:
        gdxOpenRead(gdxHandle, filename)
    except:
        raise Exception(f"File {filename} can not be opened")
    ret, symidx = gdxFindSymbol(gdxHandle, symbol)
    if not ret:
        gdxDataReadDone(gdxHandle)
        return False, None
    ret, name, dims, data_type = gdxSymbolInfo(gdxHandle, symidx)
    ret, records, userinfo, description = gdxSymbolInfoX(gdxHandle, symidx)
    ret, gdx_domain = gdxSymbolGetDomainX(gdxHandle, symidx)
    gdxDataReadDone(gdxHandle)
    gdxClose(gdxHandle)
    gdxFree(gdxHandle)
    return (
        True,
        {
            "name": name,
            "nrdims": dims,
            "dims": gdx_domain,
            "type": gamstype[data_type],
            "desc": description,
        },
    )


def gdx_get_set_coords(
    gams_dir: str = None, filename: str = None, setname: str = None
) -> List[str]:
    """Based on the set name it provides a list with the set elements

    Args:
        gams_dir (str, optional): GAMS.exe path, if None the API looks at environment variables. Defaults to None.
        filename (str, optional): GDX filename. Defaults to None.
        setname (str, optional): name of the set. Defaults to None.

    Raises:
        Exception: GDX file does not exist or is failed

    Returns:
        list: a list with elements of a set found in the GDX file
    """
    coords = []
    gdxHandle = new_gdxHandle_tp()
    gdxCreateD(gdxHandle, gams_dir, GMS_SSSIZE)
    try:
        gdxOpenRead(gdxHandle, filename)
    except:
        raise Exception(f"File {filename} can not be opened")
    ret, symidx = gdxFindSymbol(gdxHandle, setname)
    ret, nrRecs = gdxDataReadStrStart(gdxHandle, symidx)
    for i in range(nrRecs):
        ret, elements, _, _ = gdxDataReadStr(gdxHandle)
        #  elements is a list. Therefore *elements
        coords.append(*elements)
    gdxDataReadDone(gdxHandle)
    gdxClose(gdxHandle)
    gdxFree(gdxHandle)
    return coords


def gdx_get_symb_list(gams_dir: str = None, filename: str = None) -> List[str]:
    """ It returns a list of symbols' names contained in the GDX file

    Args:
        gams_dir (str, optional): GAMS.exe path, if None the API looks at environment variables. Defaults to None.
        filename (str, optional): GDX filename. Defaults to None.

    Raises:
        Exception: GDX file does not exist or is failed

    Returns:
        list: a list of symbol's names contained in the GDX file
    """
    gdxHandle = new_gdxHandle_tp()
    gdxCreateD(gdxHandle, gams_dir, GMS_SSSIZE)
    try:
        gdxOpenRead(gdxHandle, filename)
    except:
        raise Exception(f"File {filename} can not be opened")
    exists, nSymb, nElem = gdxSystemInfo(gdxHandle)
    symbols = []
    for symNr in range(nSymb):
        SymbolInfo = gdxSymbolInfo(gdxHandle, symNr)
        symbols.append(SymbolInfo[1])
    gdxDataReadDone(gdxHandle)
    gdxClose(gdxHandle)
    gdxFree(gdxHandle)
    return symbols


def gdx_get_symb_recordnr(
    gams_dir: str = None, filename: str = None, symbolname: str = None
) -> tuple:
    """Return number of records in the requested symbol

    Args:
        gams_dir (str, optional): GAMS.exe path, if None the API looks at environment variables. Defaults to None.
        filename (str, optional): GDX filename. Defaults to None.
        symbolname (str, optional): name of the symbol. Defaults to None.

    Raises:
        Exception: GDX file does not exist or is failed

    Returns:
        tuple: It returns a tuple. The first position is bool if the symbol name exists in the GDX file. Second position an integer representing the number of records.
    """
    gdxHandle = new_gdxHandle_tp()
    gdxCreateD(gdxHandle, gams_dir, GMS_SSSIZE)
    try:
        gdxOpenRead(gdxHandle, filename)
    except:
        raise Exception(f"File {filename} cann`t be opened")
    ret, symidx = gdxFindSymbol(gdxHandle, symbolname)
    if ret:
        ret, nrRecs = gdxDataReadStrStart(gdxHandle, symidx)
        gdxDataReadDone(gdxHandle)
        gdxClose(gdxHandle)
        gdxFree(gdxHandle)
        return True, nrRecs
    else:
        gdxDataReadDone(gdxHandle)
        gdxClose(gdxHandle)
        gdxFree(gdxHandle)
        return False, None


def gdx_get_symb_recordnr_from_list(
    gams_dir: str = None, filenamelist: list = None, symbolnamelist: list = None
) -> dict:
    """This function searches for each symbol of a list of symbols in the first GDX file of the list of files; if the current symbol is not present, it searches on the second file in the list. When a symbol is detected in a GDX file, it returns the symbol's number of records. It returns a dictionary.

    Args:
        gams_dir (str, optional): GAMS.exe path, if None the API looks at environment variables. Defaults to None.
        filenamelist (list[str], optional): GDX files paths sorted in descending order of importance to find the symbols. Defaults to None.
        symbolnamelist (list[str], optional): list of symbols to search on GDX files. Defaults to None.

    Raises:
        Exception: filenamelist can not be None
        Exception: filenamelist must be a list
        Exception: filenamelist is an empty list
        Exception: A symbols is not present in any GDX file listed

    Returns:
        dict: Contains the number of records of each symbol in the GDX file that contains it.
    """
    if filenamelist is None:
        raise Exception(
            "filenamelist is None. You must provide a list with at least one gdx file path"
        )
    if not isinstance(filenamelist, list):
        raise Exception("filenamelist must be a list with at least one gdx file path")
    if len(filenamelist) == 0:
        raise Exception("filenamelist must contain at least one gdx file path")

    records = {}
    for symbolname in symbolnamelist:
        # looking for symbolname in the first file of the list, if not then see the second one, and so on.
        # Hence, file order in the list prioritize the first one and so on.
        for file in filenamelist:
            ret, recNr = gdx_get_symb_recordnr(
                gams_dir=gams_dir, filename=file, symbolname=symbolname
            )
            if ret:
                break
        if not ret:
            raise Exception(f"Symbol {symbolname} is not in {filenamelist}")
        records[symbolname] = recNr
    return records


def gdx_get_summary(gams_dir: str = None, filename: str = None) -> List[dict]:
    """It returns a list of dictionaries. Each element of the list represents a symbol in the GDX file, every dictionary contains information of the symbols, such as, name, dimensions, type of symbol.

    Args:
        gams_dir (str, optional): GAMS.exe path, if None the API looks at environment variables. Defaults to None.
        filename (str, optional): GDX filename. Defaults to None.

    Raises:
        Exception: GDX file does not exist or is failed.

    Returns:
        list[dict]: a list of dictionaries with symbols' info.
    """
    gamstype = {0: "set", 1: "parameter", 2: "variable", 3: "equation", 4: "alias"}
    gdxHandle = new_gdxHandle_tp()
    gdxCreateD(gdxHandle, gams_dir, GMS_SSSIZE)
    try:
        gdxOpenRead(gdxHandle, filename)
    except:
        gdxClose(gdxHandle)
        gdxFree(gdxHandle)
        raise Exception(f"File {filename} can not be opened")
    symbols = gdx_get_symb_list(filename=filename)
    sym_list = []
    for symbname in symbols:
        ret, symidx = gdxFindSymbol(gdxHandle, symbname)
        if ret:
            ret, name, dims, data_type = gdxSymbolInfo(gdxHandle, symidx)
            ret, records, userinfo, description = gdxSymbolInfoX(gdxHandle, symidx)
            ret, gdx_domain = gdxSymbolGetDomainX(gdxHandle, symidx)
            sym_list.append(
                {
                    "name": name,
                    "nrdims": dims,
                    "dims": gdx_domain,
                    "type": gamstype[data_type],
                    "desc": description,
                }
            )
    gdxDataReadDone(gdxHandle)
    gdxClose(gdxHandle)
    gdxFree(gdxHandle)
    return sym_list
