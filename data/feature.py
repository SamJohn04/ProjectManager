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
    def from_json(json_data: str | list[str]):
        if isinstance(json_data, str):
            name = input(f'Name of feature {json_data}: ')
            description = json_data
        else:
            name, description = json_data

        return Feature(name, description)

    @staticmethod
    def from_stdin():
        name = input("Feature Name: ")
        description = input("Feature Description: ")

        return Feature(name, description)

