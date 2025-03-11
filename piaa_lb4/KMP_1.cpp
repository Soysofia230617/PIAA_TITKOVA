#include <iostream>
#include <vector>
#include <string>

using namespace std;
bool DEBUG = true;

vector<int> compute_prefix_function(const string& P) {
    int m = P.length();
    vector<int> pi(m, 0);
    int k = 0;

    for (int i = 1; i < m; ++i) {
        while (k > 0 && P[k] != P[i]) {
            k = pi[k - 1];
        }
        if (P[k] == P[i]) {
            k++;
        }
        pi[i] = k;

        if (DEBUG) {
            cout << "pi[" << i << "] = " << pi[i] << endl;
        }
    }

    return pi;
}

vector<int> kmp_search(const string& T, const string& P) {
    int n = T.length();
    int m = P.length();

    if (m == 0 || m > n) {
        return {};
    }

    vector<int> pi = compute_prefix_function(P);
    vector<int> occurrences;
    int q = 0;

    for (int i = 0; i < n; ++i) {
        while (q > 0 && P[q] != T[i]) {
            q = pi[q - 1];
        }
        if (P[q] == T[i]) {
            q++;
        }
        if (q == m) {
            int start_index = i - m + 1;
            occurrences.push_back(start_index);
            q = pi[q - 1];

            if (DEBUG) {
                cout << "Found occurrence at index: " << start_index << endl;
            }
        }
    }

    return occurrences;
}

int main() {
    string P, T;
    cin >> P >> T;

    if (DEBUG) {
        cout << "Pattern: " << P << endl;
        cout << "Text: " << T << endl;
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