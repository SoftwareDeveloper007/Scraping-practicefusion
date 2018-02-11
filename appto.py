import re
import json
from datetime import datetime

import requests
requests.packages.urllib3.disable_warnings()

# url = "http://54.172.244.133/WEB-PRO/API/api/v1/GetApptPracticeFusion?business_id=1&appt_date=2017-11-20"
base_url = "http://54.172.244.133"

def get_appointment(query_data):
    getapp_url = "/WEB-PRO/API/api/v1/GetApptPracticeFusion"
    response = requests.get(base_url+getapp_url, params=query_data, verify=False)
    j_response = json.loads(response.text)

    return j_response


def update_patient(data):
    # updatept_url = '/vizzical_api/api/v1/UpdatePatientID'
    updatePt_url = '/WEB-PRO/API/api/v1/UpdatePatientID'
    data = json.dumps(data)
    r = requests.post(base_url+updatePt_url, data=data, verify=False)
    print (r.text)
    j_response = json.loads(r.text)

    return j_response



def add_appointment(data):
    data = json.dumps(data)
    addapp_url = "/WEB-PRO/API/api/v1/AddApptPracticeFusion"
    # addapp_url = "/vizzical_api/api/v1/AddApptPracticeFusion"

    r = requests.post(base_url+addapp_url, data=data, verify=False)
    # print (r.text)
    j_response = json.loads(r.text)

    return j_response

def get_securityCode(source_number, virtual_number):
    getcode_url = "/WEB-PRO/API/api/v1/GetPracticeFusion2FactorCode"
    data = {
        "source_number": source_number,
        "virtual_number": virtual_number
    }

    r = requests.post(base_url+getcode_url, data=data, verify=False)
    # print (r.text)
    j_response = json.loads(r.text)
    try:
        code = re.search("\d+", j_response.get('code')).group()
        return code
    except:
        return False

def getCancelledAppt(query_data):
    url = "/WEB-PRO/API/api/v1/getCancelledAppt"
    response = requests.get(base_url+url, params=query_data, verify=False)
    j_response = json.loads(response.text)
    # print (j_response)
    appts = []

    for item in j_response.get('cancelled_appt', []):
        appt= {}
        appt['name'] = item.get('name')
        try:
            appt['when'] = datetime.strptime(item.get('when'), '%m/%d/%Y %H:%M %p').strftime("%H:%M %p")
        except:
            pass

        try:
            appt['phoneNumber'] = item.get('phone_number')
        except:
            pass

        appts.append(appt)


    return appts


if __name__ == "__main__":
    query_data = {'business_id':1, 'appt_date':"2017-12-05"}
    add_data =  [
        {
          "STATUS": "Pending arrival",
          "DATE_TIME": "11/15/17 8:30 AM",
          "FACILITY": "Deepti Kalghatgi Practice",
          "SEEN_BY_PROVIDER": "Deepti Kalghatgi",
          "APPOINTMENT_TYPE": "Wellness Exam",
          "PATIENT_DOB": "george K 03/05/1970"
         },
        {
          "STATUS": "Pending arrival",
          "DATE_TIME": "11/15/17 8:30 AM",
          "FACILITY": "Deepti Kalghatgi Practice",
          "SEEN_BY_PROVIDER": "Deepti Kalghatgi",
          "APPOINTMENT_TYPE": "Wellness Exam",
          "PATIENT_DOB": "george K 03/05/1971"
        }
    ]


    futureAppts_data = [{'STATUS': u'Pending arrival', 'DATE_TIME': u'01/26/2018 10:06 AM', 'PATIENT_ID': u'kS431476', 'SEEN_BY_PROVIDER': u'Dr Kiran Kulkarni', 'FACILITY': '',
                         'APPOINTMENT_TYPE': '', 'PATIENT_DOB': 'jhon Doe 01/28/1975' }]
    data = {'business_id':1, 'data':futureAppts_data}
    print (add_appointment(data))

    # update_data = [
    #             {
    #               "CUSTOMER_PHONE": "17860000000",
    #               "PATIENT_ID": "737139139",
    #          "PATIENT_DOB": "george K 03/05/1970"
    #              },
    #             {
    #               "CUSTOMER_PHONE": "17861111111",
    #               "PATIENT_ID": "1411414144",
    #          "PATIENT_DOB": "michael K 02/05/1971"
    #      }
    # ]
    # data = {'business_id':1, 'data':update_data}
    # print (update_patient(data))

    # print (get_securityCode('837-401', 17327334704))
    # print(get_appointment(query_data))
    # print (data)
    # r = add_appointment(data)
    # print (r)
    # print (r.get('message'))

    # requests.get(url,verify=False)

    # print (getCancelledAppt(query_data))