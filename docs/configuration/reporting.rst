Reporting
--------------------------------------------------------------------------------------

``reporting_symbols.csv``: This files contains a list of symbols (variable, parameter, equation) that are collected after the end of the optimization. All symbols specified here are collected from different scenario runs and saved a single file. Hence, for every symbol a separate file is created that contains all values of that symbol of all runs. In order to use that *reporting feature*, you have to set *report_data* to ``yes`` in ``project_variables.csv``. 

The file ``reporting_symbols.csv`` has per default the following column headers:

.. csv-table:: Column headers  ``reporting_symbols.csv``
   :header: "basic","reserves","prosumage","dsm","heat","ev_endogenous","ev_exogenous"

   ,,,,,,,

If reporting is activated, DIETERpy will consider the symbols noted in the column *basic* and will generate report files for every symbol in that column. In case a special module is activated in the ``features_node_selection.csv`` file, the respective column in ``reporting_symbols.csv`` will also be considered and the symbols of that column will also be reported in addition.

The folder of ``reporting_symbols.csv`` also contains the file ``reporting_symbols_original.csv`` which holds all available symbols that can be included in the reporting.