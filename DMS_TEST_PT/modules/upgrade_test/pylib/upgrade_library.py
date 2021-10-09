# -*- coding: utf-8 -*-
from library.common_lib import *          #导入公共接口模块
import zipfile
from shutil import copyfile
import os
import shutil
version_before_dir = os.path.join(os.path.dirname(__file__), r"..\..\..\tools\upgrade_package\version_before")
pack_dir = os.path.join(os.path.dirname(__file__), r"..\..\..\tools\upgrade_package")
pack_output_dir = os.path.join(pack_dir, r"output")
all_in_one_file = os.path.join(os.path.dirname(__file__), r"..\..\..\tools\upgrade_package", "all_in_one_MM_signed.zip")
all_in_one_output = os.path.join(os.path.dirname(__file__), r"..\..\..\tools\upgrade_package", "all_in_one_MM_signed.zip")
output_dir = os.path.join(pack_dir, r"output")
unzip_dir = os.path.join(pack_output_dir, r".\unzip")
sig_txt_dir = os.path.join(unzip_dir, r"signature.txt")

def switch_to_all_in_one(whether_udisk,whether_enc=0):
    if whether_udisk == 1 and whether_enc == 0:
        srcFile = os.path.join(output_dir, get_upgrade_udisk_zip())
    elif whether_udisk == 0 and whether_enc == 0:
        srcFile = os.path.join(output_dir, get_upgrade_no_udisk_zip())
    elif whether_udisk == 1 and whether_enc == 1:
        srcFile = os.path.join(output_dir, get_upgrade_udisk_enc())
    elif whether_udisk == 0 and whether_enc == 1:
        srcFile = os.path.join(output_dir, get_upgrade_no_udisk_enc())
    else:
        raise Exception("input udisk info error!")

    dstFile = all_in_one_output
    try:
        os.rename(srcFile,dstFile)
    except Exception as e:
        print(e)
        print('rename file fail\r\n')
    else:
        print('rename file success\r\n')


def remove_signature_txt(whether_udisk,whether_enc=0):
    if os.path.exists(unzip_dir):
        shutil.rmtree(unzip_dir)
    if not os.path.exists(unzip_dir):
        os.mkdir(unzip_dir)

    if whether_udisk == 1 and whether_enc == 0:
        no_udisk_zip = os.path.join(output_dir, get_upgrade_udisk_zip())
    elif whether_udisk == 0 and whether_enc == 0:
        no_udisk_zip = os.path.join(output_dir, get_upgrade_no_udisk_zip())
    elif whether_udisk == 1 and whether_enc == 1:
        no_udisk_zip = os.path.join(output_dir, get_upgrade_udisk_enc())
    elif whether_udisk == 0 and whether_enc == 1:
        no_udisk_zip = os.path.join(output_dir, get_upgrade_no_udisk_enc())

    else:
        raise Exception("input udisk info error!")

    upgrade_zip = zipfile.ZipFile(no_udisk_zip)
    if not os.path.exists(unzip_dir):
        os.mkdir(unzip_dir)
    upgrade_zip.extractall(unzip_dir)
    #删除sig文件
    try:
        os.remove(sig_txt_dir)
    except:
        raise Exception("signature.txt not exist!")

    startdir = unzip_dir  #要压缩的文件夹路径
    file_news = all_in_one_output # 压缩后文件夹的名字
    z = zipfile.ZipFile(file_news,'w',zipfile.ZIP_DEFLATED) #参数一：文件夹名
    for dirpath, dirnames, filenames in os.walk(startdir):
        fpath = dirpath.replace(startdir,'') #这一句很重要，不replace的话，就从根目录开始复制
        fpath = fpath and fpath + os.sep or ''#实现当前文件夹以及包含的所有文件的压缩
        for filename in filenames:
            z.write(os.path.join(dirpath, filename),fpath+filename)
            print ('压缩成功')
    z.close()
    

def upgrade_s202da_j2_inreboot():
    common_lib.adb_push(all_in_one_file, "/sdcard/hobot/upgrade")
    ret = upgrade_j2_s202da_ui_inreboot()
    check_j2_condition()
    return ret


