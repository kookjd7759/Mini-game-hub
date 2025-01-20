#include <iostream>
#include <random>
#include <thread>
#include <chrono>

using namespace std;

class Game {
private:
	int size = 0, sum = 0;

public:
	Game() { cin >> size; }
	void play() {
		random_device rd; mt19937 gen(rd());
		uniform_real_distribution<> dis(2.5, 6.0);

		for (int i = 1, n; i <= size; ++i) {
			cin >> n;

			double waitTime(dis(gen));
			this_thread::sleep_for(chrono::duration<double>(waitTime));

			cout << "click\n";
			auto start = chrono::high_resolution_clock::now();

			cin >> n;

			auto end = std::chrono::high_resolution_clock::now();
			auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
			sum += (int)duration.count();
			cout << duration.count() / 1000 << "\n";
		}
		cout << sum / size / 1000 << "\n";
	}
};

int main() {
	Game game;
	game.play();
}