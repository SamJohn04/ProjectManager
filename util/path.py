import os


CONFIG_JSON_FILE_NAME = "pmconfig.json"


def get_root_path_and_config_path(root_path: str | None = None):
    if root_path is None:
        root_path = os.getcwd()

    if not os.path.isdir(root_path):
        raise Exception(f"{root_path} is not a directory.")

    return root_path, os.path.join(root_path, CONFIG_JSON_FILE_NAME)


class ConfigPath:
    def __init__(self, path: str | None = None):
        self.root_path = os.path.abspath(path) if path is not None else os.getcwd()

        if not os.path.isdir(self.root_path):
            raise Exception("Path is not a directory.")

        self.config_path = os.path.join(self.root_path, CONFIG_JSON_FILE_NAME)

    def does_config_exist(self):
        return os.path.exists(self.config_path)

