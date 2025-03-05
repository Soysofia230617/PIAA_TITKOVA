from Little import little,visualize_tree
from matrix import generate_matrix, generate_symmetric_matrix,save_matrix_to_file,load_matrix_from_file
from NN import nearest_neighbor_tsp

print("Введите размер матрицы:")
size = int(input())
print("1 - Симметричная")
print("2 - Обычная")
type = int(input())

if type == 1:
    matrix = generate_symmetric_matrix(size)
elif type == 2:
    matrix = generate_matrix(size)

print("Сгенерированная матрица:")
for row in matrix:
    print(row)
filename = 'matrix.txt'
save_matrix_to_file(matrix, filename)
print(f"Матрица сохранена в файл {filename}")

print(" ")
matrix = load_matrix_from_file('matrix.txt')
result, nodes = little(matrix)
print("Модифицированный алгоритм Литтла:")
print(f"Минимальный путь: {result['route']}")
print(f"Длина пути: {result['length']}")
visualize_tree(nodes)

print(" ")
print("Алгоритм АБС:")
print("Введите стартовую вершину:")
start_vertex = int(input())
route, distance = nearest_neighbor_tsp(matrix, start_vertex)
print(f"Маршрут: {route}")
print(f"Общее расстояние: {distance}")