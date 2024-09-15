import os
from glob import glob

from util import io


class ProjectPath:
    def __init__(self, name: str, path: str, includes: list[str] | None = None, excludes: list[str] | None = None):
        self.name = name
        self.path = path

        self.includes = ['**'] if includes is None else includes
        self.excludes = [] if excludes is None else excludes

    def all_file_paths(self, root_path: str) -> set[str]:
        all_paths = set()

        for include in self.includes:
            all_paths.update(self.get_globbed_files(include, root_path))

        for exclude in self.excludes:
            all_paths -= self.get_globbed_files(exclude, root_path)

        return all_paths

    def get_globbed_files(self, inner_pattern: str, root_path: str) -> set[str]:
        globbed_paths = glob(os.path.join(root_path, self.path, inner_pattern), recursive = True)
        return set(filter(os.path.isfile, globbed_paths))

    def to_json(self) -> dict:
        project_path_json: dict[str, str | list[str]] = {'name': self.name, 'path': self.path}

        if self.includes != ['**']:
            project_path_json['includes'] = self.includes
        if self.excludes != []:
            project_path_json['excludes'] = self.excludes

        return project_path_json

    def to_stdout(self, verbose: bool = False):
        print(f"\t{self.name}: '{self.path}'")
        if verbose:
            print(f"\tInclude: [{', '.join(self.includes)}]")
            print(f"\tExclude: [{', '.join(self.excludes)}]")

    @staticmethod
    def from_json(project_path_json: dict):
        return ProjectPath(
                project_path_json['name'],
                project_path_json['path'],
                project_path_json.get('includes'),
                project_path_json.get('excludes')
                )

    @staticmethod
    def from_stdin():

        name = input('Name (src, test, etc.): ')
        path = input('Path: ')

        if input("Define inclusion categories? (All (non-excluded) files will be chosen if not) (y|N) ").lower() == 'y':
            includes = io.get_lines('Includes: ')
        else:
            includes = None

        if input("Define exclusion categories? (y|N) ").lower() == 'y':
            excludes = io.get_lines('Excludes: ')
        else:
            excludes = None

        return ProjectPath(name, path, includes, excludes)

