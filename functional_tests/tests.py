from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10
class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self,row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
        # 小张听说有一个很酷的在线代办事项应用
        #他去看了这个应用的首页11111
        self.browser.get(self.live_server_url)

        #他注意到网页的标题和头部都包含 "TO-Do"这个词
        #assert 'To-Do' in browser.title, "Browser title was " + browser.title
        self.assertIn('To-Do',self.browser.title)
        header_text =  self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do',header_text)
        # 应用邀请他输入一个代办事项
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
                         )

        # 他在一个文本框里输入了 "Buy peacock feathers"
        # 小张的爱好是使用假蝇做饵钓鱼
        inputbox.send_keys('Buy peacock feathers')

        # 他按回车键后，页面更新了
        # 待办事项表格中显示了 "1: Buy peacock feathers"
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # 页面中又显示了一个文本框，可以输入其他的待办事项
        # 他输入了 "Use peacock feathers to make a fly" (使用孔雀羽毛做假蝇)
        # 小张做事很有条理。
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        # 页面再次更新，他的清单中显示了这两个待办事项
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
        # 小张想知道这个网站是否会记住他的清单
        # 他看到网站为他生成了一个唯一的URL
        # 而且页面中有一些文字解说了这个功能

        # 他访问那个URL,发现他的待办事项列表还在

        # 他很满意，去睡觉了

    def test_multiple_users_can_start_lists_at_different_urls(self):
        #小张新建了一个待办事项清单
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        #他注意到清单有个唯一的URL
        edith_list_url = self.browser.current_url
        self.assertRegex((edith_list_url,'/lists/.+'))

        #现在一名叫弗朗西斯的新用户访问了网站

        ## 我们使用一个新的浏览器会话
        ## 确保小张的信息不会从cookie中泄漏出去
        self.browser.quit()
        self.browser = webdriver.Firefox()

        #弗朗西斯访问首页
        #页面中看不到小张的清单
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers',page_text)
        self.assertNotIn('make a fly',page_text)

        #弗朗西斯输入一个新的待办事项，新建一个清单
        #他不像小张那么兴趣盎然

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        #弗朗西斯获得了他的唯一URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url,'/lists/.+')
        self.assertNotEqual(francis_list_url,edith_list_url)

        #这个页面还是没有小张的清单
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers',page_text)
        self.assertIn('Buy milk',page_text)

        #两人都很满意，然后去睡觉了






