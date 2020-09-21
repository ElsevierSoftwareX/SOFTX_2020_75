from gams import GamsWorkspace, GamsOptions, DebugLevel
from exceltogdx import exceltogdx
from shutil import copyfile
import csv
import sys
import pandas as pd
import os
import time

from dieterpy.scripts.gdx_handler import gdx_get_set_coords


def getConfigVariables(config_path):
    '''
    Imports configuration of model control variables and scenario variables.

    Parameters
    ----------
    config_path : string
        Path referring to folder location that contains the config files, e.g.
        '../config/'.

    Returns
    -------
    cv_dict :
        Dictionary containing configuration variables.
    '''
    try:
        cv_df = pd.read_csv(os.path.join(config_path,'project_variables.csv'))
        cv_dict = {}
        for i, row in cv_df.iterrows():
            cv_dict[row['feature']] = row['value'] if not pd.isnull(row['value']) else ''
        return cv_dict
    except:
        e = sys.exc_info()[0]
        print('E:getConfigVariables\n', e)
        raise

def getGlobalFeatures(config_path, active_global_features):
    '''
    Creates dict with appropriate switch values for all global options.
    On-switch: '*'
    Off-switch: "''"

    Parameters
    ----------
    config_path : str
        Path referring to folder location that contains configuration files.
    active_gf : list
        Contains all active global features.

    Returns
    -------
    glob_feat_dc : dict
        Contains switch information for global features.

    '''
    try:
        # get all global features
        glob_feat_list = pd.read_csv(os.path.join(config_path, 'features_node_selection.csv'))['feature'].to_list()

        # assign feature switch values
        glob_feat_dc = {gf: '*' if gf in active_global_features else "''" for gf in glob_feat_list}

        return glob_feat_dc
    except:
        e = sys.exc_info()[0]
        print('E:getGlobalFeatures\n', e)
        raise

def generateInputGDX(input_path, config_path, gdx_path, convar_dc):
    '''
    Generates input gdx files if skip_import == 'no'.

    Parameters
    ----------
    input_path : string
        Path referring to folder location that contains input xlsx files.
    config_path : string
        Path referring to folder location that contains configuration files.
    gdx_path : string
        Path referring to folder location that contains input gdx files to be
        generated.
    convar_dc : dict
        contains info on skip_import (either "yes" or "no").

    Raises
    ------
    Exception
        If neither "yes" nor "no" is entered as value for control variable
        "skip_import" in the config file.

    Returns
    -------
    None.

    '''
    try:
        data_input_gdx_abspath = os.path.join(gdx_path, 'data_input.gdx')
        time_series_gdx_abspath = os.path.join(gdx_path, 'time_series.gdx')
        if convar_dc['skip_input'] == 'no':

            # import of data_input.xlsx
            if convar_dc['data_input_file']:
                print('Import from ' + convar_dc['data_input_file'] + ' commences.')
                exceltogdx(os.path.join(input_path, convar_dc['data_input_file']), data_input_gdx_abspath)
            else:
                print('''No upload for time-invariant data chosen. Hint: This
                      will shoot an error if no input gdx are available.''')

            # import of time_series.xlsx
            if convar_dc['time_series_file']:
                print('Import from ' + convar_dc['time_series_file'] + ' commences.')
                exceltogdx(os.path.join(input_path, convar_dc['time_series_file']), time_series_gdx_abspath)
            else:
                print('''No upload for time-variant data chosen. Hint: This
                      will shoot an error if no input gdx are available.''')

        elif convar_dc['skip_input'] == 'yes':
            print('Generation of input gdx files skipped.')

        # import of feature_configuration.csv <-- always required
        file_abspath = os.path.join(config_path, 'features_node_selection.csv')

        # create temporay csv file w/o comment column
        try:
            original = pd.read_csv(file_abspath, index_col='feature')
        except:
            e = sys.exc_info()[0]
            print('E:generateInputGDX\n', e)
            raise

        feature_configuration = original.drop('comment', axis=1)
        feature_configuration.to_csv(file_abspath)

        # read csv and create gdx
        feat_node_gdx_abspath = gams_feat_node(gams_dir=None,
                                       csv_path=file_abspath,
                                       gdxoutputfolder=gdx_path)

        # replace temporary csv file with original one
        original.to_csv(os.path.join(config_path,file_abspath))

        # get active global features
        active_gf = gdx_get_set_coords(filename=feat_node_gdx_abspath, setname='features')

        gdx_paths_dc = {}
        gdx_paths_dc['data_input_gdx'] = data_input_gdx_abspath
        gdx_paths_dc['time_series_gdx'] = time_series_gdx_abspath
        gdx_paths_dc['feat_node_gdx'] = feat_node_gdx_abspath

        return active_gf, gdx_paths_dc
    except:
        e = sys.exc_info()[0]
        print('E:generateInputGDX\n', e)
        raise

