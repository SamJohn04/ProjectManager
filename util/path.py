import os


CONFIG_JSON_FILE_NAME = "pmconfig.json"


class ConfigPath:
    def __init__(self, path: str | None = None):
        self.root_path = os.path.abspath(path) if path is not None else os.getcwd()

        assert os.path.isdir(self.root_path), "Path is not a directory."

        self.config_path = os.path.join(self.root_path, CONFIG_JSON_FILE_NAME)

    def does_config_exist(self):
        return os.path.exists(self.config_path)


