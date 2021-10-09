# -*- coding: utf-8 -*-
from modules.mcu_related.pylib.mcu_related_library import *

@pytest.mark.quick_start
@allure.story("测试查看版本号")                     #测试说明将体现在报告中
def test_quick_start_get_version():              #pytest.ini文件中，以python_functions值开头的用例将会执行
    assert 1 == 1
    # common_lib.call_bat('2_get_version.bat')


@allure.story("测试查看版本号")                     #测试说明将体现在报告中
def test_quick_start_get_version2():             #pytest.ini文件中，以python_functions值开头的用例将会执行
    assert 1 == 1
    # common_lib.call_bat('2_get_version.bat')


@pytest.mark.smoke                               #若为冒烟用例，添加此装饰器
@allure.story("测试 PIPELINE_0_HANG（0x2066）")    #测试说明将体现在报告中
@pytest.mark.usefixtures("fix_upgrade")
def test_pipeline0_hunged():                     #pytest.ini文件中，以python_functions值开头的用例将会执行
    common_lib.call_bat('replace_CameraModule_json.bat')
    common_lib.j2_reboot()
    ret = fun_get_diag_text()
    assert "pipeline0 hunged" in ret              #测试断言


@allure.story("测试 2.3 J2_MM_PIPELINE_1_HANG（0x2075）")
@pytest.mark.usefixtures("fix_upgrade")
def test_pipeline1_hunged():           #所传入参为fixture前后置
    common_lib.call_bat('replace_CameraModule_json.bat')
    common_lib.j2_reboot()
    ret = fun_get_diag_text()
    assert "pipeline1 hunged" in ret


@allure.story("测试 2.4 J2_MM_PIPELINE_0_FPS_LOW（0x2067）")
@pytest.mark.usefixtures("fix_upgrade")
def test_pipeline0_fps_low():
    common_lib.call_bat('replace_CameraModule_json.bat')
    common_lib.j2_reboot()
    ret = fun_get_diag_text()
    assert "pipeline0 fps low" in ret


@allure.story("测试 2.5 J2_MM_PIPELINE_1_FPS_LOW（0x2077）")
@pytest.mark.usefixtures("fix_upgrade")
def test_pipeline1_fps_low():
    common_lib.call_bat('replace_CameraModule_json.bat')
    common_lib.j2_reboot()
    ret = fun_get_diag_text()
    assert "pipeline1 fps low" in ret


@allure.story("测试 2.6 J2_MM_ REDUNDANCY_DETECT_FAILED（0x2079）")
def test_bpu_redundancy_detect_err():
    common_lib.call_bat('4_replace_hobotdms_app.bat')
    common_lib.j2_reboot()
    ret = fun_get_diag_text()
    assert "bpu redundancy detect err" in ret
    common_lib.upgrade_j2()


@allure.story("测试 2.8 J2_MM_ CAMERA_FRAME_LOSS（0x2080）")
def test_camera_frame_lost():
    common_lib.call_bat('18_replace_libvio_for_dms_lost.bat')
    common_lib.j2_reboot()
    ret = fun_get_diag_text()
    assert "camera frame lost" in ret
    common_lib.upgrade_j2()


@allure.story("测试 2.9 J2_MM_ CAMERA_FRAME_OUT_OF_ORDER（0x2081）")
def test_dms_disorder():
    common_lib.call_bat('17_replace_libvio_for_dms_disorder.bat')
    common_lib.j2_reboot()
    ret = fun_get_diag_text()
    assert "camera frame disorder" in ret
    common_lib.upgrade_j2()


@allure.story("测试 2.10 J2_MM_ CAMERA_FRAME_REPEAT（0x2082）")
def test_camera_frame_repeat():
    common_lib.call_bat('20_replace_libvio_for_dms_repeat.bat')
    common_lib.j2_reboot()
    ret = fun_get_diag_text()
    assert "camera frame repeat" in ret
    common_lib.upgrade_j2()


@allure.story("测试 2.11 J2_MM_ CAMERA_FRAME_ GET_DELAY（0x2083）")
def test_camera_get_frame_delay():
    common_lib.call_bat('19_replace_libvio_for_dms_delay.bat')
    common_lib.j2_reboot()
    ret = fun_get_diag_text()
    assert "camera get frame delay" in ret
    common_lib.upgrade_j2()


@allure.story("测试 2.19 J2_MM_SPI_JSON_PARSE_FAILED（0x2084）")
def test_SPI_JSON_PARSE_FAILED():
    common_lib.call_bat('27_change_spi_dev_json_name.bat')
    common_lib.j2_reboot()
    ret = fun_get_diag_text()
    assert "spi driver json parse err" in ret
    common_lib.upgrade_j2()


@allure.story("测试 2.20 J2_MM_SPI_NODE_OPEN_FAILED（0x2085）")
@pytest.mark.usefixtures("fix_upgrade_image")
def test_spi_node_open_fail():
    common_lib.call_bat('换Image.gz.bat')
    common_lib.j2_reboot()
    ret = fun_get_diag_text()
    assert "camera get frame delay" in ret


@allure.story("测试 2.21 J2_MM_SPI_ROLLING_COUNTER_ERR（0x2086）")
def test_SPI_ROLLING_COUNTER_ERR():
    common_lib.call_bat('换Image.gz.bat')
    common_lib.j2_reboot()
    ret = fun_get_diag_text()
    assert "xxx" in ret
    common_lib.upgrade_j2()


@allure.story("测试 2.22 J2_MM_SPI_CRC_ERR（0x2087）")
@pytest.mark.usefixtures("fix_upgrade_image")
def test_SPI_SPI_CRC_ERR():
    common_lib.call_bat('换Image.gz.bat')
    common_lib.j2_reboot()
    ret = fun_get_diag_text()
    assert "xxx" in ret


@allure.story("测试2.23 J2_MM_SPI_DATA_REPEAT（0x2088）")
@pytest.mark.usefixtures("fix_upgrade_image")
def test_SPI_DATA_REPEAT():
    common_lib.call_bat('换Image.gz.bat')
    common_lib.j2_reboot()
    ret = fun_get_diag_text()
    assert "xxx" in ret


@allure.story("测试 2.24 J2_MM_SPI_SHAKEHAND_FAIL（0x2089）")
def test_SPI_SHAKEHAND_FAIL():
    common_lib.call_bat('29_replace_spi_service.bat')
    common_lib.j2_reboot()
    ret = fun_get_diag_text()
    assert "xxx" in ret
    common_lib.upgrade_j2()


@allure.story("测试 2.25 J2_MM_MCU_DATA_ERR（0x2090）")
def test_SPI_DATA_REPEAT():
    common_lib.call_bat('换Image.gz.bat')
    common_lib.j2_reboot()
    ret = fun_get_diag_text()
    assert "xxx" in ret
    common_lib.upgrade_j2()

if __name__ == '__main__':
    pytest.main()



