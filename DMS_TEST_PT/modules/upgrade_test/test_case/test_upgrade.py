# -*- coding: utf-8 -*-
import allure
import pytest
from library.common_lib import *
from shutil import copyfile
from modules.upgrade_test.pylib.upgrade_library import *
import zipfile, os, pytest
# GLOBAL_FIND_ELEMENT = {
#     "mem":"MEM USED: (.*?)MB",
#     "cpu":"CPU: (.*?).0%",
#     "bpu0":"BPU0 Loading: (.*?) | BPU1",
#     "bpu1":"BPU1 Loading: (.*?)\n",
#     "delay":'avg_delay" : (.*?),',
#     "temp":"温度: (.*?) | BPU0",
# }


@allure.story("升级测试")
def test0128_upgradeJ2():
    common_lib.call_bat('upgrade_J2_all_in_one_MM_signed.bat')
    ret = upgrade_s202da_j2_ret()
    assert "升级成功" in ret



@allure.story("升级包大小限制")
def test_ota_case_1():
    upgrade_pack = get_upgrade_zip()
    upgrade_zip=zipfile.ZipFile(upgrade_pack)
    for upgrade_file in upgrade_zip.namelist():
        fileinfo = upgrade_zip.getinfo(upgrade_file)
        log.logger.info("size:{}".format(fileinfo.file_size))
        if fileinfo.file_size > (500 * 1024 *1024):
            raise Exception("upgrade file size > 500M")


@allure.story("升级包push到车机")
def test_ota_case_2():
    push_no_udisk_zip()


@allure.story("升级有签名校验的升级包")
def test_ota_case_3():
    push_no_udisk_zip()
    ret = upgrade_s202da_j2_ret()
    assert "升级成功" in ret


@allure.story("升级app包错误签名的升级包")
def test_ota_case_4():
    upgrade_package_extract()
    clear_all_in_one_package()
    ret = get_upgrade_no_udisk_zip()
    modify_signature("app.zip",0)
    ret = upgrade_s202da_j2_ret()
    assert "错误" in ret


@allure.story("升级kernel包错误签名的升级包")
def test_ota_case_5():
    upgrade_package_extract()
    clear_all_in_one_package()
    ret = get_upgrade_no_udisk_zip()
    modify_signature("kernel.zip",0)
    ret = upgrade_s202da_j2_ret()
    assert "错误" in ret


@allure.story("升级system包错误签名的升级包")
def test_ota_case_6():
    upgrade_package_extract()
    clear_all_in_one_package()
    ret = get_upgrade_no_udisk_zip()
    modify_signature("system.zip",0)
    ret = upgrade_s202da_j2_ret()
    assert "错误" in ret


@allure.story("升级无签名校验的升级包")
def test_ota_case_7():
    upgrade_package_extract()
    clear_all_in_one_package()
    ret = get_upgrade_no_udisk_zip()
    remove_signature_txt(0)
    ret = upgrade_s202da_j2_ret()
    assert "错误" in ret


@allure.story("上个版本升级当前版本Udisk的升级包")
def test_ota_case_8():
    push_no_udisk_zip_version_before()
    ret = upgrade_s202da_j2_ret()
    assert "升级成功" in ret
    push_udisk_zip()
    ret = upgrade_s202da_j2_ret()
    assert "升级成功" in ret


@allure.story("上个版本升级当前版本不带Udisk的升级包")
def test_ota_case_9():
    push_no_udisk_zip_version_before()
    ret = upgrade_s202da_j2_ret()
    assert "升级成功" in ret
    push_no_udisk_zip()
    ret = upgrade_s202da_j2_ret()
    assert "升级成功" in ret


@allure.story("当前版本升级当前版本Udisk的升级包")
def test_ota_case_10():
    push_udisk_zip()
    ret = upgrade_s202da_j2_ret()
    assert "升级成功" in ret
    push_udisk_zip()
    ret = upgrade_s202da_j2_ret()
    assert "升级成功" in ret


