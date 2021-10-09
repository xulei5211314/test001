# -*- coding: utf-8 -*-
# @Time    : 2021/1/9
# @Author  : TingTing.Zhao
from config.config import GLOBAL_PROJECT_CFG
import importlib

GLOBAL_DEVICES_ID = GLOBAL_PROJECT_CFG.get("ID")   # 全局的ID
GLOBAL_CARTYPE = GLOBAL_PROJECT_CFG.get("CARTYPE")     # 全局的cartype
project_varible_path = 'variables.{}_variable'.format(GLOBAL_CARTYPE)
import_project_varible = importlib.import_module(project_varible_path)
GLOBAL_LOCATOR = import_project_varible.GLOBAL_LOCATOR      # 全局的locator定位符
GLOBAL_PAGE_ACTIVITY = import_project_varible.GLOBAL_PAGE_ACTIVITY      # 全局的page activity