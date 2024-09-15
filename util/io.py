import json


def get_lines(message: str) -> list[str]:
    print(message)
    
    lines = []
    line = input('- ')
    while len(line.strip()) > 0:
        lines.append(line.strip())
        line = input('- ')

    return lines


def write_json(json_data, path: str):
    with open(path, 'w') as file:
        json.dump(json_data, file, indent = 4)


def read_json(path: str) -> any:
    with open(path, 'r') as file:
        return json.load(file)

