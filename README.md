# Poople Solver

A shortest-path word ladder solver for the game **Poople**.

Given a four-letter starting word, the solver finds a sequence of valid English words that transforms the start word into `POOP` (or any other valid 4-letter target), where each step differs by exactly one letter.

Example:
```
HUGE -> HUGS -> HUMS -> HUMP -> PUMP -> POMP -> POOP
```

Most of the time I cannot solve it with optimal guesses. You may call it skill issue, but I call it enjoying the process. To save myself from insanity, I made this Poople solver to practice coding.

## The Algorithm

The solver treats the problem as an **unweighted shortest path** on an implicit graph:

- Nodes = valid 4-letter words
- Edges = pairs of words that differ by exactly one letter

It uses **Breadth-First Search (BFS)** to guarantee the shortest possible ladder.

### Key implementation details

- The full adjacency list is pre-computed once when the solver is created (neighbour lookups become O(1)).
- BFS records only **predecessors** (the words that can reach each node at the optimal distance) instead of storing full paths.
- After the target is reached, all shortest paths are reconstructed by walking backwards from the target using the predecessor lists.
- Among all shortest solutions, the solver selects the "most human" one by maximising the sum of word frequencies (from a frequency dictionary).

This approach is both memory-efficient and fast while still returning every optimal solution.

## Performance

On the official 4-letter possible starting word list (1137 words):

- Most ladders are found in a few milliseconds.
- Memory usage stays modest thanks to the predecessor-only representation.
- The search is optimal: every returned ladder is one of the shortest possible.

For those who are interested in the source of the statistics, I've provided `poople_benchmark.py` for you to run the benchmark and get the numbers yourselves.

Bidirectional BFS or A* with Hamming distance are possible future optimisations, but plain BFS is already more than fast enough for this problem size.

## How to Use

On Windows powershell / MacOS or Linux terminal:

```bash
# Run the solver
python poople_solver.py
```

Example session:
```
===== POOPLE SOLVER =====
A script that uses brute force method to solve poople (guaranteed best solution)

Input start word: huge
"HUGE" is chosen.
Input target word (enter for "POOP"):
"POOP" is chosen.
Solving poople...
-> Looking through layer 0 (1 words)...
-> Looking through layer 1 (2 words)...
-> Looking through layer 2 (17 words)...
-> Looking through layer 3 (100 words)...
-> Looking through layer 4 (407 words)...
-> Looking through layer 5 (688 words)...
4 solution(s) found.
Most human solution:
0: HUGE
1: HUGS
2: HUMS
3: HUMP
4: PUMP
5: POMP
6: POOP
The best solution(s) takes 6 guesses.
```

You can also change the target word at runtime (just type any valid 4-letter word instead of pressing Enter).

## Contribute

Contributions are welcome!

Ideas that would be especially useful:
- Bidirectional BFS
- A* with Hamming-distance heuristic
- Support for different word lengths or custom dictionaries
- Better word-list handling / filtering
- Unit tests and a proper benchmark suite

Please open an issue or submit a pull request. Keep the code clear and add tests when possible.
