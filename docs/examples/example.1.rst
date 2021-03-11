.. _example1:

Example 1
---------

In this example, we would like to see each country's optimal investments when we reduce the annualized investment costs for the two components 'energy' and 'power' for the Li-Ion battery.

We have to edit two files: iteration_table.csv in the iterationfiles folder and features_node_selection.csv.

The iteration_table.csv modifies variables and constraints in the DIETER (model.gms) and parameters included in excel files contained in the 'data_input' folder. All the remaining parameters not included in the iteration remain intact as obtained from the excel files.

- We do not include a column heading 'country_set'. Doing this means that we will consider all the countries as included in the excel file.
- We assume then that the set 'n' contains all the countries.

In the features_node_selection.csv, we have to deactivate all the activated features by replacing 1 to 0.

See the project_variables.csv to understand the structure.