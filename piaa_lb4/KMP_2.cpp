#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

using namespace std;

const bool DEBUG = true;

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

int kmp_search(const string& T, const string& P) {
    int n = T.length();
    int m = P.length();

    if (m == 0 || m > n) {
        if (DEBUG) {
            cout << "Substring is empty or longer than the text. Returning -1." << endl;
        }
        return -1;
    }

    vector<int> pi = compute_prefix_function(P);
    int q = 0;

    for (int i = 0; i < n; ++i) {
        if (DEBUG) {
            cout << "Checking T[" << i << "] = " << T[i] << " against P[" << q << "] = " << P[q] << endl;
        }

        while (q > 0 && P[q] != T[i]) {
            q = pi[q - 1];
            if (DEBUG) {
                cout << "Mismatch. New q = " << q << endl;
            }
        }
        if (P[q] == T[i]) {
            q++;
            if (DEBUG) {
                cout << "Match. New q = " << q << endl;
            }
        }
        if (q == m) {
            if (DEBUG) {
                cout << "Full match found at index: " << i - m + 1 << endl;
            }
            return i - m + 1;
        }
    }

    if (DEBUG) {
        cout << "No match found. Returning -1." << endl;
    }
    return -1;
}

int main() {
    string A, B;
    cin >> A >> B;

    if (DEBUG) {
        cout << "Input strings: A = " << A << ", B = " << B << endl;
    }

    if (A.length() != B.length()) {
        if (DEBUG) {
            cout << "Lengths of A and B are different. Returning -1." << endl;
        }
        cout << -1 << endl;
        return 0;
    }

    string sorted_A = A;
    string sorted_B = B;
    sort(sorted_A.begin(), sorted_A.end());
    sort(sorted_B.begin(), sorted_B.end());

    if (sorted_A != sorted_B) {
        if (DEBUG) {
            cout << "A and B contain different characters. Returning -1." << endl;
        }
        cout << -1 << endl;
        return 0;
    }

    string AA = A + A;
    if (DEBUG) {
        cout << "Constructed AA: " << AA << endl;
    }
    int index = kmp_search(AA, B);

    if (index >= 0 && index < A.length()) {
        if (DEBUG) {
            cout << "Valid shift found at index: " << index << endl;
        }
        cout << index << endl;
    } else {
        if (DEBUG) {
            cout << "No valid shift found. Returning -1." << endl;
        }
        cout << -1 << endl;
    }

    return 0;
}