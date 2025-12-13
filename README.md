# Tic-Tac-Toe with Min-Max and Alpha-Beta Algorithms

This project implements the classic Tic-Tac-Toe game (also known as Noughts and Crosses) with artificial intelligence using the Min-Max algorithm and Alpha-Beta pruning. It fulfills the requirements of applying these algorithms to a two-player game, including a user-friendly interface, heuristic evaluation functions, performance analysis, and comparisons.

## Game Description

Tic-Tac-Toe is played on a 3x3 grid. Two players take turns placing their symbols ('X' or 'O') in empty cells. The goal is to align three identical symbols horizontally, vertically, or diagonally. If the grid fills without a winner, it's a draw.

## Requirements Fulfilled

This implementation addresses all specified requirements:

### a. User-Friendly Interface
- A graphical interface built with Tkinter allows convenient gameplay.
- Human player ('X') vs. AI ('O').
- Visual grid with clickable buttons.
- Displays game results (win, loss, or draw).
- Reset button for new games.

### b. Heuristic Evaluation Functions
Two heuristics are implemented for node evaluation:

- **H1(n)**: 
  - Returns `1` if the root player is winning.
  - Returns `-1` if the opponent is winning.
  - Returns `0` for a draw or ongoing game.

- **H2(n)**: 
  - Calculates `M(n) - O(n)`, where:
    - `M(n)`: Number of possible winning lines for the root player.
    - `O(n)`: Number of possible winning lines for the opponent.
  - Example: For a board where 'X' has 4 possible winning lines and 'O' has 6, H2 = 4 - 6 = -2.

### c. Min-Max Algorithm
- Recursive implementation exploring all possible moves.
- Maximizes score for the root player ('X') and minimizes for the opponent ('O').
- Uses heuristic functions to evaluate leaf nodes.

### d. Alpha-Beta Pruning Algorithm
- Optimizes Min-Max by pruning branches that won't affect the outcome.
- Reduces the number of nodes explored significantly.

### e. Maximum Depth Determination
- **Fixed Depth**: 9 (full game tree depth).
- **Argument**: Tic-Tac-Toe has a maximum of 9 moves, and the state space is small (~20,000 possible boards). Full exploration is feasible and allows complete demonstration of algorithm effectiveness without artificial limits.

### f. Node Count Comparison
Performance analysis for the first move on an empty board (depth 9):

| Heuristic | Algorithm    | Nodes Explored | Time (seconds) |
|-----------|--------------|----------------|----------------|
| H1       | Min-Max     | 549,945       | 0.849         |
| H1       | Alpha-Beta  | 14,649        | 0.033         |
| H2       | Min-Max     | 549,945       | 2.524         |
| H2       | Alpha-Beta  | 12,170        | 0.049         |

**Conclusions**:
- Alpha-Beta explores approximately 96% fewer nodes than Min-Max.
- This leads to 25-30x faster execution.
- Pruning is highly effective, making the AI responsive even with more complex heuristics like H2.

### g. Execution Time
- As detailed in the table above, Alpha-Beta is consistently faster.
- H2 takes longer due to evaluation complexity but benefits greatly from pruning.

## Project Structure

```
tic_tac_toe/
├── main.py          # Main GUI application for playing the game
├── minmax.py        # Min-Max and Alpha-Beta algorithm implementations
├── heuristics.py    # Heuristic evaluation functions (H1 and H2)
├── analysis.py      # Performance analysis script
└── README.md        # This file
```

- **main.py**: Contains the Tkinter-based GUI for human vs. AI gameplay.
- **minmax.py**: Implements the algorithms, move generation, and best-move selection.
- **heuristics.py**: Defines winner checking and heuristic evaluations.
- **analysis.py**: Runs simulations to measure nodes and time for both algorithms and heuristics.

## Dependencies

- Python 3.x
- Tkinter (included with standard Python installations)

A virtual environment is configured in the parent directory (`.venv`).

## How to Run

1. **Set Up Environment**:
   - Ensure Python is installed.
   - The virtual environment is already set up; use `C:/Users/yassine/Desktop/Yassine/fac/IA/.venv/Scripts/python.exe` to run scripts.

2. **Play the Game**:
   - Navigate to the `tic_tac_toe/` folder.
   - Run: `python main.py`
   - Click on grid cells to place 'X'. The AI will respond with 'O'.
   - Use the Reset button for new games.

3. **Run Performance Analysis**:
   - Run: `python analysis.py`
   - This prints node counts and execution times for Min-Max and Alpha-Beta with both heuristics.

## Results and Analysis

- **Node Reduction**: Alpha-Beta drastically cuts down exploration, proving its value for game AI.
- **Time Efficiency**: Faster computation enables real-time gameplay.
- **Heuristic Impact**: H1 is simpler and faster; H2 provides better strategic depth but at higher cost, mitigated by pruning.
- **Overall**: For Tic-Tac-Toe, both algorithms work, but Alpha-Beta is essential for scalability to larger games.

## Future Improvements

- Add difficulty levels by adjusting depth or heuristics.
- Implement other games (e.g., Connect Four) with the same framework.
- Enhance GUI with animations or sound.

## License

This project is for educational purposes. Feel free to modify and extend.