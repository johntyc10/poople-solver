from collections import deque, defaultdict


class PoopleSolverBase():
    def __init__(self) -> None:
        self.all_words = self._load_all_words()
        self.word_frequency_dict = self._load_word_frequency()
        # build adjacency list once
        self._adj = {w: self.get_possible_next_words(w) for w in self.all_words}

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

    def solve(self, print_progress: bool = True) -> list[list[str]]:  # bfs search
        """
        Solves poople.
        print_progress: print progress if True, not printing progress otherwise.
        Returns a list of possible shortest sequences from start word to target word inclusive.
        """
        if self.start_word == self.target_word:
            return [[self.target_word]]

        # BFS that records predecessors
        queue = deque([self.start_word])
        visited = {self.start_word: 0}          # word → distance
        parents = defaultdict(list)             # word → list of parents at optimal dist

        found_dist = None
        layer = 0

        while queue:
            layer_size = len(queue)
            if print_progress:
                print(f"-> Looking through layer {layer} ({layer_size} words)...")

            for _ in range(layer_size):
                current = queue.popleft()
                dist = visited[current]

                if found_dist is not None and dist >= found_dist:
                    continue

                for nxt in self._adj[current]:
                    if nxt not in visited:
                        visited[nxt] = dist + 1
                        parents[nxt].append(current)
                        queue.append(nxt)

                        if nxt == self.target_word:
                            found_dist = dist + 1
                    elif visited[nxt] == dist + 1:
                        # another optimal parent
                        parents[nxt].append(current)

            layer += 1
            if found_dist is not None:
                break

        if self.target_word not in parents and self.start_word != self.target_word:
            return []          # unreachable

        # Reconstruct *all* shortest paths
        return self._reconstruct_all_paths(parents, self.target_word)

    def _reconstruct_all_paths(self, parents, target):
        """DFS/backtracking from target using the parent lists."""
        results = []
        def dfs(node, path):
            if node == self.start_word:
                results.append(path[::-1])
                return
            for p in parents[node]:
                dfs(p, path + [p])
        dfs(target, [target])
        return results
