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
            print(f"Создано состояние {root} (корень)")

        for i in range(self.num_patterns):
            if DEBUG:
                print(f"\nДобавление шаблона {i + 1}: '{self.patterns[i]}'")
            current_state = root
            for char in self.patterns[i]:
                if char not in self.transitions[current_state]:
                    new_state = self.state_count
                    self.transitions[current_state][char] = new_state
                    if DEBUG:
                        print(f"Создано состояние {new_state} с переходом из {current_state} по '{char}'")
                    self.state_count += 1
                else:
                    new_state = self.transitions[current_state][char]
                    if DEBUG:
                        print(f"Переход из {current_state} по '{char}' в существующее состояние {new_state}")
                current_state = new_state
            self.output[current_state].append(i)
            if DEBUG:
                print(f"Состояние {current_state} отмечено как конец шаблона {i + 1}")

        if DEBUG:
            print("\nПостроение суффиксных и конечных ссылок:")
        queue = deque()
        for char in self.transitions[root]:
            state = self.transitions[root][char]
            self.fail[state] = root
            self.output_link[state] = state if self.output[state] else -1
            if DEBUG:
                print(f"Состояние {state}: fail = {root}, output_link = {self.output_link[state]}")
            queue.append(state)

        while queue:
            current_state = queue.popleft()
            for char in self.transitions[current_state]:
                next_state = self.transitions[current_state][char]
                queue.append(next_state)

                if DEBUG:
                    print(f"\nОбрабатываем переход из {current_state} по '{char}' в {next_state}")
                fail_state = self.fail[current_state]
                while fail_state != root and char not in self.transitions[fail_state]:
                    if DEBUG:
                        print(f"Состояние {fail_state} не имеет перехода по '{char}', переходим к fail = {self.fail[fail_state]}")
                    fail_state = self.fail[fail_state]
                self.fail[next_state] = self.transitions[fail_state].get(char, root)

                if DEBUG:
                    print(f"Установлена суффиксная ссылка: fail[{next_state}] = {self.fail[next_state]}")

                fail = self.fail[next_state]
                self.output_link[next_state] = fail if self.output[fail] else self.output_link[fail]
                if DEBUG:
                    print(f"Установлена конечная ссылка: output_link[{next_state}] = {self.output_link[next_state]}")

        if DEBUG:
            print("\nПостроенный автомат:")
        for state in range(self.state_count):
            trans = "{" + ", ".join(f"'{k}': {v}" for k, v in self.transitions[state].items()) + "}"
            if DEBUG:
                print(f"Состояние {state}: transitions = {trans}, fail = {self.fail[state]}, "
                      f"output = {self.output[state]}, output_link = {self.output_link[state]}")

    def search(self, text):
        if DEBUG:
            print("\nПроцесс поиска в тексте:", text)
        current_state = 0
        results = []
        for i in range(len(text)):
            char = text[i]
            if DEBUG:
                print(f"\nПозиция {i + 1}: символ '{char}', текущее состояние = {current_state}")
            while current_state != 0 and char not in self.transitions[current_state]:
                if DEBUG:
                    print(f"Нет перехода по '{char}' из {current_state}, переходим к fail = {self.fail[current_state]}")
                current_state = self.fail[current_state]

            if char in self.transitions[current_state]:
                next_state = self.transitions[current_state][char]
                if DEBUG:
                    print(f"Переход по '{char}' из {current_state} в {next_state}")
                current_state = next_state
            else:
                if DEBUG:
                    print(f"Нет перехода по '{char}' из {current_state}, переходим в корень (0)")
                current_state = 0

            temp_state = current_state
            visited = set()
            while temp_state != -1 and temp_state not in visited:
                visited.add(temp_state)
                if self.output[temp_state]:
                    for pattern_index in self.output[temp_state]:
                        pos = i - len(self.patterns[pattern_index]) + 2

                        if DEBUG:
                            print(f"Найдено вхождение шаблона {pattern_index + 1} на позиции {pos}")
                        results.append((pos, pattern_index + 1))
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

def find_pattern_with_wildcards(T, P, wildcard):
    substrings = [s for s in P.split(wildcard) if s]
    if not substrings:
        return [], 0, set()

    k = len(substrings)
    start_positions = []
    pos = 0
    for i, sub in enumerate(P.split(wildcard)):
        if sub:
            start_positions.append(pos)
        pos += len(sub) + (1 if i < len(P.split(wildcard)) - 1 else 0)

    ac = AhoCorasick(substrings)
    matches = ac.search(T)

    n = len(T)
    C = [0] * n

    for pos, pattern_idx in matches:
        start_pos_in_P = start_positions[pattern_idx - 1]
        text_start = pos - start_pos_in_P - 1
        if text_start >= 0:
            C[text_start] += 1

    result = []
    for i in range(n):
        if C[i] == k and i + len(P) - 1 < n:
            valid = True
            for j in range(len(P)):
                text_pos = i + j
                if P[j] != wildcard and T[text_pos] != P[j]:
                    valid = False
                    break
            if valid:
                result.append(i + 1)

    vertex_count = ac.get_vertex_count()
    overlapping = ac.find_overlapping_patterns(T, matches)
    return sorted(result), vertex_count, overlapping


if __name__ == "__main__":
    T = input().strip()
    P = input().strip()
    wildcard = input().strip()

    occurrences, vertex_count, overlapping = find_pattern_with_wildcards(T, P, wildcard)

    print(f"Количество вершин в автомате: {vertex_count}")
    if occurrences:
        for pos in occurrences:
            print(pos)
    else:
        print(-1)
    if overlapping:
        print("Шаблоны с пересечениями:", ", ".join(str(p) for p in sorted(overlapping)))
    else:
        print("Шаблоны с пересечениями отсутствуют")