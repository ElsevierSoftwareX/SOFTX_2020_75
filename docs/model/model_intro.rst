******************************
Introduction to the model
******************************

The "Dispatch and Investment Evaluation Tool with Endogenous Renewables" (DIETER) is a power sector model that has been developed to investigate the role of electricity storage and sector coupling options in future scenarios with high shares of variable renewable energy sources. Originally, DIETER has been written in the General Algebraic Modeling System (GAMS).

By now, DIETER encompasses two models: 

* **DIETERgms**, which is the renamed original, GAMS-only, DIETER model and
* **DIETERpy**, which is a Python-based tool that enables an easy pre- and post-processing of the model data, sophisticated scenario analysis, and visualization of results.

DIETERpy is a Python wrapper that enhances the functionalities of DIETER, but still uses GAMS in its core for the numerical optimization. All equations of the optimization problem can be found in the ``model.gms`` file which is currently based on `DIETERgms 1.3.1 <https://gitlab.com/diw-evu/dieter_public/dietergms/-/tree/1.3.1>`_.


General model characteristics
--------------------------------

DIETER is a power sector capacity expansion model based on linear equations. It minimizes total system costs in a long-run equilibrium setting under perfect foresight. In economic terms, it takes a social planner perspective. Its objective function is the sum of investment costs of various generation and flexibility technologies as well as transmission capacity, and related variable costs for a given time period (usually a full year). DIETER aims to minimize these costs, given exogenous techno-economic input parameters and time series such as electricity demand and renewable availability, which are provided in an hourly resolution. Hence, the solution represents a least-cost portfolio of generation and flexibility technologies, as well as their optimal dispatch for the given time period. The model is usually solved for all consecutive hours of a target year. 

A range of equations implements constraints with respect to generation capacities, renewable shares, CO:sub:2 emissions, renewable availability, balancing reserves, and electric load as well as sector coupling demand. Further, there are inter-temporal restrictions related to various types of storage and sector coupling. The model does not include a detailed representation of the underlying transmission grid infrastructure. Within regions, e.g., European countries, it makes a copper-plate assumption; between regions, DIETER uses a simple transport model approach with Net Transfer Capacities (NTCs). From the beginning, DIETER was designed as a lean, tractable and flexible open-source tool. The model applications that were published so far hardly required high-performance computing resources, but could largely be solved on a standard computer. 

Documentation
--------------

In this documentation, we discuss the most important parts of the model. In the section :ref:`principal_equations`, we present a few relevant equations of the model. In the section :ref:`model_options`, we present the most important features of the model. We aim to constantly update and expand this online documentation and are happy to receive user feedback in this respect.

For a more complete discussion of the model, we refer to the following sources:

* DIETERgms Documentation: 
    * Version 1.3.1: https://gitlab.com/diw-evu/dieter_public/dietergms/-/blob/1.3.1/DIETER_documentation.pdf
    * Latest version: https://gitlab.com/diw-evu/dieter_public/dietergms/-/blob/master/DIETER_documentation.pdf
* General introduction of the basic model:
    * Zerrahn & Schill (2017), Long-run power storage requirements for high shares of renewables: review and a new model, *Renewable and Sustainable Energy Reviews*, https://doi.org/10.1016/j.rser.2016.11.098
    * Schill & Zerrahn (2018), Long-run power storage requirements for high shares of renewables: Results and sensitivities, *Renewable and Sustainable Energy Reviews*, https://doi.org/10.1016/j.rser.2017.05.205
