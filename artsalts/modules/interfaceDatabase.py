# Database Interface

import logging

# Set Logging Level
logging.basicConfig(level=logging.DEBUG)


class dbQuery:
    def __init__(self):
        logging.debug("Created dbQuery class")
        pass

    def addIp(self):
        pass

    def getAlts(self):
        pass

#####################################################################################
# writeIP2DB() Function                                                             #
# This function adds an IP to the DB with player's Steam ID                         #
# Inputs: SteamID, IP Address (Strings)                                             #
# Returns: True or False (success or not)                                           #
#####################################################################################

    def writeIP2DB(steamid,ip):
        pass