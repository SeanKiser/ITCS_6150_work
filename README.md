# 8-Puzzle Solver (A* Search)

Solves the classic 8-puzzle using the A* search algorithm, comparing two admissible heuristics:

- **Misplaced tiles** — counts how many tiles are not in their goal position
- **Manhattan distance** — sums the horizontal + vertical distance of each tile from its goal position

The program runs both heuristics on the same puzzle so their performance can be compared via the number of nodes expanded and generated.

## Requirements

- Python 3
- [heapdict](https://pypi.org/project/HeapDict/) (used as the priority queue for the open set)

```
pip install heapdict
```

## Usage

```
python puzzle.py
```

You will be prompted to enter the initial state and the goal state. Each state is entered as 9 numbers (0-8) separated by spaces, filling the grid row by row. `0` represents the empty space.

Example input for the standard goal state:

```
1 2 3 4 5 6 7 8 0
```

## Output

For each heuristic, the program prints:

- The full solution path from the initial state to the goal, shown as a sequence of 3x3 grids
- The number of nodes expanded
- The number of nodes generated