@allure.story("当前版本升级当前不带Udisk的升级包")
def test_ota_case_11():
    push_udisk_zip()
    ret = upgrade_s202da_j2_ret()
    assert "升级成功" in ret
    push_no_udisk_zip()
    ret = upgrade_s202da_j2_ret()
    assert "升级成功" in ret


@allure.story("升级安全加密的升级包")
def test_ota_case_12():
    upgrade_pack = get_upgrade_zip()
    upgrade_zip = zipfile.ZipFile(upgrade_pack, 'r')
    for file in upgrade_zip.namelist():
        upgrade_zip.extract(file, pack_dir)
    clear_all_in_one_package()
    ret = get_upgrade_no_udisk_enc()
    copyfile(ret, all_in_one_file)
    ret = upgrade_s202da_j2_ret()
    assert "升级成功" in ret


@allure.story("验证升级重启后不会重复升级")
def test_ota_case_13():
    upgrade_pack = get_upgrade_zip()
    upgrade_zip = zipfile.ZipFile(upgrade_pack, 'r')
    for file in upgrade_zip.namelist():
        upgrade_zip.extract(file, pack_dir)
    clear_all_in_one_package()
    ret = get_upgrade_no_udisk_zip()
    copyfile(ret, all_in_one_file)
    upgrade_s202da_j2_check_again()


@allure.story("/userdata 空间为>=840M")
def test_ota_case_20():
    #检查是否每次空间都是大于840M的
    common_lib.serial_login_jx()
    content = common_lib.serial_cmd("df")
    ret = get_space_size("userdata",content)
    assert ret > 1024*840


@allure.story("升级过程中车机死机")
def test_ota_case_21():
    upgrade_pack = get_upgrade_zip()
    upgrade_zip = zipfile.ZipFile(upgrade_pack, 'r')
    for file in upgrade_zip.namelist():
        upgrade_zip.extract(file, pack_dir)
    clear_all_in_one_package()
    ret = get_upgrade_no_udisk_zip()
    copyfile(ret, all_in_one_file)
    upgrade_s202da_j2_inreboot()


@allure.story("升级压力测试")
def test_ota_case_22():
    push_no_udisk_zip()
    times = int(common_lib.get_ini_data("cfg_param","upgrade_stress_times"))
    average_success, success_times = upgrade_ui_operation_s202da_stress(times)
    assert average_success > 0.9


@allure.story("测试升级时间(Udisk包)")
def test_ota_case_23():
    upgrade_pack = get_upgrade_zip()
    upgrade_zip = zipfile.ZipFile(upgrade_pack, 'r')
    for file in upgrade_zip.namelist():
        upgrade_zip.extract(file, pack_dir)
    clear_all_in_one_package()
    ret = get_upgrade_udisk_zip()
    copyfile(ret, all_in_one_file)
    ret = upgrade_s202da_j2_ret()
    assert "升级成功" in ret


@allure.story("测试升级时间（不含Udisk包）")
def test_ota_case_24():
    upgrade_pack = get_upgrade_zip()
    upgrade_zip = zipfile.ZipFile(upgrade_pack, 'r')
    for file in upgrade_zip.namelist():
        upgrade_zip.extract(file, pack_dir)
    clear_all_in_one_package()
    ret = get_upgrade_no_udisk_zip()
    copyfile(ret, all_in_one_file)
    ret = upgrade_s202da_j2_ret()
    assert "升级成功" in ret


def test_infor_sf_11():
    #查看/useadata下是否有enable_dmsapp_signature文件，无则touch 创建
    touch_file("enable_dmsapp_signature")
    #拉下日志文件，修改文件名，然后升级
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log","dms_sytem_fail_0_pre.log")
    common_lib.upgrade_j2()
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log", "dms_sytem_fail_0.log")
    ret = check_secure_logs("| 0x11 |", "dms_sytem_fail_0_pre.log", "dms_sytem_fail_0.log")
    assert ret == 0


