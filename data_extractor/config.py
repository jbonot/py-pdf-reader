import configparser
import os

config_file = "config.ini"
example_config_file = "config.ini.example"

config = configparser.ConfigParser()
if os.path.exists(config_file):
    config.read(config_file)
else:
    print(f"{config_file} not found. Falling back to {example_config_file}.")
    config.read(example_config_file)
