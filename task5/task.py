import json
import numpy as np


def get_matrix(filepath: str):
    with open(filepath, 'r') as file:
        clusters_data = json.load(file)

    # Обрабатываем каждый кластер
    processed_clusters = []
    for cluster in clusters_data:
        processed_clusters.append(cluster if isinstance(cluster, list) else [cluster])

    # Вычисляем общий размер матрицы
    total_size = sum(len(c) for c in processed_clusters)

    # Инициализируем матрицу смежности единицами
    adjacency_matrix = np.ones((total_size, total_size), dtype=int)

    # Обновляем матрицу на основе приоритета кластеров
    for idx, current_cluster in enumerate(processed_clusters):
        # Собираем все элементы из предыдущих кластеров
        preceding_elements = [el for cl in processed_clusters[:idx] for el in cl]
        # Устанавливаем нули для нарушений приоритета
        for elem in current_cluster:
            for prev_elem in preceding_elements:
                adjacency_matrix[elem - 1, prev_elem - 1] = 0

    return adjacency_matrix

# Функция для поиска конфликтующих пар элементов в матрице
def find_clusters(matrix, estimate1, estimate2):
    conflict_list = []

    # Итерируемся по матрице, чтобы найти пары с взаимными конфликтами
    for i, row in enumerate(matrix):
        for j in range(i + 1, len(matrix)):
            if matrix[i, j] == 0 and matrix[j, i] == 0:
                # Создаем отсортированную пару конфликтующих элементов
                conflict_pair = sorted([i + 1, j + 1])
                if conflict_pair not in conflict_list:
                    conflict_list.append(conflict_pair)

    # Преобразуем конфликтующие пары в требуемый формат
    return str([pair[0] if len(pair) == 1 else pair for pair in conflict_list])


def main(file_path1, file_path2):
    
    matrix1 = get_matrix(file_path1)
    matrix2 = get_matrix(file_path2)

    # Выполняем операции пересечения и объединения матриц
    intersect_matrix = np.multiply(matrix1, matrix2)
    transpose_intersect = np.multiply(matrix1.T, matrix2.T)
    union_matrix = np.maximum(intersect_matrix, transpose_intersect)

    # Находим и возвращаем конечные кластеры
    final_clusters = find_clusters(union_matrix, matrix1, matrix2)
    return final_clusters

if __name__ == '__main__':
    print(main("example1.json", "example2.json"))
