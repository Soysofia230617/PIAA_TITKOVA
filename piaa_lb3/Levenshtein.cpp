#include <iostream>
#include <vector>
#include <algorithm>
#include <map>
using namespace std;

int levenshtein_distance(const string& S, const string& T,
                         const map<char, int>& special_replace_costs,
                         const map<char, int>& special_insert_costs,
                         bool debug = false) {
    int n = S.size(), m = T.size();
    vector<vector<int>> dp(n + 1, vector<int>(m + 1));

    for (int j = 0; j <= m; ++j) {
        dp[0][j] = j;
    }
    for (int i = 0; i <= n; ++i) {
        dp[i][0] = i;
    }

    if (debug) {
        cout << "Начальная таблица (до заполнения):" << endl;
        for (int i = 0; i <= n; ++i) {
            for (int j = 0; j <= m; ++j) {
                cout << dp[i][j] << " ";
            }
            cout << endl;
        }
        cout << endl;
    }

    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= m; ++j) {
            if (debug) {
                cout << "Заполняем dp[" << i << "][" << j << "], сравниваем S[" << i-1 << "] = '" << S[i-1]
                     << "' с T[" << j-1 << "] = '" << T[j-1] << "': ";
            }

            if (S[i - 1] == T[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1];
                if (debug) {
                    cout << "Совпадение, dp[" << i << "][" << j << "] = dp[" << i-1 << "][" << j-1 << "] = " << dp[i][j] << endl;
                }
            } else {
                int del_cost = dp[i - 1][j] + 1;
                int ins_cost = dp[i][j - 1] + (special_insert_costs.count(T[j - 1]) ? special_insert_costs.at(T[j - 1]) : 1);
                int sub_cost = dp[i - 1][j - 1] + (special_replace_costs.count(S[i - 1]) ? special_replace_costs.at(S[i - 1]) : 1);

                dp[i][j] = min({del_cost, ins_cost, sub_cost});
                if (debug) {
                    cout << "Нет совпадения, варианты: удаление=" << del_cost << ", вставка=" << ins_cost
                         << ", замена=" << sub_cost << ", dp[" << i << "][" << j << "] = " << dp[i][j] << endl;
                }
            }

            if (debug) {
                cout << "Таблица после заполнения dp[" << i << "][" << j << "]:" << endl;
                for (int x = 0; x <= n; ++x) {
                    for (int y = 0; y <= m; ++y) {
                        cout << dp[x][y] << " ";
                    }
                    cout << endl;
                }
                cout << endl;
            }
        }
    }

    if (debug) {
        cout << "Итоговое расстояние: " << dp[n][m] << endl;
    }
    return dp[n][m];
}

int main() {
    string S, T;
    map<char, int> special_replace_costs;
    map<char, int> special_insert_costs;

    cout << "Введите первую строку (S): ";
    cin >> S;
    cout << "Введите вторую строку (T): ";
    cin >> T;

    int num_replace;
    cout << "Введите количество особо заменяемых символов: ";
    cin >> num_replace;
    for (int i = 0; i < num_replace; ++i) {
        char symbol;
        int cost;
        cout << "Введите " << i + 1 << "-й особо заменяемый символ: ";
        cin >> symbol;
        cout << "Введите стоимость замены для символа '" << symbol << "': ";
        cin >> cost;
        special_replace_costs[symbol] = cost;
    }

    int num_insert;
    cout << "Введите количество особо добавляемых символов: ";
    cin >> num_insert;
    for (int i = 0; i < num_insert; ++i) {
        char symbol;
        int cost;
        cout << "Введите " << i + 1 << "-й особо добавляемый символ: ";
        cin >> symbol;
        cout << "Введите стоимость вставки для символа '" << symbol << "': ";
        cin >> cost;
        special_insert_costs[symbol] = cost;
    }

    int result = levenshtein_distance(S, T, special_replace_costs, special_insert_costs, true);
    cout << "Расстояние Левенштейна: " << result << endl;

    return 0;
}