def prepareGAMSAPI(working_directory):
    '''
    Prepares GAMS API.

    Returns
    -------
    ws : GAMS workspace object
       Base class of the gams namespace, used for initiating GAMS objects
       (e.g. GamsDatabase and GamsJob) by an "add" method of GamsWorkspace.
       Unless a GAMS system directory is specified during construction of
       GamsWorkspace, GamsWorkspace determines the location of the GAMS
       installation automatically. Aorking directory (the anchor into the file
       system) can be provided when constructing the GamsWorkspace instance.
       It is used for all file-based operations.
    cp : GAMS execution Checkpoint
        A GamsCheckpoint class captures the state of a GamsJob after the
        GamsJob.run method has been carried out. Another GamsJob can continue
        (or restart) from a GamsCheckpoint.
    opt : GAMS options object
        Stores and manages GAMS options for a GamsJob and GamsModelInstance.

    '''
    try:
        # define directories and create GAMS workspace
        ws = GamsWorkspace(working_directory=working_directory, debug=DebugLevel.KeepFiles)  # system_directory=sysdir
        version = GamsWorkspace.api_version
        print('GAMS version: ', version)
        print('MainDir ---->: ', ws.working_directory)
        cp = ws.add_checkpoint()
        opt = GamsOptions(ws)
        return ws, cp, opt
    except:
        e = sys.exc_info()[0]
        print('E:prepareGAMSAPI\n', e)
        raise

def defineGAMSOptions(opt,glob_feat_dc,convar_dc, gdx_abspaths_dc):
    '''
    Defines global and control options and hands them over to the GAMS
    options object.

    Parameters
    ----------
    opt : GAMS options object
        Stores and manages GAMS options for a GamsJob and GamsModelInstance.
    global_features : dict
        Contains information on all global features.
    convar_dc : dict
        Contains all control variable information.

    Returns
    -------
    opt : GAMS options object
        Updated GAMS options.
    '''
    try:
        global_options = ['base_year', 'end_hour', 'dispatch_only', 'network_transfer', 'no_crossover', 'infeasibility']
        for k in convar_dc.keys():
            if k in global_options:
                    if (convar_dc[k] == 'yes') or (convar_dc[k] == 'no'):
                        if k == 'dispatch_only':
                            opt.defines[str('py_dispatch_only')] = '*' if convar_dc[k] == 'yes' else "''"
                            opt.defines[str('py_investment')] = "''" if convar_dc[k] == 'yes' else '*'
                        else:
                            opt.defines[str('py_'+k)] = '*' if convar_dc[k] == 'yes' else "''"
                    elif k == 'end_hour':
                        if convar_dc[k]:
                            # provides gams string for h set from h1 to end_hour, eg. h1*h8760
                            gams_h_set_string = f'"h1*{convar_dc[k]}"'
                            opt.defines[str('py_'+k)] = "'*'"
                            opt.defines[str('py_h_set')] = gams_h_set_string
                        else:
                            # if end_hour is left in blank in 'control_variables.csv'
                            opt.defines[str('py_'+k)] = "''"
                            opt.defines[str('py_h_set')] = "''"
                    else:
                        opt.defines[str('py_'+k)] = "'{}'".format(str(convar_dc[k]))
            else:
                continue

        # define global features to (de)activate model modules
        for k, v in glob_feat_dc.items():
            opt.defines[str('py_'+k)] = v

        # define features set acc. to list of all global features
        feature_string = ','.join(list(glob_feat_dc.keys()))
        opt.defines[str('py_feature_set')] = '"' + feature_string + '"'

        # add absolute path of gdx files
        for name, abspath in gdx_abspaths_dc.items():
            opt.defines[str('py_'+ name)] = abspath

        return opt
    except:
        e = sys.exc_info()[0]
        print('E:defineGAMSOptions\n', e)
        raise

