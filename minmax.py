# Implementation of Min-Max and Alpha-Beta algorithms
# =====================================================
# This module implements game tree search algorithms for Tic-Tac-Toe:
# - Minimax: Complete tree search with no pruning
# - Alpha-Beta: Optimized search with branch pruning

from heuristics import check_winner, h1, h2

# Constants for infinity values
INF = float('inf')
NEG_INF = -float('inf')


def get_moves(board):
    """
    Get all available moves (empty cells) on the board.
    
    Args:
        board: Current game state
        
    Returns:
        List of indices of empty cells (0-8)
    """
    return [i for i, cell in enumerate(board) if cell == ' ']


def make_move(board, pos, player):
    """
    Create a new board with a move applied.
    
    Args:
        board: Current game state
        pos: Position to place the piece (0-8)
        player: Player making the move ('X' or 'O')
        
    Returns:
        New board state with the move applied
    """
    new_board = board.copy()
    new_board[pos] = player
    return new_board


def get_opponent(player):
    """
    Get the opponent of the given player.
    
    Args:
        player: Current player ('X' or 'O')
        
    Returns:
        Opponent player ('O' or 'X')
    """
    return 'O' if player == 'X' else 'X'


def minimax(board, player, depth, root_player, heuristic):
    """
    Minimax algorithm for game tree search.
    
    Explores all possible moves recursively, maximizing for root_player
    and minimizing for the opponent.
    
    Args:
        board: Current game state
        player: Current player's turn ('X' or 'O')
        depth: Maximum depth to search
        root_player: The maximizing player (player at tree root)
        heuristic: Evaluation function to use (h1 or h2)
        
    Returns:
        Tuple (evaluation_score, nodes_explored)
    """
    # Terminal state check
    winner = check_winner(board)
    if depth == 0 or winner is not None:
        return heuristic(board, root_player), 1
    
    moves = get_moves(board)
    if not moves:
        return heuristic(board, root_player), 1
    
    nodes = 1  # Count current node
    
    if player == root_player:  # Maximizing player
        max_eval = NEG_INF
        for move in moves:
            new_board = make_move(board, move, player)
            eval_val, sub_nodes = minimax(new_board, get_opponent(player), 
                                          depth - 1, root_player, heuristic)
            max_eval = max(max_eval, eval_val)
            nodes += sub_nodes
        return max_eval, nodes
    
    else:  # Minimizing player
        min_eval = INF
        for move in moves:
            new_board = make_move(board, move, player)
            eval_val, sub_nodes = minimax(new_board, get_opponent(player), 
                                          depth - 1, root_player, heuristic)
            min_eval = min(min_eval, eval_val)
            nodes += sub_nodes
        return min_eval, nodes


def alphabeta(board, player, depth, alpha, beta, root_player, heuristic):
    """
    Alpha-Beta pruning algorithm for optimized game tree search.
    
    Prunes branches that cannot affect the final decision, significantly
    reducing the number of nodes explored.
    
    Alpha = best value the maximizer can guarantee
    Beta = best value the minimizer can guarantee
    
    Pruning occurs when alpha >= beta (no need to explore further)
    
    Args:
        board: Current game state
        player: Current player's turn ('X' or 'O')
        depth: Maximum depth to search
        alpha: Best value for maximizer found so far
        beta: Best value for minimizer found so far
        root_player: The maximizing player
        heuristic: Evaluation function to use
        
    Returns:
        Tuple (evaluation_score, nodes_explored)
    """
    # Terminal state check
    winner = check_winner(board)
    if depth == 0 or winner is not None:
        return heuristic(board, root_player), 1
    
    moves = get_moves(board)
    if not moves:
        return heuristic(board, root_player), 1
    
    nodes = 1  # Count current node
    
    if player == root_player:  # Maximizing player
        max_eval = NEG_INF
        for move in moves:
            new_board = make_move(board, move, player)
            eval_val, sub_nodes = alphabeta(new_board, get_opponent(player),
                                            depth - 1, alpha, beta, 
                                            root_player, heuristic)
            max_eval = max(max_eval, eval_val)
            alpha = max(alpha, eval_val)
            nodes += sub_nodes
            
            # Beta cutoff - prune remaining branches
            if beta <= alpha:
                break
        return max_eval, nodes
    
    else:  # Minimizing player
        min_eval = INF
        for move in moves:
            new_board = make_move(board, move, player)
            eval_val, sub_nodes = alphabeta(new_board, get_opponent(player),
                                            depth - 1, alpha, beta,
                                            root_player, heuristic)
            min_eval = min(min_eval, eval_val)
            beta = min(beta, eval_val)
            nodes += sub_nodes
            
            # Alpha cutoff - prune remaining branches
            if beta <= alpha:
                break
        return min_eval, nodes


def get_best_move(board, player, depth, algorithm, heuristic):
    """
    Find the best move for a player using the specified algorithm.
    
    Evaluates all possible moves and returns the one with the best
    evaluation score according to the chosen algorithm and heuristic.
    
    Args:
        board: Current game state
        player: Player to find move for ('X' or 'O')
        depth: Maximum search depth
        algorithm: 'minimax' or 'alphabeta'
        heuristic: Evaluation function (h1 or h2)
        
    Returns:
        Tuple (best_move_index, total_nodes_explored)
        best_move_index is None if no moves available
    """
    moves = get_moves(board)
    if not moves:
        return None, 0
    
    best_move = None
    best_value = NEG_INF if player == 'X' else INF
    total_nodes = 0
    
    # Determine if player is maximizing or minimizing
    # X is always the root/maximizing player in our convention
    root_player = 'X'
    is_maximizing = (player == root_player)
    
    for move in moves:
        new_board = make_move(board, move, player)
        opponent = get_opponent(player)
        
        if algorithm == 'minimax':
            value, nodes = minimax(new_board, opponent, depth - 1, 
                                   root_player, heuristic)
        elif algorithm == 'alphabeta':
            value, nodes = alphabeta(new_board, opponent, depth - 1,
                                     NEG_INF, INF, root_player, heuristic)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
        
        total_nodes += nodes
        
        # Update best move based on player type
        if is_maximizing:
            if value > best_value:
                best_value = value
                best_move = move
        else:
            if value < best_value:
                best_value = value
                best_move = move
    
    return best_move, total_nodes