def check_j2_condition():
    time.sleep(6)
    common_lib.check_adb_connect()
    common_lib.check_hbipc_connect()

def upgrade_s202da_j2_check_again():
    common_lib.adb_push(all_in_one_file, "/sdcard/hobot/upgrade")
    ret = upgrade_j2_s202da_ui_check_again()
    return ret

def upgrade_s202da_j2_ret():
    common_lib.adb_push(all_in_one_file, "/sdcard/hobot/upgrade")
    ret = upgrade_j2_s202da_ret()
    return ret


def modify_signature(info, whether_udisk, whether_enc =0):
    if os.path.exists(unzip_dir):
        shutil.rmtree(unzip_dir)
    if not os.path.exists(unzip_dir):
        os.mkdir(unzip_dir)
    if whether_udisk == 1 and whether_enc == 0:
        no_udisk_zip = os.path.join(output_dir, get_upgrade_udisk_zip())
    elif whether_udisk == 0 and whether_enc == 0:
        no_udisk_zip = os.path.join(output_dir, get_upgrade_no_udisk_zip())
    elif whether_udisk == 1 and whether_enc == 1:
        no_udisk_zip = os.path.join(output_dir, get_upgrade_udisk_enc())
    elif whether_udisk == 0 and whether_enc == 1:
        no_udisk_zip = os.path.join(output_dir, get_upgrade_no_udisk_enc())
    else:
        raise Exception("input udisk info error!")

    upgrade_zip = zipfile.ZipFile(no_udisk_zip)
    if not os.path.exists(unzip_dir):
        os.mkdir(unzip_dir)
    upgrade_zip.extractall(unzip_dir)
    _modify_sig_txt_words(info)
    startdir = unzip_dir  #要压缩的文件夹路径
    file_news = all_in_one_output # 压缩后文件夹的名字
    z = zipfile.ZipFile(file_news,'w',zipfile.ZIP_DEFLATED) #参数一：文件夹名
    for dirpath, dirnames, filenames in os.walk(startdir):
        fpath = dirpath.replace(startdir,'') #这一句很重要，不replace的话，就从根目录开始复制
        fpath = fpath and fpath + os.sep or ''#实现当前文件夹以及包含的所有文件的压缩
        for filename in filenames:
            z.write(os.path.join(dirpath, filename),fpath+filename)
            print ('压缩成功')
    z.close()


def _modify_sig_txt_words(info):
    with open(sig_txt_dir,'r') as f:
        content=f.read()
    info_str = 'RSA-SHA256({})= '.format(info)
    position = content.find(info_str)+len(info_str)
    position2 = position + 6
    l=[]
    l=content[:position]+content[position2:]
    with open(sig_txt_dir, 'w') as f:
        f.write(l)

def _del_sig_txt_info_line(info):
    f = open(sig_txt_dir, "r")
    lines = f.readlines()
    f.close()
    f = open(sig_txt_dir, "w")
    for line in lines:
        if info in line:
            line = line.split(" ")[0]
            line = line+"\n"
        f.write(line)



def _del_sig_txt_all_words():
    open(sig_txt_dir,'w').close()

def del_all_words_signature(whether_udisk, whether_enc =0):
    if os.path.exists(unzip_dir):
        os.rmdir(unzip_dir)
    if not os.path.exists(unzip_dir):
        os.mkdir(unzip_dir)
    if whether_udisk == 1 and whether_enc == 0:
        no_udisk_zip = os.path.join(output_dir, get_upgrade_udisk_zip())
    if whether_udisk == 0 and whether_enc == 0:
        no_udisk_zip = os.path.join(output_dir, get_upgrade_no_udisk_zip())
    if whether_udisk == 1 and whether_enc == 1:
        no_udisk_zip = os.path.join(output_dir, get_upgrade_udisk_enc())
    if whether_udisk == 0 and whether_enc == 1:
        no_udisk_zip = os.path.join(output_dir, get_upgrade_no_udisk_enc())
    else:
        raise Exception("input udisk info error!")

    upgrade_zip = zipfile.ZipFile(no_udisk_zip)
    if not os.path.exists(unzip_dir):
        os.mkdir(unzip_dir)
    upgrade_zip.extractall(unzip_dir)
    _del_sig_txt_all_words()
    startdir = unzip_dir  #要压缩的文件夹路径
    file_news = all_in_one_output # 压缩后文件夹的名字
    z = zipfile.ZipFile(file_news,'w',zipfile.ZIP_DEFLATED) #参数一：文件夹名
    for dirpath, dirnames, filenames in os.walk(startdir):
        fpath = dirpath.replace(startdir,'') #这一句很重要，不replace的话，就从根目录开始复制
        fpath = fpath and fpath + os.sep or ''#实现当前文件夹以及包含的所有文件的压缩
        for filename in filenames:
            z.write(os.path.join(dirpath, filename),fpath+filename)
            print ('压缩成功')
    z.close()

