import configparser
import os
def config_file(section, variable):
    config = configparser.RawConfigParser()
    filename = os.getcwd()
    config.read(filename+'\\config\\config.ini')
    path_str = config.get(section, variable)
    return path_str