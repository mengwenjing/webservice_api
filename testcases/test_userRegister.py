import unittest
from ddt import ddt,data
from common.domsql import DoMysql
from common.doexcel import DoExcel
from common.contants import case_file
from common.request import Request
from common.context import Context
from common.collect_log import CollectLog
from common.random_create import RandomCreate

logger = CollectLog().logger(__name__)

@ddt
class TestUserRegister(unittest.TestCase):

    testdata = DoExcel(case_file,'userRegister').read_data()

    @classmethod
    def setUpClass(cls):
        cls.excel = DoExcel(case_file,'userRegister')
        cls.mysql = DoMysql()

    @data(*testdata)
    def testUserRegister(self,case):

        case.data = eval(case.data)

        if case.data.__contains__("mobile") and case.data["mobile"] == "register_phone":
            max_phone = self.mysql.fetch_one('select max(Fmobile_no) from sms_db_25.t_mvcode_info_5;')['max(Fmobile_no)']
            max_phone = int(max_phone) + 1000
            case.data["mobile"] = max_phone
            setattr(Context,'register_phone', str(max_phone))
        elif case.data.__contains__("user_id") and case.data["user_id"] == "name":
            name = RandomCreate().create_name()
            case.data["user_id"] = name
            setattr(Context, 'name', name)

        if case.title == '正常发送验证码':
            logger.info('执行用例是：{}，请求url是：{}，请求数据是：{}'.format(case.title, case.url, case.data))
            res = Request('sendMCode').request(case.url,case.data)
            try:
                self.assertEqual(res['retInfo'], eval(case.expected)['retInfo'])
                self.excel.write_data(case.case_id + 1, str(res), 'pass')
                if res['retCode'] == '0' and res['retInfo'] == 'ok':
                    case.sql = Context().replace(case.sql)
                    verify_code = self.mysql.fetch_one(case.sql)['Fverify_code']
                    setattr(Context,'verify_code',verify_code)
                    logger.info("成功发送验证码，验证码为：{}".format(verify_code))
            except AssertionError as e:
                self.excel.write_data(case.case_id + 1, str(res), 'failed')
                logger.error("断言失败，错误是：{}".format(e))
        else:
            case.data = Context().replace(str(case.data))
            logger.info('执行用例是：{}，请求url是：{}，请求数据是：{}'.format(case.title, case.url, case.data))
            res = Request('userRegister').request(case.url,eval(case.data))
            try:
                self.assertEqual(res['retInfo'], eval(case.expected)['retInfo'])
                self.excel.write_data(case.case_id + 1, str(res), 'pass')
                if case.title == '成功注册':
                    case.sql = Context().replace(case.sql)
                    user = self.mysql.fetch_one(case.sql)['Fuser_id']
                    if user:
                        try:
                            self.assertEqual(user,eval(case.data)['user_id'])
                        except AssertionError as e:
                            logger.error('注册使用数据与插入数据库数据不一致，错误是：{}'.format(e))
            except AssertionError as e:
                self.excel.write_data(case.case_id + 1, str(res), 'failed')
                logger.error("断言失败，错误是：{}".format(e))

    @classmethod
    def tearDownClass(cls):
        cls.mysql.close()



