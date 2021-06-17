   ##################################################################### 
 ##               Battlemetrics Player Session Analytics                ##
#                      Code Author: Artfcl_Intlgnce                       #  
 ##                       License: GNU GPLv3                            ##    
   ###################################################################### 

############################################################################
#                           Import Packages                                #
############################################################################

import time
import schedule
import logging
from dotenv import load_dotenv
from redis import Redis

# Import App Classes / Modules
from .Classes import *

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

# player_cache_temp is the new/latest player cache pulled from BM. 
# This eventually becomes the player_cache after player_deltas have been determined and queued. 
player_cache_temp = []


############################################################################
#                           Define Core Functions                          #
############################################################################

def getPlayerJoins(player_cache, player_cache_temp):
    logging.info("Size of Player Cache: " + str(len(player_cache)))
    logging.info("Size of Player Cache Temp: " + str(len(player_cache_temp)))

    #logging.debug("getPlayerJoins() \n player_cache: " + str(player_cache) + "\n\n Player cache Temp " + str(player_cache_temp) )
    temp = []
    for player in player_cache_temp:
        if player not in player_cache:
            temp.append(player)
            #print(str(player) + " JOINED SERVER - TAKE ACTION!")
            logging.info(str(player['attributes']['name']) + " JOINED SERVER - TAKE ACTION")
    s.player_cache = player_cache_temp
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
    changes = []
    for player in player_cache_temp:
        if player not in player_cache:
            logging.info("Taking action for player " + str(player))
            changes.append(player)
        
        #playerinfo_temp = getPlayerSession(str(change)) ### KEY LINE OF CODE FOR SESSION ANALYTICS


    # Sets / overrides latest player list into player cache    
    global player_cache
    player_cache = player_cache_temp
    player_cache_temp = []   #clear temp cache
    #logging.debug("PLAYER JOINS: " + str(changes))
    return changes


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
    schedule.every(10).seconds.do(flow())

    # Keeps app alive
    while 1:
        schedule.run_pending()
        time.sleep(1)
    
if __name__ == "__main__":
    main()

