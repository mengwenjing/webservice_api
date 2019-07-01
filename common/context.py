import configparser
import re
from common.read_config import config

class Context:

    def replace(self,data):

        p ='#(.*?)#'
        while re.search(p,data):
            m = re.search(p,data)
            g = m.group(1)
            try:
                v = config.get_str('testdata',g)
            except configparser.NoOptionError as e:
                if hasattr(Context,g):
                    v = getattr(Context,g)
                else:
                    print('找不到值')
                    raise e
            data = re.sub(p,v,data,count=1)

        return data
if __name__ == '__main__':
    from common.doexcel import DoExcel
    from common.contants import case_file
    data = DoExcel(case_file,'sendMCode').read_data()
    new = Context().replace(data[0].data)
    print(new)