def writeCountryOpt(opt, countries, topos):
    """
    Writes the sets 'n' (nodes) and 'l' (lines) in the GAMS options. Selects
    automatically the correct lines for the selected nodes.

    Parameters
    ----------
    countries : string
        Countries to be written in the opt object.
    topos : panda
        Spatial structure of the model. Defines which nodes are connected with
        which lines.

    Returns
    -------
    countries : string
        Countries to be written in the opt object.
    list_lines : list of strings
        List of lines that will be used in that model run.

    """

    # Format countries to import to GAMS
    countries_gams     = f'"{countries}"'
    # Format countries for line selection
    countries_formated = countries.split(',')

    # Write countries to GAMS
    opt.defines['py_iter_countries_set'] = countries_gams

    # Determine the right lines that have to be activated in the model
    list_lines = topos[topos[topos.columns.intersection(countries_formated)].notnull().sum(axis = 1) == 2].index.tolist()

    # Reformat list to enter into GAMS
    list_lines_gams = ','.join(list_lines)
    list_lines_gams = '"{0}"'.format(list_lines_gams)
    print(f"------------> {opt.defines['py_network_transfer']}")
    # if no-connection setting from project variables
    if opt.defines['py_network_transfer'] == "''":
        
        if len(list_lines) == 0:
            opt.defines['py_network_transfer'] = '""'
            # Load one line to avoid other loading errors
            list_lines_gams = '"l01"'
            list_lines      = ['l01']
        else:
            opt.defines['py_network_transfer'] = '""'
            print('Warning: "py_network_transfer" is deactivated from "project variables"')

    # if only one country or no lines to be in the model:
    # activate no-connection setting
    elif len(countries_formated) == 1 or len(list_lines) == 0:
        print(f'Warning: "py_network_transfer" will be deactivated because only one country is selected {countries} or no lines exist in the grid topology')
        # Deactivate NTC
        opt.defines['py_network_transfer'] = '""'
        # Load one line to avoid other loading errors
        list_lines_gams = '"l01"'
        list_lines      = ['l01']
    else:
        # Line selection based on topology
        # NTC is aready allowed from project variables
        opt.defines['py_network_transfer'] = '*'

    # Write lines to GAMS option
    opt.defines['py_iter_lines_set']            = list_lines_gams
    opt.defines['py_iter_countries_switch_on']  = '*'
    opt.defines['py_iter_countries_switch_off'] = '""'

    list_lines_export = ','.join(list_lines)

    return countries, list_lines_export

