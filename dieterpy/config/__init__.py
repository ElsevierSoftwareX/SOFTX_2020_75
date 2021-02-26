# DIETERpy is electricity market model developed by the research group
# Transformation of the Energy Economy at DIW Berlin (German Institute of Economic Research)
# copyright 2021, Carlos Gaete-Morales, Martin Kittel, Alexander Roth,
# Wolf-Peter Schill, Alexander Zerrahn
"""
This module consists of creating an object that can be called from any other module. The "setting" instance will provide preset variables.
The current implementation has names of folders and results that can be obtained in the global_config.py file. An advanced user can edit the default values of variables by accessing the settings instance.
"""
from . import setting

# generate instance. This will be called from other modules
settings = setting.LoadSettings()
