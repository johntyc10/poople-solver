import copy

class PoopleSolver():
    def __init__(self) -> None:
        self.all_words = self._load_all_words()
        self.word_frequency_dict = self._load_word_frequency()

    def _load_all_words(self) -> list[str]:
        with open("words/wordDist.txt", "r") as f:
            content = f.read()
        return [word_dist.split(",")[0] for word_dist in content.split("\n") if word_dist]

    def _load_word_frequency(self) -> dict[str, int]:
        with open("words/wordFrequency.txt", "r") as f:
            content = f.read()
        result = dict()
        for word_freq in content.split("\n"):
            if not word_freq: continue
            word, freq = word_freq.split(",")
            freq = int(freq)
            result[word] = freq
        return result

    def is_in_all_words(self, word: str) -> bool:
        return word in self.all_words

    def is_exactly_one_letter_apart(self, word1: str, word2: str) -> bool:
        counter = 0
        for i in range(len(word1)):
            if word1[i] != word2[i]:
                counter += 1
        return counter == 1

    def get_possible_next_words(self, word: str) -> list[str]:
        return [w for w in self.all_words if self.is_exactly_one_letter_apart(word, w)]

    def solve(self) -> list[list[str]]:  # bfs search
        if self.start_word == self.target_word:
            return [self.target_word]

        tree = [[self.start_word]]
        visited = {self.start_word}
        last_visited = set()
        solutions = []  # may have more than one solution
        layer = 1
        while not solutions:
            print(f"-> Looking through layer {layer} ({len(tree)} words)...")
            new_tree = []
            for word_history in tree:
                possible_next_words = self.get_possible_next_words(word_history[-1])
                if self.target_word in possible_next_words:
                    solutions.append(word_history + [self.target_word])
                for w in possible_next_words:
                    if w not in visited:
                        new_tree.append(word_history + [w])
                    last_visited.add(w)

            visited = visited.union(last_visited)
            last_visited = set()
            tree = copy.deepcopy(new_tree)
            layer += 1

        return solutions

    def get_sol_freq_sum(self, solution: list[str]) -> int:
        _sum = 0
        for word in solution:
            _sum += self.word_frequency_dict[word]
        return _sum

    def get_most_human_solution(self, solutions: list[list[str]]) -> list[str]:
        freq_sums = []
        for sol in solutions:
            freq_sums.append(self.get_sol_freq_sum(sol))

        return solutions[freq_sums.index(max(freq_sums))]

    def play(self):
        print("===== POOPLE SOLVER =====")
        print("A script that uses brute force method to solve poople (guaranteed best solution)")
        print()

        # User input
        prompt_message = "Input start word: "
        start_word_input = input(prompt_message).upper()
        while not self.is_in_all_words(start_word_input):
            print("Word is not in word list. Please try again.")
            start_word_input = input(prompt_message).upper()
        self.start_word = start_word_input
        print(f"\"{self.start_word}\" is chosen.")

        prompt_message = "Input target word (enter for \"POOP\"): "
        target_word_input = input(prompt_message).upper()
        while not self.is_in_all_words(target_word_input) and target_word_input:
            print("Word is not in word list. Please try again.")
            target_word_input = input(prompt_message).upper()
        self.target_word = target_word_input or "POOP"
        print(f"\"{self.target_word}\" is chosen.")

        # Start solving
        print("Solving poople...")

        solutions = self.solve()
        print(f"{len(solutions)} solution(s) found.")
        print("Most human solution:")
        most_human_sol = self.get_most_human_solution(solutions)
        for i in range(len(most_human_sol)):
            print(f"{i}: {most_human_sol[i]}")
        print(f"The best solution(s) takes {len(most_human_sol) - 1} guesses.")


if __name__ == "__main__":
    solver = PoopleSolver()
    solver.play()
