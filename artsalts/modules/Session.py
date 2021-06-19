# Session Class

import logging

# Set Logging Level
logging.basicConfig(level=logging.DEBUG)

class Session:
    def __init__(self,steamid):
        self.steamid = steamid
        self.playerName = ""
        self.serverName = ""
        self.sessionStart = ""
        self.sessionEnd = ""