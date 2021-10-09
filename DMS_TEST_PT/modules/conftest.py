# -*- coding: gbk -*-
# @Time    : 2021/1/3
# @Author  : tingting.zhao
from library.common_lib import *
import uiautomator2 as u2




@pytest.fixture(scope="session", autouse=True)
def modules_global_suite_setup():

    #将pytest.ini文件的中的配置信息更新到config.pyd的GLOBAL_PROJECT_CFG中
    update_project_cfg()
    #获取root权限和文件及文件夹的权限
    common_lib.switch_to_root()
    # d.debug = True


#
# @pytest.hookimpl(hookwrapper=True, tryfirst=True)
# def pytest_runtest_makereport(item, call):
#     # 获取钩子方法的调用结果
#     out = yield
#     # 从钩子方法的调用结果中获取测试报告
#     report = out.get_result()
#     log.logger.info('step type：%s' % report.when)
#     log.logger.info('nodeid：%s' % report.nodeid)
#     log.logger.info('description:%s' % str(item.function.__doc__))
#     log.logger.info(('run result: %s' % report.outcome))
#     if report.failed:
#         source = common_lib._get_current_page_screencap()
#         allure.attach.file(source, "Failure screenshots", allure.attachment_type.PNG)
