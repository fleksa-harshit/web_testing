from selenium.webdriver.common.keys import Keys

from constant import *


def get_otp():
    otp = input('Enter 5 digit otp: ')
    return otp


class LoginData:
    def __init__(self, driver, phone_no):
        self.phone_no = phone_no
        self.driver = driver

    def login(self):
        self.driver.find_element_by_xpath(login_link).click()
        self.driver.find_element_by_xpath(login_input).send_key(Keys.BACKSPACE + Keys.BACKSPACE + self.phone_no)
        self.driver.find_element_by_xpath(send_button).click()
        otp = get_otp()
        for i in [1, 2, 3, 4, 5]:
            self.driver.find_element_by_xpath(
                otp_input + str(i) + ']/input').send_key(otp[i-1])
        self.driver.find_element_by_xpath(submit_button).click()
        try:
            result = self.driver.find_element_by_xpath(otp_valid).text
            if result == 'Invalid otp':
                return 'Unsuccessful'
        except Exception as err:
            print('not Invalid output')
        success = self.driver.find_element_by_xpath(main_page_name).text
        if success == 'Name':
            print('successful')
            return 'successful'
