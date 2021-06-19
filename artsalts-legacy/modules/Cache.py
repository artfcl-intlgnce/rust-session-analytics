# Cache Class

import logging

# Set Logging Level
logging.basicConfig(level=logging.DEBUG)

class Cache:
    def __init__(self):
        logging.debug("Created Cache class object")
        Cache.players = []

    def getCache(self):
        return self.cache

    def setCache(self,cache):
        self.cache = cache
        print("I set the cache!")

    def compare(self,new_playerlist):
        print("Existing Cache: " + str(len(self.cache)))
        print("New Compare Cache: " + str(len(self.new_playerlist)))

        players_joined = []
        for player in new_playerlist:
            if player not in self:
                print("Found a new player " + str(player['id']))
                players_joined.append(player)
            else:
                pass
        return players_joined
