# -*- coding: utf-8 -*-
# @Time    : 2021/1/9
# @Author  : TingTing.Zhao
import os
import logging
import datetime
from logging import handlers
from config.config import GLOBAL_PROJECT_CFG


class logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }   # 日志级别关系映射

    def __init__(self, level=GLOBAL_PROJECT_CFG.get("LOG_LEVEL").lower(), when='D', backCount=3):
        fmt = '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
        current_time = datetime.datetime.now().strftime('%Y-%m-%d')
        if GLOBAL_PROJECT_CFG.get("LOG_PATH"):
            filedir = GLOBAL_PROJECT_CFG.get("LOG_PATH")
        else:
            filedir = os.path.join(os.path.dirname(__file__), r"..\result\log")
        if not os.path.exists(filedir):
            os.mkdir(filedir)
        filename = os.path.join(filedir, current_time + "_log.log")
        self.logger = logging.getLogger(filename)
        # 防止重复
        if self.logger.handlers:
            return
        format_str = logging.Formatter(fmt)  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename,
                                               when=when, backupCount=backCount, encoding='utf-8')
        th.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(sh)  # 把对象加到logger里
        self.logger.addHandler(th)


if __name__ == '__main__':
    log = logger()
    log.logger.debug('debug')
    log.logger.info('info')
    log.logger.warning('警告')
    log.logger.error('报错')
    log.logger.critical('严重')
