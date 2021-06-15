from logging import currentframe
import sessionanalyticsv2 as src
import requests
headers = {'Authorization': 'Bearer ', 'Content-Type': 'application/json'}

def test_session():
    resp = src.getPlayerSession(986440844)
    # print(str(result))
    current_server_id = str(resp['server'])
    print("Current Server ID: " + current_server_id)
    server_name_response = requests.get("https://api.battlemetrics.com/servers/" + current_server_id, headers=headers)
    server_name_json = server_name_response.json()
    server_name = server_name_json['data']['attributes']['name']
    print("Found Server Name: " + str(server_name))
    #print(str(server_name_json))

    return server_name

test_session()



