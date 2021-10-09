#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configparser
from _library.sys import *
from config.config import GLOBAL_PROJECT_CFG

config = configparser.ConfigParser()


def _get_pytest_ini_file():
    inifile = os.path.join(os.path.dirname(__file__), r"..", "pytest.ini")
    return inifile


def update_project_cfg():
    config.read_file(open(_get_pytest_ini_file()))
    car_type_data = config.get('cfg_param','cartype')
    GLOBAL_PROJECT_CFG['CARTYPE'] = car_type_data
    id_data = config.get('cfg_param', 'id')
    GLOBAL_PROJECT_CFG['ID'] = id_data
    reruns_data = config.get('cfg_param', 'reruns')
    GLOBAL_PROJECT_CFG['RERUNS'] = reruns_data
    log.logger.info("GLOBAL_PROJECT_CFG:{}".format(GLOBAL_PROJECT_CFG))


def set_ini_data(key1,key2,value):
    try:
        config.read_file(open(_get_pytest_ini_file()))
        config.set(key1, key2, value)
        config.write(open(_get_pytest_ini_file(), "r+"))
    except:
        raise Exception("ini update fail!")


def get_ini_data(key1,key2):
    try:
        config.read_file(open(_get_pytest_ini_file()))
        data = config.get(key1,key2)
        return data
    except:
        raise Exception("ini get fail!")


if __name__ == '__main__':
    test_ini=get_ini_data('cfg_param','cartype')
    print(test_ini)
    update_project_cfg()
    print(GLOBAL_PROJECT_CFG)

