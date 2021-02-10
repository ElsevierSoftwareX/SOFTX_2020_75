*************
Run a model
*************

After having created a project folder (last section), you are ready to run the model. There are several ways to run the model, which are presented shortly here.

Method 1: from console (simple)
================================

Activate the conda environment in which you have installed DIETER. The active path in your console has to point the projected folder (make sure that the *manage.py* file is present).

You can start the optimization by typing::

    dieterpy run

Once the optimization has finished, you can analyze the output data. You find the output (depending on your configuration) in ``project_files/output_data`` and ``project_files/report_files``.

Method 2: from Python (advanced)
=================================

You can also run DIETERpy directly from the Python console. However, you have to provide some additional information in order to run the model successfully. 

Open a Python console (make sure that the correct conda environment is activated) and import the DIETERpy package::

    >>> import dieterpy
    >>> from dieterpy.scripts import runopt
    >>> from dieterpy.config import settings

Then set the correct path so that DIETERpy finds your project folder::

    >>> settings.PROJECT_DIR_ABS = "<here the absolute path to the project directory as string>"
    >>> settings.update_changes()

Finally, run the model::

    >>> runopt.main()

TO BE DOCUMENTED::

    >>> result_configuration_dict = settings.RESULT_CONFIG