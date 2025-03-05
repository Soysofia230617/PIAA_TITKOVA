import random
import matplotlib
matplotlib.use('Agg')
import math
import networkx as nx
import matplotlib.pyplot as plt
DEBUG = False


class Node:
    def __init__(self, matrix, bound, route, pieces, parent=None, depth=0):
        self.matrix = matrix
        self.bound = bound
        self.route = route
        self.pieces = pieces
        self.parent = parent
        self.depth = depth

    @staticmethod
    def clone_matrix(matrix):
        return [row[:] for row in matrix]

    @staticmethod
    def row_mins(matrix):
        return [min(row) for row in matrix]

    @staticmethod
    def column_mins(matrix):
        return [min(matrix[i][j] for i in range(len(matrix))) for j in range(len(matrix[0]))]

    @staticmethod
    def reduce_rows(matrix, mins):
        for i in range(len(matrix)):
            if math.isfinite(mins[i]):
                matrix[i] = [cell - mins[i] for cell in matrix[i]]

    @staticmethod
    def reduce_columns(matrix, mins):
        for j in range(len(matrix[0])):
            if math.isfinite(mins[j]):
                for i in range(len(matrix)):
                    matrix[i][j] -= mins[j]

    @staticmethod
    def reduce(matrix):
        row_mins = Node.row_mins(matrix)
        Node.reduce_rows(matrix, row_mins)

        col_mins = Node.column_mins(matrix)
        Node.reduce_columns(matrix, col_mins)

        return sum(val for val in row_mins if math.isfinite(val)) + sum(val for val in col_mins if math.isfinite(val))

    def get_cell_with_max_penalty(self):
        max_penalty = -math.inf
        cell_with_max_penalty = None

        if DEBUG:
            print("Поиск ячейки с максимальной штрафной стоимостью:")

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == 0:
                    row_min = min(
                        (self.matrix[i][k] for k in range(len(self.matrix[i])) if k != j),
                        default=math.inf
                    )
                    col_min = min(
                        (self.matrix[k][j] for k in range(len(self.matrix)) if k != i),
                        default=math.inf
                    )
                    penalty = row_min + col_min
                    if penalty > max_penalty:
                        max_penalty = penalty
                        cell_with_max_penalty = (i, j, max_penalty)

                    if DEBUG:
                        print(f"  Ячейка ({i}, {j}): штраф {penalty}")

        if DEBUG:
            print(f"  Ячейка с максимальной штрафной стоимостью: {cell_with_max_penalty}\n")
        return cell_with_max_penalty

    def get_lower_bounds(self):
        if DEBUG:
            print("Вычисление нижней оценки на основе графа МОД:")

        dopustimye_dugi = self.get_acceptable_edges()
        mod_graph = self.build_mod_graph(dopustimye_dugi)
        bound2 = self.calculate_mod_weight(mod_graph)

        if DEBUG:
            print(f"  Нижняя оценка: {bound2}\n")
        return bound2

    def get_acceptable_edges(self):
        acceptable_edges = []
        for i in range(len(self.pieces)):
            for j in range(i + 1, len(self.pieces)):
                u, v = self.pieces[i][-1], self.pieces[j][0]
                if u != v and math.isfinite(self.matrix[u][v]):
                    acceptable_edges.append((u, v))
                u, v = self.pieces[j][-1], self.pieces[i][0]
                if u != v and math.isfinite(self.matrix[u][v]):
                    acceptable_edges.append((u, v))
        return acceptable_edges

    def build_mod_graph(self, edges):
        if DEBUG:
            print("Построение графа МОД:")

        mod_graph = {}
        for edge in edges:
            if edge[0] not in mod_graph:
                mod_graph[edge[0]] = []
            if edge[1] not in mod_graph:
                mod_graph[edge[1]] = []
            mod_graph[edge[0]].append((edge[1], self.matrix[edge[0]][edge[1]]))
            mod_graph[edge[1]].append((edge[0], self.matrix[edge[0]][edge[1]]))

        if DEBUG:
            print(f"  Граф МОД: {mod_graph}\n")
        return mod_graph

    def calculate_mod_weight(self, mod_graph):
        mod_weight = 0
        used_edges = set()
        edges = []
        for node in mod_graph:
            for edge in mod_graph[node]:
                if math.isfinite(edge[1]):
                    edges.append((edge[1], node, edge[0]))
        edges.sort()
        for edge in edges:
            if (edge[1], edge[2]) not in used_edges and (edge[2], edge[1]) not in used_edges:
                mod_weight += edge[0]
                used_edges.add((edge[1], edge[2]))
                used_edges.add((edge[2], edge[1]))
        return mod_weight


def is_hamiltonian_cycle(route):
    if DEBUG:
        print("Проверка на гамильтонов цикл:")

    if len(route) != len(set(route)):
        if DEBUG:
            print("  Не гамильтонов цикл: длина маршрута не соответствует количеству уникальных вершин.")
        return False
    graph = {}
    for u, v in route:
        graph[u] = v
    visited = set()
    current = route[0][0]
    while current not in visited:
        visited.add(current)
        if current not in graph:
            if DEBUG:
                print("  Не гамильтонов цикл: не все вершины посещены.")
            return False
        current = graph[current]

    if len(visited) == len(graph):
        if DEBUG:
            print("  Гамильтонов цикл найден.\n")
        return True
    else:
        if DEBUG:
            print("  Не гамильтонов цикл: не все вершины посещены.\n")
        return False


