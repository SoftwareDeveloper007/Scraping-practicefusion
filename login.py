import os

import re

import time

import logging

import pickle

import random

import datetime



from selenium import webdriver

from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.remote.remote_connection import LOGGER

LOGGER.setLevel(logging.WARNING)



import config

import appto



class PracticeFussion():

    def __init__(self, driver=None):

        if driver is not None:

            self.driver = driver

        else:

            options = Options()

            options.add_argument("--start-maximized")

            options.add_argument("user-data-dir=C:\data");

            if os.name == 'nt':

                self.driver = webdriver.Chrome(executable_path=os.path.join('driver', 'chromedriver.exe'), chrome_options=options)

                # self.driver = webdriver.Firefox(executable_path=os.path.join('driver', 'geckodriver.exe'))

            elif os.name == 'posix':

                self.driver = webdriver.Firefox(executable_path=os.path.join('driver', 'geckodriver'))



            self.driver.implicitly_wait(10)

            # self.driver.maximize_window()

            self.driver.set_page_load_timeout(600)



            self.driver.get("https://www.practicefusion.com/")

            # self.driver.get("https://static.practicefusion.com/apps/ehr/")

            time.sleep(5)



    def login(self, email, password):



        self.driver.get("https://static.practicefusion.com/apps/ehr/")



        self.driver.find_element_by_id('inputUsername').clear()

        self.driver.find_element_by_id('inputUsername').send_keys(email)

        self.driver.find_element_by_id('inputPswd').send_keys(password)

        self.driver.find_element_by_id('loginButton').click()

        time.sleep(5)



        if 'Security check' in self.driver.page_source:

            self.driver.find_element_by_id('sendCallButton').click(); time.sleep(10)

            # security_code = input("Input security code: ")

            security_code = appto.get_securityCode(config.source_number, config.virtual_number)

            self.driver.find_element_by_id('code').send_keys(security_code)

            self.driver.find_element_by_id('sendCodeButton').click()

            time.sleep(5)



        element = self.driver.find_element_by_xpath("//div[contains(@class, 'modal-close-button')]")

        self.driver.execute_script("arguments[0].click();", element)

        time.sleep(5)





        time.sleep(random.randint(3,5))





if __name__ == "__main__":

    driver = None

    praticefussion = PracticeFussion()

    praticefussion.login(config.email, config.password)



