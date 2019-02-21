import requests
import time
import json
import random
import pandas as pd

# Authentication token
api_auth = 'your-api-goes_here'
# counter
counter = 0
# Power BI Real Time API
# Replace by your own
REST_API_URL = 'https://api.powerbi.com/beta/6494460e-8600-4edc-850f-528e8faad290/datasets/288527d3-eb81-4f17-9df1-dd7270163b86/rows?key=jOtLG%2FGwRo6xcu%2B%2FkyFVn4rU9Z0fbTlNq0CQp2%2FNGB5UtLiG54TJQRauUY26chuRRpOF9d1cJTXwDlmL2MA3Rw%3D%3D'
# next departures from Montparnasse
request_url = 'https://api.sncf.com/v1/coverage/sncf/stop_areas/stop_area:OCE:SA:87391003/departures?' \
              'datetime=20180912T103450'
# endless loop to call the api every 5 seconds

def data_generation(counter=None):
    # call the SNCF Open API
    # auth = ('username', 'password')
    request_result = requests.get(request_url, auth=(api_auth, ''))
    # json output : context
    context = request_result.json()['context']
    # context sub-node: current date time
    cur_date = context['current_datetime']
    # json_output : departures
    departures = request_result.json()['departures']
    departure = departures[0]['display_informations']['direction']
    # headsign of the fisrt train
    headsign = int(departures[0]['display_informations']['headsign'])
    return [headsign, counter, departure]
while True:
    data_raw = []
    # simple counter increment
    counter += 1
    for i in range(1):
        row = data_generation(counter)
        data_raw.append(row)
    # set the header record
    HEADER = ["headsign", "counter", "departure"]
    # generate a temp data frame to convert it to json
    data_df = pd.DataFrame(data_raw, columns=HEADER)
    # prepare date for post request (to be sent to Power BI)
    data_json = bytes(data_df.to_json(orient='records'), encoding='utf-8')
    # Post the data on the Power BI API
    req = requests.post(REST_API_URL, data_json)
    print("Data posted in Power BI API")
    print(data_json)
    # wait 5 seconds
    time.sleep(4)
