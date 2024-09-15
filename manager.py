import sys

import argparse

from util.path import ConfigPath
from util import io
from data.config import Config
from data.projectpath import ProjectPath
from measure import scan


VALUE_ARG_KEYWORDS = { '--path' }
FLAG_ARG_KEYWORDS = { '-v', '--verbose', '-u', '--update' }


def get_config(config_path: ConfigPath, update_if_change: bool = False):
    assert config_path.does_config_exist(), 'Config does not exist. Use \'init\''
    config_json = io.read_json(config_path.config_path)
    config = Config.from_json(config_json)

    if config.to_json() != config_json and update_if_change:
        io.write_json(config.to_json(), config_path.config_path)

    return config


def init_config(config_path: ConfigPath, args: list[str], kwargs: dict[str, str | bool]):
    assert not config_path.does_config_exist(), 'Config already exists!'
    new_config = Config.from_stdin()
    io.write_json(new_config.to_json(), config_path.config_path)


def scan_project_path(config_path: ConfigPath, project_path: ProjectPath, verbose: bool = False):
    if input(f"Scan {project_path.name}? (Y|n)").lower() == 'n':
        return
    all_todos = scan.scan_todos(list(project_path.all_file_paths(config_path.root_path)))
    for file_path in all_todos:
        if all_todos[file_path] is None:
            continue
        if len(all_todos[file_path]) == 0:
            if verbose:
                print(f"{file_path}: Complete!")
            continue
        if verbose:
            print(f"{file_path}: ")
            for index, line in all_todos[file_path]:
                print(f"\t{index}. {line}")
        else:
            print(f"{file_path}: {', '.join(map((lambda todo_item: f'line {todo_item[0]}'), all_todos[file_path]))}")


def main():
    args, kwargs = parse(sys.argv[1:])
    command = args[0] if len(args) > 0 else 'view'
    assert command in ('init', 'view', 'scan', 'add')

    config_path = ConfigPath(kwargs.get('--path'))

    match command:
        case 'init':
            init_config(config_path, args, kwargs)
        case 'view':
            config = get_config(config_path, kwargs.get('-u', False) or kwargs.get('--update', False))
            config.to_stdout(kwargs.get('-v', False) or kwargs.get('--verbose', False))
        case 'add':
            # TODO
            pass
        case 'scan':
            config = get_config(config_path, kwargs.get('-u', False) or kwargs.get('--update', False))
            for project_path in config.project_paths:
                scan_project_path(config_path, project_path, kwargs.get('-v', False) or kwargs.get('--verbose', False))


"""
def o_main():
    arg_parser = get_arg_parser()
    args = arg_parser.parse_args(sys.argv[1:])
    config_path = ConfigPath()

    match args.command:
        case 'init':
            init_config(config_path)
        case 'view':
            get_config(config_path).to_stdout()
        case 'scan':
            config = get_config(config_path)
            project_paths = [ProjectPath('main', '')] if len(config.project_paths) == 0 else config.project_paths
            for project_path in project_paths:
                scan_project_path(config_path, project_path)
        case 'add':
            config = get_config(config_path)
            choice = input('1.\tProject Path\n2.\tFeature').lower()
            io.write_json(config.to_json(), config_path.config_path)
"""


def parse(input_args: list[str]):
    args = []
    kwargs = {}
    index = 0
    
    while index < len(input_args):
        arg = input_args[index]
        if arg in FLAG_ARG_KEYWORDS:
            kwargs[arg] = True
        elif arg in VALUE_ARG_KEYWORDS:
            index += 1
            assert index < len(input_args), f"{arg} expects an argument"
            kwargs[arg] = kwargs[input_args[index]]
        else:
            args.append(arg)
        index += 1

    return args, kwargs


def get_arg_parser():
    arg_parser = argparse.ArgumentParser(
            prog='manage',
            description='CLI tool for concise project management.',
            )
    arg_parser.add_argument('command', choices = ['init', 'view', 'add', 'scan'], default = 'view', nargs='?')
    return arg_parser

if __name__ == '__main__':
    main()

