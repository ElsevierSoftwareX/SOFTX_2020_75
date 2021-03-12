#############################################
DIETERpy: A GAMS-Python framework for DIETER
#############################################

.. image:: https://img.shields.io/pypi/v/dieterpy.svg
   :target: https://pypi.org/project/dieterpy/
   :alt: DIETERpy Status Badge

.. image:: https://img.shields.io/pypi/pyversions/dieterpy.svg
   :target: https://pypi.org/project/dieterpy/
   :alt: DIETERpy Python Versions

.. image:: https://img.shields.io/pypi/l/dieterpy.svg
   :target: https://pypi.org/project/dieterpy/
   :alt: DIETERpy license

DIETERpy is electricity market model developed by the research group `Transformation of the Energy Economy <https://twitter.com/transenerecon>`_ at `DIW Berlin <https://www.diw.de/en/diw_01.c.604205.en/energy__transportation__environment_department.html>`__ (German Institute of Economic Research).

The open-source power sector optimization model `"Dispatch and Investment Evaluation Tool with Endogenous Renewables" (DIETER) <https://www.diw.de/de/diw_01.c.599753.de/modelle.html#ab_599749>`__ has been developed to investigate the role of electricity storage and sector coupling options in future scenarios with high shares of renewable energy sources. 

DIETERpy is a Python-based tool that enables an easy pre- and post-processing of the model data, sophisticated scenario analysis, and visualization of results. The optimization routine of DIETERpy is based on the General Algebraic Modeling System (GAMS) of DIETER, which is now maintained separately as a GAMS-only version called DIETERgms_.

.. _DIETERgms: https://gitlab.com/diw-evu/dieter_public/dietergms


.. youtube:: n7L0i5Dc5fM
   

***************
Installation
***************

DIETERpy is distributed on PyPI_ and can installed with ``pip``:

.. code-block:: console

    $ pip install dieterpy

Read the documentation to learn how to properly install_ DIETERpy.

.. _PyPI: https://pypi.org/project/dieterpy
.. _install: https://diw-evu.gitlab.io/dieter_public/dieterpy/gettingstarted/installation

*************************************
Configuration and running the model
*************************************

Please consult our full documentation_ on how to configure and run DIETERpy.

.. _documentation: https://diw-evu.gitlab.io/dieter_public/dieterpy/

***************
Links
***************

* Documentation: https://diw-evu.gitlab.io/dieter_public/dieterpy
* Source code: https://gitlab.com/diw-evu/dieter_public/dieterpy
* Issues: https://gitlab.com/diw-evu/dieter_public/dieterpy/issues
* PyPI releases: https://pypi.org/project/dieterpy
* License: http://opensource.org/licenses/MIT

***************
Authors
***************

The developers are `Carlos Gaete-Morales (lead) <mailto:cdgaete@gmail.com>`_, Alexander Roth and Martin Kittel, and Wolf-Peter Schill, in collaboration with Alexander Zerrahn.

***************
Applications
***************

DIETER has been used for numerous publications, both by DIW and external researchers. Please have a look at our *Applications* section of our documentation for a full list of DIW_ as well as external_ papers and projects. There, we provide detailed descriptions and the DIETER version used in the respective projects.

.. _DIW: https://diw-evu.gitlab.io/dieter_public/dieterpy/applications/diw.html
.. _external: https://diw-evu.gitlab.io/dieter_public/dieterpy/applications/external.html

***************
License
***************

DIETERpy is an open source tool which code may be freely used and modified by anyone. The code is licensed under the MIT License and available https://gitlab.com/diw-evu/dieter_public/dieterpy.

DIETER is an open source model which may be freely used and modified by anyone. The code is licensed under the MIT License. Input data is licensed under the Creative Commons Attribution-ShareAlike 4.0 International Public License and available under http://www.diw.de/dieter.