def test_infor_sf_12():
    #查看/useadata下是否有enable_dmsapp_signature文件，无则touch 创建
    touch_file("enable_dmsapp_signature")
    #拉下日志文件，修改文件名，然后升级
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log","dms_sytem_fail_0_pre.log")
    common_lib.upgrade_j2()##J2 启动时kernel_sign文件签名校验失败
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log", "dms_sytem_fail_0.log")
    ret = check_secure_logs("| 0x11 |", "dms_sytem_fail_0_pre.log", "dms_sytem_fail_0.log")
    assert ret > 0


def test_infor_sf_13():
    #查看/useadata下是否有enable_dmsapp_signature文件，无则touch 创建
    touch_file("enable_dmsapp_signature")
    #拉下日志文件，修改文件名，然后升级
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log","dms_sytem_fail_0_pre.log")
    common_lib.upgrade_j2()
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log", "dms_sytem_fail_0.log")
    ret = check_secure_logs("| 0x22 |", "dms_sytem_fail_0_pre.log", "dms_sytem_fail_0.log")
    assert ret == 0


def test_infor_sf_14():
    #查看/useadata下是否有enable_dmsapp_signature文件，无则touch 创建
    touch_file("enable_dmsapp_signature")
    #拉下日志文件，修改文件名，然后升级
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log","dms_sytem_fail_0_pre.log")
    common_lib.upgrade_j2()#J2 启动时signature_app文件签名校验失败
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log", "dms_sytem_fail_0.log")
    ret = check_secure_logs("| 0x22 |", "dms_sytem_fail_0_pre.log", "dms_sytem_fail_0.log")
    assert ret > 0


def test_infor_sf_15():
    #查看/useadata下是否有enable_dmsapp_signature文件，无则touch 创建
    touch_file("enable_dmsapp_signature")
    #拉下日志文件，修改文件名，然后升级
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log","dms_sytem_fail_0_pre.log")
    upgrade_package_extract()
    clear_all_in_one_package()
    switch_to_all_in_one(0,1)
    ret = upgrade_s202da_j2()
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log", "dms_sytem_fail_0.log")
    ret = check_secure_logs("| 0x33 |", "dms_sytem_fail_0_pre.log", "dms_sytem_fail_0.log")
    assert ret == 0


def test_infor_sf_16():
    #查看/useadata下是否有enable_dmsapp_signature文件，无则touch 创建
    touch_file("enable_dmsapp_signature")
    #拉下日志文件，修改文件名，然后升级
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log","dms_sytem_fail_0_pre.log")
    upgrade_package_extract()
    clear_all_in_one_package()
    switch_to_all_in_one(1,1)
    upgrade_s202da_j2()
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log", "dms_sytem_fail_0.log")
    ret = check_secure_logs("| 0x33 |", "dms_sytem_fail_0_pre.log", "dms_sytem_fail_0.log")
    assert ret > 0

def test_infor_sf_17():
    #查看/useadata下是否有enable_dmsapp_signature文件，无则touch 创建
    touch_file("enable_dmsapp_signature")
    #拉下日志文件，修改文件名，然后升级
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log","dms_sytem_fail_0_pre.log")

    upgrade_package_extract()
    clear_all_in_one_package()
    switch_to_all_in_one(1,0)
    upgrade_s202da_j2()

    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log", "dms_sytem_fail_0.log")
    ret = check_secure_logs("| 0x33 |", "dms_sytem_fail_0_pre.log", "dms_sytem_fail_0.log")
    assert ret > 0

def test_infor_sf_18():
    #查看/useadata下是否有enable_dmsapp_signature文件，无则touch 创建
    touch_file("enable_dmsapp_signature")
    #拉下日志文件，修改文件名，然后升级
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log","dms_sytem_fail_0_pre.log")

    upgrade_package_extract()
    clear_all_in_one_package()
    switch_to_all_in_one(0,0)
    upgrade_s202da_j2()

    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log", "dms_sytem_fail_0.log")
    ret = check_secure_logs("| 0x33 |", "dms_sytem_fail_0_pre.log", "dms_sytem_fail_0.log")
    assert ret > 0