def writeConstraintOpt(opt, block_iter_dc, list_constraints, itercon_dc):
    """
    Writes the selected constraints in the GAMS opt object.

    Parameters
    ----------
    main_iter_dict : dict
        Main iteration dictionary.
    list_constraints : list
        List of all constraints that can be varied.
    itercon_dc : panda
        Panda that stores the different constraint and available configurations.
    block : string
        Number of block run.

    Returns
    -------
    selected_constraints : List of strings
        Selected constraint configurations.

    """
    selected_constraints = {}
    for constraint in itercon_dc.columns:
        if constraint not in list_constraints:  # If list_constraints is missing all or some constraints, it means that these constraints were not present in iteration_main_file.csv
            # The first option of the contraint is selected as a default option from constraints_list.csv
            i = 0
            for con in itercon_dc[constraint]:
                if pd.isna(con):
                    continue
                if i == 0:
                    opt.defines[str('py_'+con)] = '*'
                    selected_constraints[constraint] = con
                    print('%s: No constraint selected. %s is selected by default' % (constraint, con))
                else:
                    opt.defines[str('py_'+con)] = '""'
                i+=1

    # Loop through all contraints
    for constraint in list_constraints:
        # If no constraint selected
        # TODO: We should set a default constraint in case 'NA',
        #       otherwise the model may omit an important constraint. So If 'NA' is better to raise an Exception
        if block_iter_dc[constraint] == "NA":
            i = 0
            for con in itercon_dc[constraint]:
                if pd.isna(con):
                    continue
                if i == 0:
                    opt.defines[str('py_'+con)] = '*'
                    selected_constraints[constraint] = con
                    print('%s: No constraint selected. %s is selected by default' % (constraint, con))
                else:
                    opt.defines[str('py_'+con)] = '""'
                i+=1
        # If one constraint selected
        else:
            # Select constraint
            constraint_config = block_iter_dc[constraint]
            if constraint_config in itercon_dc[constraint].tolist():
                # handover iteration contraint options to GAMS
                for con in itercon_dc[constraint]:
                    if pd.isna(con):
                        continue
                    else:
                        opt.defines[str('py_' + con)] = '*' if con == constraint_config else '""'
                selected_constraints[constraint] = constraint_config
                print('%s: %s' % (constraint, constraint_config))
            else:
                string_options = ','.join(itercon_dc[constraint].tolist())
                raise Exception(f'{constraint_config} is not in {string_options}. Check for any typo in iteration_main_file.csv and compare with constraints_list.csv')
    return selected_constraints

def getIterableDataDict(input_path, output_path, control_dict):
    """
    Generates a dictionary that holds the information for (data) time series
    iteration.

    Parameters
    ----------
    control_dict : dict
        Main control variable dictionary.
    input_path : string
        String that defines the input path for the excel file.
    output_path : string
        String that defines the output path for the gdx file.

    Returns
    -------
    iter_data_dict : dict
        Holds the information for (data) time series iteration.
    output_gdxfile_abspath: string
        string absolute path of the output gdx file

    """
    iteration_data_file_abspath = os.path.join(input_path,
                                            control_dict['iteration_data_file'])
    output_gdx_abspath = os.path.join(output_path, 'iter_data.gdx')
    # Convert iteration data excel to GDX
    if control_dict['skip_iteration_data_file'] == "no":
        print('----------------------------')
        print('Start excel-to-GDX-conversion for iterable time series.')
        print('----------------------------')
        exceltogdx(iteration_data_file_abspath, output_gdx_abspath)
    else:
        pass
    # Convert iteration data to Panda
    data_in = pd.read_excel(iteration_data_file_abspath,
                        sheet_name = "scenario", index_col  = 0,
                        header     = 0, skiprows   = 1)
    iter_data_set_scenario = set(data_in.loc['scenario',:].to_list())

    # Create dict of dict for scenarios, parameters, identifiers
    iter_data_dict = {}
    for entry in iter_data_set_scenario:
        # Create first scenario entry
        iter_data_dict[entry] = {}
        # Create tempory list with parameters & identifiers
        temp_para_list = data_in.loc['parameter'][
            data_in.loc['scenario',:] == entry].to_list()
        temp_id_list = data_in.loc['identifier'][
            data_in.loc['scenario',:] == entry].to_list()
        # Fill scenario keys
        for i in range(0,len(temp_id_list)):
            iter_data_dict[entry][temp_id_list[i]] = temp_para_list[i]
        # delete temp
        del(temp_para_list,temp_id_list,entry,i)
    return iter_data_dict, output_gdx_abspath

