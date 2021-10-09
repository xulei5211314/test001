# -*- coding: utf-8 -*-
# @Time    : 2021/1/26
# @Author  : TingTing.Zhao
from library.common_lib import *

log_preview_dir = os.path.join(os.path.dirname(__file__), r"..\..\..\result\sys_log", "auto_diag_preview.log")
log_dir = os.path.join(os.path.dirname(__file__), r"..\..\..\result\sys_log", "auto_diag.log")
ap_top_log_file = os.path.join(os.path.dirname(__file__), r"..\..\..\result\sys_log", r"ap_top_log.txt")

GLOBAL_TOP_ELEMENT = {
    "mem":9,
    "cpu":8,
}

def get_aiservice_info(element):
    content = open(ap_top_log_file, 'r', encoding='utf-8').readlines()
    info_list = []
    sum = 0
    for line in content:
        if "com.incall.apps.aiservice" in line:
            line_info = line.split()
            info_list.append(line_info[GLOBAL_TOP_ELEMENT[element]])
            sum = sum + (float)(line_info[8])
    length = len(info_list)
    avg = sum/length
    return avg


def get_avg_fps(camera_id, obj_avg):
    #指明文件路径
    pre_file = os.path.join(os.path.dirname(__file__), r"..\..\..\result\sys_log\auto_diag_preview.log")
    final_file = os.path.join(os.path.dirname(__file__), r"..\..\..\result\sys_log\auto_diag.log")
    #读取文件，存储到列表当中
    pre_content=open(pre_file,'r',encoding='utf-8').readlines()
    final_content=open(final_file,'r',encoding='utf-8').readlines()
    #计算列表的长度
    previous_line = len(pre_content)
    #截取列表
    temp_list=final_content[previous_line:]
    fps=[]
    #记录位置
    count=0
    camera_id_str = '"camera_id" : {},'.format(camera_id)
    for i in temp_list:
        if (camera_id_str in i):
            take_time = re.findall(r'\t\t\t\t"fps" : (.*)\n', temp_list[count+1])
            fps.append((int)(take_time[0]))
        count+=1 #记录位置
    sum=0
    length=len(fps)
    for i in fps:
        sum+=i
    avg=sum/length
    log.logger.info("fps:{},average_num:{}".format(fps, avg))
    return avg


def get_avg_diag_info(re_compile):
    #指明文件路径
    pre_file = os.path.join(os.path.dirname(__file__), r"..\..\..\result\sys_log\auto_diag_preview.log")
    final_file = os.path.join(os.path.dirname(__file__), r"..\..\..\result\sys_log\auto_diag.log")
    #读取文件，存储到列表当中
    pre_content=open(pre_file,'r',encoding='utf-8').readlines()
    final_content=open(final_file,'r',encoding='utf-8').readlines()
    #计算列表的长度
    previous_line = len(pre_content)
    #截取列表
    temp_list=final_content[previous_line:]
    info_list=[]
    for i in temp_list:
        value = re.findall(re_compile, i)
        if len(value):
            log.logger.info(value)
            info_list.append((int)(value[0]))#try,可能转不成功，没有新内容等等
    sum=0
    length=len(info_list)
    for i in info_list:
        sum+=i
    try:
        avg=sum/length
    except:
        raise Exception("no new value")
    log.logger.info("value:{},average_num:{}".format(info_list, avg))
    return avg


def diag_ui_period_s202da():
    common_lib.goto_page("工程界面")
    common_lib.click_element("工程模式_主界面_BUTTON_诊断")
    common_lib.swipe_up(4)
    common_lib.click_element("工程模式_主界面_BUTTON_诊断_周期诊断")


def stability_diag_period_prepare():
    common_lib.adb_pull("/sdcard/hobot/diag/auto_diag.log", log_preview_dir)
    diag_ui_period_s202da()
    #保持车机持续运行24 小时
    time.sleep(40)#10*60*60
    #获取日志放到sys_log文件夹下
    common_lib.adb_pull("/sdcard/hobot/diag/auto_diag.log", log_dir)


def stability_auto_diag_prepare():
    #J2端/app/output_linux_J2/etc/global.json文件verbose_level设置为1
    common_lib.replace_j2_file("/app/output_linux_J2/etc/global.json", "global.json")
    #kill掉hobot进程号（hobot进程自启后会产生新的日志）
    common_lib.serial_login_jx()
    ret = common_lib.serial_cmd("ps |grep hobotdms_app")
    ps_grep_split = ret.split()
    kill_cmd = "kill -9 {}".format(ps_grep_split[3])
    common_lib.serial_cmd(kill_cmd)
    #先获取auto_diag.log并重命名为auto_diag_preview.log
    common_lib.adb_pull("/sdcard/hobot/diag/auto_diag.log", log_preview_dir)
    #保持车机持续运行24 小时
    time.sleep(40)#10*60*60
    #获取日志放到sys_log文件夹下
    common_lib.adb_pull("/sdcard/hobot/diag/auto_diag.log", log_dir)


if __name__ == '__main__':
    get_avg_diag_info("CPU")