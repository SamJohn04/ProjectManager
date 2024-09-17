from data.feature import Feature
from data.projectpath import ProjectPath

class Config:
    def __init__(self, title: str, description: str, features: list[Feature] | None = None, project_paths: list[ProjectPath] | None = None, options: dict | None = None):
        if not options:
            options = {}

        self.title = title
        self.description = description

        self.features = [] if features is None else features
        self.project_paths = [] if project_paths is None else project_paths

        self.options = options

        self.todo_flag = options.get('todo-flag', 'todo'.upper())
        self.feat_flag = options.get('feat-flag', '@feat'.upper())

    def add_feature_from_stdin(self):
        new_feature = Feature.from_stdin()
        assert new_feature.name not in [feature.name for feature in self.features], "Feature name already defined."
        self.features.append(new_feature)

    def add_new_project_path(self):
        new_project_path = ProjectPath.from_stdin()
        assert new_project_path.name not in [project_path.name for project_path in self.project_paths], "Name already defined."
        self.project_paths.append(new_project_path)

    def to_json(self) -> dict:
        config_json = {
                'title': self.title,
                'description': self.description,
                'features': [feature.to_json() for feature in self.features],
                'paths': [project_path.to_json() for project_path in self.project_paths],
                }
        config_json.update(self.options)
        return config_json

    def to_stdout(self, verbose: bool = False):
        print(self.title)
        print(self.description, '\n')

        print("\nFeatures: ")
        for feature in self.features:
            feature.to_stdout(verbose)
        if len(self.features) == 0:
            print("No Feature added.")

        print("\nPaths: ")
        for project_path in self.project_paths:
            project_path.to_stdout(verbose)
        if len(self.project_paths) == 0:
            print("No Project Paths added.")

    @staticmethod
    def from_json(json_data: dict):
        options = {key: json_data[key] for key in json_data if key not in ['title', 'description', 'features', 'paths']}
        return Config(
                json_data['title'],
                json_data['description'],
                list(map(Feature.from_json, json_data['features'])),
                list(map(ProjectPath.from_json, json_data.get('paths', []))),
                options
                )

    @staticmethod
    def from_stdin():
        title = input('Title: ')
        description = input('Description: ')
        return Config(
                title,
                description,
                )

