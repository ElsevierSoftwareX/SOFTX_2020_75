.. _prog_options:

**********************
Program options
**********************

Run a model
----------------------

Make sure you are within your project folder. Via the console, you can start an optimization by::

    dieterpy run


Create new project
--------------------

Once you are in the right folder, type the following command (*firstproject* will be the name of the new project and the new folder)::

    dieterpy create_project -n firstproject

or::

    dieterpy create_project --name firstproject


Example:
::
    some example code here


Convert output files
---------------------

.. code-block::

    dieterpy gdxconvert


Create output report
----------------------

.. code-block::

    dieterpy create_report

Start browser interface
------------------------

.. code-block::

    dieterpy ???

Taken from code (delete at the end)
-----------------------------------

.. code-block::

    parser.add_argument('command', help='This argument can be "create_project","run", or "gdxconvert"', type=str)

.. code-block::
    
    parser.add_argument('-n','--name', help='Required argument for create_project. A project name must be provided', type=str)

.. code-block::
    parser.add_argument('-t','--template', help='Required argument for create_project. Examples can be selected through templates, name of template are example1, example2 ...', type=str)

.. code-block::
    
    parser.add_argument('-m','--method', help='Required argument for gdxconvert. Options: global, custom', type=str)

.. code-block::
    
    parser.add_argument('-c','--cores', help='Optional argument for gdxconvert. Integer, number of parallel cores to process each symbol', type=str)

.. code-block::
    
    parser.add_argument('-o','--output', help='Optional argument for gdxconvert. E.g "vaex-pickle-csv"', type=str)

.. code-block::
    
    parser.add_argument('-w','--web', help='Optional argument for web. This argument can be "all" or "report"', type=str)

