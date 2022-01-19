import sys

from dotenv import dotenv_values

current_module = sys.modules[__name__]

# import config variables from the .env file at the root of the project
for k, v in dotenv_values().items():
    # set the attributes for the config object
    setattr(current_module, str(k), str(v))
