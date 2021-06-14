import requests
import json

headers = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbiI6IjgyOTljNGYzYjBlZjM3ZmYiLCJpYXQiOjE2MjA0NTEwNjYsIm5iZiI6MTYyMDQ1MTA2NiwiaXNzIjoiaHR0cHM6Ly93d3cuYmF0dGxlbWV0cmljcy5jb20iLCJzdWIiOiJ1cm46dXNlcjo0MDQ3MTMifQ.lCNPar3Y6MrvaxEzmfJgw4UVc3bFhM5JdKWniezkIcs', 'Content-Type': 'application/json'}
response = requests.get("https://api.battlemetrics.com/players/" + str(986440844) + "?include=identifier", headers=headers)
print(response.json()['included']) 

for id in response.json()['included']:
    if id['attributes']['type'] == "ip":
        print(id['attributes']['identifier'])
    elif id['attributes']['type'] == "steamID":
        print(id['attributes']['identifier'])
    else:
        pass


