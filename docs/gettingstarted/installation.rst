************************
Installing the program
************************

To run DIETERpy, you need to have a functioning installation of Python and GAMS. 

The following instructions describes in detail how to install Python, how to create a ``conda`` environment, how to install the Python API for GAMS, finally how to install DIETEpy and its dependencies.

Installation of GAMS
========================

If not already done, install first GAMS using the installation files from the `GAMS Website`_. GAMS is a proprietary software that requires a working license. If you do not have one, you can request a `Free Demo License`_ which will enable you to run a very basic version of DIETER. For questions regarding the installation and licensing of GAMS, we refer to the information_ provided by GAMS.

.. _GAMS Website: https://www.gams.com/download/
.. _Free Demo License: https://www.gams.com/download/
.. _information: https://www.gams.com/latest/docs/

Installation of Python
========================

The easiest and most convenient way to install Python is to install Anaconda (or Miniconda). Download the latest version from their website_ and install it.

During the installation of Anaconda on **Windows**, you will be asked to specify several options. We recommend you to choose the following ones so that DIETERpy will run smoothly:

* Install Anaconda to a custom directory (such as ``C:/Anaconda`` or ``D:/Anaconda``) and do not install it in the default folder, because this might increase the log-in and log-out out time;
* Do not use ``C:/Programs/`` or ``C:/Program Files/`` because this will require admin rights (recommended for permission restricted computers);
* During the installation, select "advanced option" and check both boxes (despite not recommended by the application). This will add this Conda Python Installation to the path and enables it as default python.

.. _website: https://www.anaconda.com/products/individual

Create a new Conda environment
--------------------------------

An conda environment is an isolated Python space. Different environments can contain different  Python packages of different versions. In order to have reproducible and stable "working space", it is useful to create a new environment for DIETERpy. 

.. warning:: Before creating the new environment, you need first to check which Python version is supported by your current GAMS version. To do so, you can either go the the `GAMS Documentation`_ and see which Python version is supported by your GAMS version or navigate to your GAMS directory (e.g. ``C:/GAMS/win64/26.1``). Within that folder, go to ``apifiles/Python/`` and see which Python versions are supported (e.g. the existence of the folders ``api_26``, ``api_34``, and ``api_36`` means that Python 2.6, 3.4, and 3.6 are supported).

Anaconda offers different ways to create a new environment:

**1. Anaconda Navigator**

Start the Anaconda Navigator and go on *Environments* and then *create*. Choose a name, tick the box next to *Python* and choose a Python version compatible with your GAMS installation (see box above).

**2. Console**

Open a console (Anaconda Prompt, CMD, PowerShell, Windows Terminal) and create a new conda environment with the name *yourenvname* and the exemplary Python version *X.X* with the following command::

    $ conda create -n yourenvname python=X.X

Do not forget to change the version to the version supported by your GAMS installation.

.. note:: To verify the successful creation of your environment, type ``conda info --envs`` in your console.

For further information on how to edit and delete conda environments, we refer to the `conda documentation`_.

.. _GAMS Documentation: https://www.gams.com/latest/docs/
.. _conda documentation: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html

Installation of the GAMS Python API
====================================

DIETERpy relies on the Python API that is provided by GAMS. Before installing and using DIETERpy, you need first manually install it. 

First, navigate to the correct folder in your GAMS installation such as ``C:/GAMS/win64/26.1/apifiles/Python/api_36``. The last part, ``api_36`` depends on the Python version you have installed in the step above.

In that folder, open a console and activate your conda environment which you just have created::

    $ conda activate yourenvname

Then execute the following command::

    $ python setup.py install

That will install the necessary GAMS-Python API files in your Python environment. For more details on the installation of the API, please consult the documentation_ provided by GAMS.

.. _documentation: https://www.gams.com/latest/docs/API_PY_TUTORIAL.html

Installation of DIETERpy
=========================

Now, your are ready to install DIETERpy. Make sure you have activated the correct environment::

    $ conda activate yourenvname

You can install DIETERpy easily from PyPI_::

    $ pip install dieterpy

Installing DIETERpy from PyPI ensures that all necessary linked packages are downloaded and installed.

.. note:: You can uninstall DIETERpy, while having activated the *yourenvname* environment, simply by executing ``$ pip uninstall dieterpy`` in the console.

.. _PyPI: https://pypi.org/project/dieterpy/