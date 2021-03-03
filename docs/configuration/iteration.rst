Iteration
-----------

``iteration_table.csv``: This file is central to define scenario runs. If only a single run is intended, this file needs no further configuration.

The only required column is *run* as well as the respective number of each run (1, 2, 3, ...). To vary data, the selection of countries to be modeled, constraints, etc. between runs, the column headers of that file have configured accordingly, which will be explained briefly in the following. 

Countries
^^^^^^^^^^^^^^^^^^^^^^^^^^

To vary the set of nodes between the different scenario runs, add the column ``country_set`` to ``iteration_table.csv``. The row values of that column define the nodes to be considered for the respective run. No value means that all available nodes are included.

.. csv-table:: Configuration ``iteration_table.csv``: nodes
   :header: "run","country_set"

   1, 
   2, "DE"
   3, "DE,FR"

In this example, the first scenario run uses all available nodes (as provided ``static_input.xlsx``), the second run only Germany (``DE``), the third Germany and France (``"DE,FR"``). You will notice that the optimization time will be drastically lower for the 2nd and 3rd run. However, the model has to be recompiled between all three runs.

Time series
^^^^^^^^^^^^^^^^^^^^^^^^^^

To vary time-variant data between different runs, you have to configure two files. First, add the column ``time_series_scen`` to ``iteration_table.csv``. When you don't add that column or leave the column ``time_series_scen`` empty, the model will take the default time series. By adding an identifier in the column ``time_series_scen``, you can specify for every run, which data is to be used. 

Let's assume that you want to use three different time series scenarios: (1) German demand varied (scen1), (2) German capacity factors for PV and onshore wind varied (scen2), and (3) German and French demand varied (scen3). The ``iteration_table.csv`` has to be configured as following, assuming your first run uses default values:

.. csv-table:: Configuration ``iteration_table.csv``: time-variant data
   :header: "run","time_series_scen"

   1, 
   2,"scen1" 
   3,"scen2"
   4,"scen3"

Edit the ``iteration_data.xlsx`` file such that the sheet *scenario* looks as follows:

.. csv-table:: Time series iteration: configuration ``iteration_data.xlsx``
   :header: "","A","B","C","D","E","F"

   1,"Comments", , , , , 
   2,          , , , , , 
   3,"parameter", "d('DE',h)", "phi_res('DE','pv',h)", "phi_res('DE','wind_on',h)", "d('DE',h)", "d('FR',h)"
   4,"identifier","d(DE,h)","phi_res(DE,pv,h)","phi_res(DE,wind_on,h)","d(DE,h)","d(FR,h)"
   5,"scenario","scen1","scen2","scen2","scen3","scen3"
   6,"h1",38067,0,0.2327,38067,56328
   "...","...","...","...","...","...","..."
   8765,"h8760",61168,0,0.1824,61168,41618

For further details regarding the configuration of the file ``iteration_data.xlsx``, we refer to the section :ref:`data_options`.

Constrains
^^^^^^^^^^^^^^^^^^^^^^^^^^

There is a number of alternative constraints available in DIETERpy that (de-)activate carbon policy instruments. Currently, users can choose between different formulations of *renewable energy share* constraints and *CO2 budget* constraints:

.. csv-table:: Available constraint alternatives
   :header: "Constraint type","Identifer","Constraint","Explanation"

   "RES share", "constraint_minRES","rescon_0a", "Maximum share of conventional generation in total demand, losses are fulfilled with the minRES share"
   "RES share", "constraint_minRES","rescon_1b", "Maximum share of conventional generation in total demand, losses completely covered by RES"
   "RES share", "constraint_minRES","rescon_2c", "Maximum share of conventional generation in total generation, losses covered by RES proportional to (1-phi_min_res)"
   "RES share", "constraint_minRES","rescon_3b", "Maximum share of conventional generation in total demand, losses completely covered by RES"
   "RES share", "constraint_minRES","rescon_4e", "Maximum share of conventional generation in total demand, losses fulfilled in proportion to RES share"
   "CO2 budget","constraint_carbon","max_overall_CO2", "There is a cap on the available carbon budget, which applies to the generation across the entire spatial scope of the model."
   "CO2 budget","constraint_carbon","max_node_CO2", "There is a country-specific cap on the available carbon budget, which applies to the generation within each region separately."
   
