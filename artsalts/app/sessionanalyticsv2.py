   ##################################################################### 
 ##               Battlemetrics Player Session Analytics                ##
#                      Code Author: Artfcl_Intlgnce                       #  
 ##                       License: GNU GPLv3                            ##    
   ###################################################################### 

############################################################################
#                           Import Packages                                #
############################################################################

import requests
import json
import time
import datetime
import schedule
import logging
import zmq
import sys
import threading
import sched
from dotenv import load_dotenv



############################################################################
#                           Configure Logger                               #
############################################################################

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    # Change level to INFO or ERROR to change terminal output (reduces storage stress)
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')
logging.info("Logger Initialized")


############################################################################
#                Initialize Global Variables / Caches                      #
############################################################################

logging.info("Initializing Variables and Caches")

# player_cache is the main baseline (or the "old" baseline)
# global player_cache
player_cache = []

# player_cache_temp is the new/latest player cache pulled from BM. 
# This eventually becomes the player_cache after player_deltas have been determined and queued. 
player_cache_temp = []

# Battlemetrics API Token goes here. This sets the headers for the http request
headers = {'Authorization': 'Bearer ', 'Content-Type': 'application/json'}

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

    logging.debug("Hit getPlayerlist()") # Log Everything!
    temp = [] # used to store return results of function

    # Call Battlemetrics API and format/parse. Returns array of BM Player ID's (NOT Steam ID's)
    #response = requests.get("https://api.battlemetrics.com/players?page[size]=100&fields[identifier]=type,identifier&filter[servers]='" + str(serverid) + "'", headers=headers)
    response = requests.get("https://api.battlemetrics.com/servers/" + str(serverid) + "?include=player", headers=headers)
    responsejson = response.json()
    data = responsejson['included']

    # Loop through BM Response, Extract ID of player and append to result
    for row in data:
        temp.append(row['id'])
    # logging.debug("Page1 Players: " + str(temp))
    # Wrap Up and Return Result of getPlayerList()
    #print("Retrieved Player List" + str(temp))
    logging.info("Retrieved Player List \n" + str(temp))
    return temp

def getPlayerLeaves(player_cache, player_cache_temp):
    logging.info("Size of Player Cache: " + str(len(player_cache)))
    logging.info("Size of Player Cache Temp: " + str(len(player_cache_temp)))

    #logging.debug("GetPlayerLeaves() \n player_cache: " + str(player_cache) + "\n\n Player cache Temp " + str(player_cache_temp) )
    temp = []
    for player in player_cache:
        if player not in player_cache_temp:
            temp.append(player)
            print(str(player) + " NOT IN SERVER!")
            logging.info(str(player) + " NOT IN SERVER!")
    logging.debug("Results of getPlayerLeaves():" +  str(temp))
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
    global player_cache
    if len(player_cache) > 0:
        changes = getPlayerLeaves(player_cache,player_cache_temp)
        for change in changes:
            logging.info("Taking action for player " + str(change))
            playerinfo_temp = getPlayerSession(str(change))
            logging.debug("SESSION FOUND: " + str(playerinfo_temp))
    else:
        changes = []

    # Sets / overrides latest player list into player cache    
    player_cache = player_cache_temp
    player_cache_temp = []   #clear temp cache

    logging.info("PLAYER LEAVES: " + str(changes))

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
    print(str(result))
    return result


############################################################################
#                                 Queue Sys                                #
############################################################################


context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

#  Do 10 requests, waiting each time for a response
for request in range(10):
    print("Sending request %s …" % request)
    socket.send(b"Hello")

    #  Get the reply.
    message = socket.recv()
    print("Received reply %s [ %s ]" % (request, message))




############################################################################
#                                   Main                                   #
############################################################################

# Standard Python Main Function - runs on app init
def main():
    print("Initialize Main")
    logging.info("main*()")

    # player_cache is the main baseline (or the "old" baseline)
    # global player_cache
    # player_cache = []

    # Scheduler for checking Server Playerlist Updates
    schedule.every(20).seconds.do(flow)


    # Keeps app alive
    while 1:
        schedule.run_pending()
        time.sleep(1)
        #logging.debug("Scheduler Run")
    
if __name__ == "__main__":
    main()