def test_infor_sf_19():
    #查看/useadata下是否有enable_dmsapp_signature文件，无则touch 创建
    touch_file("enable_dmsapp_signature")
    #拉下日志文件，修改文件名，然后升级
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log","dms_sytem_fail_0_pre.log")

    upgrade_package_extract()
    clear_all_in_one_package()
    modify_signature("disk.img",1)
    upgrade_s202da_j2()

    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log", "dms_sytem_fail_0.log")
    ret = check_secure_logs("| 0x33 |", "dms_sytem_fail_0_pre.log", "dms_sytem_fail_0.log")
    assert ret > 0

def test_infor_sf_20():
    #查看/useadata下是否有enable_dmsapp_signature文件，无则touch 创建
    touch_file("enable_dmsapp_signature")
    #拉下日志文件，修改文件名，然后升级
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log","dms_sytem_fail_0_pre.log")

    upgrade_package_extract()
    clear_all_in_one_package()
    ret = get_upgrade_udisk_zip()
    modify_signature("app.zip", 0)
    upgrade_s202da_j2()

    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log", "dms_sytem_fail_0.log")
    ret = check_secure_logs("| 0x33 |", "dms_sytem_fail_0_pre.log", "dms_sytem_fail_0.log")
    assert ret > 0

def test_infor_sf_21():
    #查看/useadata下是否有enable_dmsapp_signature文件，无则touch 创建
    touch_file("enable_dmsapp_signature")
    #拉下日志文件，修改文件名，然后升级
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log","dms_sytem_fail_0_pre.log")

    upgrade_package_extract()
    clear_all_in_one_package()
    switch_to_all_in_one(1,0)
    upgrade_s202da_j2()

    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log", "dms_sytem_fail_0.log")
    ret = check_secure_logs("| 0x55 |", "dms_sytem_fail_0_pre.log", "dms_sytem_fail_0.log")
    assert ret == 0

def test_infor_sf_22():
    #查看/useadata下是否有enable_dmsapp_signature文件，无则touch 创建
    touch_file("enable_dmsapp_signature")
    #拉下日志文件，修改文件名，然后升级
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log","dms_sytem_fail_0_pre.log")

    upgrade_package_extract()
    clear_all_in_one_package()
    remove_signature_txt(1,0)
    upgrade_s202da_j2()

    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log", "dms_sytem_fail_0.log")
    ret = check_secure_logs("| 0x55 |", "dms_sytem_fail_0_pre.log", "dms_sytem_fail_0.log")
    assert ret > 0

def test_infor_sf_23():
    #查看/useadata下是否有enable_dmsapp_signature文件，无则touch 创建
    touch_file("enable_dmsapp_signature")
    #拉下日志文件，修改文件名，然后升级
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log","dms_sytem_fail_0_pre.log")

    upgrade_package_extract()
    clear_all_in_one_package()
    del_all_words_signature(1, 0)
    upgrade_s202da_j2()

    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log", "dms_sytem_fail_0.log")
    ret = check_secure_logs("| 0x55 |", "dms_sytem_fail_0_pre.log", "dms_sytem_fail_0.log")
    assert ret > 0


def test_infor_sf_24():
    touch_file("enable_dmsapp_signature")
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log","dms_sytem_fail_0_pre.log")
    upgrade_package_extract()
    clear_all_in_one_package()
    del_info_line_signature("update.sh",1, 0)
    upgrade_s202da_j2()
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log", "dms_sytem_fail_0.log")
    ret = check_secure_logs("| 0x55 |", "dms_sytem_fail_0_pre.log", "dms_sytem_fail_0.log")
    assert ret > 0

def test_infor_sf_25():
    touch_file("enable_dmsapp_signature")
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log","dms_sytem_fail_0_pre.log")
    upgrade_package_extract()
    clear_all_in_one_package()
    modify_signature("update.sh", 1)
    upgrade_s202da_j2()
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log", "dms_sytem_fail_0.log")
    ret = check_secure_logs("| 0x55 |", "dms_sytem_fail_0_pre.log", "dms_sytem_fail_0.log")
    assert ret > 0

