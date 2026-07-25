import copy

class PoopleSolver():
    def __init__(self) -> None:
        self.all_words = self._load_all_words()

    def _load_all_words(self) -> list[str]:
        with open("words/wordDist.txt", "r") as f:
            content = f.read()
        return [word_dist.split(",")[0] for word_dist in content.split("\n")]

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

    def solve(self) -> list[list[str]]:
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
        print(f"{len(solutions)} solutions found.")
        print("First solution:")
        for i in range(len(solutions[0])):
            print(f"{i}: {solutions[0][i]}")
        print(f"The best solution takes {len(solutions[0]) - 1} guesses.")


if __name__ == "__main__":
    solver = PoopleSolver()
    solver.play()
