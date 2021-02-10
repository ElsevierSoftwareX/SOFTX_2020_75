##########################
DIETERpy: A GAMS-Python framework for DIETER
##########################

.. image:: https://img.shields.io/pypi/v/dieterpy.svg
   :target: https://pypi.python.org/pypi/dieterpy
   :alt: DIETERpy Version

DIETERpy is electricity market model developed by the research group `Transformation of the Energy Economy <https://twitter.com/transenerecon>`_ at `DIW Berlin <https://www.diw.de/en/diw_01.c.604205.en/energy__transportation__environment_department.html>`__ (German Institute of Economic Research).

DIETERpy is a Python-based tool that enables an easy pre- and post-processing of the model data, sophisticated scenario analysis, and visualization of results. The optimization routine of DIETERpy is based on the GAMS-code of DIETERgms.

The open-source power sector optimization model `"Dispatch and Investment Evaluation Tool with Endogenous Renewables" (DIETER) <https://www.diw.de/de/diw_01.c.599753.de/modelle.html#ab_599749>`__ has been developed to investigate the role of electricity storage and sector coupling options in future scenarios with high shares of renewable energy sources. DIETER has originally been written entirely in the General Algebraic Modeling System (GAMS) and the GAMS-only version is now maintained as DIETERgms_. 

.. _DIETERgms: https://gitlab.com/diw-evu/dieter_public/dietergms

***************
Installation
***************

DIETERpy can is distributed on PyPI_ and can installed with ``pip``:

.. code-block:: console

    $ pip install dieterpy

For more information read the full documentation on Installation_.

.. _PyPI: https://pypi.org/project/dieterpy
.. _Installation: https://diw-evu.gitlab.io/dieter_public/dieterpy/gettingstarted/installation

***************
Running the model and configuration
***************

Please check out the full documentation on how to run_ and configure_ DIETERpy.

.. _run: https://diw-evu.gitlab.io/dieter_public/dieterpy/gettingstarted/running
.. _configure: https://diw-evu.gitlab.io/dieter_public/dieterpy/gettingstarted/configuration

***************
Links
***************

Documentation: https://diw-evu.gitlab.io/dieter_public/dieterpy

Source code: https://gitlab.com/diw-evu/dieter_public/dieterpy

PyPI releases: https://pypi.org/project/dieterpy

License: http://opensource.org/licenses/MIT

***************
Authors
***************

The developers are `Carlos Gaete-Morales (lead) <mailto:cdgaete@gmail.com>`_, Alexander Roth and Martin Kittel, and Wolf-Peter Schill, in collaboration with Alexander Zerrahn.

***************
License
***************

DIETERpy is an open source tool which code may be freely used and modified by anyone. The code is licensed under the MIT License and available https://gitlab.com/diw-evu/dieter_public/dieterpy.

DIETER is an open source model which may be freely used and modified by anyone. The code is licensed under the MIT License. Input data is licensed under the Creative Commons Attribution-ShareAlike 4.0 International Public License and available under http://www.diw.de/dieter.