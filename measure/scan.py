from data.projectpath import ProjectPath


class Scan:
    def __init__(self, path: str, flag: str):
        self.path = path
        self.flag = flag
        with open(path, 'r') as file:
            self.lines = file.readlines()
        self.indices = [index for (index, line) in enumerate(self.lines) if self.flag in line]

    def to_stdout(self, verbose: bool = False, line_pad: int = 1):
        if len(self.indices) == 0:
            return

        if not verbose:
            print(f"{self.path}:\t{', '.join(str(index) for index in self.indices)}")
            return

        print(f"{self.path}: ")
        for index in self.indices:
            low_index = max(0, index - line_pad)
            high_index = min(index + line_pad + 1, len(self.lines))
            for line_index in range(low_index, high_index):
                print(f"\t{line_index}. {self.lines[line_index].rstrip('\n')}")
            print()


def scan_keyword_in_project_path(project_path: ProjectPath, root_path: str, flag: str) -> tuple[list[Scan], list[str]]:
    results, cannot_open = [], []
    for path in project_path.all_file_paths(root_path):
        try:
            results.append(Scan(path, flag))
        except:
            cannot_open.append(path)
    return results, cannot_open

