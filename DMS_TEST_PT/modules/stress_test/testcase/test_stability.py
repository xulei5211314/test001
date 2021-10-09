# -*- coding: utf-8 -*-
# @Time    : 2021/1/26
# @Author  : TingTing.Zhao

import pytest
from library.common_lib import *
from modules.stress_test.pylib.stability_library import *
from modules.stress_test.pylib.stress_library import *

log_dir = os.path.join(os.path.dirname(__file__), r"..\..\..\result\sys_log")
GLOBAL_FIND_ELEMENT = {
    "mem":"MEM USED: (.*?)MB",
    "cpu":"CPU: (.*?).0%",
    "bpu0":"BPU0 Loading: (.*?) | BPU1",
    "bpu1":"BPU1 Loading: (.*?)\n",
    "delay":'avg_delay" : (.*?),',
    "temp":"温度: (.*?) | BPU0",
}

def test_resource_01():
    top_log_dir = os.path.join(log_dir, r"ap_top_log.txt")
    common_lib.adb_shell("top -d 1 -n 8 -b > {}".format(top_log_dir))#-n 24hour
    ret = get_aiservice_info("cpu")
    assert ret < 5

def test_resource_02():
    top_log_dir = os.path.join(log_dir, r"ap_top_log.txt")
    common_lib.adb_shell("top -d 1 -n 8 -b > {}".format(top_log_dir))#-n 24hour
    ret = get_aiservice_info("mem")
    assert ret < 10

def test_resource_3():
    stability_diag_period_prepare()
    avg = get_avg_diag_info(GLOBAL_FIND_ELEMENT["cpu"])
    assert avg < 65

def test_resource_4():
    stability_diag_period_prepare()
    avg = get_avg_diag_info(GLOBAL_FIND_ELEMENT["mem"])
    assert avg < 65

def test_resource_5():
    stability_auto_diag_prepare()
    avg = get_avg_fps(0, 15)
    assert avg > 15

def test_resource_6():
    stability_auto_diag_prepare()
    #统计分析日志文件里的fps0数值（关键字 fps0）
    avg = get_avg_fps(1, 30)
    assert avg > 30

def test_resource_7():
    stability_diag_period_prepare()
    avg = get_avg_diag_info(GLOBAL_FIND_ELEMENT["bpu0"])
    assert avg < 65

def test_resource_8():
    stability_diag_period_prepare()
    avg = get_avg_diag_info(GLOBAL_FIND_ELEMENT["bpu1"])
    assert avg < 65

def test_resource_9():
    stability_diag_period_prepare()
    avg = get_avg_diag_info(GLOBAL_FIND_ELEMENT["delay"])
    assert avg < 65

def test_resource_10():
    stability_diag_period_prepare()
    avg = get_avg_diag_info(GLOBAL_FIND_ELEMENT["temp"])
    assert avg < 65


if __name__ == '__main__':
    pytest.main()