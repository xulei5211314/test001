# -*- coding:utf-8 -*-
# @Time    : 2021/1/3
# @Author  : tingting.zhao
import pytest
import os
import shutil
import re
from _library.prase_ini import update_project_cfg
import _library.sys
from config.config import GLOBAL_PROJECT_CFG
from library.common_lib import *

current_file = os.path.dirname(__file__).replace('/', '\\')
reports_path = os.path.join(current_file, "result", "reports")
html_path = os.path.join(current_file, "result", "html")
sys_log_dir = os.path.join(current_file, "result", "sys_log")
file_from_j2_dir = os.path.join(current_file, "result", "file_from_j2")
html_port = 8080


def allure_add_path():
    allure_dir = os.path.join(current_file, "tools", "allure", "bin")
    if allure_dir not in os.environ["PATH"]:
        os.environ["PATH"] = os.environ["PATH"] + os.pathsep + allure_dir


def clear_reports_file():
    if not os.path.exists(sys_log_dir):
        os.mkdir(sys_log_dir)
    if not os.path.exists(file_from_j2_dir):
        os.mkdir(file_from_j2_dir)

    reports_history = os.path.join(reports_path, "history")
    temporary_history = os.path.join(current_file, "result", "history")
    if os.path.exists(reports_path):
        if os.path.exists(reports_history):
            if os.path.exists(temporary_history):
                shutil.rmtree(temporary_history)
            shutil.move(reports_history, temporary_history)
        shutil.rmtree(reports_path)  # 能删除该文件夹和文件夹下所有文件
    os.mkdir(reports_path)
    if os.path.exists(temporary_history):
        shutil.move(temporary_history, reports_history)


def kill_port(port):
    # 查找端口的pid
    find_port = 'netstat -aon | findstr {}'.format(port)
    result = os.popen(find_port)
    text = result.read()
    pid = re.findall("LISTENING\s+([\s\S+]*?)\s+", text)
    if pid:
        # 占用端口的pid
        find_kill = 'taskkill -f -pid {}'.format(pid[0])
        os.popen(find_kill)


def run():
    kill_port(html_port)
    allure_add_path()
    clear_reports_file()
    # 设置默认pytest的运行参数
    update_project_cfg()
    RERUNS = GLOBAL_PROJECT_CFG.get("RERUNS")
    arguments = ["-vs", "--reruns", RERUNS, "--alluredir", reports_path]
    pytest.main(arguments)
    # os.system("allure generate {} -o {} --clean".format(reports_path, html_path))
    # os.system(r"xcopy {} {} /e /Y /I".format(os.path.join(html_path, "history"), os.path.join(reports_path, "history")))
    # # 打开测试报告
    # os.popen("allure open -h 127.0.0.1 -p {} {}".format(html_port, html_path))
    # if(common_lib.get_ini_data("cfg_param","auto_email") == "1"):
    #     _library.sys.send_mail()
    #     _library.sys.send_report_to_server()


if __name__ == '__main__':
    run()