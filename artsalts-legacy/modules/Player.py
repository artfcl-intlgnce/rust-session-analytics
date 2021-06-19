# Player Class

import logging

# Set Logging Level
logging.basicConfig(level=logging.DEBUG)


class Player:
    def __init__(self,steamid):
        self.steamid = steamid
        self.bmid = ""
        self.name = ""
        self.sessions = []
        logging.debug("Created Player class object")

    def getBMID(self):
        return self.bmid

    def setBMID(self,bmid):
        self.bmid = bmid

    def getName(self):
        return self.name

    def setName(self,name):
        self.name = name

    def getSessions(self):
        return self.sessions

    def setSessions(self,sessions):
        self.sessions = sessions

    def appendSession(self,session):
        self.sessions.append(session)