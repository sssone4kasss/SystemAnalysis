import csv
from sys import argv
from typing import List, Union, Any, Sequence


def get_value_from_csv(filename: str, row_index: int, column_index: int) -> Union[str, None]:
    try:
        with open(filename, mode='r', newline='') as file:
            data_reader = csv.reader(file)
            rows = list(data_reader)
            if len(rows) > row_index:
                row = rows[row_index]
                if len(row) > column_index:
                    return row[column_index]
    except FileNotFoundError:
        print(f'File {filename} not found.')
    return None


if __name__ == "__main__":
    if len(argv) != 4:
        print("The input format is incorrect. Use the following command:")
        print("./task.py<file path> <line number> <column number>")
        exit(1)
    
    filename = argv[1]
    row_index = int(argv[2])
    column_index = int(argv[3])
    
    result = get_value_from_csv(filename, row_index, column_index)
    if result is not None:
        print(result)
