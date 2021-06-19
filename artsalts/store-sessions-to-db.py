#!/usr/bin/env python3

   ##################################################################### 
 ##               Battlemetrics Player Session Analytics                ##
#                      Code Author: Artfcl_Intlgnce                       #  
 ##                       License: GNU GPLv3                            ##    
   ###################################################################### 

############################################################################
#                           Import Packages                                #
############################################################################

import requests
import time
import datetime
import schedule
import logging
from dotenv import load_dotenv
from redis import Redis
from rq import Queue
import configparser
import os
import Classes.Cache as c

c = Cache()
c.setCache("test")


############################################################################
#                           Configure Logger                               #
############################################################################

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    # Change level to INFO or ERROR to change terminal output (reduces storage stress)
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
logging.info("Logger Initialized")

############################################################################
#                Initialize Global Variables / Caches                      #
############################################################################

logging.info("Initializing Variables and Caches")

# player_cache is the main baseline (or the "old" baseline)
global player_cache
player_cache = []

class State(object):
    def __init__(self):
        self.player_cache = player_cache

s = State()

# player_cache_temp is the new/latest player cache pulled from BM. 
# This eventually becomes the player_cache after player_deltas have been determined and queued. 
player_cache_temp = []


# BM_API_KEY = config.bmconfig()['apikey']
path = os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(path)
f = open("keys.ini", "r")
config = configparser.ConfigParser()
config.read('keys.ini')
BM_API_KEY = config['battlemetrics']['apikey']
#print(BM_API_KEY)

f.close
# Battlemetrics API Token goes here. This sets the headers for the http request
headers = {'Authorization': 'Bearer ' + str(BM_API_KEY), 'Content-Type': 'application/json'}

############################################################################
#                           Define Core Functions                          #
############################################################################


#####################################################################################
# getPlayerlist() Function                                                          #
# This function calls Battlemtrics API to retrieve playerlist for a given server.   #
# Includes pagination and error handling*                                           #
# Inputs: Battlemetrics Server ID                                                   #
# Returns: Array of Battlemetrics Player ID's                                       #
#####################################################################################

def getPlayerlist(serverid):

    logging.debug("Hit getPlayerlist()") 
    temp = [] # used to store return results of function

    # Call Battlemetrics API and format/parse. Returns array of BM Player ID's (NOT Steam ID's)
    #response = requests.get("https://api.battlemetrics.com/players?page[size]=100&fields[identifier]=type,identifier&filter[servers]='" + str(serverid) + "'", headers=headers)
    response = requests.get("https://api.battlemetrics.com/servers/" + str(serverid) + "?include=player", headers=headers)
    #print(headers)
    responsejson = response.json()
    #print(responsejson)
    data = responsejson['included']

    # Loop through BM Response, Extract ID of player and append to result
    for row in data:
        temp.append(row)

    # Wrap Up and Return Result of getPlayerList()
    #print("Retrieved Player List" + str(temp))
    logging.debug("Retrieved Player List \n" + str(temp))
    return temp

def getPlayerJoins(player_cache, player_cache_temp):
    print("Size of Player Cache: " + str(len(player_cache)))
    print("Size of Player Cache Temp: " + str(len(player_cache_temp)))

    #logging.debug("getPlayerJoins() \n player_cache: " + str(player_cache) + "\n\n Player cache Temp " + str(player_cache_temp) )
    temp = []
    for player in player_cache_temp:
        if player not in player_cache:
            temp.append(player)
            #print(str(player) + " JOINED SERVER - TAKE ACTION!")
            logging.info(str(player['attributes']['name']) + " JOINED SERVER - TAKE ACTION")
    player_cache = player_cache_temp
    logging.debug("Results of getPlayerJoins():" +  str(temp))
    return temp

#####################################################################################
# flow() Function                                                                   #
# This function runs every N minutes/seconds. It takes historical cache of players, #
# finds the new players, and queues events for the players that left                #
# Inputs: None (Scheduled)                                                          #
# Returns: True                                                                     #
#####################################################################################

# Main sequence being scheduled
def flow():
    logging.info("Hit flow()")
    # Get refreshed player list
    player_cache_temp = getPlayerlist(2387727)
    # player_cache = pcache
    
    #global player_cache
    changes = []
    for player in player_cache_temp:
        if player['id'] not in player_cache:
            logging.info("Taking action for player " + str(player['id']))
            changes.append(player)


        #pass

        #playerinfo_temp = getPlayerSession(str(change)) ### KEY LINE OF CODE FOR SESSION ANALYTICS
        #logging.debug("SESSION FOUND: " + str(playerinfo_temp))
    #changes=[]

    # Sets / overrides latest player list into player cache    
    player_cache = player_cache_temp
    player_cache_temp = []   #clear temp cache
    #logging.debug("PLAYER JOINS: " + str(changes))
    return changes

#####################################################################################
# getPlayerSession() Function                                                          #
# This function pulls a specific player's info, including name, current server, etc #
# Inputs: Player Battlemetrics ID                                                   #
# Returns: Player Object                                                            #
#####################################################################################

def getPlayerSession(id):
    result = {}

    # Prepare time filter for BM API
    bmtime = datetime.datetime.now().replace(microsecond=0).isoformat()
    bmtime = str(bmtime) + "Z"

    # Call Battlemetrics Session API to get active session (BM Server ID)
    player_session = requests.get("https://api.battlemetrics.com/sessions?filter[players]=" + str(id) + "&filter[at]=" + str(bmtime), headers=headers).json()
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
    #print(str(result))
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


#####################################################################################
# writeIP2DB() Function                                                             #
# This function adds an IP to the DB with player's Steam ID                         #
# Inputs: SteamID, IP Address (Strings)                                             #
# Returns: True or False (success or not)                                           #
#####################################################################################

def writeIP2DB(steamid,ip):
    pass



############################################################################
#                                   Main                                   #
############################################################################

# Standard Python Main Function - runs on app init
def main():
    print("Initialize Main")
    logging.info("main*()")

    # player_cache is the main baseline (or the "old" baseline)
    global player_cache
    player_cache = []

    # Scheduler for checking Server Playerlist Updates
    schedule.every(10).seconds.do(flow)

    # Keeps app alive
    while 1:
        schedule.run_pending()
        time.sleep(1)
    
if __name__ == "__main__":
    main()

