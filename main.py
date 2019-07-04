import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
LOGIN_USER_ONE = "user_one"
PASSWORD_USER_ONE = "userone"
LOGIN_USER_TWO = "user_two"
PASSWORD_USER_TWO = "usertwo"


class TestFirstUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.get("https://webmail.meta.ua/")

    def test_open_mail_service(self):
        self.assertIn("МетаПошта", self.driver.title)

    def test_login_input(self):
        login = self.driver.find_element_by_id('login-field')
        login.send_keys(LOGIN_USER_ONE)
        password = self.driver.find_element_by_id('pass-field')
        password.send_keys(PASSWORD_USER_ONE)
        password.send_keys(Keys.RETURN)
        time.sleep(10)
        self.assertIn(LOGIN_USER_ONE, self.driver.find_element_by_tag_name('strong').text)

    def test_send_mail_and_logout(self):
        self.driver.find_element_by_id('id_send_email').click()
        time.sleep(10)

        to_whom = self.driver.find_element_by_id('send_to')
        to_whom.send_keys('user_two@meta.ua')

        theme = self.driver.find_element_by_id('subject')
        theme.send_keys('test')

        body = self.driver.find_element_by_id('body')
        body.send_keys("Hello, it is test")

        send = self.driver.find_element_by_xpath("//input[@name='send'][@type='submit']")
        send.click()
        time.sleep(5)
        self.assertEqual("Ваше повідомлення надiслано", self.driver.find_element_by_id('send_ok').text)

        self.driver.find_element_by_id('id_logout').click()
        self.driver.find_element_by_xpath("//label[@class='checkholder']").click()
        self.assertIn("<META>", self.driver.title)

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()


class TestSecondUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.get("https://webmail.meta.ua/")

    def test_open_mail_service(self):
        self.assertIn("<META>", self.driver.title)

    def test_login_input(self):
        login = self.driver.find_element_by_id('login-field')
        login.send_keys(LOGIN_USER_TWO)
        password = self.driver.find_element_by_id('pass-field')
        password.send_keys(PASSWORD_USER_TWO)
        password.send_keys(Keys.RETURN)
        time.sleep(10)
        self.assertIn(LOGIN_USER_TWO, self.driver.find_element_by_tag_name('strong').text)

    def test_open_mail_and_logout(self):
        self.driver.find_element_by_link_text('test user_1').click()
        self.assertIn('test', self.driver.find_element_by_xpath("//h1[@class='mess_subj']").text)
        self.assertIn('Hello, it is test', self.driver.find_element_by_id('message_body').text)
        self.driver.find_element_by_id('id_logout').click()
        self.assertIn("<META>", self.driver.title)

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()


if __name__ == "__main__":
    unittest.main()