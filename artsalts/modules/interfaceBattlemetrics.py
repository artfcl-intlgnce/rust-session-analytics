# Battlemetrics Interface

import logging
import configparser
import os
import requests
import datetime

# Set Logging Level
logging.basicConfig(level=logging.DEBUG)



# BM API Configuration (Keys)
path = os.chdir(os.path.dirname(os.path.abspath(__file__)))
f = open("Config/keys.ini", "r")
config = configparser.ConfigParser()
config.read('Config/keys.ini')
BM_API_KEY = config['battlemetrics']['apikey']
f.close

# Battlemetrics API Token goes here. This sets the headers for the http request
headers = {'Authorization': 'Bearer ' + str(BM_API_KEY), 'Content-Type': 'application/json'}

############################################################################
#                               bmQuery Class                              #
############################################################################

class bmQuery:
    def __init__(self):
        logging.debug("Created bmQuery class object")
        pass

    ### GETTERS AND SETTERS ###

    def getQuery(self, query):
        self.query = query
        pass

    def postQuery(self):
        pass

    #####################################################################################
    # getPlayerlist() Function                                                          #
    # This function calls Battlemtrics API to retrieve playerlist for a given server.   #
    # Includes pagination and error handling*                                           #
    # Inputs: Battlemetrics Server ID                                                   #
    # Returns: Array of Battlemetrics Player ID's                                       #
    #####################################################################################

    def getPlayerlist(bm_server_id):

        logging.debug("Hit getPlayerlist()") 
        temp = [] # used to store return results of function

        # Call Battlemetrics API and format/parse. Returns array of BM Player ID's (NOT Steam ID's)
        response = requests.get("https://api.battlemetrics.com/servers/" + str(bm_server_id) + "?include=player", headers=headers)
        print(headers)
        responsejson = response.json()
        data = responsejson['included']

        # Loop through BM Response, Extract ID of player and append to result
        for row in data:
            temp.append(row)

        # Wrap Up and Return Result of getPlayerList()
        logging.debug("Retrieved Player List \n" + str(temp))
        return temp

    #####################################################################################
    # getPlayerSession() Function                                                       #
    # This function pulls a specific player's info, including name, current server, etc #
    # Inputs: Player Battlemetrics ID                                                   #
    # Returns: Player Object                                                            #
    #####################################################################################

    def getPlayerSession(bm_player_id):
        result = {}

        # Prepare time filter for BM API
        bmtime = datetime.datetime.now().replace(microsecond=0).isoformat()
        bmtime = str(bmtime) + "Z"

        # Call Battlemetrics Session API to get active session (BM Server ID)
        player_session = requests.get("https://api.battlemetrics.com/sessions?filter[players]=" + str(bm_player_id) + "&filter[at]=" + str(bmtime), headers=headers).json()
        try:
            result['server'] = player_session['data'][0]['relationships']['server']['data']['id']

            # Call Battlemetrics Server API to get the server name
            server_name_response = requests.get("https://api.battlemetrics.com/servers/" + result['server'], headers=headers)
            server_name_json = server_name_response.json()
            server_name = server_name_json['data']['attributes']['name']
            print("Found Server Name: " + str(server_name))
            #print(str(server_name_json))

        except:
            # THIS IS WHERE TO PUT THE SCHEDULED TIMER EVENT
            logging.warn("No player session found")
            pass

        return result

    #####################################################################################
    # getPlayerID() Function                                                            #
    # This function gets steam ID and IP's based on player BM ID                        #
    # Inputs: Battlemetrics Player ID                                                   #
    # Returns: Array of Identifier Objects {'steamid':"string",'ip':"string"}           #
    #####################################################################################

    def getPlayerIP(bmid):
        response = requests.get("https://api.battlemetrics.com/players/" + str(986440844) + "?include=identifier", headers=headers)
        print(response.json()['included']) 

        resp_arr = []
        resp_obj = {}
        for id in response.json()['included']:
            if id['attributes']['type'] == "ip":
                resp_obj['steamid'] = id['attributes']['identifier']
                resp_arr.append(resp_obj)
                print(id['attributes']['identifier'])
            elif id['attributes']['type'] == "steamID":
                resp_obj['steamid'] = id['attributes']['identifier']
                resp_arr.append(resp_obj)
                print(id['attributes']['identifier'])
            else:
                pass
        print(str(resp_arr))
        return str(resp_arr)
