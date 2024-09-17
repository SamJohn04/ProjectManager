import sys

from data.feature import Feature
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


def scan_project_path(config: Config, root_path: str, project_path: ProjectPath, verbose: bool = False):
    if input(f"Scan {project_path.name} for todos? (Y|n) ").lower() == 'n':
        return
    all_todos, cannot_open = scan.scan_keyword_in_project_path(project_path, root_path, config.todo_flag)
    if verbose:
        if len(cannot_open) > 0:
            print("Cannot Open:", ', '.join(cannot_open))
    for item in all_todos:
        item.to_stdout(verbose)


def scan_feature_complete(config: Config, root_path: str, project_path: ProjectPath, verbose: bool = False):
    if input(f"Scan {project_path.name} for features? (Y|n) ").lower() == 'n':
        return

    all_feats, cannot_open = scan.scan_keyword_in_project_path(project_path, root_path, config.feat_flag)

    feature_names = [feature.name.replace(' ', '_') for feature in config.features]
    
    if verbose:
        if len(cannot_open) > 0:
            print("Cannot Open:", ', '.join(cannot_open))

    feature_flags = {}
    for item in all_feats:
        if len(item.indices) == 0:
            continue
        for index in item.indices:
            curr_feature_flag = item.lines[index]
            curr_feature_flag = curr_feature_flag[curr_feature_flag.index(config.feat_flag):]
            curr_split = curr_feature_flag.rstrip().split()
            if len(curr_split) < 2:
                continue
            if len(curr_split) == 2:
                curr_feature_flag, status = curr_split[1], 'UNMARKED'
            else:
                curr_feature_flag, status = curr_split[1], curr_split[2]

            if curr_feature_flag not in feature_names:
                print(curr_feature_flag, "not found in features.")
                continue

            if curr_feature_flag in feature_flags:
                print(f"Feature flag {curr_feature_flag} found in {feature_flags[curr_feature_flag][0].path} and {item.path}")
                continue
            feature_flags[curr_feature_flag] = status, item.path

    for feature_name in feature_names:
        if feature_name not in feature_flags:
            print(f"{feature_name}:\t\tNot Started")
            continue
        if verbose:
            print(f"{feature_name}:\t\t{'\t'.join(feature_flags[feature_name])}")
        else:
            print(f"{feature_name}:\t\t{feature_flags[feature_name][0]}")
  

def main():
    args, kwargs = parse(sys.argv[1:])
    command = args[0] if len(args) > 0 else 'view'
    assert command in ('init', 'view', 'scan', 'edit', 'set')

    config_path = ConfigPath(kwargs.get('--path'))

    match command:
        # @FEAT create DONE
        case 'init':
            init_config(config_path, args, kwargs)
        case 'view':
            config = get_config(config_path, kwargs.get('-u', False) or kwargs.get('--update', False))
            config.to_stdout(kwargs.get('-v', False) or kwargs.get('--verbose', False))
        # @FEAT edit TODO
        case 'edit':
            pass
        case 'scan':
            config = get_config(config_path, kwargs.get('-u', False) or kwargs.get('--update', False))
            for project_path in config.project_paths:
                # @FEAT scan-todo DONE
                scan_project_path(config, config_path.root_path, project_path, kwargs.get('-v', False) or kwargs.get('--verbose', False))
                print("\n")
                # @FEAT measure-feat
                scan_feature_complete(config, config_path.root_path, project_path, kwargs.get('-v', False) or kwargs.get('--verbose', False))
        case 'set':
            config = get_config(config_path)

            if len(args) < 2:
                # TODO
                pass
            elif args[1] not in ['todo-flag', 'feat-flag', 'line-padding']:
                # TODO
                pass
            elif len(args) < 3:
                config.options.pop(args[1], None)
            else:
                config.options[args[1]] = args[2]

            io.write_json(config.to_json(), config_path.config_path)


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


if __name__ == '__main__':
    main()