To change the constraint in a specific run, add the value from the column *Identifer* to as a column to ``iteration_table.csv`` (hence ``constraint_minRES`` to vary a *RES share* and ``constraint_carbon`` a *CO2 budget*). In that respective column, choose the constraint type of your choice by adding the respective value (such as ``rescon_1b`` for the respective formulation). In case you do not specify anything, DIETERpy will use ``rescon_0a`` as *RES share* and ``max_node_CO2`` as *CO2 budget*.

A possible scenario setting, with changing *RES share* and *CO2 budget* formulations between runs, could be defined as follows:

.. csv-table:: Configuration ``iteration_table.csv``: constraints
   :header: "run","constraint_minRES","constraint_carbon"

   1,"rescon_1b",
   2,"rescon_2c",
   3,"rescon_4e","max_overall_CO2"
   4,"","max_node_CO2"

Variables & parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^

Values of parameter and variables can be set by adding the name of that symbol as a column header to the ``iteration_table.csv``. You have to check in the ``model.gms`` file how exactly the symbol is called and defined. In the following, we provide some examples for better understanding.

Setting a value of a variable 
***************************************************

Let's assume you want to set the generation capacity of solar power in Germany to 25 GW in one run and to 50 GW in another run. First, you need to find the correct symbol for generation capacity in the GAMS model (``N_TECH(n,tech)``), then the identifier for solar power (``pv``), then the identifier for Germany (``DE``). In order to fix a variable to a specific value, you need to append ``.fx`` to the respective symbol name (before the brackets though). Then add the country and technology identifier with '' in the right place within the bracket. As ``N_TECH`` is defined in terms of MW, you need to adjust your values accordingly.

In the first run, the PV capacity in Germany could be set freely (yet check possible limits in the ``static_input.xlsx`` file), set to 25 GW in the 2nd, and 50 GW in the 3rd run:

.. csv-table:: Configuration ``iteration_table.csv``: variables (1)
   :header: "run","country_set", "N_TECH.fx('DE','pv')"

   1, , 
   2, , 25000
   3, , 50000

Let's assume that you want to set these limits not only for Germany, but for all countries. Then your sheet has to look like the following. Note that ``'DE'`` has been replace by ``n`` (without ''), so it applies to the entire set ``n``:

.. csv-table:: Configuration ``iteration_table.csv``: variables (2)
   :header: "run","country_set", "N_TECH.fx(n,'pv')"

   1, , 
   2, , 25000
   3, , 50000

Setting a (lower/upper) limit of variable value
***************************************************

Setting an lower or upper limit for a value of variable follows the same logic as fixing a value. Instead of appending ``.fx``, you append ``.lo`` for lower value and ``.up`` for upper value. Let's assume you want to set an lower limit for the generation capacity of PV in Germany (25 GW and 50 GW) and an upper limit to the generation capacity of nuclear power (10 GW and 5 GW). As reference, the first run does not define any limits:

.. csv-table:: Configuration ``iteration_table.csv``: variable limits
   :header: "run","country_set", "N_TECH.lo('DE,'pv')", "N_TECH.up('DE,'nuc')"

   1, , 
   2, , 25000, 10000
   3, , 50000, 5000

Setting a value of a parameter 
***************************************************

Setting a value of a parameter has the same logic as for a variable, except that you can leave out the suffices ``.fx .lo .up``. Let's assume you want to run a two-country scenario (DE & FR) and you want to set the share of renewable energy (``phi_min_res_exog(n)``) of Germany to 50% in the 1st, and to 75% in the 2nd run. In the 3rd and 4th run these values should apply to both countries. Whenever you leave a cell empty, the default value will be taken:

.. csv-table:: Configuration ``iteration_table.csv``: parameters
   :header: "run", "country_set", "phi_min_res_exog('DE')", "phi_min_res_exog(n)"

   1,"DE,FR",0.50, 
   2,"DE,FR",0.75, 
   3,"DE,FR",    , 0.50
   4,"DE,FR",    , 0.75

In that same logic, you can vary the value of every parameter and variable in the entire model. Of course, you can also vary several of the above-described options at the same time, as shown in the example below:

.. csv-table:: Configuration ``iteration_table.csv``: several variations
   :header: "run", "country_set", "time_series_scen", "constraint_minRES", "phi_min_res_exog('DE')", "N_TECH.up('DE','nuc')", "N_TECH.lo(n,'pv')", "NTC.fx('l01')"
   
   1,    "DE", "scen1",             ,0.50, 10000,  50000,  5000
   2, "DE,FR", "scen1",            , 0.75,  5000, 100000, 10000
   3, "DE,FR",        , "rescon_1b", 0.50, 10000,  50000, 15000
   4,        ,        , "rescon_1b", 0.75,      , 100000,     0