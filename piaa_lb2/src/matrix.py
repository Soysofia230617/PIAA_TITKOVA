import random
import math
DEBUG = 0

def generate_matrix(size, max_weight=50):
    matrix = [[math.inf if i == j else random.randint(1, max_weight) for j in range(size)] for i in range(size)]
    return matrix
def generate_symmetric_matrix(size, max_weight=50):
    matrix = [[math.inf if i == j else 0 for j in range(size)] for i in range(size)]
    for i in range(size):
        for j in range(i + 1, size):
            weight = random.randint(1, max_weight)
            matrix[i][j] = weight
            matrix[j][i] = weight
    return matrix


def save_matrix_to_file(matrix, filename):
    with open(filename, 'w') as file:
        for row in matrix:
            file.write(' '.join(map(str, row)) + '\n')


def load_matrix_from_file(filename):
    matrix = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                row = list(map(lambda x: float(x) if x != 'inf' else math.inf, line.split()))
                matrix.append(row)

        n = len(matrix)
        if not all(len(row) == n for row in matrix):
            print("Ошибка: Матрица не квадратная (число столбцов не равно числу строк).")
            return None

        for i in range(n):
            for j in range(n):
                if i == j:
                    if not math.isinf(matrix[i][j]):
                        print(
                            f"Ошибка: Элемент на диагонали ({i}, {j}) должен быть бесконечностью, а не {matrix[i][j]}.")
                        return None
                else:
                    if matrix[i][j] < 0:
                        print(
                            f"Ошибка: Элемент ({i}, {j}) = {matrix[i][j]} отрицательный, ожидается неотрицательное значение.")
                        return None
                    if math.isnan(matrix[i][j]):
                        print(f"Ошибка: Элемент ({i}, {j}) содержит NaN, что недопустимо.")
                        return None

        if DEBUG:
            print(f"Матрица успешно загружена из файла {filename} и проверена на корректность.")
        return matrix

    except FileNotFoundError:
        print(f"Ошибка: Файл {filename} не найден.")
        return None
    except ValueError:
        print("Ошибка: В файле содержатся некорректные значения (не числа).")
        return None
