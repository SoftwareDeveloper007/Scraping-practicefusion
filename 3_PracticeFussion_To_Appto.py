import os
import time
import json
import pickle
from datetime import datetime, timedelta

import config
import appto
import practice_fussion

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
    print ("\n. --- pulling from pratice fussion and adding to Appto ---")
    driver = None
    pf = practice_fussion.PracticeFussion(driver)
    pf.login(config.email, config.password)
    today1 =  datetime.now().strftime("%Y-%m-%d")
    today2 = datetime.now().strftime("%m/%d/%Y")
    data = {'startDate':'01/01/2018', 'endDate': today2}
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

if __name__ == "__main__":
    main()