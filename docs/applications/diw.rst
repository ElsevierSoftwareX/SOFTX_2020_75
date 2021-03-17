.. _application-diw:

.. |br| raw:: html

    <br>

=========================
DIW
=========================

2021
""""

so far empty

|br|

2020
""""

**DIETERpy: a Python framework for The Dispatch and Investment Evaluation Tool with Endogenous Renewables** |br| Carlos Gaete-Morales, Martin Kittel, Alexander Roth, Wolf-Peter Schill, Alexander Zerrahn

*Abstract:* |br| DIETER is an open-source power sector model designed to analyze future settings with very high shares of variable renewable energy sources. It minimizes overall system costs, including fixed and variable costs of various generation, storage and sector coupling options. Here we introduce DIETERpy that builds on the existing model version, written in the General Algebraic Modeling System (GAMS), and enhances it with a Python framework. This combines the flexibility of Python regarding pre- and post-processing of data with a straightforward algebraic formulation in GAMS and the use of efficient solvers. DIETERpy also offers a browser-based graphical user interface. The new framework is designed to be easily accessible as it enables users to run the model, alter its configuration, and define numerous scenarios without a deeper knowledge of GAMS. Code, data, and manuals are available in public repositories under permissive licenses for transparency and reproducibility.

Download: `arXiv <https://arxiv.org/abs/2010.00883>`_ |br| Model version: `0.2.0 (DIETERpy) <https://gitlab.com/diw-evu/dieter_public/dieterpy/-/releases/v0.2.0>`_

---------------

**Green hydrogen: optimal supply chains and power sector benefits** |br| Fabian Stöckl, Wolf-Peter Schill, Alexander Zerrahn

*Abstract:* |br| Green hydrogen can help to decarbonize transportation, but its power sector interactions are not well understood. It may contribute to integrating variable renewable energy sources if production is sufficiently flexible in time. Using an open-source co-optimization model of the power sector and four options for supplying hydrogen at German filling stations, we find a trade-off between energy efficiency and temporal flexibility: for lower shares of renewables and hydrogen, more energy-efficient and less flexible small-scale on-site electrolysis is optimal. For higher shares of renewables and/or hydrogen, more flexible but less energy-efficient large-scale hydrogen supply chains gain importance as they allow disentangling hydrogen production from demand via storage. Liquid hydrogen emerges as particularly beneficial, followed by liquid organic hydrogen carriers and gaseous hydrogen. Large-scale hydrogen supply chains can deliver substantial power sector benefits, mainly through reduced renewable surplus generation. Energy modelers and system planners should consider the distinct flexibility characteristics of hydrogen supply chains in more detail when assessing the role of green hydrogen in future energy transition scenarios.

Download: `arXiv <https://arxiv.org/abs/2005.03464>`_ |br| Model version: `1.4 (DIETERgms) <https://gitlab.com/diw-evu/dieter_public/dietergms/-/releases/1.4.0>`_

---------------

**Substituting Clean for Dirty Energy: A Bottom-Up Analysis** |br| Fabian Stöckl, Alexander Zerrahn

*Abstract:* |br| We fit CES and VES production functions to data from a numerical bottom-up optimization model of electricity supply with clean and dirty inputs. This approach allows for studying high shares of clean energy not observable today and for isolating mechanisms that impact the elasticity of substitution between clean and dirty energy. Central results show that (i) dirty inputs are not essential for production. As long as some energy storage is available, the elasticity of substitution between clean and dirty inputs is above unity; (ii) no single clean technology is indispensable, but a balanced mix facilitates substitution; (iii) substitution is harder for higher shares of clean energy. Finally, we demonstrate how changing availability of generation and storage technologies can be implemented in macroeconomic models.

Download: `DIW Discussion Paper <https://www.diw.de/documents/publikationen/73/diw_01.c.795779.de/dp1885.pdf>`_ |br| Model version: `1.3.1 based reduced version (DIETERgms) <https://zenodo.org/record/3940514#.YD9fLmhKg2w>`_

