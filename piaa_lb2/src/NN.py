import math

DEBUG = False

def nearest_neighbor_tsp(distance_matrix, start_vertex=0):
    n = len(distance_matrix)
    visited = [False] * n
    route = [start_vertex]
    visited[start_vertex] = True

    if DEBUG:
        print("Начало поиска маршрута ближайшего соседа.")
        print(f"  Матрица расстояний: {distance_matrix}")
        print(f"  Начальный город: {start_vertex}")

    for _ in range(n - 1):
        last_city = route[-1]

        if DEBUG:
            print(f"\nИщем ближайшего соседа для города {last_city}...")
        eligible_neighbors = [(i, distance_matrix[last_city][i]) for i in range(n) if not visited[i] and distance_matrix[last_city][i] != math.inf]

        if DEBUG:
            print(f"  Возможные соседи: {eligible_neighbors}")

        nearest_city = min(eligible_neighbors, key=lambda x: x[1], default=(None, math.inf))

        if nearest_city[0] is None:
            print("Невозможно найти путь без бесконечностей.")
            return None, None

        if DEBUG:
            print(f"  Ближайший город: {nearest_city[0]} (расстояние: {nearest_city[1]})")

        route.append(nearest_city[0])
        visited[nearest_city[0]] = True

    if distance_matrix[route[-1]][start_vertex] == math.inf:
        print("Невозможно вернуться в начальный город без бесконечностей.")
        return None, None

    total_distance = 0
    for i in range(n - 1):
        total_distance += distance_matrix[route[i]][route[i + 1]]
    total_distance += distance_matrix[route[-1]][start_vertex]

    if DEBUG:
        print(f"\nЗавершен поиск маршрута.")

    return route, total_distance

