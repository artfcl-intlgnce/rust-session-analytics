import flask
from flask import request, jsonify
import requests
import json

headers = {'Authorization': 'Bearer ', 'Content-Type': 'application/json'}

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])    
def home():
    return '''<h1>Paranoid.gg Alt Bot</h1>
<p>A prototype API for checking Player Match Identifiers.</p>'''

@app.route('/api/v1/resources/alts', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'steamid' in request.args:
        steamid = str(request.args['steamid'])
        
        
        
        #get players IP

        # first lookup BM ID from Steam ID using player match
        body = {
            "data": [
                {
                    "type": "identifier",
                    "attributes": {
                        "type": "steamID",
                        "identifier": steamid
                    }
                }
            ]
        }
        response = requests.post(url="https://api.battlemetrics.com/players/match", headers=headers, data=json.dumps(body))
        responsejson = response.json()
        responsedata = responsejson['data']
        #bm_player_id = responsedata[]
        result = str(responsejson)
        playerips = []
        #result = 'test'
        return jsonify(responsejson)

    elif 'ip' in request.args:
        ip = str(request.args['ip'])
        body = {
            "data": [
                {
                    "type": "identifier",
                    "attributes": {
                        "type": "ip",
                        "identifier": ip
                    }
                }
            ]
        }
        response = requests.post(
        url="https://api.battlemetrics.com/players/match", headers=headers, data=json.dumps(body))
        result = response['data']
        
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    '''for alt in alts:
        if book['id'] == id:
            results.append(alt)'''

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(result)

app.run()