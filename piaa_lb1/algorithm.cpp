#include <algorithm>
#include <iostream>
#include <vector>
#include <tuple>

using namespace std;

struct Square {
    int x, y, h;
};

int cnt = 0;
bool DEBUG=0;

void print_solution_matrix(int n, const vector<tuple<int, int, int>>& result) {

    vector<vector<int>> matrix(n, vector<int>(n, 0));
    int num = 0;

    for (const auto& s : result) {
        num += 1;
        int x, y, h;
        tie(x, y, h) = s;

        for (int i = x; i < x + h; ++i) {
            for (int j = y; j > y - h; --j) {
                matrix[i][j] = num;
            }
        }
    }

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {

            if (matrix[i][j] < 10) {
                cout << matrix[i][j] << "  ";
            } else {
                cout << matrix[i][j] << " ";
            }
        }
        cout << endl;
    }
}

void rec(vector<int>& diagram, vector<int> marks, vector<Square>& ans) {
    static vector<Square> stack = {};
    if (DEBUG==1){
        cnt += 1;
        cout << "IT #" << cnt << '\n';

        for (Square s : stack) {
            cout << '\t' << s.x << ' ' << s.y << ' ' << s.h << '\n';
        }
    }

    if (*max_element(diagram.begin(), diagram.end()) == 0) {
        if (ans.empty() || ans.size() > stack.size()) {
            ans = stack;
        }
        return;
    }

    int corners = (diagram.back() != 0);
    for (int i = 0; i < diagram.size() - 1; ++i) {
        corners += (diagram[i] != diagram[i + 1]);
    }

    if (!ans.empty() && stack.size() + corners >= ans.size()) {
        return;
    }

    for (int i = 0; i < diagram.size(); ++i) {
        int j = diagram[i] - 1;
        int max_h = 0;
        while (i - max_h >= 0 && diagram[i - max_h] == diagram[i]) {
            ++max_h;
        }
        if (i == diagram.size() - 1) {
            max_h = min(max_h, diagram[i]);
        } else {
            max_h = min(max_h, diagram[i] - diagram[i + 1]);
        }
        max_h = min(max_h, (int)diagram.size() - 1);
        for (int k = 0; k < max_h; ++k) {
            diagram[i - k] -= max_h;
        }
        for (int h = max_h; h >= 1; --h) {
            if (h > marks[i]) {
                stack.push_back({i + 1 - h, j, h});
                int x = marks[i];
                marks[i] = -1;
                rec(diagram, marks, ans);
                marks[i] = x;
                stack.pop_back();
            }
            diagram[i + 1 - h] += h;
            for (int k = 0; k < h - 1; ++k) {
                ++diagram[i - k];
            }
        }
        marks[i] = max_h;
    }
}

int main() {
    int n;
    cin >> n;
    vector<Square> ans;
    vector<int> hs;

    for (int h = (n + 1) / 2; h < min((n + 1) / 2 + 5, n); ++h) {
        hs.push_back(h);
    }

    if (n > 20) {
        if (n % 2 == 0) {
            hs = {n / 2};
        } else if (n % 3 == 0) {
            hs = {2 * n / 3};
        } else if (n == 25 || n == 27) {
            hs = {(n + 1) / 2 + 2};
        } else if (n == 37) {
            hs = {(n + 1) / 2 + 1};
        } else {
            hs = {(n + 1) / 2 + 1, (n + 1) / 2 + 3};
        }
    }

    for (int h : hs) {
        vector<int> diagram(n, n);
        vector<Square> cur_ans;

        for (int i = 0; i < h; ++i) {
            diagram[n - 1 - i] -= h;
        }
        for (int i = 0; i < n - h; ++i) {
            diagram[i] -= n - h;
        }
        for (int i = 0; i < n - h; ++i) {
            diagram[n - 1 - i] -= n - h;
        }


        rec(diagram, vector<int>(n, -1), cur_ans);

        cur_ans.push_back({n - h, n - 1, h});
        cur_ans.push_back({0, n - 1, n - h});
        cur_ans.push_back({n - 1 - (n - h) + 1, n - h - 1, n - h});

        if (ans.empty() || ans.size() > cur_ans.size()) {
            ans = cur_ans;
        }
    }



    cout << ans.size() << endl;
    for (Square s : ans) {
        cout << s.x + 1 << ' ' << s.y - s.h + 2 << ' ' << s.h << endl;
    }

    vector<tuple<int, int, int>> result;
    for (const auto& s : ans) {
        result.push_back(make_tuple(s.x, s.y, s.h));
    }

    if (DEBUG==1){
        cout << "Total iterations: " << cnt << '\n';
        print_solution_matrix(n, result);
    }

    return 0;
}
