from poople_solver_base import PoopleSolverBase


class PoopleSolver(PoopleSolverBase):
    def __init__(self) -> None:
        super().__init__()

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
