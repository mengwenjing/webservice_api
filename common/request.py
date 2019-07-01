from suds.client import Client
from common.read_config import config

class Request:

    def __init__(self,api):
        self.api = api

    def request(self, url, data):
        url = config.get_str('api','pre_url') + url
        client = Client(url)
        if self.api == 'sendMCode':
            result = client.service.sendMCode(data)
        elif self.api == 'userRegister':
            result = client.service.userRegister(data)
        elif self.api == 'verifiedUserAuth':
            result = client.service.verifyUserAuth(data)
        elif self.api == 'bindBankCard':
            result = client.service.bindBankCard(data)
        return result


if __name__ == '__main__':
    from common.doexcel import DoExcel
    from common.contants import case_file
    url = DoExcel(case_file,'sendMCode').read_data()[0].url
    data = eval(DoExcel(case_file,'sendMCode').read_data()[0].data)
    a = Request('sendMCode').request(url,data)
