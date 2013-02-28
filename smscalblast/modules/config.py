
import json

class Config:

    def __init__(self, cfile):
        # load cross language config
        self.config = self.load_file(cfile)

    def load_file(self, fname):
        cfile = open(fname)
        config = json.load(cfile)
        cfile.close()
        return config

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

    def DEBUG_SMTP(self):
        return self.cf("DEBUG_SMTP")
