Features in nodes
------------------

``features_node_selection.csv``: In this file, you can switch on and off several submodules of the model for different nodes (countries).

The files looks as following (the comment column is not shown).

.. csv-table:: features_node_selection.csv
   :header: "feature","DE","FR","DK","BE","NL","PL","CZ","AT","CH","ES","IT","PT"

    "dsm",0,0,0,0,0,0,0,0,0,0,0,0
    "ev_endogenous",0,0,0,0,0,0,0,0,0,0,0,0
    "ev_exogenous",0,0,0,0,0,0,0,0,0,0,0,0
    "reserves",0,0,0,0,0,0,0,0,0,0,0,0
    "prosumage",0,0,0,0,0,0,0,0,0,0,0,0
    "heat",0,0,0,0,0,0,0,0,0,0,0,0

If a ``0`` is set in the respective cell, that particular module is not activated in that country. A ``1`` on the other side will activate that module in that country.

A brief description of the modules below:

dsm: Demand sight management
    Add brief description here.

ev_endogenous: Endogenous electric vehicles
    Add brief description here.

ev_exogenous: Exogenous electric vehicles
    Add brief description here.

reserves: Reserves
    Add brief description here.

prosumage: Prosumage
    Add brief description here.

heat: Heat provision
    Add brief description here.