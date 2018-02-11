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

def save_source(driver):
    import codecs
    with codecs.open("source.html", "w", "utf-8") as f:
        f.write(driver.page_source)

class PracticeFussion():
    def __init__(self, driver=None):
        if driver is not None:
            self.driver = driver
        else:
            options = Options()
            options.add_argument("--start-maximized")
            options.add_argument("user-data-dir=C:\data")
            if os.name == 'nt':
                self.driver = webdriver.Chrome(executable_path=os.path.join('driver', 'chromedriver.exe'), chrome_options=options)
                # self.driver = webdriver.Firefox(executable_path=os.path.join('driver', 'geckodriver.exe'))
            elif os.name == 'posix':
                self.driver = webdriver.Firefox(executable_path=os.path.join('driver', 'geckodriver'))

            self.driver.implicitly_wait(10)
            # self.driver.maximize_window()
            self.driver.set_page_load_timeout(600)

            self.driver.get("https://www.practicefusion.com/")
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

    def push_appointment(self, data_list):
        self.driver.find_element_by_xpath("//a[@data-tracking='Schedule']").click(); time.sleep(random.randint(3,5))
        self.driver.find_element_by_xpath("//a[@data-tracking='Day']").click(); time.sleep(random.randint(3,5))
        update_appts = []
        for data_item in data_list:
            self.driver.find_element_by_xpath("//button[contains(@class, 'add-appointment-button')]").click();time.sleep(random.randint(3,5))
            self.driver.find_element_by_xpath("//input[@data-element='patient-search']").send_keys(data_item.get('name'));time.sleep(random.randint(1,3))
            self.driver.find_element_by_class_name('glyphicon-search').click(); time.sleep(random.randint(1,3))

            element = self.driver.find_element_by_xpath("//div[contains(@class, 'scheduler-search-results')]//li")
            if "No Patients Found" in element.text:
                update_appt = config.update_appt_template
                self.driver.find_element_by_xpath("//h12[contains(text(), 'Add new patient')]").click(); time.sleep(random.randint(1,3))
                self.driver.find_element_by_id('first-name').send_keys(data_item.get('name').split()[0])
                self.driver.find_element_by_id('last-name').send_keys(data_item.get('name').split()[-1])
                if data_item.get('DOB'):
                    self.driver.find_element_by_id('birth-date').send_keys(data_item.get('DOB')); time.sleep(random.randint(1,3))
                else:
                    self.driver.find_element_by_id('birth-date').send_keys(config.push_sample_data.get('DOB')); time.sleep(random.randint(1,3))
                if data_item.get('sex'):
                    self.driver.find_element_by_xpath("//button[contains(text(), '%s')]" %data_item.get('sex')).click(); time.sleep(random.randint(1,3))
                else:
                    self.driver.find_element_by_xpath("//button[contains(text(), '%s')]" %config.push_sample_data.get('sex')).click(); time.sleep(random.randint(1,3))
                if data_item.get('phone_number'):
                    self.driver.find_element_by_id('mobile-phone').send_keys(data_item.get('phone_number')[:10]); time.sleep(random.randint(1,3))
                else:
                    self.driver.find_element_by_id('mobile-phone').send_keys(config.push_sample_data.get('phone_number')); time.sleep(random.randint(1,3))
                if data_item.get('email'):
                    self.driver.find_element_by_id('email-address').send_keys(data_item.get('email')); time.sleep(random.randint(1,3))
                else:
                    self.driver.find_element_by_id('email-address').send_keys(config.push_sample_data.get('email')); time.sleep(random.randint(1,3))
                self.driver.find_element_by_xpath("//button[@data-element='add-patient-btn']").click(); time.sleep(random.randint(1,3))
                print ('STEP 1')
                update_appt['CUSTOMER_PHONE'] = data_item.get('phone_number')                
                print ('STEP 1a')
                update_appt['PATIENT_DOB'] = data_item.get('DOB')
                print ('STEP 1b')
                update_appt['PATIENT_ID'] = self.driver.find_element_by_xpath("//span[contains(text(), 'PRN')]/following-sibling::span").text.strip()
                print ('STEP 1c')

                print ('STEP 2')
                update_appts.append(update_appt)
                print ('STEP 3')
            else:
                element.click(); time.sleep(random.randint(1,3))
                print ('STEP 4')

            self.driver.find_element_by_xpath("//div[@data-element='appointment-type']").click(); time.sleep(random.randint(1,3))
            if data_item.get('appointment_type'):
                self.driver.find_element_by_xpath("//ul[@class='ember-select-results']//a[contains(text(), '%s')]" %data_item.get('appointment_type')).click(); time.sleep(random.randint(1,3))
            else:
                self.driver.find_element_by_xpath("//ul[@class='ember-select-results']//a[contains(text(), '%s')]" %config.push_sample_data.get('appointment_type')).click(); time.sleep(random.randint(1,3))
            when_element = self.driver.find_element_by_xpath("//input[@data-element='appointment-start']")
            when_element.clear()
            when_element.send_keys(data_item.get('when')); time.sleep(random.randint(1,3))
            self.driver.find_element_by_xpath("//button[contains(@class, 'save-button')]").click(); time.sleep(random.randint(5,7))

        return update_appts

    def pull_appointments(self, data):
        self.driver.find_element_by_xpath("//a[@data-tracking='Reports']").click(); time.sleep(random.randint(3,5))
        self.driver.find_element_by_xpath("//a[contains(@href, 'appointmentsreport')]").click();time.sleep(random.randint(3,5))
        startDate_element = self.driver.find_element_by_xpath("//input[@data-element='start-date']")
        startDate_element.clear()
        startDate_element.send_keys(data['startDate'])
        endDate_element = self.driver.find_element_by_xpath("//input[@data-element='end-date']")
        endDate_element.clear()
        endDate_element.send_keys(data['endDate'])
        self.driver.find_element_by_xpath("//button[contains(text(), 'Run report')]").click(); time.sleep(random.randint(3,5))

        appointments = []
        rows = self.driver.find_elements_by_xpath("//tr[@class='ember-view']")
        for row in rows:
            appointment = {}
            columns = row.find_elements_by_xpath(".//td")
            appointment['DATE_TIME'] = columns[0].text.replace("\n", ' ')
            appointment['PATIENT_DOB'] = columns[1].text
            appointment['STATUS'] = columns[2].text
            appointment['APPOINTMENT_TYPE'] = columns[3].text
            appointment['SEEN_BY_PROVIDER'] = columns[4].text
            appointment['FACILITY'] = columns[5].text

            appointments.append(appointment)

        self.driver.find_element_by_xpath("//a[@data-tracking='Charts']").click(); time.sleep(random.randint(3,5))
        for appointment in appointments:
            # self.driver.find_element_by_xpath("//*[@class='ember-select-search-field is-shorter']/input").send_keys(Keys.RETURN)
            # self.driver.find_element_by_xpath("//*[@class='ember-select-search-field is-shorter']/input").send_keys(Keys.RETURN)
            existing_search_links = self.driver.find_elements_by_class_name('ember-select-search-choice-close')
            for link in existing_search_links:
                link.click()

            self.driver.find_element_by_xpath("//*[@class='ember-select-search-field is-shorter']/input").send_keys(appointment['PATIENT_DOB'].split("\n")[0]+Keys.ENTER); time.sleep(3)
            self.driver.find_element_by_xpath("//*[@class='ember-select-search-field is-shorter']/input").send_keys(appointment['PATIENT_DOB'].split("\n")[1]+Keys.ENTER); time.sleep(3)
            appointment['PATIENT_ID'] = self.driver.find_element_by_xpath("//span[contains(text(), 'PRN')]/following-sibling::span").text.strip()
            appointment['PATIENT_DOB'] = appointment['PATIENT_DOB'].replace("\n", ' ')

        return appointments

    def cancel_appts(self, appts):
        self.driver.find_element_by_xpath("//a[@data-tracking='Schedule']").click(); time.sleep(random.randint(3,5))
        self.driver.find_element_by_xpath("//a[@data-tracking='Appointments']").click(); time.sleep(random.randint(3,5))
        # self.driver.find_element_by_xpath("//button[@data-element='btn-filter-options']").click(); time.sleep(10)
        # self.driver.find_element_by_xpath("//button[@data-element='users-toggle']").click(); time.sleep(random.randint(3,5))
        # self.driver.find_element_by_xpath("//button[@data-element='chk-all-users']").click(); time.sleep(random.randint(3,5))

        if len(appts) > 0:
            elements = self.driver.find_elements_by_xpath("//div[@class='detail-inner']/div")
            for element in elements:
                try:
                    status = element.find_element_by_class_name('display-name').text
                except:
                    continue
                patient_info = element.find_element_by_class_name('patient-column').text
                when = element.find_element_by_class_name('time-column').text.strip()

                if 'Cancelled' in status:
                    continue

                info = {}
                info['name'] = patient_info.split("\n")[0].split()[0]
                try:
                    info['phoneNumber'] = patient_info.split("\n")[-1].replace("M.", "").strip()
                except:
                    pass
                info['when'] = when

                print (status)
                print (info)

                if info in appts:
                    print ('CANCELLING')
                    element.find_element_by_class_name('status-column').click(); time.sleep(random.randint(3,5))
                    element.find_element_by_xpath(".//span[text()='Cancelled']/..").click(); time.sleep(random.randint(3,5))
                    self.driver.find_element_by_xpath("//button[text()='Done']").click(); time.sleep(random.randint(3, 5))

        else:
            print ("There is no appts to be cancelled at this time.")

        return

    def get_futureAppts(self):
        self.driver.find_element_by_xpath("//a[@data-tracking='Schedule']").click(); time.sleep(random.randint(3,5))
        self.driver.find_element_by_xpath("//a[@data-tracking='Appointments']").click(); time.sleep(random.randint(3,5))

        today = datetime.datetime.now()
        i = 0
        future_appointments = []
        while i < 365:
            elements = self.driver.find_elements_by_xpath("//div[@class='detail-inner']/div")
            for element in elements:
                try:
                    status = element.find_element_by_class_name('display-name').text
                except:
                    continue
                patient_info = element.find_element_by_class_name('patient-column').text.strip()
                when = element.find_element_by_class_name('time-column').text.strip()

                if 'Cancelled' in status:
                    continue

                info = config.appto_data_template
                info['STATUS'] = status

                # info['FULL_NAME'] = patient_info.split("\n")[0].split()[0]
                # try:
                #     info['CUSTOMER_PHONE'] = patient_info.split("\n")[-1].replace("M.", "").strip()
                # except:
                #     pass

                day = (today + datetime.timedelta(days=i)).strftime("%m/%d/%Y")
                info['DATE_TIME'] = day + " " + when
                info['SEEN_BY_PROVIDER'] = element.find_element_by_class_name('provider-column').text.strip()

                element.find_element_by_xpath("//div[@class='lead']/a"). click(); time.sleep(5)
                info['PATIENT_ID'] = self.driver.find_element_by_xpath("//span[contains(text(), 'PRN:')]/following-sibling::span").text.strip()
                info['PATIENT_DOB'] = self.driver.find_element_by_xpath("//span[contains(text(), 'DOB:')]/following-sibling::span").text.strip()
                # info['PATIENT_DOB'] =

                self.driver.execute_script("window.history.go(-1)"); time.sleep(5)


                print (status)
                print (info)

                future_appointments.append(info)

            self.driver.find_element_by_xpath("//*[contains(@class, 'increment-date')]").click()
            time.sleep(1)
            i += 1

        return future_appointments, self.driver




if __name__ == "__main__":

    driver = None
    praticefussion = PracticeFussion()
    praticefussion.login(config.email, config.password)

