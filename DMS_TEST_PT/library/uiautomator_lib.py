# -*- coding: utf-8 -*-
# @Time    : 2021/1/4
# @Author  : tingting.zhao
import re
import allure
from library.adb_lib import adb_lib
from _library.json_lib import json_lib
from _library.sys import *

# from DMS_TEST_PT._library.global_valule import GLOBAL_LOCATOR


class uiautomator_lib(adb_lib):
    @classmethod
    def _get_current_page_xml(self):
        """
        获取当前车机界面的xml布局
        :return:
        """
        remote_file_name = r"/sdcard/app.uix"
        command = "uiautomator dump {}".format(remote_file_name)
        for i in range(16):
            ret = self.adb_shell(command)
            if ("UI hierchary dumped to:" in ret):
                log.logger.info("ui dumped times:{}".format(i))
                break
            if i == 15 :
                raise Exception("dump error")

        filedir = os.path.join(os.path.dirname(__file__), r"..\result\uiautomator")
        if not os.path.exists(filedir):
            os.mkdir(filedir)
        xml_file_name = os.path.join(filedir, "app.uix")
        self.adb_pull(remote_file_name, xml_file_name)
        return xml_file_name

    @classmethod
    def _get_current_page_screencap(self):
        """
        获取当前车机界面的截图
        :param :
        :return:
        """
        current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
        remote_file_name = r"/sdcard/app.png"
        command = "screencap -p {}".format(remote_file_name)
        self.adb_shell(command)
        filedir = os.path.join(os.path.dirname(__file__), r"..\result\uiautomator", current_time)
        if not os.path.exists(filedir):
            os.mkdir(filedir)
        screencap_file_name = os.path.join(filedir, "app.png")
        self.adb_pull(remote_file_name, screencap_file_name)
        return screencap_file_name

    @classmethod
    def _open_xml(self):
        """
        获取当前页面的xml布局
        :return:
        """
        xml_file_name = self._get_current_page_xml()
        with open(xml_file_name, "rb") as f:
            try:
                ret = str(f.readline(), encoding="utf-8").rstrip()
            except:
                ret = str(f.readline(), encoding="gbk").rstrip()
        return ret

    @classmethod
    def _get_screen_size(self):
        """
        获取屏幕size
        :param :
        :return: 屏幕size
        """
        size_str = self.adb_shell("wm size")
        m = re.search(r'(\d+)x(\d+)', size_str)
        if m:
            screen_height = int(m.group(2))
            screen_width = int(m.group(1))
            return (screen_width, screen_height)

    @classmethod
    def _find_element(self, locator):
        """
        查找当前页面元素所在位置
        :param locator: 坐标
        :return:
        """
        locator_moudle_name = locator.split("_")[0]
        locator_value = GLOBAL_LOCATOR.get(locator_moudle_name).get(locator)
        if isinstance(locator_value, list):
            center_x = (locator_value[0] + locator_value[2]) / 2
            center_y = (locator_value[1] + locator_value[3]) / 2
            return (center_x, center_y)
        else:
            ret = self._open_xml()
            ret = xml_to_dict(ret)
            jsonlib = json_lib(ret)
            # attributes = re.findall(r'[^(,]+(?=[),])', locator_value)
            # key_0, value_0 = attributes[0].strip().split("=")
            the_value_paths = jsonlib.the_value_path(locator_value)
            for the_value_path in the_value_paths:
                _flag = 1
                the_value_path = the_value_path[:len(the_value_path) - len("[@'{}']".format("resource-id"))]
                # if len(attributes) > 1:
                #     for attribute in attributes[1:]:
                #         key, value = attribute.strip().split("=")
                #         if the_value_path.endswith(']') and eval(
                #                         'ret' + the_value_path).get('@{}'.format(key)).strip() == value:
                #             _flag += 1
                # if _flag == len(attributes):
                element_info = eval('ret' + the_value_path)
                log.logger.info("find element : {}".format(locator))
                return element_info
            raise "not find element: {}".format(locator)

    @classmethod
    def _get_attr_value(self, locator, attr):
        """
        获取指定属性的value值
        :param locator: 坐标
        :return:
        """
        element_info = self._find_element(locator)
        attr_value = element_info.get("@{}".format(attr))
        log.logger.info("get element {} is : {}".format(attr, attr_value))
        return attr_value

    @classmethod
    def click_element(self, locator):
        """
        点击屏幕上的元素
        :param locator: /variables/*.py文件中对应的文件坐标范围字符串
        :return:
        """
        center_x, center_y = self._find_element(locator)
        command = "input tap {} {}".format(center_x, center_y)
        log.logger.info("click(center_x:{}, center_y:{})".format(center_x, center_y))
        self.adb_shell(command)
        time.sleep(0.5)

    @classmethod
    def check_element(self, locator):
        """
        校验element是否存在当前页面，若失败则截取当前车机界面的图片
        :param locator: /variables/*.py文件中对应的文件坐标范围字符串
        :return:
        """
        i = 0
        while i < 3:
            try:
                ret = self._find_element(locator)
                log.logger.info("check element successed: {}".format(locator))
                return ret
            except:
                i += 1
                time.sleep(1)
        log.logger.error("check element failed: {}".format(locator))
        raise "check element failed: {}".format(locator)

    @classmethod
    def input_text(self, locator, text):
        """
        在车机文本框中输入文本信息，暂时不支持中文  坐标
        :param locator: /variables/*.py文件中对应的文件坐标范围字符串
        :param text:待输入的字段
        :return:
        """
        center_x, center_y = self._find_element(locator)
        command = "input tap {} {}".format(center_x, center_y)
        self.adb_shell(command)
        command = "input text {}".format(text)
        log.logger.info("input : {} (center_x:{}, center_y:{})".format(text, center_x, center_y))
        self.adb_shell(command)

    @classmethod
    def get_text(self, locator):
        """
        获取元素的文本信息
        :param locator: /variables/*.py文件中对应的文件坐标范围字符串
        :return:元素的文本信息
        """
        text = self._get_attr_value(locator, "text")
        return text

    @classmethod
    def swipe(self, center_l_x, center_l_y, center_r_x, center_r_y):
        """
        由（center_l_x, center_l_y）滑动至（center_r_x, center_r_y）
        :param center_l_x:
        :param center_l_y:
        :param center_r_x:
        :param center_r_y:
        :return:
        """
        command = "input swipe {} {} {} {}".format(center_l_x, center_l_y, center_r_x, center_r_y)
        log.logger.info("swipe (center_l_x:{}, center_l_y:{}) to (center_r_x:{}, center_r_y:{})".format(center_l_x, center_l_y, center_r_x, center_r_y))
        self.adb_shell(command)

    @classmethod
    def swipe_up(self, num=1):
        """
        向上滑动
        :return:
        """
        for i in range(num):
            screen_width, screen_height = self._get_screen_size()
            screen_width_center = screen_width // 2
            screen_height_center = screen_height // 2
            self.swipe(screen_width_center, screen_height_center, screen_width, screen_height - 200)
        log.logger.info("swipe to up num is :{}".format(num))

    @classmethod
    def swipe_down(self, num=1):
        """
        向下滑动
        :return:
        """
        for i in range(num):
            screen_width, screen_height = self._get_screen_size()
            screen_width_center = screen_width // 2
            screen_height_center = screen_height // 2
            self.swipe(screen_width_center, screen_height_center, screen_width, 200)
        log.logger.info("swipe to down num is :{}".format(num))

    @classmethod
    def swipe_left(self, num=1):
        """
        向左滑动
        :return:
        """
        for i in range(num):
            screen_width, screen_height = self._get_screen_size()
            screen_width_center = screen_width // 2
            screen_height_center = screen_height // 2
            self.swipe(screen_width_center, screen_height_center, screen_width - 200, screen_height_center)
        log.logger.info("swipe to left num is :{}".format(num))

    @classmethod
    def swipe_right(self, num=1):
        """
        向右滑动
        :return:
        """
        for i in range(num):
            screen_width, screen_height = self._get_screen_size()
            screen_width_center = screen_width // 2
            screen_height_center = screen_height // 2
            self.swipe(screen_width_center, screen_height_center, 200, screen_height_center)
        log.logger.info("swipe to right num is :{}".format(num))


if __name__ == '__main__':
    uiautomator_lib._find_element("工程模式_主界面_BUTTON_升级_升级结果")