def genStringOptData(iter_data_dict, key):
    """
    Generates a string that is compatible and used in the GAMS model to
    overwrite parameters for time series iteration.

    Parameters
    ----------
    iter_data_dict : dict
        Dictioary that holds the time series iteration information.
    key : string
        Identifier that selects the correct time series iteration "scenario".

    Returns
    -------
    script : string
        String to write in the GAMS opt object.

    """
    script = '{0}'.format(''.join([str(v) + ' = ' + 'iter_data(' + 'h,' +"'"+ str(k) +"'"+
         "," +"'"+str(key) +"'"+ "); " for k, v in iter_data_dict[key].items()]))
    return script

def genIterationDict(config_dict, path):
    """
    Function that creates the main iteration dict. First, a panda is imported
    from a csv file and then converted to a dictionary.

    Parameters
    ----------
    config_dict : dict
        Dictionary that holds the config variables and their status.
    key : string
        Key to optain file name.
    path : string
        Input path to the folder where the main iteration csv files is saved.

    Returns
    -------
    iteration_main_dict : dict
        Main iteration dictionary that hold all relevent informatio for the
        different scenario (block) runs.

    """
    if config_dict['scenarios_iteration'] == 'no':
        iteration_main = pd.DataFrame({'run':[0]})
    elif config_dict['scenarios_iteration'] == 'yes':
        ##### MAIN FILE
        # Read main iteration file
        iteration_main = pd.read_csv(os.path.join(path, 'iteration_main_file.csv'))
        # remove from strings leading and trailing whitespaces in columns and cells
        iteration_main = iteration_main.rename(columns={k:k.strip() for k in iteration_main.columns})
        iteration_main = iteration_main.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        # Fill empty cells with "NA"
        iteration_main = iteration_main.fillna("NA")
    else:
        raise Exception('scenarios_iteration must be either "yes" or "no". Check project_variables.csv')

    ##### WORK on column names and lists

    # Get all columns names
    iteration_main_columns = iteration_main.columns.to_list()

    # Read all constraints (currently only minRES)
    list_constraints = [col for col in iteration_main.columns if 'constraint' in col]

    # Make a list of all non-parameter elements
    list_no_parameters_original = ['run', 'country_set', 'time_series_scen']

    list_no_parameters = []
    for col in iteration_main_columns:
        if col in list_no_parameters_original:
            list_no_parameters.append(col)

    list_no_parameters.extend(list_constraints)

    # Identify parameter
    list_parameters = list(set(iteration_main_columns) - set(list_no_parameters))

    ##### DEFINE "BLOCK" RUNS

    # Remove 'run' from list of elements
    list_no_parameters_no_run = list_no_parameters
    if 'run' in list_no_parameters_no_run:
        list_no_parameters_no_run.remove('run')

    # sort dataframe to eventually reduce the number of blocks
    if list_no_parameters_no_run:
        iteration_main = iteration_main.sort_values(list_no_parameters_no_run).reset_index(drop=True)


    print(iteration_main)


    # Define a 'running dict'
    # e.g. {0: ('DE,FR', 'NA', 'rescon_1b'), 1: ('NA', 'NA', 'rescon_1b')}
    run_dict = {i:tuple(v) for i, v in enumerate(iteration_main[list_no_parameters_no_run].values)}

    # Define a 'running block list'
    run_block_list = list()

    for i in run_dict:
        if i == 0:
            block = 0
            run_block_list.append(block)
        if i > 0:
            if run_dict[i] != run_dict[i-1]:
                block = block + 1
            else:
                pass
            run_block_list.append(block)

    # Create set

    run_block_set      = set(run_block_list)
    run_block_set_list = list(run_block_set)

    # Add 'running block list' to 'iteration_main'

    iteration_main['block'] = run_block_list

    # Creat main iteration dictionary

    iteration_main_dict = {}

    for block in run_block_set_list:
        iteration_main_dict[block] = {}
        # Fill non-GUSS elements
        for element in list_no_parameters_no_run:
            # Define entry
            entry = list(set(iteration_main[element][iteration_main['block'] == block]))[0]
            # Write in dict
            iteration_main_dict[block][element] = entry

        # Fill GUSS elements
        # Create parameter dict
        iteration_main_dict[block]['par_var'] = {}
        iteration_main_dict[block]['run_nr'] = {}
        i = 0
        for ix, row in iteration_main[iteration_main['block'] == block].iterrows():
            iteration_main_dict[block]['par_var'][i] = {}
            iteration_main_dict[block]['run_nr'][i] = row['run']
            for parameter in list_parameters:
                entry_list = iteration_main[parameter][iteration_main['block'] == block].tolist()
                entry = entry_list[i]
                if entry == "NA":
                    pass
                else:
                    iteration_main_dict[block]['par_var'][i][parameter] = entry
            i += 1
    return iteration_main_dict, list_constraints

