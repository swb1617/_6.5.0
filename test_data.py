"""
user:石文斌
time：2021/11/15
equipment：IGS50S
"""
import os
import time
import unittest

from appium import webdriver


class test_DATA(unittest.TestCase):

    def setUp(self) -> None:  # 执行方法前准备工作
        self.driver.implicitly_wait(15)  # 稳定元素
        print("...........开始.............")

    def tearDown(self) -> None:  # 执行方法后工作
        print("...........结束..............")

    @classmethod
    def setUpClass(cls) -> None:  # 执行测试类前准备工作
        os.system('start startAppiumServer.bat')  # 启动appium服务
        time.sleep(8)  # 等待appium服务启动完毕

        desired_caps = {
            'platformName': 'Android',
            'platformVersion': '9',
            'deviceName': 'test01',
            'appPackage': 'com.igpsport.globalapp',
            'appActivity': 'com.igpsport.globalapp.activity.v3.SplashActivity',
            'noReset': True,
            'newCommandTimeout': 6000,
            # 更换底层驱动
            'automationName': 'UiAutomator2',
            'unicodeKeyboard': True,  # 修改手机的输入法
            'resetKeyboard': True
        }
        cls.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    @classmethod
    def tearDownClass(cls) -> None:  # 执行测试类后工作
        os.system('start stopAppiumServer.bat')  # 关闭appium服务
        time.sleep(10)

    def swipe_down(self):  # 定义下滑动方法
        size = self.driver.get_window_size()  # 获取手机屏幕尺寸
        width = size['width']
        height = size['height']
        x1 = x2 = width * 0.5
        y1, y2 = height * 0.25, height * 0.75
        time.sleep(3)
        self.driver.swipe(x1, y1, x2, y2, 1500)  # 滑动方法

    def data_up(self):
        self.driver.find_element_by_id("com.igpsport.globalapp:id/tv_activity_name").click()
        time.sleep(35)  # 上传时间
        self.driver.find_element_by_id("com.igpsport.globalapp:id/tv_activity_name").click()
        try:
            message = self.driver.find_element_by_id("android:id/message").text
            if message:
                self.driver.save_screenshot('error.png')
                time.sleep(1)
                for k in range(4):
                    self.driver.find_element_by_id("android:id/button1").click()  # retry操作
                    time.sleep(35)  # 上传时间
                    self.driver.find_element_by_id("com.igpsport.globalapp:id/tv_activity_name").click()
                    print('重试', k, ' 次')
                    if k == 4:
                        print("重试失败")
        except:
            pass
        time.sleep(2)
        self.driver.find_element_by_xpath(
            "//android.widget.ImageView[@resource-id='com.igpsport.globalapp:id/ivMenu']").click()
        time.sleep(3)
        self.driver.find_element_by_id("com.igpsport.globalapp:id/tvDelete").click()
        time.sleep(5)
        self.driver.find_element_by_id("com.igpsport.globalapp:id/md_button_positive").click()
        try:
            id_name = self.driver.find_element_by_id("com.igpsport.globalapp:id/tv_activity_name").text
            if not id_name:
                print("重新尝试删除")
                self.driver.find_element_by_xpath(
                    "//android.widget.ImageView[@resource-id='com.igpsport.globalapp:id/ivMenu']").click()
                time.sleep(3)
                self.driver.find_element_by_id("com.igpsport.globalapp:id/tvDelete").click()
                time.sleep(5)
                self.driver.find_element_by_id("com.igpsport.globalapp:id/md_button_positive").click()

        except:
            pass

    def test_data(self):
        global i
        self.driver.find_element_by_id("com.igpsport.globalapp:id/item_device").click()
        time.sleep(10)
        self.driver.find_element_by_xpath(
            "//android.widget.TextView[@resource-id='com.igpsport.globalapp:id/tvFunctionName' and @text='Data "
            "Management']").click()
        time.sleep(8)
        self.swipe_down()
        time.sleep(5)
        try:
            for i in range(500):  # 上传次数
                self.data_up()
                time.sleep(3)
                print(f"第", i + 1, "次 OK")
                time.sleep(5)
                self.swipe_down()
                time.sleep(5)
        except:
            self.driver.save_screenshot('data_error.png')
            print(f"第", i + 1, "次 ERROR")


if __name__ == '__main__':
    unittest.main()
