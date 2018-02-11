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

def check_newPFappts(appts, today):
    pickle_file = today+".pkl"
    if os.path.exists(pickle_file):
        old_appts = pickle.load(open(pickle_file, "rb"))
        new_appts = [appt for appt in appts if not appt in old_appts]
        appts = old_appts + new_appts
        pickle.dump(appts , open(pickle_file,"wb"))

        return new_appts

    else:
        try:
            yesterday = (datetime.strptime(today, '%Y-%m-%d') - timedelta(days=1)).strftime("%Y-%m-%d")
            os.remove(yesterday+'.pkl')
        except:
            pass

        pickle.dump(appts , open(pickle_file,"wb"))

        return appts

def main():
    print (datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print ("----------------------------------------")

    driver = None
    while True:
        print ("\n0. --- Login ---")
        pf = practice_fussion.PracticeFussion(driver)
        pf.login(config.email, config.password)
        today1 =  datetime.now().strftime("%Y-%m-%d")

        print ("\n1. --- Getting from Appto and pushing to Practice Fussion ---")
        try:
            appts = appto.get_appointment({'business_id':config.business_id, 'appt_date':today1})
            print ("Appts from Appto: ", appts)
            appts = check_newAppts(today1, appts)
            print (json.dumps(appts, indent=2))
            print ("NEW Attps from Appto: ")
            print (json.dumps(appts, indent=2))
            if len(appts) > 0:
                pf.push_appointment(appts)
                time.sleep(10)
        except:
            print ("APPTO ERROR in getting appointements")

        print ("\n2. --- pulling from pratice fussion and adding to Appto ---")
        today2 = datetime.now().strftime("%m/%d/%Y")
        data = {'startDate':today2, 'endDate': today2}
        appts = pf.pull_appointments(data)
        print ("Appts From Pratice Fussion: ")
        print (json.dumps(appts, indent=2))
        appts = check_newPFappts(appts, today1)
        print ("NEW Appts From Pratice Fussion: ")
        print (json.dumps(appts, indent=2))
        if len(appts) > 0:
            data = {'business_id': config.business_id, 'data': appts}
            try:
                r = appto.add_appointment(data)
                print (r)
            except:
                print ("APPTO ERROR in ")

        print ("\n3. --- Cancelling appts ---")
        cancelled_appts = appto.getCancelledAppt({'business_id':config.business_id, 'appt_date':today1})
        # cancelled_appts = [{'when': u'9:00 AM', 'phoneNumber': u'(555) 555-5555', 'name': u'Steve'}]
        print ('Cancelling_appts from Appto:')
        print (json.dumps(cancelled_appts, indent=2))
        pf.cancel_appts(cancelled_appts)

        print ("\n4. --- Pushing Future Appts ---")
        future_appts, driver = pf.get_futureAppts()
        print ('Future Appts:')
        print (future_appts)
        if len(future_appts) > 0:
            data = {'business_id': config.business_id, 'data': appts}
            try:
                r = appto.add_appointment(data)
                print (r)
            except:
                print ("APPTO ERROR in ")

        time.sleep(3600*config.interval_hours)


    print ("--------------------------------------------")
    print ('\n\n')


if __name__ == "__main__":
    main()