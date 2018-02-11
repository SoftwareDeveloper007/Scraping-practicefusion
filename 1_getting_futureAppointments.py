import time
import datetime

import config
import appto
import practice_fussion


def main():
    print ("--- Getting Future Appts From Practice Fussion and Pushing to Appto---")

    driver = None
    pf = practice_fussion.PracticeFussion(driver)
    pf.login(config.email, config.password)

    today_string = datetime.datetime.now().strftime("%m/%d/%Y")
    after_year_string = (datetime.datetime.now() + datetime.timedelta(days=365)).strftime("%m/%d/%Y")
    data = {'startDate':today_string, 'endDate': after_year_string}
    future_appts = pf.pull_appointments(data)

    print ('Future Appts:')
    print (future_appts)
    if len(future_appts) > 0:
        data = {'business_id': config.business_id, 'data': future_appts}
        try:
            r = appto.add_appointment(data)
            print (r)
        except:
            print ("APPTO ERROR in ")


if __name__ == "__main__":
    main()

