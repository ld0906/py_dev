from selenium import webdriver
import unittest



class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrive_it_later(self):
        # 小张听说有一个很酷的在线代办事项应用
        #他去看了这个应用的首页
        self.browser.get('http://localhost:8000')

        #他注意到网页的标题和头部都包含 "TO-Do"这个词
        #assert 'To-Do' in browser.title, "Browser title was " + browser.title
        self.assertIn('To-Do',self.browser.title)
        self.fail('Finish the test!')

if __name__ == "__main__":
    unittest.main(warnings='ignore')

#应用邀请他输入一个代办事项

#他在一个文本框里输入了 "Buy peacock feathers"
#小张的爱好是使用假蝇做饵钓鱼

#他按回车键后，页面更新了
#待办事项表格中显示了 "1: Buy peacock feathers"

#页面中又显示了一个文本框，可以输入其他的待办事项
#他输入了 "Use peacock feathers to make a fly" (使用孔雀羽毛做假蝇)
#小张做事很有条理。

#页面再次更新，他的清单中显示了这两个待办事项

#小张想知道这个网站是否会记住他的清单
#他看到网站为他生成了一个唯一的URL
#而且页面中有一些文字解说了这个功能

#他访问那个URL,发现他的待办事项列表还在

#他很满意，去睡觉了
