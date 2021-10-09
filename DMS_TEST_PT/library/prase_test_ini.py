#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configparser
from _library.sys import *
from config.config import GLOBAL_PROJECT_CFG

config = configparser.ConfigParser()

class prase_ini():
    @classmethod
    def _get_pytest_ini_file(self):
        """
        获取ini文件路径
        :return: 返回文件句柄
        """
        inifile = os.path.join(os.path.dirname(__file__), r"..", "pytest.ini")
        return inifile

    @classmethod
    def update_project_cfg(self):
        """
        根据ini文件配置内容，更新工程
        """
        config.read_file(open(self._get_pytest_ini_file()))
        car_type_data = config.get('cfg_param','cartype')
        GLOBAL_PROJECT_CFG['CARTYPE'] = car_type_data
        id_data = config.get('cfg_param', 'id')
        GLOBAL_PROJECT_CFG['ID'] = id_data
        reruns_data = config.get('cfg_param', 'reruns')
        GLOBAL_PROJECT_CFG['RERUNS'] = reruns_data
        log.logger.info("GLOBAL_PROJECT_CFG:{}".format(GLOBAL_PROJECT_CFG))

    @classmethod
    def set_ini_data(self,key1,key2,value):
        """
        设置ini文件中某key对应的内容
        :param key1：ini文件中的父key  如cfg_param
        :param key2：ini文件中的子key  如cartype
        :return:
        """
        try:
            config.read_file(open(self._get_pytest_ini_file()))
            config.set(key1, key2, value)
            config.write(open(self._get_pytest_ini_file(), "r+"))
        except:
            raise Exception("ini update fail!")

    @classmethod
    def get_ini_data(self,key1,key2):
        """
        获取ini文件中某key对应的内容
        :param key1：ini文件中的父key  如cfg_param
        :param key2：ini文件中的子key  如cartype
        :return:key对应的内容字符串
        """
        try:
            config.read_file(open(self._get_pytest_ini_file()))
            data = config.get(key1,key2)
            return data
        except:
            raise Exception("ini get fail!")


if __name__ == '__main__':
    test_ini=prase_ini.get_ini_data('cfg_param','cartype')
    print(test_ini)
    prase_ini.update_project_cfg()
    print(GLOBAL_PROJECT_CFG)

