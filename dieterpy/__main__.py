import argparse
import os


def parser():
    parser = argparse.ArgumentParser(description='dieterpy command line')
    # add positional argument create_project and run
    parser.add_argument('command', help='This argument can be "create_project","run", or "gdxconvert"', type=str)
    parser.add_argument('-n','--name', help='Required argument for create_project. A project name must be provided', type=str)
    parser.add_argument('-t','--template', help='Required argument for create_project. Examples can be selected through templates, name of template are example1, example2 ...', type=str)
    parser.add_argument('-m','--method', help='Required argument for gdxconvert. Options: global, custom', type=str)
    parser.add_argument('-c','--cores', help='Optional argument for gdxconvert. Integer, number of parallel cores to process each symbol', type=str)
    parser.add_argument('-o','--output', help='Optional argument for gdxconvert. E.g "vaex-pickle-csv"', type=str)
    parser.add_argument('-w','--web', help='Optional argument for web. This argument can be "all" or "report"', type=str)

    args = parser.parse_args()
    return args

def main():
    arg_option = ['create_project', 'run', 'gdxconvert', 'web', 'create_report']
    args = parser()
    if not args.command in arg_option:
        raise Exception(f'First positional argument must be in {arg_option}')
    if args.command == 'create_project':
        if args.name:
            try:
                from dieterpy.tools import create_project
            except ImportError as exc:
                raise ImportError(
                 "Couldn't import dieterpy. Are you sure it's installed and "
                 "available on your PYTHONPATH environment variable? Did you "
                 "forget to activate a virtual environment?"
                 ) from exc
            if args.template:
                tmpl = args.template
            else:
                tmpl = 'base'
            return create_project(args.name, tmpl)
        else:
            raise Exception(f'Create_project argument must have a project name as --name argument')
    else:
        try:
            from dieterpy.tools import module_from_file
            from dieterpy.config import settings
            manage = module_from_file('manage', 'manage.py')
            settings.PROJECT_DIR_ABS = manage.PROJECT_DIR_ABS
            settings.update_changes()
        except ImportError as exc:
            raise ImportError("Couldn't import manage.py. Are you sure it's in current working dir?") from exc
        if args.command == 'run':
            try:
                from dieterpy.scripts import runopt
            except ImportError as exc:
                raise ImportError(
                    "Couldn't import dieterpy. Are you sure it's installed and "
                    "available on your PYTHONPATH environment variable? Did you "
                    "forget to activate a virtual environment?"
                ) from exc
            print('Running DIETER model\n ')
            return runopt.main()
        elif args.command == 'gdxconvert':
            if args.method:
                try:
                    from dieterpy.scripts.output_data import GDXpostprocessing
                except ImportError:
                    raise
                if args.method == 'global':
                    paths_list = os.path.join(settings.RESULTS_DIR_ABS,'*','*_config.yml')
                    print(paths_list)
                elif args.method == 'custom':
                    paths_list = []
                    print('Please, provide ID you want to include')
                    while True:
                        print("ID: ", end='')
                        add_id = input()
                        print(f'Is this ID correct: {add_id}? (Y/N):', end='')
                        confirm = input()
                        if confirm.lower() == 'y':
                            print(f'{add_id} added...')
                            paths_list.append(os.path.join(settings.RESULTS_DIR_ABS, add_id,add_id + '_config.yml'))
                        else:
                            print(f'Your answer is "{confirm}". Try with a new ID...')
                            continue
                        print(f'Do you want to add a new ID? (Y/N):', end='')
                        stop = input()
                        if stop.lower() == 'y':
                            pass
                        else:
                            break
                    print('Ids provided correspond to the following files:')
                    for path in paths_list:
                        print(f' {path}')
                else:
                    raise Exception(f'--method not recognized. It can be "global" or "custom"')
                if args.cores:
                    core = int(args.cores)
                else:
                    core = 0
                output_dc = {'vaex_bool':True, 'pickle_bool':True, 'csv_bool':True}
                if args.output:
                    if ' ' in args.output:
                        raise Exception('output formats requested must not have whitespaces. The possible options are vaex-pickle-csv')
                    ls = args.output.split('-')
                    if 'vaex' not in ls:
                        output_dc['vaex_bool'] = False
                    if 'pickle' not in ls:
                        output_dc['pickle_bool'] = False
                    if 'csv' not in ls:
                        output_dc['csv_bool'] = False
                    if not any(output_dc.values()):
                        raise Exception(f'--output "{args.output}" not recognized. Valid options are "vaex" "pickle" "csv" separated by hyphens (-) for more than one option')
                print('\nStarting with gdx conversion...')
                return GDXpostprocessing(method=args.method, input=paths_list, cores_data=core, **output_dc)
            else:
                raise Exception(f'--method is a required argument. It can be "global" or "custom"')
        elif args.command == 'create_report':

            try:
                from dieterpy.scripts.report import CollectScenariosPerSymbol
            except ImportError as exc:
                raise ImportError(
                    "Couldn't import dieterpy. Are you sure it's installed and "
                    "available on your PYTHONPATH environment variable? Did you "
                    "forget to activate a virtual environment?"
                ) from exc
            print('Generating report files:\nCollecting all pickle files that contain the symbols')
            print('Warning: Pickle files contain symbols listed in /project_files/settings/reporting_symbols.csv\nYou can add more symbols to the list and then call "GDXpostprocessing" from Python IDE or "gdxconvert" as dieterpy argument in the terminal or prompt')

            Data = CollectScenariosPerSymbol()
            Data.collectinfo()
            Data.join_all_symbols('v', True)
            try:
                Data.join_scens_by_symbol('con1a_bal', 'm', True, False)
            except:
                raise Exception('Pickle files do not contain symbol "con1a_bal", include it to /project_files/settings/reporting_symbols.csv, then run "gdxconvert" first to include the missing symbol in the pickle files')

        elif args.command == 'web':
            try:
                import sys
                from streamlit import cli as stcli
                import dieterpy
            except ImportError as exc:
                raise ImportError("Streamlit is not installed") from exc
            if not args.web:
                sys.argv = ["streamlit", "run", os.path.join(dieterpy.__path__[0], 'tools', "web_interface.py")]
            else:
                if args.web.lower == 'report':
                    raise Exception('This is not implemented yet')
                    sys.argv = ["streamlit", "run", os.path.join(settings.SETTINGS_DIR_ABS, "web_interface_report.py")]
                elif args.web == 'debug':
                    sys.argv = ["streamlit", "run", os.path.join(dieterpy.__path__[0], 'tools', "web_interface.py"), "--logger.level=debug"]
            sys.exit(stcli.main())

if __name__ == '__main__':
    main()
