.. _data_output:

******************
Model data output
******************

(Still developing this section)

Two different pickle files can be generated. After finishing the optimization, GDX files can be converted to Pickle files. This file contain all selected parameters and variables per scenario. In the second place, if users run the function create_report in the command line, the tool generates new pickle files. Every pickle file will contain only one symbol (GAMS nomenclature for parameters, variables and equations) for all the different scenarios. In both files, the tool store dictionary objects. In the first case, the file's name is the corresponding scenario name, and the dictionary contains pandas data-frames of the symbols. In the second case, the file's name is the corresponding symbol's name, and the dictionary’s keys are the scenario names. The pickle files are compressed with gzip library. To open the pickle files, we have to use both libraries: gzip and pickle. Every scenario's pickle files are located in the data_output folder, while the files representing scenarios' symbols are located in the report_files folder. Alternatively, we have created an object that deals with the reporting files. They are called SymbolHandler and Symbol. SymbolHandler collects all files in the report_files folder. At the same time, Symbols open the requested symbol and enables operations between them to generate new symbols by taking care of the dimensions and scenarios. For all the mentioned options is recommended to use jupyter notebooks or spyder since they allow us to query the data as we see it. This is explained in the documentation in the user guide section.