def test_infor_sf_26():
    touch_file("enable_dmsapp_signature")
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log","dms_sytem_fail_0_pre.log")
    upgrade_package_extract()
    clear_all_in_one_package()
    del_info_line_signature("disk.img",1, 0)
    upgrade_s202da_j2()
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log", "dms_sytem_fail_0.log")
    ret = check_secure_logs("| 0x55 |", "dms_sytem_fail_0_pre.log", "dms_sytem_fail_0.log")
    assert ret > 0


def test_infor_sf_27():
    touch_file("enable_dmsapp_signature")
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log","dms_sytem_fail_0_pre.log")
    upgrade_package_extract()
    clear_all_in_one_package()
    modify_signature("disk.img", 1)
    upgrade_s202da_j2()
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log", "dms_sytem_fail_0.log")
    ret = check_secure_logs("| 0x55 |", "dms_sytem_fail_0_pre.log", "dms_sytem_fail_0.log")
    assert ret > 0


def test_infor_sf_28():
    touch_file("enable_dmsapp_signature")
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log","dms_sytem_fail_0_pre.log")
    upgrade_package_extract()
    clear_all_in_one_package()
    remove_signature_txt(0,0)
    upgrade_s202da_j2()
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log", "dms_sytem_fail_0.log")
    ret = check_secure_logs("| 0x55 |", "dms_sytem_fail_0_pre.log", "dms_sytem_fail_0.log")
    assert ret > 0

def test_infor_sf_29():
    touch_file("enable_dmsapp_signature")
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log","dms_sytem_fail_0_pre.log")
    upgrade_package_extract()
    clear_all_in_one_package()
    del_all_words_signature(0, 0)
    upgrade_s202da_j2()
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log", "dms_sytem_fail_0.log")
    ret = check_secure_logs("| 0x55 |", "dms_sytem_fail_0_pre.log", "dms_sytem_fail_0.log")
    assert ret > 0

def test_infor_sf_30():
    touch_file("enable_dmsapp_signature")
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log","dms_sytem_fail_0_pre.log")

    upgrade_package_extract()
    clear_all_in_one_package()
    del_info_line_signature("update.sh",0, 0)
    upgrade_s202da_j2()

    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log", "dms_sytem_fail_0.log")
    ret = check_secure_logs("| 0x55 |", "dms_sytem_fail_0_pre.log", "dms_sytem_fail_0.log")
    assert ret > 0

def test_infor_sf_31():
    touch_file("enable_dmsapp_signature")
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log","dms_sytem_fail_0_pre.log")

    upgrade_package_extract()
    clear_all_in_one_package()
    modify_signature("update.sh",0,0)
    upgrade_s202da_j2()

    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log", "dms_sytem_fail_0.log")
    ret = check_secure_logs("| 0x55 |", "dms_sytem_fail_0_pre.log", "dms_sytem_fail_0.log")
    assert ret > 0

def test_infor_sf_32():
    touch_file("enable_dmsapp_signature")
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log","dms_sytem_fail_0_pre.log")

    upgrade_package_extract()
    clear_all_in_one_package()
    del_info_line_signature("kernel.zip",0, 0)
    upgrade_s202da_j2()

    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log", "dms_sytem_fail_0.log")
    ret = check_secure_logs("| 0x55 |", "dms_sytem_fail_0_pre.log", "dms_sytem_fail_0.log")
    assert ret > 0

def test_infor_sf_33():
    touch_file("enable_dmsapp_signature")
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log","dms_sytem_fail_0_pre.log")

    upgrade_package_extract()
    clear_all_in_one_package()
    modify_signature("kernel.zip",0,0)
    upgrade_s202da_j2()

    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log", "dms_sytem_fail_0.log")
    ret = check_secure_logs("| 0x55 |", "dms_sytem_fail_0_pre.log", "dms_sytem_fail_0.log")
    assert ret > 0

