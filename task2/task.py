from collections import defaultdict
import csv

def main(input_csv: str) -> str:
    descendants = defaultdict(list)
    ancestors = defaultdict(list)

    reader = csv.reader(input_csv.splitlines(), delimiter=',')

    for entry in reader:
        if not entry:
            continue
        
        parent, child = entry
        descendants[parent].append(child)
        ancestors[child].append(parent)

        if parent not in ancestors:
            ancestors[parent] = []
        if child not in descendants:
            descendants[child] = []

    root_node = next((node for node in ancestors if not ancestors[node]), None)
    leaf_nodes = [node for node in descendants if not descendants[node]]

    results = {node: {'d1': set(descendants[node]),
                      'd2': set(ancestors[node]),
                      'd3': set(),
                      'd4': set(),
                      'd5': set()} for node in ancestors}

    queue = [root_node]
    while queue:
        current = queue.pop()
        for child in descendants[current]:
            results[child]['d4'] |= results[current]['d2'] | results[current]['d4']
            results[child]['d5'] |= results[current]['d1'] - {child}
            queue.append(child)

    reverse_queue = leaf_nodes[:]
    while reverse_queue:
        current = reverse_queue.pop()
        for parent in ancestors[current]:
            results[parent]['d3'] |= results[current]['d1'] | results[current]['d3']
            if parent not in reverse_queue:
                reverse_queue.append(parent)

    output_fields = ('d1', 'd2', 'd3', 'd4', 'd5')
    csv_result = '\n'.join([','.join([str(len(results[node][field])) for field in output_fields]) 
                            for node in sorted(results)]) + '\n'

    return csv_result

if __name__ == '__main__':
    example_input = "1,2\n1,3\n3,4\n3,5\n"
    print(main(example_input))