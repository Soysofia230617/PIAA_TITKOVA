from collections import deque

DEBUG = False

class AhoCorasick:
    def __init__(self, patterns):
        self.patterns = [p for p in patterns if p]
        self.num_patterns = len(self.patterns)
        self.max_states = sum(len(p) for p in self.patterns) + 1
        self.transitions = [{} for _ in range(self.max_states)]
        self.output = [[] for _ in range(self.max_states)]
        self.fail = [0] * self.max_states
        self.output_link = [-1] * self.max_states
        self.state_count = 0
        self.build_automaton()

    def build_automaton(self):
        root = 0
        self.fail[root] = root
        self.output_link[root] = -1
        self.state_count = 1

        if DEBUG:
            print("Построение бора:")
        for i in range(self.num_patterns):
            current_state = root
            for char in self.patterns[i]:
                if char not in self.transitions[current_state]:
                    self.transitions[current_state][char] = self.state_count
                    if DEBUG:
                        print(f"Добавлено ребро из состояния {current_state} в состояние {self.state_count} по символу '{char}'")
                    self.state_count += 1
                current_state = self.transitions[current_state][char]
            self.output[current_state].append(i)
            if DEBUG:
                print(f"Добавлен шаблон {i} в состояние {current_state}")

        if DEBUG:
            print("\nПостроение автомата:")
        queue = deque()
        for char in self.transitions[root]:
            state = self.transitions[root][char]
            self.fail[state] = root
            self.output_link[state] = state if self.output[state] else -1
            queue.append(state)
            if DEBUG:
                print(f"Установлен fail-переход для состояния {state} в состояние {root}")

        while queue:
            current_state = queue.popleft()
            for char in self.transitions[current_state]:
                next_state = self.transitions[current_state][char]
                queue.append(next_state)

                fail_state = self.fail[current_state]
                while fail_state != root and char not in self.transitions[fail_state]:
                    fail_state = self.fail[fail_state]
                self.fail[next_state] = self.transitions[fail_state].get(char, root)
                if DEBUG:
                    print(f"Установлен fail-переход для состояния {next_state} в состояние {self.fail[next_state]}")

                fail = self.fail[next_state]
                self.output_link[next_state] = fail if self.output[fail] else self.output_link[fail]
                if DEBUG:
                    print(f"Установлен output-переход для состояния {next_state} в состояние {self.output_link[next_state]}")

        if DEBUG:
            print("\nПостроенный автомат:")
            for state in range(self.state_count):
                print(f"Состояние {state}:")
                print(f"  Переходы: {self.transitions[state]}")
                print(f"  Выходы: {self.output[state]}")
                print(f"  Fail-переход: {self.fail[state]}")
                print(f"  Output-переход: {self.output_link[state]}")

    def search(self, text):
        current_state = 0
        results = []
        if DEBUG:
            print("\nПроцесс поиска:")
        for i in range(len(text)):
            char = text[i]
            while current_state != 0 and char not in self.transitions[current_state]:
                current_state = self.fail[current_state]
                if DEBUG:
                    print(f"Переход по fail-ссылке в состояние {current_state}")

            if char in self.transitions[current_state]:
                current_state = self.transitions[current_state][char]
                if DEBUG:
                    print(f"Переход в состояние {current_state} по символу '{char}'")
            else:
                current_state = 0
                if DEBUG:
                    print(f"Символ '{char}' не найден, переход в корневое состояние")

            temp_state = current_state
            visited = set()
            while temp_state != -1 and temp_state not in visited:
                visited.add(temp_state)
                if self.output[temp_state]:
                    for pattern_index in self.output[temp_state]:
                        pos = i - len(self.patterns[pattern_index]) + 2
                        results.append((pos, pattern_index + 1))
                        if DEBUG:
                            print(f"Найден шаблон {pattern_index + 1} на позиции {pos}")
                temp_state = self.output_link[temp_state]
        return sorted(results)

    def get_vertex_count(self):
        return self.state_count

    def find_overlapping_patterns(self, text, results):
        if not results:
            return set()

        occurrences = [(pos, pos + len(self.patterns[pattern_num - 1]) - 1, pattern_num)
                       for pos, pattern_num in results]
        overlap_patterns = set()

        for i in range(len(occurrences)):
            start1, end1, pattern1 = occurrences[i]
            for j in range(len(occurrences)):
                if i != j:
                    start2, end2, pattern2 = occurrences[j]
                    if start1 <= end2 and start2 <= end1:
                        overlap_patterns.add(pattern1)
                        overlap_patterns.add(pattern2)
        return overlap_patterns

def process_search(T, patterns):
    automaton = AhoCorasick(patterns)
    results = automaton.search(T)
    vertex_count = automaton.get_vertex_count()
    overlapping = automaton.find_overlapping_patterns(T, results)
    return results, vertex_count, overlapping

if __name__ == "__main__":
    T = input().strip()
    n = int(input())
    patterns = [input().strip() for _ in range(n)]

    results, vertex_count, overlapping = process_search(T, patterns)

    print(f"\nКоличество вершин в автомате: {vertex_count}")
    for pos, pattern_num in results:
        print(pos, pattern_num)
    if overlapping:
        print("Шаблоны с пересечениями:", ", ".join(str(p) for p in sorted(overlapping)))
    else:
        print("Шаблоны с пересечениями отсутствуют")