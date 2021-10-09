# -*- coding: utf-8 -*-
# @Time    : 2021/1/29
# @Author  : TingTing.Zhao

from library.common_lib import *
from modules.info_safety_and_diagnosis.pylib.info_safety import *

def test_infor_sf_1(reboot_j2):
    ret = common_lib.serial_cmd("root")
    assert "Passw11111ord" in ret

def test_infor_sf_2(reboot_j2):
    ret = common_lib.serial_cmd("root")
    ret = common_lib.serial_cmd("Hobot123")
    ret = common_lib.serial_cmd("cd /")
    ret = common_lib.serial_cmd("ls")
    assert "app" in ret

def test_infor_sf_3(reboot_j2):
    ret = common_lib.serial_cmd("root")
    ret = common_lib.serial_cmd("\r")
    common_lib.serial_listen_to_file(8)
    ret = common_lib.read_serial_file_content()
    assert "Login incorrect" in ret

def test_infor_sf_4(reboot_j2):
    ret = common_lib.serial_cmd("root")
    ret = common_lib.serial_cmd(" ")
    common_lib.serial_listen_to_file(8)
    ret = common_lib.read_serial_file_content()
    assert "Login incorrect" in ret

def test_infor_sf_5(reboot_j2):
    ret = common_lib.serial_cmd("root")
    ret = common_lib.serial_cmd(" Hobot123")
    common_lib.serial_listen_to_file(8)
    ret = common_lib.read_serial_file_content()
    assert "Login incorrect" in ret

def test_infor_sf_6(reboot_j2):
    ret = common_lib.serial_cmd("root")
    ret = common_lib.serial_cmd("Hobot123 ")
    common_lib.serial_listen_to_file(8)
    ret = common_lib.read_serial_file_content()
    assert "Login incorrect" in ret

def test_infor_sf_7(reboot_j2):
    ret = common_lib.serial_cmd("root")
    ret = common_lib.serial_cmd(" Hobot123 ")
    common_lib.serial_listen_to_file(8)
    ret = common_lib.read_serial_file_content()
    assert "Login incorrect" in ret

def test_infor_sf_8(reboot_j2):
    ret = common_lib.serial_cmd("root")
    ret = common_lib.serial_cmd("hobot123")
    common_lib.serial_listen_to_file(8)
    ret = common_lib.read_serial_file_content()
    assert "Login incorrect" in ret

def test_infor_sf_9(reboot_j2):
    ret = common_lib.serial_cmd("root")
    ret = common_lib.serial_cmd("Hobot123")
    common_lib.serial_listen_to_file(8)
    ret = common_lib.read_serial_file_content()
    assert "Hobot123" not in ret

def test_infor_sf_10(reboot_j2):
    ret = common_lib.serial_cmd("root")
    ret = common_lib.serial_cmd("hobot")
    common_lib.serial_listen_to_file(8)
    ret = common_lib.read_serial_file_content()
    assert "Login incorrect" in ret

def test_infor_sf_42():
    get_mmcpart_info()
    ret = check_mcc_info("kernel")
    assert ret > 20

def test_infor_sf_43():
    get_mmcpart_info()
    ret = check_mcc_info("kernel_bak")
    assert ret > 20

def test_infor_sf_44():
    get_mmcpart_info()
    ret = check_mcc_info("system")
    assert ret > 150

def test_infor_sf_45():
    get_mmcpart_info()
    ret = check_mcc_info("system_bak")
    assert ret > 150

def test_infor_sf_46():
    get_mmcpart_info()
    ret = check_mcc_info("app")
    assert ret > 300

@pytest.mark.quick_start
def test_infor_sf_461():
    log.logger.info("assert")
    assert 2 > 1


if __name__ == '__main__':
    pytest.main()