def convert_par_var_dict(symbols_dict = None):
    '''
    convert dict to GUSS dict
    '''
    # collect all the symbols through the runs of the block
    collect_keys = []
    for k, v in symbols_dict.items():
        for kk in v.keys():
            collect_keys.append(kk)
    symbols_block_set_list = list(set(collect_keys))

    # dictionary of current symbols notation to guss dict nomenclature.
    # e.g. {'ev_quant': {'body': 'ev_quant', 'dims': ('.',)},
    #        "N_TECH.lo('DE','pv')": {'body': 'N_TECH.lo', 'dims': ('DE', 'pv')}
    symb_translate_dict = {}
    for long_symb in symbols_block_set_list:
        symb_parts = {}
        if '.' in long_symb:
            symb_parts['body'] = long_symb.split('(')[0]
            elements = []
            for elem in long_symb.split('(')[1][:-1].split(','):
                for sign in ["'","‘","’",'"']: # removing unwanted signs from strings e.g. "‘DE’" to 'DE'
                    elem = elem.replace(sign,"")
                elements.append(elem)
            symb_parts['dims'] = tuple(elements)
        else:
            if '(' in long_symb:
                symb_parts['body'] = long_symb.split('(')[0]
                elements = []
                for elem in long_symb.split('(')[1][:-1].split(','):
                    for sign in ["'","‘","’",'"']:
                        elem = elem.replace(sign,"")
                    elements.append(elem)
                symb_parts['dims'] = tuple(elements)

            else:
                symb_parts['body'] = long_symb
                symb_parts['dims'] = ('.',)
        symb_translate_dict[long_symb] = symb_parts

    # create guss dict. e.g. {0: {'ev_quant': {('.',): 500.0},'N_TECH.lo': {('DE', 'pv'): 5000.0}
    symb_guss_dict = {}
    for k, v in symbols_dict.items():
        symb_guss_dict[k] = {}
        for symbs, val in v.items():
            symb_guss_dict[k][symb_translate_dict[symbs]['body']] = {}
        for symbs, val in v.items():
            symb_guss_dict[k][symb_translate_dict[symbs]['body']].update({symb_translate_dict[symbs]['dims']:val})

    # obtain list of raw symbols. e.g. ['ev_quant', 'N_TECH']
    symbols_guss_block_list = []
    for k, v in symb_translate_dict.items():
        symbols_guss_block_list.append(v['body'])

    symbols_guss_block_set_list = list(set(symbols_guss_block_list))

    return symb_guss_dict, symbols_guss_block_set_list


def getGussVariables(config_dict):

    if config_dict['GUSS'].lower() in ['yes', 'no']:
        guss = True if config_dict['GUSS'].lower() == 'yes' else False
    else:
        raise Exception('GUSS should be "yes" or "no"')

    if config_dict['GUSS_parallel'].lower() in ['yes', 'no']:
        guss_parallel = True if config_dict['GUSS_parallel'].lower() == 'yes' else False
    else:
        raise Exception('GUSS_parallel should be "yes" or "no"')

    if isinstance(config_dict['GUSS_parallel_threads'], int):
        guss_parallel_threads = config_dict['GUSS_parallel_threads']
    elif config_dict['GUSS_parallel_threads'].isdigit():
        guss_parallel_threads = int(config_dict['GUSS_parallel_threads'])
    else:
        raise Exception('GUSS_parallel_threads must be an integer')

    return guss, guss_parallel, guss_parallel_threads

