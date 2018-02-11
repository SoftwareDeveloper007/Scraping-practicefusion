import sys
import time
from datetime import datetime, timedelta
import random
import pandas as pd

import practice_fussion
import config

def strTimeProp(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def randomDate(start, end, prop):
    return strTimeProp(start, end, '%m/%d/%Y %I:%M %p', prop)


def main():
    df = pd.read_csv(import_csv)
    print (df)

    driver = None
    pf = practice_fussion.PracticeFussion(driver)
    pf.login(config.email, config.password)

    pf.driver.find_element_by_xpath("//a[@data-tracking='Schedule']").click(); time.sleep(random.randint(3,5))
    pf.driver.find_element_by_xpath("//a[@data-tracking='Day']").click(); time.sleep(random.randint(3,5))

    # update_appts = []
    for index, row in df.iterrows():

        pf.driver.find_element_by_xpath("//button[contains(@class, 'add-appointment-button')]").click();time.sleep(random.randint(3,5))
        pf.driver.find_element_by_xpath("//input[@data-element='patient-search']").send_keys(row['First Name'] + ' ' + row['Middle Name'] + ' ' + row['Last Name']);time.sleep(random.randint(1,3))
        pf.driver.find_element_by_class_name('glyphicon-search').click(); time.sleep(random.randint(1,3))

        element = pf.driver.find_element_by_xpath("//div[contains(@class, 'scheduler-search-results')]//li")
        if "No Patients Found" in element.text:
            pf.driver.find_element_by_xpath("//h12[contains(text(), 'Add new patient')]").click(); time.sleep(random.randint(1,3))
            pf.driver.find_element_by_id('first-name').send_keys(row['First Name'])
            pf.driver.find_element_by_id('last-name').send_keys(row['Last Name'])
            pf.driver.find_element_by_id('middle-name').send_keys(row['Middle Name'])
            pf.driver.find_element_by_id('birth-date').send_keys(row['Date of Birth']); time.sleep(random.randint(1,3))
            pf.driver.find_element_by_xpath("//button[contains(text(), '%s')]" %config.sex[row['Gender']]).click(); time.sleep(random.randint(1,3))
            pf.driver.find_element_by_id('is-user-of-mobile-phone').click(); time.sleep(random.randint(1,3))
            pf.driver.find_element_by_xpath("//*[contains(text(), 'Add work phone')]").click()
            pf.driver.find_element_by_id('work-phone').send_keys(row['Work Phone']); time.sleep(random.randint(1,3))
            pf.driver.find_element_by_id('email-address').send_keys(row['EMAIL_ADDR']); time.sleep(random.randint(1,3))
            pf.driver.find_element_by_xpath("//button[@data-element='add-patient-btn']").click(); time.sleep(random.randint(1,3))

            # update_appt = config.update_appt_template
            # update_appt['PATIENT_ID'] = pf.driver.find_element_by_xpath("//span[contains(text(), 'PRN:')]/following-sibling::span").text.strip()
            # update_appt['CUSTOMER_PHONE'] = row['Work phone']
            # update_appt['PATIENT_DOB'] =


        else:
            element.click(); time.sleep(random.randint(1,3))

        pf.driver.find_element_by_xpath("//div[@data-element='appointment-type']").click(); time.sleep(random.randint(1,3))
        pf.driver.find_element_by_xpath("//ul[@class='ember-select-results']//a[contains(text(), '%s')]" %config.push_sample_data.get('appointment_type')).click(); time.sleep(random.randint(1,3))
        when_element = pf.driver.find_element_by_xpath("//input[@data-element='appointment-start']")
        when_element.clear()
        when_element.send_keys(randomDate(datetime.now().strftime('%m/%d/%Y %I:%M %p'), (datetime.now()+timedelta(days=30)).strftime('%m/%d/%Y %I:%M %p'), random.random())); time.sleep(random.randint(1,3))
        pf.driver.find_element_by_xpath("//button[contains(@class, 'save-button')]").click(); time.sleep(random.randint(5,7))


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print ("No input csv file")
    else:
        import_csv = sys.argv[1]
        # import_csv = "ImportTemplate_appto.csv"
        main()