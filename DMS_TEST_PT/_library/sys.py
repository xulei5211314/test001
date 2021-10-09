# -*- coding: utf-8 -*-
# @Time    : 2021/1/9
# @Author  : TingTing.Zhao
import json
import subprocess
import time
import xmltodict
from _library.log import *
from email.utils import formataddr
import zipfile
from PIL import ImageGrab
import os,sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from config.config import GLOBAL_PROJECT_CFG
from _library.log import *
from _library.global_valule import *

log = logger()
zipFilePath = os.path.join(os.path.dirname(__file__), r"..\result\html.zip")
html_path = os.path.join(os.path.dirname(__file__), r"..\result\html")
# image_path = os.path.join(os.path.dirname(__file__), r"..\result\email_content.png")
image_dir = os.path.join(os.path.dirname(__file__), r"..\result\email_picture")
server_report_path = r"\\bjnas\bjnas\公共\00-临时文件\100_座舱自动化工具\test_report"
def send_report_to_server():
    send_cmd = "xcopy /s /e /y {} {}".format(html_path, server_report_path)
    os.system(send_cmd)
    log.logger.info("send_report_to_server ok")


def set_image_path():
    if not os.path.exists(image_dir):
        os.mkdir(image_dir)
    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
    time_path = r"..\result\email_picture\email_content-{}.png".format(current_time)
    image_path = os.path.join(os.path.dirname(__file__), time_path)
    return image_path

def send_mail():
    time.sleep(3)
    picture_path = set_image_path()
    get_screen(picture_path)
    zip_report()
    my_sender = 'tingting.zhao@horizon.ai'  # 发件人邮箱账号
    my_pass = 'Rwi_6681689'  # 发件人邮箱密码
    my_user = 'tingting.zhao@horizon.ai'  # 收件人邮箱账号，我这边发送给自己
    fan_ge = 'lifan.wang@horizon.ai'
    qq_mail = '479520568@qq.com'
    auto_mm = "auto-mm@horizon.ai"
    receiver = my_user
    ret = True
    try:
        msg = MIMEMultipart('related')
        content = MIMEText('<html><body>'
                           '<h3>本次测试结果如下.</h3>'
                           '<h3>详细内容请至以下路径或者解压附件，用Microsoft Edge浏览器打开index.html查看</h3>'
                           '<h4>\\\\bjnas\\bjnas\\公共\\00-临时文件\\100_座舱自动化工具\\test_report</h4>'
                           '<h3>\t</h3>'
                           '<img src="cid:imagid" alt="imageid" height="600" width="1150">'
                           '</body></html>', 'html', 'utf-8')  # 正文
        msg.attach(content)

        file = open(picture_path, "rb")
        img_data = file.read()
        file.close()
        img = MIMEImage(img_data)
        img.add_header('Content-ID', 'imagid')
        msg.attach(img)

        # 附件
        att2 = MIMEText(open(zipFilePath, 'rb').read(), 'base64', 'utf-8')
        att2["Content-Type"] = 'text/plain'
        att2["Content-Disposition"] = 'attachment; filename="report.zip"'
        msg.attach(att2)

        current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
        mail_subject = "(自动发送)软件自动化测试报告-{}".format(current_time)

        msg['From'] = formataddr(["FromRunoob", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["FK", receiver])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = mail_subject  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP("mail.horizon.ai", 587)  # 发件人邮箱中的SMTP服务器，端口是587
        server.set_debuglevel(1)
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [receiver, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False

    if ret:
        print("邮件发送成功")
    else:
        print("邮件发送失败")


def get_screen(path):
    im = ImageGrab.grab((0, 50, 1900, 1000))
    im.save(path)
    time.sleep(3)


def zip_report():
    zipFile = zipfile.ZipFile(zipFilePath, "w", zipfile.ZIP_DEFLATED)
    absDir = html_path
    writeAllFileToZip(absDir, zipFile)


def writeAllFileToZip(absDir,zipFile):
    for f in os.listdir(absDir):
        absFile=os.path.join(absDir,f) #子文件的绝对路径
        if os.path.isdir(absFile): #判断是文件夹，继续深度读取。
            relFile=absFile[len(os.getcwd())+1:] #改成相对路径，否则解压zip是/User/xxx开头的文件。
            zipFile.write(relFile) #在zip文件中创建文件夹
            writeAllFileToZip(absFile,zipFile) #递归操作
        else: #判断是普通文件，直接写到zip文件中。
            relFile=absFile[len(os.getcwd())+1:] #改成相对路径
            zipFile.write(relFile)
    return

def cmd(command):
    """
    运行cmd指令
    :param command: 命令内容
    :return:
    """
    log.logger.info(command)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    out = process.stdout.readlines()
    ret = b"\n"
    for line in out:
        ret = ret + (line.strip() + b"\n")
    try:
        ret = str(ret, encoding="utf-8").rstrip()
    except Exception as e:
        ret = str(ret, encoding="gbk").rstrip()
    log.logger.info(ret)
    return ret


def xml_to_dict(xml):
    """
    将xml格式转换为dict格式
    :param xml:
    :return:
    """
    convertejson = xmltodict.parse(xml, encoding="utf-8")
    json_str = json.dumps(convertejson, indent=4)
    json_dict = json.loads(json_str)
    return json_dict


if __name__ == '__main__':
    pass
