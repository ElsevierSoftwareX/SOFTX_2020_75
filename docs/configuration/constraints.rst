Constraints
--------------------------------------------------------------------------------------

``constraints_list.csv``: This file contains information on all iterable constraint formulations. The column header specifies the *constraint type*, the row value the respective name of the constraint.

In the default setting, this file looks as follows:

.. csv-table:: Default ``constraints_list.csv``
   :header: "constraint_minRES","constraint_carbon"

    "rescon_0a","max_node_CO2"
    "rescon_1b","max_overall_CO2"
    "rescon_2c",
    "rescon_3b",
    "rescon_4e",

Currently, there are five different specifications of the *minimum renewable energy share* constraint and two different for the *CO2 budget* constraint.

There is no need to change this file unless you want to rename the existing constraints, add (1) new formulations for existing constraints, or (2) add formulations for a new constraint. In case of (1), add the respective name in the right column and adjust the code accordingly in the ``model.gms`` file. In case of (2), you have to add a new column to ``constraints_list.csv`` that contains the formulation names of the constraint.