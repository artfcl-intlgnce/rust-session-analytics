from logging import currentframe
import sessionanalyticsv2 as src
import requests
headers = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbiI6IjgyOTljNGYzYjBlZjM3ZmYiLCJpYXQiOjE2MjA0NTEwNjYsIm5iZiI6MTYyMDQ1MTA2NiwiaXNzIjoiaHR0cHM6Ly93d3cuYmF0dGxlbWV0cmljcy5jb20iLCJzdWIiOiJ1cm46dXNlcjo0MDQ3MTMifQ.lCNPar3Y6MrvaxEzmfJgw4UVc3bFhM5JdKWniezkIcs', 'Content-Type': 'application/json'}

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



