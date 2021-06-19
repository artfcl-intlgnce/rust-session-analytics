# Cache Class

import logging

# Set Logging Level
logging.basicConfig(level=logging.DEBUG)

class Cache:
    def __init__(self, cache):
        self.cache = cache
        logging.debug("Created Cache class object")

    def getCache(self):
        return self.cache

    def setCache(self,cache):
        self.cache = cache
        print("I set the cache!")