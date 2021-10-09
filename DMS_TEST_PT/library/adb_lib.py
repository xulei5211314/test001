# -*- coding: utf-8 -*-
# @Time    : 2021/1/9
# @Author  : TingTing.Zhao
from _library.sys import *


class adb_lib(object):
    """
    adb相关的操作（包括在adb shell中与goto系统进行通讯）
    前置条件：检查adb连接成功
    """

    @classmethod
    def adb_push(self, local_file_name, remote_file_nane):
        """
        由PC端向车机端传递文件
        param local_file_name: PC路径
        param adb_file_nane: 车机路径
        return: PUSH结果 1：push成功  0push失败 并抛出异常
        """
        for i in range(5):
            command = "adb push {} {}".format(local_file_name, remote_file_nane)
            ret = cmd(command)
            log.logger.info(ret)
            if ("file pushed") in ret:
                log.logger.info("file pushed ok")
                return 1
                break
            if (i >4):
                raise Exception(ret)


    @classmethod
    def adb_pull(self, remote_file_name, local_file_name):
        """
        由车机端向PC端传递文件
        :param remote_file_name: 车机文件路径
        :param local_file_name:  PC路径
        :return:  PULL结果 1：pull成功  0:pull失败 并抛出异常
        """
        for i in range(5):
            command = "adb pull {} {}".format(remote_file_name, local_file_name)
            time.sleep(1)
            ret = cmd(command)
            log.logger.info(ret)
            if ("file pulled") in ret:
                log.logger.info("file pulled ok")
                return 1
                break
            if (i > 4):
                raise Exception(ret)
            return 0

    @classmethod
    def switch_to_root(self):
        """
        adb切换到root用户
        :return: 终端回显内容
        """

        ret = cmd("adb root")#获取root权限
        ret = cmd("adb remount")#获取文件及文件夹权限
        if "succeeded" in ret:
            log.logger.info("switch to root successed")
            return
        log.logger.error("switch to root failed")

    @classmethod
    def goto_page(self, page_name):
        """
        使用命令直接调用activity，以达到切换界面的效果
        :param page_name: /variables/*.py目录下配置的参数
        :return:
        """
        activity_value = GLOBAL_PAGE_ACTIVITY.get(page_name)
        command = "am start -n {}".format(activity_value)
        command = "adb shell {}".format(command)
        os.system(command)
        num = 0
        time.sleep(1)
        while True:
            if activity_value in self.adb_shell("dumpsys activity top | findstr ACTIVITY"):
                log.logger.info("goto page successed: {}".format(activity_value))
                break
            else:
                num = num + 1
                time.sleep(1)
                if num >= 2:
                    error_message = "goto page failed:{}".format(activity_value)
                    log.logger.error(error_message)
                    raise Exception(error_message)
        


    @classmethod
    def adb_shell(self, command):
        """
        运行adb指令
        :param command:指令
        :return:指令回显内容
        """
        command = "adb shell {}".format(command)#adb shell hbipc-utils run \"reboot\" --bifsd
        ret = cmd(command)
        return ret

    @classmethod
    def avn_reboot(self):
        """
        重启车机
        :return:
        """
        cmd("adb reboot")
        time.sleep(180)

    @classmethod
    def check_adb_connect(self):
        """
        检查车机是否连接成功，若没有连接成功则退出程序
        :return:
        """
        num = 0
        while True:
            ret = cmd("adb devices")
            if GLOBAL_DEVICES_ID in ret:
                log.logger.info("avn connect successed: {}".format(GLOBAL_DEVICES_ID))
                break
            else:
                num  += 1
                log.logger.info("sleep 60 s")
                time.sleep(60)
                if num == 5:
                    error_message = "avn connect failed: {}".format(GLOBAL_DEVICES_ID)
                    log.logger.error(error_message)
                    raise Exception(error_message)

    @classmethod
    def adb_hbipc_put(self, adb_file_nane, jx_file_nane):
        """
        有车机端向J2系统传递文件##增加判断
        :param adb_file_nane:
        :param goto_file_nane:
        :return:
        """
        command = "hbipc-utils ru,remount /\" --bifsd"
        self.adb_shell(command)
        command = 'hbipc-utils put \"{}\" \"{}\" --bifsd'.format(adb_file_nane, jx_file_nane)
        ret = self.adb_shell(command)
        time.sleep(1)
        log.logger.info(ret)
        log.logger.info("************************************************")
        return ret

    @classmethod
    def adb_hbipc_get(self, jx_file_nane, adb_file_nane):
        """
        由J2系统向车机端传递文件
        :param jx_file_nane: J2文件路径
        :param adb_file_nane: 车机文件路径
        :return:
        """
        command = "hbipc-utils run \"mount -o rw,remount /\" --bifsd"
        self.adb_shell(command)
        command = 'hbipc-utils get {} {} --bifsd'.format(adb_file_nane, jx_file_nane)
        ret = self.adb_shell(command)
        time.sleep(1)
        log.logger.info(ret)
        return ret

    @classmethod
    def adb_hbipc_run(self,command):
        """
        运行J2系统的指令
        :param command:  需要J2执行的指令
        :return: 执行指令之后，终端的回显值
        """
        command = 'hbipc-utils run \"{}\" --bifsd'.format(command) #hbipc-utils run \"reboot\" --bifsd
        time.sleep(1)
        return self.adb_shell(command)

    @classmethod
    def j2_reboot(self):
        """
        重启J2系统
        :return:
        """
        self.adb_hbipc_run("reboot")

    @classmethod
    def check_hbipc_connect(self):
        """
        检查os系统和J2系统是否通讯成功，若没有启动成功则退出程序
        :return:
        """
        out = self.adb_hbipc_run("ps")
        if "dms-sysMng-workflow" in out:
            log.logger.info("Hbipc successed)")
        else:
            error_message = "GHbipc failed)"
            log.logger.error(error_message)
            raise Exception(error_message)




if __name__ == '__main__':
    log.logger.info("1213" + "\n" + "34")
