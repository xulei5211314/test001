# -*- coding: utf-8 -*-
# @Time    : 2021/1/9
# @Author  : TingTing.Zhao
from library.common_lib import *

@allure.step("重启并检查车机、J2系统启动成功，AIService预览界面可启动")
def reboot_and_check_system_state_is_normal():
    common_lib.avn_reboot()
    time.sleep(150)
    common_lib.check_adb_connect()
    common_lib.check_hbipc_connect()
    common_lib.goto_page("AIservice预览界面")
def get_errorpin_reboot_times(ret):
    serialfile = os.path.join(os.path.dirname(__file__), r"..\..\..\result\serial", "serial_out.txt")
    file = open(serialfile,"r")
    errpin_str = "Starting kernel ..."
    start_times = 0
    for line in file.readlines():
        if errpin_str in line:
            start_times = start_times +1
    log.logger.info("==============================start_times==============================: {}".format(start_times))
    return start_times