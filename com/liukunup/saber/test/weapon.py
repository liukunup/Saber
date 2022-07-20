import unittest
from fate import excalibur


class MyTestCase(unittest.TestCase):

    @excalibur(
        name="测试标题",
        desc="用例描述/操作步骤",
        date="2022-01-01 12:00:00")
    def test_something(self):
        """
        dasd
        :return: 不涉及
        """
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
