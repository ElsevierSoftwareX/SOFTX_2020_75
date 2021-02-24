# DIETERpy is electricity market model developed by the research group
# Transformation of the Energy Economy at DIW Berlin (German Institute of Economic Research)
# copyright 2021, Carlos Gaete-Morales, Martin Kittel, Alexander Roth,
# Wolf-Peter Schill, Alexander Zerrahn
"""
    LoadSettings class contains the default values of global variables and include methods to change them.
    The main objective of this class is to be able to obtain such variables from any module.
"""
import os
from . import global_config


class LoadSettings:
    """
    Class contains settings variables such as project path.
    """

    def __init__(self):
        """
        Creates an instances of Settings class.
        """
        self.variables = Settings()

    def update_changes(self):
        """
        It updates all dependent variables.

        When a variable is modified such as the name of the project,
        then the path to all project folders must be updated.
        """
        self.variables.load_custom_settings()

    def __getattr__(self, name):
        """It returns a variable instance if exists

        Args:
            name (str): variable name

        Raises:
            AttributeError: if the name of the variable is not in capital letters

        Returns:
            object: instance of the variable
        """
        if not name.isupper():
            raise AttributeError
        return getattr(self.variables, name)

    def __setattr__(self, name: str, value: object):
        """It sets a new value for an existing variable

        Args:
            name (str): variable name
            value (object): new value

        Raises:
            AttributeError: if the variable name is not in capital letters
            AttributeError: if the variable does not exists
        """
        if hasattr(self, "variables"):
            if not name.isupper():
                raise AttributeError
            else:
                if hasattr(self.variables, name):
                    self.variables.__dict__[name] = value
                else:
                    raise AttributeError
        else:
            self.__dict__[name] = value

    def list(self):
        """
        It shows a list of the variable names and their values.
        """
        for k, v in self.variables.__dict__.items():
            if k.isupper():
                print(k, ":", v)


class Settings:
    """
    This class extract the variables from global_config.py and generates the paths that will be used by other dieterpy's modules
    """

    def __init__(self):
        """First gets default variables from global_config.py
        """
        for setting in dir(global_config):
            if setting.isupper():
                setattr(self, setting, getattr(global_config, setting))
        self.load_custom_settings()

    def load_custom_settings(self):
        """Method that generates the paths that will be used for other dieterpy's modules
        """
        self.BASE_DIR_ABS = os.path.join(self.PROJECT_DIR_ABS, self.BASE_DIR_NAME)
        self.INPUT_DIR_ABS = os.path.join(self.BASE_DIR_ABS, self.INPUT_DIR_NAME)
        self.SETTINGS_DIR_ABS = os.path.join(self.BASE_DIR_ABS, self.SETTINGS_DIR_NAME)
        self.ITERATION_DIR_ABS = os.path.join(
            self.BASE_DIR_ABS, self.ITERATION_DIR_NAME
        )
        self.MODEL_DIR_ABS = os.path.join(self.BASE_DIR_ABS, self.MODEL_DIR_NAME)
        self.RUN_DIR_ABS = os.path.join(self.BASE_DIR_ABS, self.RUN_DIR_NAME)
        self.GDX_INPUT_ABS = os.path.join(self.BASE_DIR_ABS, self.GDX_INPUT_NAME)
        self.RESULTS_DIR_ABS = os.path.join(self.BASE_DIR_ABS, self.RESULTS_DIR_NAME)
        self.REPORT_DIR_ABS = os.path.join(self.BASE_DIR_ABS, self.REPORT_DIR_NAME)
        self.TMP_DIR_ABS = os.path.join(self.BASE_DIR_ABS, self.TMP)
