.. _prog_options:

**********************
Program options
**********************

Explain the following commands:

dieterpy

    parser.add_argument('command', help='This argument can be "create_project","run", or "gdxconvert"', type=str)
    parser.add_argument('-n','--name', help='Required argument for create_project. A project name must be provided', type=str)
    parser.add_argument('-t','--template', help='Required argument for create_project. Examples can be selected through templates, name of template are example1, example2 ...', type=str)
    parser.add_argument('-m','--method', help='Required argument for gdxconvert. Options: global, custom', type=str)
    parser.add_argument('-c','--cores', help='Optional argument for gdxconvert. Integer, number of parallel cores to process each symbol', type=str)
    parser.add_argument('-o','--output', help='Optional argument for gdxconvert. E.g "vaex-pickle-csv"', type=str)
    parser.add_argument('-w','--web', help='Optional argument for web. This argument can be "all" or "report"', type=str)

