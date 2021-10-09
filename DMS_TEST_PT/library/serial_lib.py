# coding=utf-8
import serial
from _library.prase_ini import get_ini_data
from _library.sys import *

serial_path = os.path.join(os.path.dirname(__file__), r"..\result\serial")
serialfile = os.path.join(os.path.dirname(__file__), r"..\result\serial", "serial_out.txt")

class serial_lib():
    @classmethod
    def serial_cmd(self, cmd):
        """
        串口输入命令，返回命令回显值，注意，请提前登录系统
        :param cmd: 输入的串口指令
        ：return: 返回串口命令的回显值
        """
        ser_cmd = cmd+"\r"
        log.logger.info(cmd)
        try:
            portx=get_ini_data("cfg_param","j2_serial_port")  # 端口
            bps=int(get_ini_data("cfg_param","j2_serial_baud"))
            # 超时设置,None：永远等待操作，0为立即返回请求结果，其他值为等待超时时间(单位为秒）
            ser=serial.Serial(portx,bps,timeout=1)
            result=ser.write(ser_cmd.encode("gbk"))# 写数据
            # 循环接收数据，此为死循环，可用线程实现
            time.sleep(0.3)
            while True:
                 if ser.in_waiting:
                     try:
                         str = ser.read(ser.in_waiting ).decode("gbk")
                     except:
                         str = ser.read(ser.in_waiting ).decode("utf-8")

                     if(str == "exit"):# 退出标志
                         break
                     else:
                         log.logger.info(str)
                         return str
            ser.close() # 关闭串口
            return str
        except Exception as e:
            log.logger.error("serial error: {}".format(e))
            raise Exception(e)

    @classmethod
    def serial_listen_to_file(self, listen_time):
        """
        监听串口输出内容(如日志)，并写入文件
        :param listen_time: 监听的时间
        ：return: 返回文件句柄
        """
        try:
            if not os.path.exists(serial_path):
                os.makedirs(serial_path)
            serfile = open(serialfile,"w")
            portx=get_ini_data("cfg_param","j2_serial_port")  #端口
            bps=int(get_ini_data("cfg_param","j2_serial_baud"))
            ser=serial.Serial(portx,bps,timeout=listen_time)
            i = 0
            t1 = time.time()
            while (1):
                 if ser.in_waiting:
                     str=ser.read(ser.in_waiting ).decode('utf-8')
                     print(str)
                     serfile.write(str)
                     t2 = time.time()
                     if(t2 - t1 > listen_time):
                        break
            ser.close()#关闭串口
            return serfile  #文件
        except Exception as e:
            log.logger.error("serial error: {}".format(e))
            raise Exception(e)

    @classmethod
    def read_serial_file_content(self):
        """
        读取串口文件中的内容
        ：return: 文件内容
        """
        with open(serialfile, 'r') as file:
            content = file.read()
            return (str)(content)


    @classmethod
    def listen_serial_content(self, listen_time):
        """
        监听串口特定时长的输出（5分钟以内），并返回这段时间的内容
        :param listen_time: 监听的时间
        ：return: 返回监听的所有内容
        """
        self.serial_listen_to_file(listen_time)
        content = self.read_serial_file_content()
        return content


    @classmethod
    def serial_login_jx(self):
        """
        串口登录J2
        """
        self.serial_cmd("\r")
        self.serial_cmd("root")
        self.serial_cmd("Hobot123")


if __name__ == '__main__':
    serial_lib = serial_lib()
    serial_lib.serial_login_jx()