def del_info_line_signature(info, whether_udisk, whether_enc =0):
    if os.path.exists(unzip_dir):
        os.rmdir(unzip_dir)
    if not os.path.exists(unzip_dir):
        os.mkdir(unzip_dir)
    if whether_udisk == 1 and whether_enc == 0:
        no_udisk_zip = os.path.join(output_dir, get_upgrade_udisk_zip())
    if whether_udisk == 0 and whether_enc == 0:
        no_udisk_zip = os.path.join(output_dir, get_upgrade_no_udisk_zip())
    if whether_udisk == 1 and whether_enc == 1:
        no_udisk_zip = os.path.join(output_dir, get_upgrade_udisk_enc())
    if whether_udisk == 0 and whether_enc == 1:
        no_udisk_zip = os.path.join(output_dir, get_upgrade_no_udisk_enc())
    else:
        raise Exception("input udisk info error!")

    upgrade_zip = zipfile.ZipFile(no_udisk_zip)
    if not os.path.exists(unzip_dir):
        os.mkdir(unzip_dir)
    upgrade_zip.extractall(unzip_dir)
    _del_sig_txt_info_line(info)
    startdir = unzip_dir  #要压缩的文件夹路径
    file_news = all_in_one_output # 压缩后文件夹的名字
    z = zipfile.ZipFile(file_news,'w',zipfile.ZIP_DEFLATED) #参数一：文件夹名
    for dirpath, dirnames, filenames in os.walk(startdir):
        fpath = dirpath.replace(startdir,'') #这一句很重要，不replace的话，就从根目录开始复制
        fpath = fpath and fpath + os.sep or ''#实现当前文件夹以及包含的所有文件的压缩
        for filename in filenames:
            z.write(os.path.join(dirpath, filename),fpath+filename)
            print ('压缩成功')
    z.close()

def upgrade_package_extract():
    if not os.path.exists(output_dir):
        upgrade_pack = get_upgrade_zip()
        upgrade_zip = zipfile.ZipFile(upgrade_pack, 'r')
        for file in upgrade_zip.namelist():
            upgrade_zip.extract(file, pack_dir)

def clear_all_in_one_package():
    if os.path.exists(all_in_one_file):  # 如果文件存在
        os.remove(all_in_one_file)


def change_app_signature():
    with open('signature.txt', 'r') as f:
        content = f.read()
    position = content.find('RSA-SHA256(app.zip)=') + len('RSA-SHA256(app.zip)= ')
    position2 = position + 5
    l = []
    l = content[:position] + content[position2:]
    with open('signature.txt ', 'w') as f:
        f.write(l)


def push_no_udisk_zip1():
    upgrade_pack = get_upgrade_zip()
    upgrade_zip = zipfile.ZipFile(upgrade_pack, 'r')
    for file in upgrade_zip.namelist():
        upgrade_zip.extract(file, pack_dir)
    clear_all_in_one_package()
    ret = get_upgrade_no_udisk_zip()
    copyfile(ret, all_in_one_file)
    common_lib.adb_push(all_in_one_file, "/sdcard/hobot/upgrade")


def push_no_udisk_zip():
    upgrade_pack = get_upgrade_zip()
    push_no_udisk(upgrade_pack)

