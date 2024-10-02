class Feature:
    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description

    def to_json(self) -> list[str]:
        return [self.name, self.description]

    def to_stdout(self, verbose: bool = False):
        if verbose:
            print(f"\t{self.name}: {self.description}")
        else:
            print(f"\t{self.name}")

    @staticmethod
    def from_json(json_data: list[str]):
        name, description = json_data

        return Feature(name, description)

    @classmethod
    def from_stdin(cls):
        name = cls.get_feature_name_from_stdin("Feature Name: ")

        description = input("Feature Description: ")

        return Feature(name, description)

    @staticmethod
    def get_feature_name_from_stdin(message: str):
        name = input(message)

        while name == '' or ' ' in name:
            if name == '':
                print("Name cannot be empty")
            if ' ' in name:
                print("Name cannot have whitespaces.")
            name = input(message)

        return name

