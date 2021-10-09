# -*- coding: utf-8 -*-
# @Time    : 2021/1/9
# @Author  : TingTing.Zhao
from library.common_lib import *


@allure.step("进入BPU页面，检查界面显示正常")
def goto_and_check_bpu_page():
    common_lib.goto_page("工程界面")  # 进入工程页面
    time.sleep(10) # sleep 10s, wait for app to run
    d(text="BPU管理").click()
    time.sleep(1) # sleep 1s, wait for app to run
    ret = d(resourceId=(common_lib.id("工程模式_BPU管理_TEXT_获取系统信息"))).get_text()
    assert "1.获取BPU系统信息" in ret, "BPU管理页面，界面显示正常"


@allure.step("获取apk版本")
def get_apk_version():
    time.sleep(1) # sleep 1s, wait for app to run
    d(text="获取APK版本信息").click()
    time.sleep(1) # sleep 1s, wait for app to run
    ret = d(resourceId=(common_lib.id("工程模式_BPU管理_TEXT_APK版本信息"))).get_text()
    assert "***" not in ret, "BPU管理页面，获取APK版本信息失败"


@allure.step("获取BPU版本信息")
def get_bpu_version():
    time.sleep(1) # sleep 1s, wait for app to run
    d(text="获取BPU版本信息").click()
    time.sleep(1) # sleep 1s, wait for app to run
    ret = d(resourceId=(common_lib.id("工程模式_BPU管理_TEXT_BPU版本"))).get_text()
    assert "***" not in ret, "BPU管理页面，获取BPU版本信息失败"


@allure.step("获取J2_CHIPID")
def get_j2_chipID():
    time.sleep(1) # sleep 1s, wait for app to run
    d(text="获取J2 CHIPID").click()
    time.sleep(1) # sleep 1s, wait for app to run
    ret = d(resourceId=(common_lib.id("工程模式_BPU管理_TEXT_J2chipID"))).get_text()
    assert "***" not in ret, "BPU管理页面，获取J2chipID失败"


@allure.step("获取BPU运行状态")
def get_bpu_run_state():
    time.sleep(1) # sleep 1s, wait for app to run
    d(text="获取BPU运行状态").click()
    time.sleep(1) # sleep 1s, wait for app to run
    ret = d(resourceId=(common_lib.id("工程模式_BPU管理_TEXT_BPU运行状态"))).get_text()
    assert " RUNNING" == ret, "BPU管理页面，获取BPU运行状态失败"


@allure.step("获取BPU运行时系统信息状态")
def get_sys_info():
    time.sleep(1) # sleep 1s, wait for app to run
    d(text="获取BPU运行时系统信息状态").click()
    time.sleep(1) # sleep 1s, wait for app to run
    ret = d(resourceId=(common_lib.id("工程模式_BPU管理_TEXT_BPU系统信息状态"))).get_text()
    assert "***" not in ret, "BPU管理页面，获取BPU运行时系统信息失败"


@allure.step("获取BPU感知能力")
def get_bpu_capabilities():
    common_lib.swipe_down() # Slide down
    time.sleep(1) # sleep 1s, wait for app to run
    d(text="获取BPU感知能力").click()
    ret = d(resourceId=(common_lib.id("工程模式_BPU管理_TEXT_BPU感知能力"))).get_text()
    assert "***" not in ret, "BPU管理页面，获取BPU感知能力信息失败"
