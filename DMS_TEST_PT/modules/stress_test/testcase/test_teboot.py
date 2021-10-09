# -*-coding:utf-8-*-
import pytest
from modules.stress_test.pylib.stress_library import *


@allure.story("重启压力测试，重启次数：${rebootcnt}")
def test_reboot(rebootcnt=1):
    log.logger.info("即将重启的次数为 :{}".format(rebootcnt))
    for msgcout in range(int(rebootcnt)):
        log.logger.info('第 {} 次重启'.format(msgcout + 1))
        reboot_and_check_system_state_is_normal()
    log.logger.info('重启结束，共重启 {} 次'.format(rebootcnt))


def test_err_pin():
    """can发送车速大于2信号"""
    common_lib.call_bat('replace_CameraModule_json.bat')
    common_lib.j2_reboot()
    time.sleep(6)
    ret = common_lib.serial_listen_to_file(400)   #50*6 = 300s
    times = get_errorpin_reboot_times("ret")
    assert times == 6




if __name__ == '__main__':
    pytest.main()
