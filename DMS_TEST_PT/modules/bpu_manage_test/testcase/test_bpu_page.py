# -*- coding: utf-8 -*-
# @Time    : 2021/1/6
# @Author  : TingTing.Zhao
import pytest
from modules.bpu_manage_test.pylib.bpu_manage_library import *


@allure.story("BPU模块界面显示")
def test_check_page():
    goto_and_check_bpu_page()


@allure.story("获取apk版本信息")
def test_get_apk_version():
    get_apk_version()


@allure.story("获取BPU版本信息")
def test_get_bpu_version():
    get_bpu_version()


@allure.story("获取J2_CHIPID")
def test_get_j2_chipID():
    get_j2_chipID()


@allure.story("获取BPU运行状态")
def test_get_bpu_run_state():
    get_bpu_run_state()


@allure.story("获取BPU运行时系统信息状态")
def test_get_sys_info():
    get_sys_info()


@allure.story("获取BPU感知感知能力")
def test_get_bpu_capabilities():
    get_bpu_capabilities()


if __name__ == '__main__':
    pytest.main()
