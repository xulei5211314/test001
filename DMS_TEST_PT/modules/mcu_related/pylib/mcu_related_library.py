# -*- coding: utf-8 -*-
from library.common_lib import *
import time

import allure

from DMS_TEST_PT.library.common_lib import common_lib


@allure.step("进入诊断页面，获取诊断信息")
def fun_get_diag_text():
    common_lib.goto_page("工程界面")  # 进入工程页面
    log.logger.info("in to project")
    common_lib.click_element("工程模式_主界面_BUTTON_诊断")
    common_lib.swipe_up(4)
    common_lib.click_element("工程模式_主界面_BUTTON_诊断_单次诊断")
    common_lib.click_element("工程模式_主界面_BUTTON_诊断_单次诊断")
    common_lib.swipe_down(4)
    time.sleep(5)
    ret = common_lib.get_text("工程模式_主界面_BUTTON_诊断_DEV诊断")
    return ret


