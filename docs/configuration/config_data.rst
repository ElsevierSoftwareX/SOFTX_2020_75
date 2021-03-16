.. _data_options:

**********************
Input data
**********************

static_input.xlsx
----------------------------------------

This files contains time-invariant input data organized in spreadsheet format.

.. csv-table:: Spreadsheets in ``static_input.xlsx``
   :header: "sheet","content"

   "LICENSE","Information on licensing." 
   "spatial","Data on the underlying grid infrastructure and static bounds for net transfer capacities limiting electricity exchange." 
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
