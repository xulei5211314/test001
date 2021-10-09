# coding:utf-8
from library.common_lib import *
from modules.upgrade_test.pylib.upgrade_library import upgrade_j2_s202da_ui_preoperation



# @pytest.fixture(scope="session", autouse=True)
# def modules_global_suite_setup():
#     upgrade_j2_s202da_ui_preoperation()


@pytest.fixture( )
def reboot_j2():
    #重启J2
    common_lib.j2_reboot()
