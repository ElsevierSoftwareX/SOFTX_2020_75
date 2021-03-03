Reporting
--------------------------------------------------------------------------------------

``reporting_symbols.csv``: This files contains a list of symbols (variable, parameter, equation) that are collected after the end of the optimization. All symbols specified here are collected from different scenario runs and saved a single file. Hence, for every symbol a separate file is created that contains all values of that symbol for all runs. In order to use that *reporting feature*, you have to set *report_data* to ``yes`` in ``project_variables.csv``. 

The file ``reporting_symbols.csv`` has per default the following column headers:

.. csv-table:: Column headers  ``reporting_symbols.csv``
   :header: "basic","rsvr_outflow","reserves","prosumage","dsm","heat","ev_endogenous","ev_exogenous"

   ,,,,,,,


