from gdxcc import gdxSystemInfo, gdxSymbolInfo, gdxCreateD, gdxOpenRead, \
                    GMS_SSSIZE, gdxDataReadDone, new_gdxHandle_tp, gdxFindSymbol, \
                        gdxDataReadStrStart, gdxDataReadStr, gdxSymbolGetDomainX, gdxSymbolInfoX


def gdx_get_symb_info(gams_dir=None, filename=None, symbol=None):
    gamstype = {0:'set', 1:'parameter', 2:'variable', 3:'equation', 4:'alias'}
    gdxHandle = new_gdxHandle_tp()
    gdxCreateD(gdxHandle, gams_dir, GMS_SSSIZE)
    try:
        gdxOpenRead(gdxHandle, filename)
    except:
        raise Exception(f'File {filename} can not be opened')
    ret, symidx = gdxFindSymbol(gdxHandle, symbol)
    if not ret:
        gdxDataReadDone(gdxHandle)
        return False, None
    ret, name, dims, data_type = gdxSymbolInfo(gdxHandle, symidx)
    ret, records, userinfo, description = gdxSymbolInfoX(gdxHandle,symidx)
    ret, gdx_domain = gdxSymbolGetDomainX(gdxHandle, symidx)
    gdxDataReadDone(gdxHandle)
    return True, {'name':name, 'nrdims':dims, 'dims':gdx_domain, 'type':gamstype[data_type], 'desc':description}

def gdx_get_set_coords(gams_dir=None, filename=None, setname=None):
    '''
    it uses gdxcc library to access the gdx file.
    Based on the set name it provides a list with the set elements.
    gams_dir: None by default. Automaticly detects gams directory.
    filename: gdx file path.
    setname: name of the set.
    '''
    coords = []
    gdxHandle = new_gdxHandle_tp()
    gdxCreateD(gdxHandle, gams_dir, GMS_SSSIZE)
    try:
        gdxOpenRead(gdxHandle, filename)
    except:
        raise Exception(f'File {filename} can not be opened')
    ret, symidx = gdxFindSymbol(gdxHandle, setname)
    ret, nrRecs = gdxDataReadStrStart(gdxHandle, symidx)
    for i in range(nrRecs):
        ret, elements, _, _ = gdxDataReadStr(gdxHandle)
        #  elements is a list. Therefore *elements
        coords.append(*elements)
    gdxDataReadDone(gdxHandle)
    return coords

def gdx_get_symb_list(gams_dir=None, filename=None):
    gdxHandle = new_gdxHandle_tp()
    gdxCreateD(gdxHandle, gams_dir, GMS_SSSIZE)
    try:
        gdxOpenRead(gdxHandle, filename)
    except:
        raise Exception(f'File {filename} can not be opened')
    exists, nSymb, nElem = gdxSystemInfo(gdxHandle)
    symbols = []
    for symNr in range(nSymb):
        SymbolInfo = gdxSymbolInfo(gdxHandle, symNr)
        symbols.append(SymbolInfo[1])
    gdxDataReadDone(gdxHandle)
    return symbols

def gdx_get_symb_recordnr(gams_dir=None, filename=None, symbolname=None):
    gdxHandle = new_gdxHandle_tp()
    gdxCreateD(gdxHandle, gams_dir, GMS_SSSIZE)
    try:
        gdxOpenRead(gdxHandle, filename)
    except:
        raise Exception(f'File {filename} cann`t be opened')
    ret, symidx = gdxFindSymbol(gdxHandle, symbolname)
    if ret:
        ret, nrRecs = gdxDataReadStrStart(gdxHandle, symidx)
        gdxDataReadDone(gdxHandle)
        return True, nrRecs
    else:
        gdxDataReadDone(gdxHandle)
        return False, None

def gdx_get_symb_recordnr_from_list(gams_dir=None, filenamelist=None, symbolnamelist=None):
    if filenamelist is None:
        raise Exception('filenamelist is None. You must provide a list with at least one gdx file path')
    if not isinstance(filenamelist, list):
        raise Exception('filenamelist must be a list with at least one gdx file path')
    if len(filenamelist) == 0:
        raise Exception('filenamelist must contain at least one gdx file path')

    records = {}
    for symbolname in symbolnamelist:
        # looking for symbolname in the first file of the list, if not then see the second one, and so on.
        # Hence, file order in the list prioritize the first one and so on.
        for file in filenamelist:
            ret, recNr = gdx_get_symb_recordnr(gams_dir=gams_dir, filename=file, symbolname=symbolname)
            if ret:
                break
        if not ret:
            raise Exception(f'Symbol {symbolname} is not in {filenamelist}')
        records[symbolname] = recNr
    return records

def gdx_get_summary(gams_dir=None, filename=None):
    gamstype = {0:'set', 1:'parameter', 2:'variable', 3:'equation', 4:'alias'}
    gdxHandle = new_gdxHandle_tp()
    gdxCreateD(gdxHandle, gams_dir, GMS_SSSIZE)
    try:
        gdxOpenRead(gdxHandle, filename)
    except:
        raise Exception(f'File {filename} can not be opened')
    symbols = gdx_get_symb_list(filename=filename)
    sym_list = []
    for symbname in symbols:
        ret, symidx = gdxFindSymbol(gdxHandle, symbname)
        if ret:
            ret, name, dims, data_type = gdxSymbolInfo(gdxHandle, symidx)
            ret, records, userinfo, description = gdxSymbolInfoX(gdxHandle,symidx)
            ret, gdx_domain = gdxSymbolGetDomainX(gdxHandle, symidx)
            sym_list.append({'name':name, 'nrdims':dims, 'dims':gdx_domain, 'type':gamstype[data_type], 'desc':description})
    gdxDataReadDone(gdxHandle)
    return sym_list
