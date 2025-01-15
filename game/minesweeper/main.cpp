#include <iostream>
#include <cassert>
#include <random>
#include <set>

using namespace std;

#define Fori(x) for (int i = 0; i < x; ++i)
#define Forj(x) for (int j = 0; j < x; ++j)
#define Fork(x) for (int k = 0; k < x; ++k)

int dir[8][2] = { {-1, 0}, {1, 0}, {0, -1}, {0, 1}, {-1, -1}, {-1, 1}, {1, -1}, {1, 1} };

enum Cell_info : int {
    ZERO, ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, MINE
};
inline static void operator++(Cell_info& s) { s = Cell_info(int(s) + 1); }

enum Mask_info : int {
    OPEN, CLOSE, FLAG
};

enum Level : int {
    BEGINNER, INTERMEDIATE, ADVANCED
};

struct Level_data {
    int x = 18, y = 14, mine_cnt = 40; // default Level is INTERMEDIATE
    Level_data() {}
    Level_data(Level lev) {
        assert(BEGINNER <= lev && lev <= ADVANCED);

        if (lev == BEGINNER) { x = 8, y = 10, mine_cnt = 10; }
        else if (lev == INTERMEDIATE) { x = 14, y = 18, mine_cnt = 40; }
        else { x = 20, y = 24, mine_cnt = 99; }
    }
};



class Minesweeper {
private:
    Cell_info** board;
    Mask_info** mask;
    Level_data  data;

    int mask_cnt = 0;

    bool isFirst    = true;
    bool isGameOver = false;

    inline bool isOk(int x, int y) const { return (0 <= x && x < data.x && 0 <= y && y < data.y); }
    inline bool isWin() const { return mask_cnt == data.mine_cnt; }
    inline int  dist(int aX, int aY, int bX, int bY) const { return abs(aX - bX) + abs(aY - bY); }

    void create_board(int x, int y) {
        // Create random mines position
        random_device rd; mt19937 gen(rd());
        uniform_int_distribution<> dis(0, data.x * data.y - 1);

        set<int> s;
        while (s.size() < data.mine_cnt) {
            int rand = dis(gen);
            if (dist(x, y, rand / data.y, rand % data.y) <= 2 || s.count(rand)) continue;
            s.insert(rand);
        }

        // Place the mines 
        for (const int i : s) board[i / data.y][i % data.y] = MINE;

        // Count adjacent mines
        Fori(data.x) Forj(data.y) if (board[i][j] == MINE) {
            Fork(8) {
                int adj_x = i + dir[k][0];
                int adj_y = j + dir[k][1];
                if (isOk(adj_x, adj_y) && board[adj_x][adj_y] != MINE) ++board[adj_x][adj_y];
            }
        }
    }
    void DFS_open(int x, int y) {
        mask[x][y] = OPEN;
        --mask_cnt;

        if (board[x][y] >= ONE) return;

        Fori(8) {
            int adj_x = x + dir[i][0];
            int adj_y = y + dir[i][1];
            if (isOk(adj_x, adj_y) && mask[adj_x][adj_y] == CLOSE) DFS_open(adj_x, adj_y);
        }
    }
    void click(int x, int y, bool isFlag) {
        if (!isOk(x, y) || isGameOver) return;

        if (isFlag) {
            if (mask[x][y] != OPEN) mask[x][y] = (mask[x][y] == FLAG ? CLOSE : FLAG);
            return;
        }

        if (isFirst) {
            create_board(x, y);
            isFirst = false;
        }

        if (mask[x][y] != CLOSE) return;
        if (board[x][y] == MINE) {
            isGameOver = true;
            return;
        }

        DFS_open(x, y);

        if (isWin()) isGameOver = true;
    }
    void SEND() {
        Fori(data.x) Forj(data.y) {
            if (mask[i][j] != OPEN) cout << (mask[i][j] == CLOSE ? 'c' : 'f');
            else cout << board[i][j];
        }
        cout << "\n";
    }

public:
    Minesweeper(Level lev) {
        data = Level_data(lev);

        board = new Cell_info * [data.x];
        Fori(data.x) board[i] = new Cell_info[data.y];
        Fori(data.x) Forj(data.y) board[i][j] = ZERO;

        mask = new Mask_info * [data.x];
        Fori(data.x) mask[i] = new Mask_info[data.y];
        Fori(data.x) Forj(data.y) mask[i][j] = CLOSE;

        mask_cnt = data.x * data.y;
    }
    ~Minesweeper() {
        Fori(data.x) delete[] board[i]; delete[] board;
        Fori(data.x) delete[] mask[i];  delete[] mask;
    }

    void play() {
        while (!isGameOver) {
            int x, y, f; cin >> x >> y >> f;
            click(x, y, (bool)f);
            SEND();
        }

        cout << (isWin() ? "CLEAR !!\n" : "LOSE ..\n");
    }
};

int main() {
    int level_int; cin >> level_int;
    Minesweeper game((Level)level_int);
    game.play();
}