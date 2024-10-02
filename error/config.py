class ConfigNotFoundError(Exception):
    def __str__(self):
        return f"Config file pmconfig.json has not been found. {' '.join(self.args)}"
    

class ConfigParseError(Exception):
    def __str__(self):
        return f"The config file pmconfig.json might be corrupted. To initialize a new config, delete the corrupted one or use init --force"

