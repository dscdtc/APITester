# -*- coding: utf_8 -*-
import logging

class Logger():
    def __init__(self, logfile, loglevel, logger):
        '''
           指定保存日志的文件路径，日志级别，以及调用文件
           将日志存入到指定的文件中
        '''
        '''
#######################基础日志配置#####################
        #日志级别等级CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET
        log_format = '[%(asctime)s] [%(levelname)s] %(message)s'
        ##创建路径及对应的log文件---待解决

        logging.basicConfig(level=logging.DEBUG,
                            format=log_format,
                            filename=logfile,
                            filemode='w',)
########################################################
        '''
        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(logfile)
        fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # 定义handler的输出格式
        #用字典保存日志级别#现完成0、5级的定义
        format_dict = {
           0 : logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s'),
           1 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
           2 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
           3 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
           4 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
           5 : logging.Formatter('[%(asctime)s] %(name)-12s: %(filename)s[line:%(lineno)d] <%(levelname)s> %(message)s')
        }
        formatter_c = format_dict[int(loglevel)]
        formatter_f = format_dict[5]

        fh.setFormatter(formatter_f)
        ch.setFormatter(formatter_c)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

   
    def getlog(self):
        return self.logger