def test_infor_sf_34():
    touch_file("enable_dmsapp_signature")
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log","dms_sytem_fail_0_pre.log")

    upgrade_package_extract()
    clear_all_in_one_package()
    del_info_line_signature("system.zip",0, 0)
    upgrade_s202da_j2()

    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log", "dms_sytem_fail_0.log")
    ret = check_secure_logs("| 0x55 |", "dms_sytem_fail_0_pre.log", "dms_sytem_fail_0.log")
    assert ret > 0

def test_infor_sf_35():
    touch_file("enable_dmsapp_signature")
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log","dms_sytem_fail_0_pre.log")

    upgrade_package_extract()
    clear_all_in_one_package()
    modify_signature("system.zip",0,0)
    upgrade_s202da_j2()

    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log", "dms_sytem_fail_0.log")
    ret = check_secure_logs("| 0x55 |", "dms_sytem_fail_0_pre.log", "dms_sytem_fail_0.log")
    assert ret > 0

def test_infor_sf_36():
    touch_file("enable_dmsapp_signature")
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log","dms_sytem_fail_0_pre.log")

    upgrade_package_extract()
    clear_all_in_one_package()
    del_info_line_signature("app.zip",0, 0)
    upgrade_s202da_j2()

    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log", "dms_sytem_fail_0.log")
    ret = check_secure_logs("| 0x55 |", "dms_sytem_fail_0_pre.log", "dms_sytem_fail_0.log")
    assert ret > 0

def test_infor_sf_37():
    touch_file("enable_dmsapp_signature")
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log","dms_sytem_fail_0_pre.log")

    upgrade_package_extract()
    clear_all_in_one_package()
    modify_signature("app.zip",0,0)
    upgrade_s202da_j2()

    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log", "dms_sytem_fail_0.log")
    ret = check_secure_logs("| 0x55 |", "dms_sytem_fail_0_pre.log", "dms_sytem_fail_0.log")
    assert ret > 0

def test_infor_sf_38():
    touch_file("enable_dmsapp_signature")
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log","dms_sytem_fail_0_pre.log")
    common_lib.upgrade_j2()#正常升级AI升级包，且升级成功
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log", "dms_sytem_fail_0.log")
    ret = check_secure_logs("| 0x55 |", "dms_sytem_fail_0_pre.log", "dms_sytem_fail_0.log")
    assert ret > 0

def test_infor_sf_38():
    touch_file("enable_dmsapp_signature")
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log","dms_sytem_fail_0_pre.log")
    common_lib.upgrade_j2()#正常升级AI升级包，且升级成功
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log", "dms_sytem_fail_0.log")
    ret = check_secure_logs("| 0x66 |", "dms_sytem_fail_0_pre.log", "dms_sytem_fail_0.log")
    assert ret > 0

def test_infor_sf_39():
    touch_file("enable_dmsapp_signature")
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log","dms_sytem_fail_0_pre.log")
    common_lib.upgrade_j2()#修改升级流程文件，模拟升级更新镜像失败
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log", "dms_sytem_fail_0.log")
    ret = check_secure_logs("| 0x66 |", "dms_sytem_fail_0_pre.log", "dms_sytem_fail_0.log")
    assert ret > 0

def test_infor_sf_40():
    touch_file("enable_dmsapp_signature")
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log","dms_sytem_fail_0_pre.log")
    common_lib.upgrade_j2()#J2 启动时Image.gz文件MD5值校验成功
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log", "dms_sytem_fail_0.log")
    ret = check_secure_logs("| 0x77 |", "dms_sytem_fail_0_pre.log", "dms_sytem_fail_0.log")
    assert ret > 0

def test_infor_sf_41():
    touch_file("enable_dmsapp_signature")
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log","dms_sytem_fail_0_pre.log")
    common_lib.upgrade_j2()#J2 启动时Image.gz文件MD5值校验失败
    common_lib.pull_j2_file_to_pc("/userdata/secure_logs/dms_sytem_fail_0.log", "dms_sytem_fail_0.log")
    ret = check_secure_logs("| 0x77 |", "dms_sytem_fail_0_pre.log", "dms_sytem_fail_0.log")
    assert ret > 0


if __name__ == '__main__':
    pytest.main()