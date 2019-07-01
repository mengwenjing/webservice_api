import logging
from logging.handlers import TimedRotatingFileHandler
from common.read_config import config
from common.contants import log_dir

class CollectLog:
    def logger(self,name):
        collect_level = config.get_str('log','collect_level')
        output_level = config.get_str('log','output_level')
        fmt = config.get_str('log','fmt')
        output = config.get_str('log','output')
        logger = logging.getLogger(name)
        logger.setLevel(collect_level)
        if output == 'console':
            ch = logging.StreamHandler()
        else:
            ch = TimedRotatingFileHandler(log_dir+output, when='D', interval=1, backupCount=2, encoding='utf-8')
        ch.setLevel(output_level)
        logger.addHandler(ch)
        formatter = logging.Formatter(fmt)
        ch.setFormatter(formatter)

        return logger