def setCountryIteration(opt, block_iter_dc, topography):
    if 'country_set' not in list(block_iter_dc.keys()):
        opt.defines['py_iter_countries_switch_on']  = '""'
        opt.defines['py_iter_countries_switch_off'] = '*'
        print('Default country set used')
        countries = "NA"
        lines     = "NA"
    # No country set defined -> take default
    elif block_iter_dc['country_set'] == "NA":
        opt.defines['py_iter_countries_switch_on']  = '""'
        opt.defines['py_iter_countries_switch_off'] = '*'
        print('Default country set used')
        countries = "NA"
        lines     = "NA"
    # Country set defined
    else:
        #Write country set
        countries, lines = writeCountryOpt(opt, block_iter_dc['country_set'], topography)
        print('Countries used: %s' % countries)
        print('Lines used:     %s' % str(lines))
    return opt, countries, lines

def setDataIteration(opt, block_iter_dc):
    # if time_series_scen is not in iteration_main_file.csv
    if 'time_series_scen' not in list(block_iter_dc.keys()):
        # Default switch data off
        opt.defines['py_iter_data_switch'] = '""'
        data_scen_key = "NA"
        print('No time series iteration.')
    # if no data scen defined
    elif block_iter_dc['time_series_scen'] == "NA":
        # Default switch data off
        opt.defines['py_iter_data_switch'] = '""'
        data_scen_key = "NA"
        print('No time series iteration.')
    # if data scen defined
    else:
        # Switch on data iteration
        opt.defines['py_iter_data_switch'] = '*'
        data_scen_key = block_iter_dc['time_series_scen']
        print('Time series scenario: %s' % data_scen_key)
    return opt, data_scen_key

def createModelCheckpoint(ws, opt, cp, model_dir_abspath, gdx_output, dict_data_it=None, data_scen_key="NA", str_block=None):
    '''
    Creates the initial checkpoint containing a model instance without
    solve command.

    Parameters
    ----------
    ws : GAMS workspace object
        Base class of the gams namespace, used for initiating GAMS objects
        (e.g. GamsDatabase and GamsJob) by an "add" method of GamsWorkspace.
        Unless a GAMS system directory is specified during construction of
        GamsWorkspace, GamsWorkspace determines the location of the GAMS
        installation automatically. Aorking directory (the anchor into the file
        system) can be provided when constructing the GamsWorkspace instance.
        It is used for all file-based operations.
    opt : GAMS options object
        Stores and manages GAMS options for a GamsJob and GamsModelInstance.
    cp : GAMS execution Checkpoint
        A GamsCheckpoint class captures the state of a GamsJob after the
        GamsJob.run method has been carried out. Another GamsJob can continue
        (or restart) from a GamsCheckpoint.

    Returns
    -------
    cp_file : GAMS model instance
        Contains defined model including the intended constraint w/o solve
        command.

    '''
    try:
        start_time = time.time()
        print('Creating first checkpoint with precompiled model without solve statement.')
        jobs = ws.add_job_from_file(os.path.join(model_dir_abspath, 'model.gms'))
        try:
            jobs.run(gams_options=opt, checkpoint=cp)
        except:
            e = sys.exc_info()[0]
            print('E:createModelCheckpoint\n', e)
            raise
        if not data_scen_key == "NA":
            try:
                # Add data string
                jobs = ws.add_job_from_string(genStringOptData(dict_data_it, data_scen_key), cp)
                # Run model
                jobs.run(checkpoint = cp)
            except:
                e = sys.exc_info()[0]
                print('E:createModelCheckpoint\n', e)
                raise
        else:
            pass
        # Define checkpoint-file
        cp_file = os.path.join(ws.working_directory, cp.name + ".g00")
        elapsed_time = (time.time() - start_time)/60
        print('Creating first checkpoint done. process took {} minutes.'.format(int(elapsed_time)))
    except:
        e = sys.exc_info()[0]
        print('E:createModelCheckpoint\n', e)
        raise
    # copy precompiled gdx file useful for reporting and guss results
    main_gdx_file = os.path.join(ws.working_directory, jobs.out_db.name + ".gdx")
    return cp_file, main_gdx_file

