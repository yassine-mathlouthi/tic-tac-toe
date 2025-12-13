# Heuristic functions for Tic-Tac-Toe
# =====================================
# This module implements two heuristic evaluation functions:
# - H1: Simple win/loss/draw evaluation
# - H2: Strategic evaluation based on possible winning lines

# Board representation:
# - List of 9 elements (indices 0-8)
# - ' ' for empty cell
# - 'X' or 'O' for player moves
# 
# Board layout:
#   0 | 1 | 2
#   ---------
#   3 | 4 | 5
#   ---------
#   6 | 7 | 8

# All possible winning lines (8 total: 3 rows, 3 columns, 2 diagonals)
WINNING_LINES = [
    [0, 1, 2],  # Top row
    [3, 4, 5],  # Middle row
    [6, 7, 8],  # Bottom row
    [0, 3, 6],  # Left column
    [1, 4, 7],  # Middle column
    [2, 5, 8],  # Right column
    [0, 4, 8],  # Main diagonal
    [2, 4, 6]   # Anti-diagonal
]


def check_winner(board):
    """
    Check if there's a winner or draw on the board.
    
    Args:
        board: List of 9 elements representing the game state
        
    Returns:
        'X' if X wins
        'O' if O wins
        'Draw' if the board is full with no winner
        None if the game is still ongoing
    """
    # Check all winning lines
    for line in WINNING_LINES:
        a, b, c = line
        if board[a] == board[b] == board[c] != ' ':
            return board[a]
    
    # Check for draw (no empty cells)
    if ' ' not in board:
        return 'Draw'
    
    # Game still in progress
    return None


def h1(board, root_player):
    """
    Heuristic H1: Simple terminal state evaluation.
    
    H1(n) = 1  if root_player is winning
    H1(n) = -1 if root_player is losing (opponent wins)
    H1(n) = 0  if draw or game ongoing
    
    Args:
        board: Current game state
        root_player: The player at the root of the search tree ('X' or 'O')
        
    Returns:
        Integer evaluation score: 1, -1, or 0
    """
    winner = check_winner(board)
    
    if winner == root_player:
        return 1
    elif winner is not None and winner != 'Draw' and winner != root_player:
        return -1
    else:
        return 0


def h2(board, root_player):
    """
    Heuristic H2: Strategic evaluation based on possible winning lines.
    
    H2(n) = M(n) - O(n)
    
    Where:
    - M(n) = Number of winning lines still possible for root_player
    - O(n) = Number of winning lines still possible for opponent
    
    A line is "possible" for a player if:
    - It contains no opponent pieces
    - It has at least one empty cell (can still be completed)
    
    Example:
        Board:    X | O |          X has 4 possible winning lines
                  --|---|--        O has 6 possible winning lines  
                    |   |          H2 = 4 - 6 = -2
    
    Args:
        board: Current game state
        root_player: The player at the root of the search tree
        
    Returns:
        Integer score representing the advantage for root_player
    """
    opponent = 'O' if root_player == 'X' else 'X'
    
    # Check for terminal states first
    winner = check_winner(board)
    if winner == root_player:
        return 100  # High positive score for winning
    elif winner == opponent:
        return -100  # High negative score for losing
    elif winner == 'Draw':
        return 0
    
    # Count possible winning lines for each player
    m = 0  # Root player's possible lines
    o = 0  # Opponent's possible lines
    
    for line in WINNING_LINES:
        root_count = sum(1 for i in line if board[i] == root_player)
        opp_count = sum(1 for i in line if board[i] == opponent)
        empty_count = sum(1 for i in line if board[i] == ' ')
        
        # Line is possible for root_player if no opponent pieces
        if opp_count == 0 and (root_count > 0 or empty_count == 3):
            m += 1
        
        # Line is possible for opponent if no root_player pieces
        if root_count == 0 and (opp_count > 0 or empty_count == 3):
            o += 1
    
    return m - o


def count_possible_wins(board, player):
    """
    Count the number of possible winning lines for a player.
    Utility function for analysis.
    
    Args:
        board: Current game state
        player: Player to count for ('X' or 'O')
        
    Returns:
        Number of possible winning lines
    """
    opponent = 'O' if player == 'X' else 'X'
    count = 0
    
    for line in WINNING_LINES:
        opp_count = sum(1 for i in line if board[i] == opponent)
        if opp_count == 0:
            count += 1
    
    return count