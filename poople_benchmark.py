from poople_solver_base import PoopleSolverBase
from tqdm import tqdm
import json
from pathlib import Path
from datetime import datetime

def get_date():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


class PoopleSolverBenchmark(PoopleSolverBase):
    def __init__(self) -> None:
        super().__init__()
        self.word_dist_dict = self._load_word_dist()

    def _load_word_dist(self) -> dict[str, int]:
        with open("words/wordDist.txt", "r") as f:
            content = f.read()
        result = dict()
        for word_dist in content.split("\n"):
            if not word_dist: continue
            word, dist = word_dist.split(",")
            dist = int(dist)
            result[word] = dist
        return result

    def save_statistics(self):
        path = Path("output/statistics")
        path.mkdir(parents=True, exist_ok=True)
        with open(path / f"{get_date()}.json", "w") as f:
            json.dump(self.benchmark_statistics, f, indent=4)
        print("Statistics saved.")

    def print_statistics(self):
        print("===== STATISTICS REPORT =====")
        print(f"Match: {self.words_benchmarked - len(self.solver_wins) - len(self.official_wins)}/{self.words_benchmarked}")
        print(f"Solver wins: {len(self.solver_wins)}/{self.words_benchmarked}")
        print(f"-> Solver win list: {self.solver_wins}")
        print(f"Official wins: {len(self.official_wins)}/{self.words_benchmarked}")
        print(f"-> Official win list: {self.official_wins}")

    def benchmark(self):
        try:
            self.benchmark_statistics = dict()
            self.words_benchmarked = 0
            self.solver_wins = []
            self.official_wins = []
            self.target_word = "POOP"
            for word in self.word_dist_dict:
                self.start_word = word
                solutions = self.solve(print_progress=False, fast=True)

                solver_guesses_taken = len(solutions[0]) - 1
                official_guesses_taken = self.word_dist_dict[word]
                self.benchmark_statistics[word] = {
                    "official": official_guesses_taken,
                    "solver": solver_guesses_taken
                }
                print(f"{self.words_benchmarked+1}/{len(list(self.word_dist_dict))}: ", end="")
                if official_guesses_taken == solver_guesses_taken:
                    print(f"{word} takes {solver_guesses_taken} guesses, which matches with the official optimal guesses.")
                elif official_guesses_taken < solver_guesses_taken:
                    print(f"For word {word}, solver takes {solver_guesses_taken} guesses, but official optimal guesses is {official_guesses_taken}, which is more. Official wins.")
                    self.official_wins.append(word)
                else:
                    print(f"For word {word}, solver takes {solver_guesses_taken} guesses, but official optimal guesses is {official_guesses_taken}, which is less. Solver wins.")
                    self.solver_wins.append(word)
                self.words_benchmarked += 1
        except KeyboardInterrupt:
            pass  # intended way of terminating
        finally:
            self.print_statistics()
            self.save_statistics()


if __name__ == "__main__":
    benchmarker = PoopleSolverBenchmark()
    benchmarker.benchmark()
