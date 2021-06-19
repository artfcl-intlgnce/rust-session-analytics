import requests
import json
headers = {'Authorization':'Bearer ', 'Content-Type':'application/json'}
response = requests.get("https://api.battlemetrics.com/players?filter[servers]='2387727'&fields[identifier]=type,identifier&filter[public]=false&include=identifier", headers=headers)

print(json.dumps(response.json()))