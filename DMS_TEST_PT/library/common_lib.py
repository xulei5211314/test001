# -*- coding: utf-8 -*-
# @Time    : 2021/1/3
# @Author  : tingting.zhao
from library.prase_test_ini import prase_ini
from library.serial_lib import serial_lib
from library.uiautomator_lib import *
from _library.sys import *
from _library.prase_ini import update_project_cfg
import allure
import pytest
import uiautomator2 as u2

# from DMS_TEST_PT.library.uiautomator_lib import uiautomator_lib

# d = u2.connect()
d=''


all_in_one_file_resource = os.path.join(os.path.dirname(__file__), r"..\tools\upgrade_package", "all_in_one_MM_signed.zip")
local_file_dir = os.path.join(os.path.dirname(__file__), r"..\result\file_from_j2")

class common_lib(uiautomator_lib, serial_lib, prase_ini):
    @classmethod
    def id(self,locator):
        locator_moudle_name = locator.split("_")[0]
        locator_value = GLOBAL_LOCATOR.get(locator_moudle_name).get(locator)
        return locator_value

    @classmethod
    def call_bat(self,batname):
        """
        调用Bat文件
        :param batname: \tools\bat目录下，bat文件名称
        :return:
        """
        batfile = os.path.join(os.path.dirname(__file__), r"..\tools\bat", batname)
        log.logger.info("batfile:{}".format(batfile))
        os.system(batfile)
        return

    @classmethod
    def upgrade_j2_s202da(self):
        self.adb_push(all_in_one_file_resource, "/sdcard/hobot/upgrade")
        self.upgrade_j2_s202da_ui()


    @classmethod
    def upgrade_j2_s202da_ui(self):
        self.goto_page("工程界面")
        time.sleep(2)
        if (common_lib.get_ini_data("cfg_param", "ui_automator") == "1"):
            d(text="OTA升级").click()
            time.sleep(2)
            d(text="OTA升级").click()
            d(text="开始升级").click()
            time.sleep(2)
            d(text="开始升级").click()
        else:
            self.click_element("工程模式_主界面_BUTTON_升级")
            self.click_element("工程模式_主界面_BUTTON_升级_开始升级")
            time.sleep(5)
            self.click_element("工程模式_主界面_BUTTON_升级_开始升级")
        i = 0
        while (1):
            time.sleep(5)
            i = i + 5
            ret = self.common_get_ui_text("工程模式_主界面_BUTTON_升级_升级结果")
            log.logger.info("upgrade process: {}".format(ret))
            if "升级成功" in ret:
                self.avn_reboot()
                break
            if (i > 180):
                log.logger.error("upgrade fail!")
                raise Exception("upgrade fail!")


    @classmethod
    def common_get_ui_text(self,text):
        if (common_lib.get_ini_data("cfg_param", "ui_automator") == "1"):
            ret = d(resourceId=text).get_text()
        else:
            ret = common_lib.get_text(text)


    @classmethod
    def upgrade_j2_bat(self):
        """
        升级J2
        :return:升级结果
        """
        self.call_bat('upgrade_J2_all_in_one_MM_signed.bat')
        self.upgrade_j2_s202da_ui()


    @classmethod
    def replace_j2_file(self,j2_dir,file_name):
        """
        用PC上的文件去替换J2内的文件
        :param j2_dir: J2上的文件路径
        :param file_name: PC上的文件路径
        :return:替换结果  1替换成功  0 替换失败并抛出异常
        """
        i = 0
        #尝试最多5次直到成功
        while i < 6:
            i = i + 1
            #检查adb
            self.check_adb_connect()
            local_file_name = os.path.join(os.path.dirname(__file__), r"..\tools\replace_to_j2",file_name)
            log.logger.info(local_file_name)
            #push车机
            self.adb_push(local_file_name, r"data")
            adb_file_nane = r"/data/{}".format(file_name)#    os.path.join(r"data",file_name)
            self.adb_hbipc_run("mount -o rw,remount")
            # push j2
            self.adb_hbipc_put( adb_file_nane, j2_dir)
            #串口check
            self.serial_login_jx()
            self.serial_cmd("cd /app/output_linux_J2/etc/")
            ret = self.serial_cmd("ls")
            log.logger.info(ret)
            if file_name in ret:
                break
        if i < 6:
            return 1
        else:
            log.logger.error("replace_j2_file error")
            raise


    @classmethod
    def pull_j2_file_to_pc(self,j2_dir,file_name):
        """
        从J2上拉文件到pc.
        :param j2_dir：j2上的文件路径
        :param file_name：\result\file_from_j2文件夹下的文件名称
        :return:替换结果  1替换成功  0 替换失败并抛出异常
        """
        local_file_name = os.path.join(os.path.dirname(__file__), r"..\result\file_from_j2", file_name)
        adb_file_name = r"/data/{}".format(file_name)  # os.path.join(r"data",file_name)
        log.logger.info(local_file_name)
        self.check_adb_connect()
        i = 0
        while i < 6:
            i = i + 1
            self.adb_hbipc_get(j2_dir, adb_file_name)
            self.adb_pull(adb_file_name, local_file_name)

            #检查目录下是否出现该文件
            list_file = os.listdir(local_file_dir)
            if file_name in list_file:
                break
        if i < 6:
            return 1
        else:
            log.logger.error("pull_j2_file_to_pc error")
            raise


    @classmethod
    def touch_J2_file(self, file):
        """
        从J2上创建文件.
        :param j2_dir：j2上的文件路径
        :param file_name：\result\file_from_j2文件夹下的文件名称
        :return:创建结果  1创建成功  0 创建失败并抛出异常
        """
        self.serial_login_jx()
        self.serial_cmd("mount -o rw,remount")
        touch_command = "touch {}".format(file)
        for i in range(4):
            ret = self.serial_cmd("ls")
            if file not in ret:
                ret = self.serial_cmd(touch_command)
            else:
                break
        if i >= 3:
            raise Exception("touch fail")
            return 0
        else:
            return 1


if __name__ == '__main__':
    pass