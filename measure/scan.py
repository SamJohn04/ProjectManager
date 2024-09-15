def scan_todos_in_file(file_path: str, todo_flag: str) -> list[tuple[int, str]] | None:
    try:
        file = open(file_path)
        lines = file.readlines()
        file.close()
    except Exception as e:
        print(file_path, 'cannot be read:', e)
        return None 
    
    return [(index, line) for index, line in enumerate(lines) if todo_flag in line]


def scan_todos(file_paths: list[str], todo_flag: str | None = None):
    if todo_flag is None:
        todo_flag = "todo".upper()

    all_todos_by_file = {}

    for file_path in file_paths:
        todos_of_file_path = scan_todos_in_file(file_path, todo_flag)
        if todos_of_file_path is None:
            continue
        all_todos_by_file[file_path] = todos_of_file_path

    return all_todos_by_file

