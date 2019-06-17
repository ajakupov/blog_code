# a pandas dataframe containing a text colummn
items_df = pd.DataFrame()
web_input = []
for item in items_df['Text Column']:
    web_input.append([item])

data = {

    "Inputs": {

        "input1":
        {
            "ColumnNames": ["UserRequest"],
            "Values": web_input
        }, },
    "GlobalParameters": {
    }
}

body = str.encode(json.dumps(data))

url = 'https://europewest.services.azureml.net/workspaces/workspace-id/services/service-id/execute?api-version=2.0&details=true'
api_key = 'your-api-key'
headers = {'Content-Type': 'application/json',
            'Authorization': ('Bearer ' + api_key)}

req = urllib.request.Request(url, body, headers)
output = []
try:
    response = urllib.request.urlopen(req)

    result = json.loads(response.read())
    responses = result['Results']['output1']['value']['Values']
    for response in responses:
        output += response
except:
    pass
