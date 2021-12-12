import time

from prompt_toolkit.layout import Dimension
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from constant import *

emails = 'krishnatrea@gmail.com'


class OrderDetails:
    def __init__(self, name, price, sub_cat):
        self.name = name
        self.sub_cat = sub_cat
        self.price = price


class Orders:
    order_details = []

    def __init__(self, order_type, name, max_amount, email, phone_no, driver, payment_type, website):
        self.website = website
        self.driver = driver
        self.type = order_type
        self.name = name
        self.max_amount = max_amount
        self.email = email
        self.phone_no = phone_no
        self.order_type = order_type
        self.payment_type = payment_type

    def select_order_type(self):
        if self.order_type != 'Delivery':
            self.driver.find_element_by_xpath(
                '/html/body/div/div[1]/main/div[4]/div/ul/li[contains(.,"' + self.order_type + '")]').click()

        else:
            print('nothing set for Delivery')

    #         TODO: Set up every thing for Delivery

    def banner_and_decline(self):
        time.sleep(3)
        try:
            self.driver.find_element_by_xpath(banner_button).click()
        except Exception as err:
            print(err)
        try:
            self.driver.find_element_by_id(decline_button).click()
        except Exception as err:
            print(err)

    def open_website(self):
        self.driver.get(self.website)

    def maximise(self):
        self.driver.maximize_window()

    def create_order_mobile_view(self):
        self.open_website()
        self.maximise()
        self.driver.implicitly_wait(3)
        self.banner_and_decline()
        self.click_order_now()
        self.select_order_type()
        self.make_random_order()
        time.sleep(10)

    def create_order_not_login(self):
        self.open_website()
        self.maximise()
        self.driver.implicitly_wait(3)
        self.banner_and_decline()
        self.click_order_now()
        self.select_order_type()
        self.make_random_order()
        self.click_checkout()
        self.add_details()
        self.click_payment_method()
        self.proceed_order()
        self.fill_otp()
        self.driver.implicitly_wait(10)
        self.order_and_pay()
        self.driver.implicitly_wait(10)
        time.sleep(10)
        result = self.check_order_done()
        self.driver.close()
        return result

    def check_order_done(self):
        try:
            self.driver.find_element_by_xpath('//*[contains(.,"Your order is placed successfully")]')
            return True
        except Exception as er:
            return False

    def order_and_pay(self):
        self.driver.find_element_by_xpath(order_and_pay_button).click()

    def fill_otp(self):
        time.sleep(60)
        # self.driver.find_element_by_xpath(submit_order_otp).click()

    def proceed_order(self):
        self.driver.find_element_by_xpath(proceed_button).click()
        self.driver.find_element_by_xpath(send_otp_button).click()

    def click_payment_method(self):
        i = 3
        if self.payment_type == stripe:
            i = 1
        elif self.payment_type == paypal:
            i = 2
        self.driver.find_element_by_xpath(payment_type_button + str(i) + ']').click()

    def make_random_order(self):
        ids = self.driver.find_elements_by_xpath(order_ids)
        for i in ids:
            print(i.get_property("id"), end="\n")
            price = int()
            try:
                price = float(self.driver.find_element_by_xpath(
                    '//*[@id="' + i.get_property('id') + '"]/div[1]/div/div[1]/p[2]'
                ).text.replace('€', '').replace(',', ''))
                print(price)
                try:
                    element = self.driver.find_element_by_xpath(
                        '//*[@id="' + i.get_property('id') + '"]/div[1]/div/div[2]/div/div/a')
                    if element.text == 'ADD':
                        if price < self.max_amount and self.max_amount > 0:
                            self.max_amount = self.max_amount - price
                            element.click()
                            print('click or not')
                            time.sleep(2)
                        elif self.max_amount < 0:
                            pass
                    elif element.text == 'ADD +':
                        print('different product')
                except Exception as err:
                    print("error")
            except Exception:
                print("not a Food item")

    def click_checkout(self):
        self.driver.find_element_by_xpath(checkout).click()

    def click_order_now(self):
        self.driver.find_element_by_xpath(
            '/html/body/div[2]/div[1]/main/div/section[1]/div[2]/div/div/div/div/a[2]').click()

    def add_details(self):
        self.driver.implicitly_wait(3)
        self.driver.find_element_by_xpath(name_input).send_keys(self.name)
        self.driver.find_element_by_xpath(email_input).send_keys(self.email)
        self.driver.find_element_by_xpath(number_input).send_keys(Keys.BACKSPACE + Keys.BACKSPACE + self.phone_no)
        time.sleep(3)

    def add_tip(self):
        self.driver.find_element_by_xpath(
            '//*[@id="__next"]/div[1]/main/div/div/div[2]/div/div/div/div[3]/div[2]/div[2]/div[2]').click()

    def add_comment(self):
        self.driver.find_element_by_xpath('//*[@id="__next"]/div[1]/main/div/div/div[1]/div[4]/div[1]/div/svg').click()
        self.driver.find_element_by_xpath('//*textarea').send_key('Test Comment')

# if __name__ == '__main__':
#     mobileEmulation = {"deviceMetrics": {"width": WIDTH, "height": HEIGHT, "pixelRatio": PIXEL_RATIO},
#                        "userAgent": android_emulator}
#     options = Options()
#     options.add_experimental_option('mobileEmulation', mobileEmulation)
#
#     driver = webdriver.Chrome(options=options)
#     order = Orders(driver=driver, email=emails, max_amount=300, phone_no='918218233503', name='Harsh',
#                    order_type='Pickup', payment_type=cash, website='https://roma.fleksa.com/')
#     order.create_order_mobile_view()
#     driver.close()
