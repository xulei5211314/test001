# -*- coding: gbk -*-
# @Time    : 2021/1/3
# @Author  : tingting.zhao
from library.common_lib import *
import uiautomator2 as u2




@pytest.fixture(scope="session", autouse=True)
def modules_global_suite_setup():

    #��pytest.ini�ļ����е�������Ϣ���µ�config.pyd��GLOBAL_PROJECT_CFG��
    update_project_cfg()
    #��ȡrootȨ�޺��ļ����ļ��е�Ȩ��
    common_lib.switch_to_root()
    # d.debug = True


#
# @pytest.hookimpl(hookwrapper=True, tryfirst=True)
# def pytest_runtest_makereport(item, call):
#     # ��ȡ���ӷ����ĵ��ý��
#     out = yield
#     # �ӹ��ӷ����ĵ��ý���л�ȡ���Ա���
#     report = out.get_result()
#     log.logger.info('step type��%s' % report.when)
#     log.logger.info('nodeid��%s' % report.nodeid)
#     log.logger.info('description:%s' % str(item.function.__doc__))
#     log.logger.info(('run result: %s' % report.outcome))
#     if report.failed:
#         source = common_lib._get_current_page_screencap()
#         allure.attach.file(source, "Failure screenshots", allure.attachment_type.PNG)
