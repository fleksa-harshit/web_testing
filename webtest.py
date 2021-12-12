import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from constant import *
from order_creation import Orders, emails


class WebsiteTest(unittest.TestCase):
    def test_(self):
        # mobileEmulation = {"deviceMetrics": {"width": WIDTH, "height": HEIGHT, "pixelRatio": PIXEL_RATIO},
        #                    "userAgent": android_emulator}
        options = Options()
        # options.add_experimental_option('mobileEmulation', mobileEmulation)

        driver = webdriver.Chrome()
        order = Orders(driver=driver, email=emails, max_amount=300, phone_no='918218233503', name='Harsh',
                       order_type='Pickup', payment_type=cash, website='https://goodtaste.fleksa.de/')
        self.assertEqual(order.create_order_not_login(), True)


if __name__ == '__main__':
    unittest.main()
