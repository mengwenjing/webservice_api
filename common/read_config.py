from configparser import RawConfigParser
from common import contants

class ReadConfig:
    """读取配置文件"""
    def __init__(self):
        """初始化函数中先读取global.conf文件，如果on为ture读取online.conf，如果on为false读取test.conf"""
        self.config = RawConfigParser()
        self.config.read(contants.global_file,encoding='utf-8')
        switch = self.config.getboolean('switch','on')
        if switch:
            self.config.read(contants.online_file,encoding='utf-8')
        else:
            self.config.read(contants.test_file,encoding='utf-8')

    def get_str(self,section,option):
        return self.config.get(section,option)

    def get_int(self,section,option):
        return self.config.getint(section,option)

    def get_float(self,section,option):
        return self.config.getfloat(section,option)

    def get_bool(self,section,option):
        return self.config.getboolean(section,option)

config = ReadConfig()

