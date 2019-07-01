import unittest

import suds
from ddt import ddt,data
from common.doexcel import DoExcel
from common.contants import case_file
from common.request import Request
from common.context import Context
from common.collect_log import CollectLog
from common.domsql import DoMysql

logger = CollectLog().logger(__name__)

@ddt
class TestSendMCode(unittest.TestCase):

    testdata = DoExcel(case_file,'sendMCode').read_data()

    @classmethod
    def setUpClass(cls):
        cls.excel = DoExcel(case_file,'sendMCode')
        cls.mysql = DoMysql()

    @data(*testdata)
    def testSendMCode(self,case):
        logger.info('执行用例是：{}，请求url是：{}，请求数据是：{}'.format(case.title, case.url, case.data))
        try:
            case.data = Context().replace(case.data)
            res = Request('sendMCode').request(case.url,eval(case.data))
            try:
                self.assertEqual(res['retCode'],eval(case.expected)['retCode'])
                self.excel.write_data(case.case_id+1, str(res), 'pass')
                if res['retCode'] == '0' and res['retInfo'] == 'ok':
                    case.sql = Context().replace(case.sql)
                    mcode = self.mysql.fetch_one(case.sql)['Fverify_code']
                    if mcode:
                        logger.info('成功获取验证码：{}'.format(mcode))
                    else:
                        logger.info('获取验证码失败')
            except AssertionError as e:
                self.excel.write_data(case.case_id + 1, str(res), 'filed')
                logger.error('断言失败，错误是：{}'.format(e))
        except suds.WebFault as e:
            try:
                self.assertEqual(e.fault['faultstring'],case.expected)
                self.excel.write_data(case.case_id + 1, str(e.fault), 'pass')
            except AssertionError as e:
                self.excel.write_data(case.case_id + 1, str(e.fault), 'failed')
                logger.error('断言失败，错误是：{}'.format(e))

    @classmethod
    def tearDownClass(cls):
        cls.mysql.close()





