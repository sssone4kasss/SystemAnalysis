import json
import numpy as np

def build_adjacency_matrix(json_str: str):
    groups = [g if isinstance(g, list) else [g] for g in json.loads(json_str)]
    size = sum(len(group) for group in groups)

    adjacency = [[1] * size for _ in range(size)]

    blocked_elements = []
    for group in groups:
        for block_element in blocked_elements:
            for element in group:
                adjacency[element - 1][block_element - 1] = 0
        for element in group:
            blocked_elements.append(element)

    return np.array(adjacency)

def extract_groups(matrix, estimate1, estimate2):
    clusters = {}

    num_rows = len(matrix)
    num_cols = len(matrix[0])
    skipped_rows = set()
    for row in range(num_rows):
        if row + 1 in skipped_rows:
            continue
        current_group = [row + 1]
        clusters[row + 1] = current_group
        for col in range(row + 1, num_cols):
            if matrix[row][col] == 0:
                current_group.append(col + 1)
                skipped_rows.add(col + 1)

    result = []
    for k in clusters:
        if not result:
            result.append(clusters[k])
            continue

        for idx, item in enumerate(result):
            sum_estimate1_item = np.sum(estimate1[item[0] - 1])
            sum_estimate2_item = np.sum(estimate2[item[0] - 1])
            sum_estimate1_k = np.sum(estimate1[k - 1])
            sum_estimate2_k = np.sum(estimate2[k - 1])

            if sum_estimate1_item == sum_estimate1_k and sum_estimate2_item == sum_estimate2_k:
                for c in clusters[k]:
                    result[idx].append(c)
                    break
            if sum_estimate1_item < sum_estimate1_k or sum_estimate2_item < sum_estimate2_k:
                result = result[:idx] + clusters[k] + result[idx:]
                break

        result.append(clusters[k])

    final_result = [r[0] if len(r) == 1 else r for r in result]
    return str(final_result)

def main(string_a, string_b):
    matrix_a = build_adjacency_matrix(string_a)
    matrix_b = build_adjacency_matrix(string_b)

    combined_matrix = np.multiply(matrix_a, matrix_b)
    transposed_combined_matrix = np.multiply(np.transpose(matrix_a), np.transpose(matrix_b))

    union_matrix = np.maximum(combined_matrix, transposed_combined_matrix)
    extracted_groups = extract_groups(union_matrix, matrix_a, matrix_b)
    return extracted_groups

if __name__ == "__main__":
    input_str1 = '[1,[2,3],4,[5,6,7],8,9,10]'
    input_str2 = '[[1,2],[3,4,5],6,7,9,[8,10]]'
    processed_results = main(input_str1, input_str2)
    print(processed_results)
