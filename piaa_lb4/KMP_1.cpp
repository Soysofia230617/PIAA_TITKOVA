#include <iostream>
#include <vector>
#include <string>

using namespace std;
bool DEBUG = true;

vector<int> compute_prefix_function(const string& P) {
    int m = P.length();
    vector<int> pi(m, 0);
    int k = 0;

    if (DEBUG) {
        cout << "Вычисление префикс-функции для образца: " << P << endl;
        cout << "Длина образца: " << m << endl;
    }

    for (int i = 1; i < m; ++i) {
        if (DEBUG) {
            cout << "Обрабатываем позицию i = " << i << ", текущее k = " << k << endl;
            cout << "Сравниваем P[" << k << "] = '" << P[k] << "' с P[" << i << "] = '" << P[i] << "'" << endl;
        }

        while (k > 0 && P[k] != P[i]) {
            if (DEBUG) {
                cout << "Несовпадение, уменьшаем k с " << k << " до pi[" << (k - 1) << "] = ";
            }
            k = pi[k - 1];
            if (DEBUG) {
                cout << k << endl;
            }
        }

        if (P[k] == P[i]) {
            k++;
            if (DEBUG) {
                cout << "Совпадение найдено, увеличиваем k до " << k << endl;
            }
        }

        pi[i] = k;
        if (DEBUG) {
            cout << "pi[" << i << "] = " << pi[i] << endl;
        }
    }

    if (DEBUG) {
        cout << "Префикс-функция завершена: ";
        for (int i = 0; i < m; ++i) {
            cout << pi[i] << " ";
        }
        cout << endl;
    }

    return pi;
}

vector<int> kmp_search(const string& T, const string& P) {
    int n = T.length();
    int m = P.length();

    if (DEBUG) {
        cout << "\nЗапуск поиска KMP" << endl;
        cout << "Текст: " << T << " (длина = " << n << ")" << endl;
        cout << "Образец: " << P << " (длина = " << m << ")" << endl;
    }

    if (m == 0 || m > n) {
        if (DEBUG) {
            cout << "Недопустимая длина образца, возвращаем пустой результат" << endl;
        }
        vector<int> empty;
        return empty;
    }

    vector<int> pi = compute_prefix_function(P);
    vector<int> occurrences;
    int q = 0;

    for (int i = 0; i < n; ++i) {
        if (DEBUG) {
            cout << "\nОбрабатываем позицию текста i = " << i << ", текущее q = " << q << endl;
            cout << "Сравниваем T[" << i << "] = '" << T[i] << "' с P[" << q << "] = '" << P[q] << "'" << endl;
        }

        while (q > 0 && P[q] != T[i]) {
            if (DEBUG) {
                cout << "Несовпадение, уменьшаем q с " << q << " до pi[" << (q - 1) << "] = ";
            }
            q = pi[q - 1];
            if (DEBUG) {
                cout << q << endl;
            }
        }

        if (P[q] == T[i]) {
            q++;
            if (DEBUG) {
                cout << "Совпадение найдено, увеличиваем q до " << q << endl;
            }
        }

        if (q == m) {
            int start_index = i - m + 1;
            occurrences.push_back(start_index);
            if (DEBUG) {
                cout << "Полное совпадение найдено! Вхождение на индексе: " << start_index << endl;
            }
            q = pi[q - 1];
            if (DEBUG) {
                cout << "Сбрасываем q до pi[" << (m - 1) << "] = " << q << endl;
            }
        }
    }

    if (DEBUG) {
        cout << "\nПоиск KMP завершён. Найдено вхождений: " << occurrences.size() << endl;
    }

    return occurrences;
}

int main() {
    string P, T;
    cin >> P >> T;

    if (DEBUG) {
        cout << "Получен ввод:" << endl;
        cout << "Образец: " << P << endl;
        cout << "Текст: " << T << endl;
    }

    vector<int> result = kmp_search(T, P);

    if (!result.empty()) {
        for (size_t i = 0; i < result.size(); ++i) {
            if (i > 0) {
                cout << ",";
            }
            cout << result[i];
        }
        cout << endl;
    } else {
        cout << -1 << endl;
    }

    return 0;
}