def push_no_udisk_zip_version_before():
    upgrade_pack = get_upgrade_zip_version_before()
    push_no_udisk(upgrade_pack)

def push_udisk_zip():
    upgrade_pack = get_upgrade_zip()
    push_udisk(upgrade_pack)

def push_no_udisk(upgrade_pack):
    upgrade_zip = zipfile.ZipFile(upgrade_pack, 'r')
    for file in upgrade_zip.namelist():
        upgrade_zip.extract(file, pack_dir)
    clear_all_in_one_package()
    ret = get_upgrade_no_udisk_zip()
    copyfile(ret, all_in_one_file)
    common_lib.adb_push(all_in_one_file, "/sdcard/hobot/upgrade")

def push_udisk(upgrade_pack):
    upgrade_zip = zipfile.ZipFile(upgrade_pack, 'r')
    for file in upgrade_zip.namelist():
        upgrade_zip.extract(file, pack_dir)
    clear_all_in_one_package()
    ret = get_upgrade_udisk_zip()
    copyfile(ret, all_in_one_file)
    common_lib.adb_push(all_in_one_file, "/sdcard/hobot/upgrade")



def get_upgrade_no_udisk_zip():
    resource_dir_list = os.listdir(pack_output_dir)
    upgrade_pack = ""
    for file in resource_dir_list:
        if ("HobotJ2_J2-DMS" in file) and (file.endswith(".zip")) and ("U_disk" not in file):
            upgrade_pack = os.path.join(pack_output_dir, file)
            break
    return upgrade_pack


def get_upgrade_udisk_zip():
    resource_dir_list = os.listdir(pack_output_dir)
    for file in resource_dir_list:
        if ("HobotJ2_J2-DMS" in file) and (file.endswith(".zip")) and ("U_disk" in file):
            upgrade_pack = os.path.join(pack_output_dir, file)
            break
    return upgrade_pack


def get_upgrade_no_udisk_enc():
    resource_dir_list = os.listdir(pack_output_dir)
    for file in resource_dir_list:
        if ("HobotJ2_J2-DMS" in file) and (file.endswith(".enc")) and ("U_disk" not in file):
            upgrade_pack = os.path.join(pack_output_dir, file)
            break
    return upgrade_pack


def get_upgrade_udisk_enc():
    resource_dir_list = os.listdir(pack_output_dir)
    for file in resource_dir_list:
        if ("HobotJ2_J2-DMS" in file) and (file.endswith(".enc")) and ("U_disk" in file):
            upgrade_pack = os.path.join(pack_output_dir, file)
            break
    return upgrade_pack


def get_upgrade_zip():
    resource_dir_list = os.listdir(pack_dir)
    for file in resource_dir_list:
        if ("J2-DMS-" in file) and (file.endswith(".zip")):
            upgrade_pack = file
            break
    upgrade_pack_file = os.path.join(pack_dir,upgrade_pack)
    return upgrade_pack_file

def get_upgrade_zip_version_before():
    resource_dir_list = os.listdir(version_before_dir)
    for file in resource_dir_list:
        if ("J2-DMS-" in file) and (file.endswith(".zip")):
            upgrade_pack = file
            break
    upgrade_pack_file = os.path.join(pack_dir,upgrade_pack)
    return upgrade_pack_file


def upgrade_s202da_j2():
    common_lib.adb_push(all_in_one_file_resource, "/sdcard/hobot/upgrade")
    ret = upgrade_j2_s202da_ui_ret()
    return ret

def upgrade_j2_s202da_ret():
    common_lib.adb_push(all_in_one_file_resource, "/sdcard/hobot/upgrade")
    ret = upgrade_j2_s202da_ui_ret()
    return ret


def get_space_size(space,content):
    lines = content.split("\n")
    num = []
    log.logger.info(lines)
    for line in lines:
        if space in line:
            num = line.split( )
            break
    return int(num[3])



