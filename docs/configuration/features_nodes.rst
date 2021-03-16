Features in nodes
------------------

``features_node_selection.csv``: In this file, you can switch on and off different modules for specific nodes (i.e., countries).

The file looks as folls (the comment column is not shown).

.. csv-table:: features_node_selection.csv
   :header: "feature","DE","FR","DK","BE","NL","PL","CZ","AT","CH","ES","IT","PT"

    "dsm",0,0,0,0,0,0,0,0,0,0,0,0
    "ev_endogenous",0,0,0,0,0,0,0,0,0,0,0,0
    "ev_exogenous",0,0,0,0,0,0,0,0,0,0,0,0
    "reserves",0,0,0,0,0,0,0,0,0,0,0,0
    "prosumage",0,0,0,0,0,0,0,0,0,0,0,0
    "heat",0,0,0,0,0,0,0,0,0,0,0,0

If a ``0`` is set in the respective cell, that particular module is not activated in that country. In contrast, a value ``1`` will activate the module in the respective country.

A brief description of the modules below:

dsm: Demand-side management
    This module contains two types of demand-side management (DSM): load curtailment and load shifting. Load curtailment means that demand can be reduced at some point in time without a repsective demand increase at a later point in time. A recovery period and a maximum curtailment duration are implemented with respective constraints. Load shifting, in contrast, means that DSM units which are shifted up in a given hour must be shifted down again in surrounding hours, which is again enforced by respective contraints. We provide input data for different types of both load shifting and load curtailment options, which differ in terms of investment and variable costs as well as duration times. An in-depth description of DIETER's DSM formulation is provided in Zerrahn & Schill (2015): On the representation of demand-side management in power system models. Energy 84, 840-845. http://dx.doi.org/10.1016/j.energy.2015.03.037

ev_endogenous: Endogenous electric vehicles
    Explanations will be added soon.

ev_exogenous: Exogenous electric vehicles
    Explanations will be added soon.

reserves: Reserves
    Explanations will be added soon.

prosumage: Prosumage
    Explanations will be added soon.

heat: Heat provision
    Explanations will be added soon.