def gams_feat_node(gams_dir=None, csv_path=None, gdxoutputfolder=None):
    '''
    gams_dir: directory where gams.exe is located, optional, None by default.
    csv_path: absolute path of the csv file. Hint: The name of the file must fit the symbol name.
    gdxoutputfolder: absolute path of the directory, without a "/" at the end.
    The name of the output file will be the same as the symbol with .gdx extension.
    '''
    def gams_script():
        '''
        This script is a raw gams code. It calls csv2gdx gams application, available for linux and windows.
        '''
        return '''
Set
features
n;

$call csv2gdx "%csv_path%" output = "%gdxfile%" id=feat_node index=1 values=%range% useHeader=y
$ifE errorLevel<>0 $abort Problems reading csv file
$gdxIn %gdxfile%
$load features = dim1
$load n = dim2

Parameter feat_node(features,n);
$load feat_node
$gdxIn
execute_unload '%gdxfile%';
'''

    start = time.time()
    # reading first row of csv file to get columns number
    with open(csv_path) as csvFile:
        reader = csv.reader(csvFile)
        header_names_list = next(reader)
    header_len = len(header_names_list)
    strrng = ','.join(str(i) for i in range(2,header_len+1))  # passing to gams a range of columns omiting first column. First value is 1 in gams
    #  verify linux or windows
    if os.name == 'posix':
        rng = strrng
    elif os.name == 'nt':
        rng = f'({strrng})'
    os.makedirs(gdxoutputfolder, exist_ok=True)  # create folder if it does not exist.
    symbname = os.path.basename(csv_path).split('.')[0]
    gdxfilename = os.path.join(gdxoutputfolder, symbname + '.gdx')
    ws = GamsWorkspace(system_directory=gams_dir)
    jobs = ws.add_job_from_string(gams_script())
    opt = GamsOptions(ws)
    opt.defines['csv_path'] = f'"{csv_path}"'
    opt.defines['gdxfile'] = f'"{gdxfilename}"'
    opt.defines['range'] = f'"{rng}"'
    jobs.run(gams_options=opt)
    # print(f'{csv_path} -> {gdxfilename}: Elapsed time {round(time.time() - start, 3)} sec.')
    return gdxfilename

def getConstraintsdata(path):
    '''
        path : string
            Input path to the folder where the 'constraints_list.csv' is hosted.
    '''
    dataframe = pd.read_csv(os.path.join(path, 'constraints_list.csv'))
    return dataframe

def getTopographydata(path, convar_dc):
    '''
        path : string
            Input path to the folder where the 'data_input.xlsx' is hosted.
    '''
    dataframe = pd.read_excel(os.path.join(path, convar_dc['data_input_file']),
                              sheet_name = "spatial",
                              usecols    = "M:AZ",
                              index_col  = 0,
                              header     = 0,
                              skiprows   = 1)
    return dataframe

def getGDXoutputOptions(convar_dc):
    features = ['gdx_convert_parallel_threads',
                'gdx_convert_to_csv',
                'gdx_convert_to_pickle',
                'gdx_convert_to_vaex']
    selection = {}
    for feat in features:
        if feat == 'gdx_convert_parallel_threads':
            selection[feat] = int(convar_dc[feat])
        else:
            if convar_dc[feat] == 'yes':
                selection[feat] = True
            elif convar_dc[feat] == 'no':
                selection[feat] = False
            else:
                raise Exception(f'{feat} must be "yes" or "no"')
    convert_cores = selection['gdx_convert_parallel_threads']
    csv_bool = selection['gdx_convert_to_csv']
    pickle_bool = selection['gdx_convert_to_pickle']
    vaex_bool = selection['gdx_convert_to_vaex']
    return csv_bool, pickle_bool, vaex_bool, convert_cores
