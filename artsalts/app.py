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
from Modules import Cache,Player,Session,interfaceBattlemetrics,interfaceDatabase

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

logging.info("Initializing Variables, Objects and Caches")

player_cache = Cache.Cache()

############################################################################
#                           Define Core Functions                          #
############################################################################

def getPlayerJoins(player_cache, player_cache_temp):
    logging.info("Size of Player Cache: " + str(len(player_cache)))
    logging.info("Size of Player Cache Temp: " + str(len(player_cache_temp)))


    temp = []
    for player in player_cache_temp:
        if player not in player_cache:
            temp.append(player)
            print(str(player.getName()) + " JOINED SERVER - TAKE ACTION!")
            #logging.info(str(player) + " \nJOINED SERVER - TAKE ACTION\n")
    #logging.debug("Results of getPlayerJoins():" +  str(temp))
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
    logging.debug("Hit flow()")
    
    player_cache_temp = interfaceBattlemetrics.bmQuery.getPlayerlist(2387727)

    changes = getPlayerJoins(player_cache, player_cache_temp)
    print("Playerlist " + str(player_cache))
    print("Player Cache " + str(player_cache))
    print("Cache Temp " + str(player_cache_temp))

    player_cache = player_cache_temp

    print("changes " + str(changes))
    #print("player cache 123" + str(playerlist))
    return player_cache


############################################################################
#                                   Main                                   #
############################################################################

# Standard Python Main Function - runs on app init
def main():
    print("Initialize Main")
    logging.info("main*()")

    player_cache = Cache.Cache()

    # Scheduler for checking Server Playerlist Updates
    schedule.every(10).seconds.do(flow)

    # Keeps app alive
    while 1:
        schedule.run_pending()
        time.sleep(1)
    
if __name__ == "__main__":
    main()

