#方便Jenkins执行时，找到当前文件。后期用pytest后就不用这步了
import sys
sys.path.append('./')


import unittest
import HTMLTestRunner
from common import contants

suite = unittest.TestSuite()
loader = unittest.TestLoader()
discover = unittest.defaultTestLoader.discover(contants.case_dir,'test_*.py')

with open(contants.report_dir + '/webserviceAPI_testreport.html','wb+') as file:
    runner =HTMLTestRunner.HTMLTestRunner(stream=file,verbosity=3,title='webservice接口实战测试报告',
                                          description='测试报告',tester = '夜莺')
    runner.run(discover)