def make_children(min_node):
    if DEBUG:
        print("Создание потомков:")

    row, column, left_penalty = min_node.get_cell_with_max_penalty()
    if row is None or column is None:
        return []
    left_matrix = Node.clone_matrix(min_node.matrix)
    left_matrix[row][column] = math.inf
    left_route = min_node.route[:]
    left_pieces = [piece[:] for piece in min_node.pieces]

    forbidden_row, forbidden_col = None, None
    if min_node.depth == 0:
        forbidden_row, forbidden_col = column, row
    else:
        for piece in left_pieces:
            if piece[-1] == row:
                piece.append(column)
                break
        else:
            left_pieces.append([row, column])

        for piece in left_pieces:
            if len(piece) >= 3:
                if piece[-2] == row and piece[-1] == column:
                    for other_piece in left_pieces:
                        if other_piece != piece and other_piece[0] != piece[-1]:
                            forbidden_row, forbidden_col = piece[-1], other_piece[0]
                            break
                    if forbidden_row is None:
                        forbidden_row, forbidden_col = piece[-1], piece[0]
                    break

        if forbidden_row is None or forbidden_col is None:
            forbidden_row, forbidden_col = column, row

    if forbidden_row is not None and forbidden_col is not None:
        left_matrix[forbidden_row][forbidden_col] = math.inf

    Node.reduce(left_matrix)
    left_bound = min_node.bound + left_penalty
    left_child = Node(left_matrix, left_bound, left_route, left_pieces, parent=min_node, depth=min_node.depth + 1)

    right_matrix = Node.clone_matrix(min_node.matrix)
    right_matrix[column][row] = math.inf
    for i in range(len(right_matrix)):
        right_matrix[row][i] = math.inf
        right_matrix[i][column] = math.inf

    right_route = min_node.route + [(row, column)]
    right_penalty = Node.reduce(right_matrix)
    right_bound = min_node.bound + right_penalty
    right_pieces = [piece[:] for piece in min_node.pieces]
    for piece in right_pieces:
        if piece[-1] == row:
            piece.append(column)
            break
    else:
        right_pieces.append([row, column])

    right_child = Node(right_matrix, right_bound, right_route, right_pieces, parent=min_node, depth=min_node.depth + 1)

    if DEBUG:
        print(f"  Левый потомок: граница {left_bound}, маршрут {left_route}, запрещена дуга ({forbidden_row}, {forbidden_col})")
        print(f"  Правый потомок: граница {right_bound}, маршрут {right_route}")

    return [left_child, right_child]


def little(matrix):
    if DEBUG:
        print("Запуск алгоритма Little:")

    root_matrix = Node.clone_matrix(matrix)
    min_bound = Node.reduce(root_matrix)
    root = Node(root_matrix, min_bound, [], [[0]])
    priority_queue = [root]
    record = None
    nodes_for_graph = []

    while priority_queue:
        if DEBUG:
            print("Выбор узла с минимальной границей:")

        min_node = min(priority_queue, key=lambda node: node.bound)
        priority_queue.remove(min_node)
        nodes_for_graph.append(min_node)

        if DEBUG:
            print(f"  Узел с минимальной границей: граница {min_node.bound}, маршрут {min_node.route}\n")

        if record is not None and record['length'] <= min_node.bound:
            if DEBUG:
                print("Остановка алгоритма: найден оптимальный маршрут.")
            break

        if len(min_node.route) == len(matrix) - 1:
            if DEBUG:
                print("Построение полного маршрута:")

            for row in range(len(matrix)):
                for column in range(len(matrix)):
                    if math.isfinite(min_node.matrix[row][column]):
                        min_node.bound += min_node.matrix[row][column]
                        min_node.route.append((row, column))

            if is_hamiltonian_cycle(min_node.route):
                if record is None or record['length'] > min_node.bound:
                    record = {'length': min_node.bound, 'route': min_node.route}
                    if DEBUG:
                        print(f"Найден оптимальный маршрут: длина {record['length']}, маршрут {record['route']}\n")


        else:
            if DEBUG:
                print("Вычисление нижней оценки:")

            lower_bound = min_node.get_lower_bounds()
            if lower_bound > min_node.bound:
                min_node.bound = lower_bound
                if DEBUG:
                    print(f"  Обновлена граница узла: {min_node.bound}\n")

            left_child, right_child = make_children(min_node)
            priority_queue.append(left_child)
            priority_queue.append(right_child)

    return record, nodes_for_graph


def hierarchy_pos(G, root=None, width=2., vert_gap=0.4, vert_loc=0, xcenter=0.5):

    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))
        else:
            root = random.choice(list(G.nodes))

    def _hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None):


        if pos is None:
            pos = {root: (xcenter, vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)
        if len(children) != 0:
            dx = width / len(children)
            nextx = xcenter - width / 2 - dx / 2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap,
                                     vert_loc=vert_loc - vert_gap, xcenter=nextx, pos=pos,
                                     parent=root)
        return pos

    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)


def visualize_tree(nodes):
    G = nx.DiGraph()
    root_node = None

    for node in nodes:
        G.add_node(id(node), label=f"B:{node.bound:.0f}, R:{node.route}")
        if node.parent:
            G.add_edge(id(node.parent), id(node))
        else:
            root_node = node

    pos = hierarchy_pos(G, root=id(root_node), width=4, vert_gap=0.8)

    labels = {node_id: G.nodes[node_id]['label'] for node_id in G.nodes()}

    plt.figure(figsize=(20, 12))  # Increased figure size
    nx.draw(G, pos, with_labels=False, node_size=2000, node_color='lightblue', font_size=10,
            arrowsize=20)
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=10)

    plt.title("Search Tree", fontsize=16)
    plt.savefig("search_tree.png")
    print("График сохранен в search_tree.png")

