import os
import time
import json
import pickle
from datetime import datetime, timedelta

import config
import appto
import practice_fussion

def check_newAppts(today, appts):
    if os.path.exists(today+'.txt'):
        with open(today+'.txt') as f:
            old_apptIds = [id.strip() for id in f.readlines()]
            # print (old_apptIds)
        with open(today+'.txt', 'a') as f:
            for id in [appt.get('appointment_id') for appt in appts if not appt.get('appointment_id') in old_apptIds]:
                f.write(id)
                f.write("\n")

        return [appt for appt in appts if not appt.get('appointment_id') in old_apptIds]

    else:
        try:
            yesterday = (datetime.strptime(today, '%Y-%m-%d') - timedelta(days=1)).strftime("%Y-%m-%d")
            os.remove(yesterday+'.txt')
        except:
            pass

        with open(today+'.txt', 'w') as f:
            for id in [item.get('appointment_id') for item in appts]:
                f.write(id)
                f.write("\n")

        return appts


def main():
    print ("\n --- Getting from Appto and pushing to Practice Fussion ---")

    driver = None
    pf = practice_fussion.PracticeFussion(driver)
    pf.login(config.email, config.password)

    today1 =  datetime.now().strftime("%Y-%m-%d")
    today1 = '2018-01-30';

    try:
        appts = appto.get_appointment({'business_id':config.business_id, 'appt_date':today1})
        print ("Appts from Appto: ", appts)
        appts = check_newAppts(today1, appts)
        print (json.dumps(appts, indent=2))
        print ("NEW Attps from Appto: ")
        print (json.dumps(appts, indent=2))
        if len(appts) > 0:
            update_appts = pf.push_appointment(appts)
            print('push completed')
            data = {'business_id':config.business_id, 'data':update_appts}
            print (json.dumps(data, indent=2))
            print ('UPDATE DATA: \n', update_appts)
            # time.sleep(10)
            appto.update_patient(data)
    except:
        print ("APPTO ERROR in getting appointements")


if __name__ == "__main__":
    main()