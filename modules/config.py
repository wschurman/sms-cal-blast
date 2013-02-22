import json
import os.path
import sys

class Config:

    def __init__(self):
        # load cross language config
        cfile = open(os.path.dirname(__file__) + '/../config.json')
        config = json.load(cfile)
        cfile.close()

        cfile_private = open(os.path.dirname(__file__) + '/../config_private.json')
        config_private = json.load(cfile_private)
        cfile_private.close()

        # merge private
        config.update(config_private)

        self.config = config

    def cf(self, key):
        """
        Gets a config value, removes unicode if necessary.
        """
        if isinstance(self.config[key], int):
            return self.config[key]
        else:
            return str(self.config[key])

    def get(self, key):
        """
        For compatibility.
        """
        return self.cf(key)

    def DEBUG(self):
        return self.cf("DEBUG")
