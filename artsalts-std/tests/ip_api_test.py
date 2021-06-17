import requests
import json

headers = {'Authorization': 'Bearer ', 'Content-Type': 'application/json'}
response = requests.get("https://api.battlemetrics.com/players/" + str(986440844) + "?include=identifier", headers=headers)
print(response.json()['included']) 

for id in response.json()['included']:
    if id['attributes']['type'] == "ip":
        print(id['attributes']['identifier'])
    elif id['attributes']['type'] == "steamID":
        print(id['attributes']['identifier'])
    else:
        pass