def upgrade_j2_s202da_ui_check_again():
    upgrade_j2_s202da_ui_operation()
    i = 0
    while (1):
        time.sleep(5)
        i = i + 5
        ret = get_ui_text("工程模式_主界面_BUTTON_升级_升级结果")
        log.logger.info("upgrade process: {}".format(ret))
        if "升级成功" in ret:
            time.sleep(10)
            ret = get_ui_text("工程模式_主界面_BUTTON_升级_升级结果")
            if "升级成功" in ret:
                common_lib.avn_reboot()
                pass
            else:
                raise Exception("auto upgrade again")
            break
        if (i > 180):
            log.logger.error("upgrade fail!")
            common_lib.avn_reboot()
            raise Exception("upgrade fail!")



def upgrade_j2_s202da_ui_inreboot():
    upgrade_j2_s202da_ui_operation()
    i = 0
    while (1):
        time.sleep(3)
        i = i + 3
        ret = get_ui_text("工程模式_主界面_BUTTON_升级_升级结果")
        log.logger.info("upgrade process: {}".format(ret))
        if "升级中..." in ret:
            common_lib.avn_reboot()
            break
        if (i > 200):
            log.logger.error("upgrade fail!")
            raise Exception("upgrade fail!")

def upgrade_j2_s202da_ui_ret():
    upgrade_j2_s202da_ui_operation()
    i = 0
    while (1):
        time.sleep(10)
        i = i + 10
        ret = get_ui_text("工程模式_主界面_BUTTON_升级_升级结果")
        log.logger.info("upgrade process: {}".format(ret))
        if "升级成功" in ret:
            break
        if "错误" in ret:
            break
        if "超时" in ret:
            break
        if (i > 200):
            break
    common_lib.avn_reboot()
    return ret


def get_ui_text(text):
    if (common_lib.get_ini_data("cfg_param", "ui_automator") == "1"):
        ret = d(resourceId=common_lib.id(text)).get_text()
    else:
        ret = common_lib.get_text(text)
    return ret

def upgrade_j2_s202da_ui_operation():
    upgrade_j2_s202da_ui_preoperation()
    if (common_lib.get_ini_data("cfg_param", "ui_automator") == "1"):
        time.sleep(2)
        d(text="开始升级").click()
    else:
        common_lib.click_element("工程模式_主界面_BUTTON_升级_开始升级")
        time.sleep(2)
        common_lib.click_element("工程模式_主界面_BUTTON_升级_开始升级")

def upgrade_j2_s202da_ui_preoperation():
    common_lib.goto_page("工程界面")
    time.sleep(5)
    if(common_lib.get_ini_data("cfg_param","ui_automator") == "1"):
        d(text="OTA升级").click()
        time.sleep(2)
    else:
        common_lib.click_element("工程模式_主界面_BUTTON_升级")
        time.sleep(2)



def upgrade_ui_operation_s202da_stress(times):
    i = 0
    success_times = 0
    while i < times:
        ret = upgrade_j2_s202da_ui_ret()
        if "升级成功" in ret:
            success_times = success_times + 1
        i = i + 1
    average_success = success_times/times
    return average_success, success_times



def check_secure_logs(info, file_pre, file):
    #指明文件路径
    pre_file = os.path.join(local_file_dir, file_pre)
    final_file = os.path.join(local_file_dir, file)
    #读取文件，存储到列表当中
    pre_content=open(pre_file,'r',encoding='utf-8').readlines()
    final_content=open(final_file,'r',encoding='utf-8').readlines()
    #计算列表的长度
    previous_line = len(pre_content)
    #截取列表
    temp_list=final_content[previous_line:]
    count = 0
    for i in temp_list:
        if info in i:
            count = count + 1
    return count


def touch_file(file):
    common_lib.serial_login_jx()
    common_lib.serial_cmd("cd /")
    common_lib.serial_cmd("mount -o rw,remount")
    common_lib.serial_cmd("cd userdata/")
    touch_command = "touch {}".format(file)
    for i in range(3):
        ret = common_lib.serial_cmd("ls")
        if "enable_dmsapp_signature" not in ret:
            ret = common_lib.serial_cmd(touch_command)
        else:
            break



if __name__ == '__main__':
    _del_sig_txt_info_line("update.sh")
