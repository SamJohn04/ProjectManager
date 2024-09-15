import json
from util import io


def get_config(config_path: str | None) -> dict:
    if config_path is None:
        return None
    
    with open(config_path) as config_file:
        return json.load(config_file)


def put_config(config: dict, config_path: str):
    with open(config_path, 'w') as config_file:
        return json.dump(config, config_file, indent=4)


def new_config() -> dict:
    title = io.get('Title: ')
    description = io.get('Description: ')
    features = io.get_lines('Features: ')

    return {
            'title': title,
            'description': description,
            'features': features 
            }


def show_config(config: dict):
    io.put(config['title'])
    io.put(config['description'], '\n')
    io.put('FEATURES: ')
    io.put_lines(config['features'])


