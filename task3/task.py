import csv
import math

def task(csv_content: str) -> float:
    rows = csv.reader(csv_content.splitlines(), delimiter=',')
    dataset = list(rows)
    total_count = len(dataset)
    entropy_result = 0.0

    for row in dataset:
        for value in row:
            try:
                cell_val = int(value)
            except ValueError:
                continue
            if cell_val > 0:
                probability = cell_val / (total_count - 1)
                entropy_result -= probability * math.log2(probability)

    return round(entropy_result, 1)

if __name__ == '__main__':
    csv_input = '2,0,2,0,0\n0,1,0,0,1\n2,1,0,0,1\n0,1,0,1,1\n0,1,0,1,1\n'
    calculated_entropy = task(csv_input)
    print(calculated_entropy)
