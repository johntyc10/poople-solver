import copy


class PoopleSolverBase():
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

    def solve(self, print_progress: bool = True, fast: bool = False) -> list[list[str]]:  # bfs search
        """
        Solves poople.
        print_progress: print progress if True, not printing progress otherwise.
        fast: only finds one route/solution (which is faster) if True, finds all possible routes otherwise.
        Returns the sequence from start word to target word inclusive.
        """
        if self.start_word == self.target_word:
            return [[self.target_word]]

        tree = [[self.start_word]]
        visited = {self.start_word}
        if not fast:
            last_visited = set()  # visited words in current layer
        solutions = []  # may have more than one solution
        layer = 1
        while not solutions:
            if print_progress:
                print(f"-> Looking through layer {layer} ({len(tree)} words)...")
            new_tree = []
            for word_history in tree:
                possible_next_words = self.get_possible_next_words(word_history[-1])
                if self.target_word in possible_next_words:
                    if fast:
                        return [word_history + [self.target_word]]
                    solutions.append(word_history + [self.target_word])
                for w in possible_next_words:
                    if w not in visited:  # don't reject words that are visited in the current layer
                        new_tree.append(word_history + [w])
                    if fast:
                        visited.add(w)
                    else:
                        last_visited.add(w)  # don't reject words that are visited in the current layer

            if not fast:
                visited = visited.union(last_visited)  # visited becomes all visited words so far
                last_visited = set()  # reset last_visited
            tree = copy.deepcopy(new_tree)
            layer += 1

        return solutions
