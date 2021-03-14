.. _data_options:

**********************
Input and output data
**********************

Input data
++++++++++++

static_input.xlsx
----------------------------------------

This files contains time-invariant input data organized in spreadsheet format.

.. csv-table:: Spreadsheets in ``static_input.xlsx``
   :header: "sheet","content"

   "LICENSE","Information on licensing." 
   "spatial","Data on the underlying grid infrastructure." 
   "technologies","Techno-economic assumptions on available generation technologies."
   "storage","Techno-economic assumptions on available storage technologies."
   "reservoir","Techno-economic assumptions on available reservoir technologies."
   "DSM","Techno-economic assumptions on available demand side management technologies."
   "EV","Techno-economic assumptions on available electric vehicles."
   "prosumage","Techno-economic assumptions on available prosumage technologies."
   "reserves","Techno-economic assumptions on available reserve technologies."
   "heat","Techno-economic assumptions on available heat technologies."
   "2dim","Country-specific system configuration of the minimum renewable share, available carbon budget, share of prosumagers among total load, and the number of electric vehicles."
   "1dim","System-wide configuration of the minimum renewable share, available carbon budget, minimum self-generation shares for prosumagers, and variable costs of the slack generator which catches infeasibilies."
   "py","Configures data import."
   "Sources","List of references."


timeseries_input.xlsx
----------------------------------------

This files contains hourly time-variant input data organized in spreadsheet format.

.. csv-table:: Spreadsheets in ``timeseries_input.xlsx``
   :header: "sheet","content"

   "basic","Basic data required for each run, such as demand and various renewable availablity profiles." 
   "EV","Profiles for demand for driving from electric vehicles, battery capacity etc. disaggregated for different vehicle types." 
   "reserves_provision","Profiles for reserve demand."
   "reserves_activation","Profiles for reserve activation."
   "heat","Profiles for heat demand disaggregated for different building types."
   "heat_dhw","Profiles for DHW demand disaggregated for different building types."
   "NETS","Heat demand for NETS."
   "heat_pump","Temperature assumptions."
   "py","Configures data import."

iteration_data.xlsx
----------------------------------------

*Detailed explanations will be added soon.*

For now, check the `time series iteration`_ section on how to configure the `iteration_data.xlsx` file.

.. _time series iteration: ../configuration/iteration.html#time-series

Output data
+++++++++++++

Two different pickle files can be generated. After finishing the optimization, GDX files can be converted to Pickle files. This file contain all selected parameters and variables per scenario. In the second place, if users run the function create_report in the command line, the tool generates new pickle files. Every pickle file will contain only one symbol (GAMS nomenclature for parameters, variables and equations) for all the different scenarios. In both files, the tool store dictionary objects. In the first case, the file's name is the corresponding scenario name, and the dictionary contains pandas data-frames of the symbols. In the second case, the file's name is the corresponding symbol's name, and the dictionary’s keys are the scenario names. The pickle files are compressed with gzip library. To open the pickle files, we have to use both libraries: gzip and pickle. Every scenario's pickle files are located in the data_output folder, while the files representing scenarios' symbols are located in the report_files folder. Alternatively, we have created an object that deals with the reporting files. They are called SymbolHandler and Symbol. SymbolHandler collects all files in the report_files folder. At the same time, Symbols open the requested symbol and enables operations between them to generate new symbols by taking care of the dimensions and scenarios. For all the mentioned options is recommended to use jupyter notebooks or spyder since they allow us to query the data as we see it. This is explained in the documentation in the user guide section.
