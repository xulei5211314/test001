# -*- coding: utf-8 -*-
# @Time    : 2021/1/29
# @Author  : TingTing.Zhao
from library.common_lib import *

mmc_part_file = os.path.join(os.path.dirname(__file__), r"..\..\..\result\sys_log\mmc_part.txt")

def get_mmcpart_info():
    common_lib.serial_login_jx()
    common_lib.serial_cmd("reboot")
    time.sleep(1)
    for i in range(20):
        common_lib.serial_cmd("\r")
        time.sleep(0.1)
    common_lib.serial_cmd("\r")
    ret = common_lib.serial_cmd("mmc part")
    file_handle = open(mmc_part_file,mode='w')
    file_handle.write(ret)

def check_mcc_info(info):
    with open(mmc_part_file,'r') as f:
        lines = f.readlines()
    l = []
    for line in lines:
        if info in line:
            l.append(line)
    a = l[0].split()[1]
    b = l[0].split()[2]
    result = abs(int(a,16)-int(b,16))/2048
    return result



