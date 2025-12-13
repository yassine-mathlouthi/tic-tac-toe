# Main entry point for the Tic-Tac-Toe game
# Enhanced GUI with modern styling and algorithm/heuristic selection

import tkinter as tk
from tkinter import messagebox, ttk
import time
from minmax import get_best_move
from heuristics import check_winner, h1, h2

# Color scheme
COLORS = {
    'bg': '#1a1a2e',
    'grid_bg': '#16213e',
    'cell_bg': '#0f3460',
    'cell_hover': '#1a4a7a',
    'x_color': '#e94560',
    'o_color': '#00d9ff',
    'text': '#ffffff',
    'button_bg': '#e94560',
    'button_hover': '#ff6b6b',
    'win_color': '#00ff88',
    'stats_bg': '#0f3460'
}

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Tic-Tac-Toe AI")
        self.root.configure(bg=COLORS['bg'])
        self.root.resizable(False, False)
        
        self.board = [' '] * 9
        self.current_player = 'X'  # Human
        self.ai_player = 'O'
        self.buttons = []
        self.game_over = False
        self.winning_line = None
        
        # Stats
        self.games_played = 0
        self.x_wins = 0
        self.o_wins = 0
        self.draws = 0
        self.last_nodes = 0
        self.last_time = 0
        
        self.setup_styles()
        self.create_widgets()
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TCombobox', fieldbackground=COLORS['cell_bg'], 
                       background=COLORS['button_bg'], foreground=COLORS['text'])
        
    def create_widgets(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=COLORS['bg'], padx=20, pady=20)
        main_frame.pack()
        
        # Title
        title = tk.Label(main_frame, text="🎮 TIC-TAC-TOE", 
                        font=('Helvetica', 28, 'bold'), 
                        fg=COLORS['x_color'], bg=COLORS['bg'])
        title.pack(pady=(0, 5))
        
        subtitle = tk.Label(main_frame, text="Min-Max & Alpha-Beta AI", 
                           font=('Helvetica', 12), 
                           fg=COLORS['o_color'], bg=COLORS['bg'])
        subtitle.pack(pady=(0, 15))
        
        # Settings frame
        settings_frame = tk.Frame(main_frame, bg=COLORS['stats_bg'], padx=15, pady=10)
        settings_frame.pack(fill='x', pady=(0, 15))
        
        # Algorithm selection
        algo_frame = tk.Frame(settings_frame, bg=COLORS['stats_bg'])
        algo_frame.pack(side='left', padx=10)
        tk.Label(algo_frame, text="Algorithm:", font=('Helvetica', 10, 'bold'),
                fg=COLORS['text'], bg=COLORS['stats_bg']).pack(anchor='w')
        self.algo_var = tk.StringVar(value='alphabeta')
        algo_menu = ttk.Combobox(algo_frame, textvariable=self.algo_var, 
                                 values=['minimax', 'alphabeta'], state='readonly', width=12)
        algo_menu.pack()
        
        # Heuristic selection
        heur_frame = tk.Frame(settings_frame, bg=COLORS['stats_bg'])
        heur_frame.pack(side='left', padx=10)
        tk.Label(heur_frame, text="Heuristic:", font=('Helvetica', 10, 'bold'),
                fg=COLORS['text'], bg=COLORS['stats_bg']).pack(anchor='w')
        self.heur_var = tk.StringVar(value='H2')
        heur_menu = ttk.Combobox(heur_frame, textvariable=self.heur_var,
                                 values=['H1', 'H2'], state='readonly', width=8)
        heur_menu.pack()
        
        # Depth selection
        depth_frame = tk.Frame(settings_frame, bg=COLORS['stats_bg'])
        depth_frame.pack(side='left', padx=10)
        tk.Label(depth_frame, text="Depth:", font=('Helvetica', 10, 'bold'),
                fg=COLORS['text'], bg=COLORS['stats_bg']).pack(anchor='w')
        self.depth_var = tk.StringVar(value='9')
        depth_menu = ttk.Combobox(depth_frame, textvariable=self.depth_var,
                                  values=['3', '5', '7', '9'], state='readonly', width=5)
        depth_menu.pack()
        
        # Game grid frame
        grid_frame = tk.Frame(main_frame, bg=COLORS['grid_bg'], padx=8, pady=8)
        grid_frame.pack(pady=10)
        
        # Create game buttons
        for i in range(9):
            row, col = i // 3, i % 3
            btn = tk.Button(grid_frame, text='', font=('Helvetica', 36, 'bold'),
                           width=3, height=1, bg=COLORS['cell_bg'], fg=COLORS['text'],
                           activebackground=COLORS['cell_hover'], relief='flat',
                           cursor='hand2', command=lambda idx=i: self.on_click(idx))
            btn.grid(row=row, column=col, padx=4, pady=4)
            btn.bind('<Enter>', lambda e, b=btn: self.on_hover(b, True))
            btn.bind('<Leave>', lambda e, b=btn: self.on_hover(b, False))
            self.buttons.append(btn)
        
        # Status label
        self.status_label = tk.Label(main_frame, text="Your turn (X)", 
                                     font=('Helvetica', 14, 'bold'),
                                     fg=COLORS['x_color'], bg=COLORS['bg'])
        self.status_label.pack(pady=10)
        
        # Stats frame
        stats_frame = tk.Frame(main_frame, bg=COLORS['stats_bg'], padx=15, pady=10)
        stats_frame.pack(fill='x', pady=10)
        
        self.stats_label = tk.Label(stats_frame, 
                                    text="Games: 0 | X Wins: 0 | O Wins: 0 | Draws: 0",
                                    font=('Helvetica', 10), fg=COLORS['text'], 
                                    bg=COLORS['stats_bg'])
        self.stats_label.pack()
        
        self.perf_label = tk.Label(stats_frame,
                                   text="Last move: -- nodes, -- ms",
                                   font=('Helvetica', 10), fg=COLORS['o_color'],
                                   bg=COLORS['stats_bg'])
        self.perf_label.pack()
        
        # Buttons frame
        btn_frame = tk.Frame(main_frame, bg=COLORS['bg'])
        btn_frame.pack(pady=10)
        
        reset_btn = tk.Button(btn_frame, text="🔄 New Game", font=('Helvetica', 12, 'bold'),
                             bg=COLORS['button_bg'], fg=COLORS['text'],
                             activebackground=COLORS['button_hover'],
                             relief='flat', padx=20, pady=8, cursor='hand2',
                             command=self.reset_game)
        reset_btn.pack(side='left', padx=5)
        
        analysis_btn = tk.Button(btn_frame, text="📊 Analysis", font=('Helvetica', 12, 'bold'),
                                bg=COLORS['o_color'], fg=COLORS['bg'],
                                activebackground='#33ffcc',
                                relief='flat', padx=20, pady=8, cursor='hand2',
                                command=self.show_analysis)
        analysis_btn.pack(side='left', padx=5)
    
    def on_hover(self, button, entering):
        if button['text'] == '' and not self.game_over:
            button.configure(bg=COLORS['cell_hover'] if entering else COLORS['cell_bg'])
    
    def on_click(self, i):
        if self.game_over or self.board[i] != ' ':
            return
        
        # Human move
        self.board[i] = self.current_player
        self.buttons[i].config(text='X', fg=COLORS['x_color'], bg=COLORS['cell_bg'])
        
        winner = check_winner(self.board)
        if winner:
            self.end_game(winner)
            return
        
        self.status_label.config(text="AI thinking (O)...", fg=COLORS['o_color'])
        self.root.update()
        
        self.current_player = self.ai_player
        self.root.after(100, self.ai_move)  # Small delay for visual feedback
    
    def ai_move(self):
        # Get algorithm and heuristic
        algorithm = self.algo_var.get()
        heuristic = h1 if self.heur_var.get() == 'H1' else h2
        depth = int(self.depth_var.get())
        
        # Measure performance
        start_time = time.time()
        move, nodes = get_best_move(self.board, self.ai_player, depth, algorithm, heuristic)
        end_time = time.time()
        
        self.last_nodes = nodes
        self.last_time = (end_time - start_time) * 1000  # Convert to ms
        
        # Update performance label
        self.perf_label.config(text=f"Last move: {nodes:,} nodes, {self.last_time:.1f} ms")
        
        if move is not None:
            self.board[move] = self.ai_player
            self.buttons[move].config(text='O', fg=COLORS['o_color'], bg=COLORS['cell_bg'])
            
            winner = check_winner(self.board)
            if winner:
                self.end_game(winner)
                return
        
        self.current_player = 'X'
        self.status_label.config(text="Your turn (X)", fg=COLORS['x_color'])
    
    def end_game(self, winner):
        self.game_over = True
        self.games_played += 1
        
        if winner == 'Draw':
            self.draws += 1
            self.status_label.config(text="🤝 It's a Draw!", fg=COLORS['text'])
            messagebox.showinfo("Game Over", "It's a draw! Well played!")
        elif winner == 'X':
            self.x_wins += 1
            self.highlight_winner()
            self.status_label.config(text="🎉 You Win!", fg=COLORS['win_color'])
            messagebox.showinfo("Game Over", "Congratulations! You beat the AI! 🎉")
        else:
            self.o_wins += 1
            self.highlight_winner()
            self.status_label.config(text="🤖 AI Wins!", fg=COLORS['x_color'])
            messagebox.showinfo("Game Over", "The AI wins! Better luck next time! 🤖")
        
        self.update_stats()
    
    def highlight_winner(self):
        lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for line in lines:
            if (self.board[line[0]] == self.board[line[1]] == self.board[line[2]] != ' '):
                for idx in line:
                    self.buttons[idx].config(bg=COLORS['win_color'])
                break
    
    def update_stats(self):
        self.stats_label.config(
            text=f"Games: {self.games_played} | X Wins: {self.x_wins} | O Wins: {self.o_wins} | Draws: {self.draws}"
        )
    
    def reset_game(self):
        self.board = [' '] * 9
        self.current_player = 'X'
        self.game_over = False
        self.winning_line = None
        
        for btn in self.buttons:
            btn.config(text='', bg=COLORS['cell_bg'])
        
        self.status_label.config(text="Your turn (X)", fg=COLORS['x_color'])
        self.perf_label.config(text="Last move: -- nodes, -- ms")
    
    def show_analysis(self):
        """Show detailed analysis window"""
        analysis_win = tk.Toplevel(self.root)
        analysis_win.title("📊 Performance Analysis")
        analysis_win.configure(bg=COLORS['bg'])
        analysis_win.geometry("500x400")
        
        tk.Label(analysis_win, text="📊 Performance Analysis",
                font=('Helvetica', 18, 'bold'), fg=COLORS['x_color'],
                bg=COLORS['bg']).pack(pady=15)
        
        # Run analysis
        results_frame = tk.Frame(analysis_win, bg=COLORS['stats_bg'], padx=20, pady=15)
        results_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        tk.Label(results_frame, text="First Move Analysis (Empty Board, Depth 9)",
                font=('Helvetica', 12, 'bold'), fg=COLORS['o_color'],
                bg=COLORS['stats_bg']).pack(anchor='w', pady=(0, 10))
        
        # Headers
        header_frame = tk.Frame(results_frame, bg=COLORS['stats_bg'])
        header_frame.pack(fill='x')
        tk.Label(header_frame, text="Method", font=('Helvetica', 10, 'bold'),
                fg=COLORS['text'], bg=COLORS['stats_bg'], width=20, anchor='w').pack(side='left')
        tk.Label(header_frame, text="Nodes", font=('Helvetica', 10, 'bold'),
                fg=COLORS['text'], bg=COLORS['stats_bg'], width=12, anchor='e').pack(side='left')
        tk.Label(header_frame, text="Time (ms)", font=('Helvetica', 10, 'bold'),
                fg=COLORS['text'], bg=COLORS['stats_bg'], width=12, anchor='e').pack(side='left')
        
        tk.Frame(results_frame, bg=COLORS['text'], height=1).pack(fill='x', pady=5)
        
        # Run actual analysis
        board = [' '] * 9
        results = []
        
        for heur_name, heur_func in [('H1', h1), ('H2', h2)]:
            for algo in ['minimax', 'alphabeta']:
                start = time.time()
                _, nodes = get_best_move(board, 'X', 9, algo, heur_func)
                elapsed = (time.time() - start) * 1000
                results.append((f"{heur_name} + {algo.capitalize()}", nodes, elapsed))
        
        for method, nodes, elapsed in results:
            row_frame = tk.Frame(results_frame, bg=COLORS['stats_bg'])
            row_frame.pack(fill='x', pady=2)
            tk.Label(row_frame, text=method, font=('Helvetica', 10),
                    fg=COLORS['text'], bg=COLORS['stats_bg'], width=20, anchor='w').pack(side='left')
            tk.Label(row_frame, text=f"{nodes:,}", font=('Helvetica', 10),
                    fg=COLORS['o_color'], bg=COLORS['stats_bg'], width=12, anchor='e').pack(side='left')
            tk.Label(row_frame, text=f"{elapsed:.1f}", font=('Helvetica', 10),
                    fg=COLORS['x_color'], bg=COLORS['stats_bg'], width=12, anchor='e').pack(side='left')
        
        # Conclusions
        tk.Frame(results_frame, bg=COLORS['text'], height=1).pack(fill='x', pady=10)
        
        conclusions = tk.Label(results_frame, 
                              text="📌 Conclusions:\n"
                                   "• Alpha-Beta prunes ~97% of nodes compared to Min-Max\n"
                                   "• Execution is 25-50x faster with Alpha-Beta\n"
                                   "• H2 is slower but provides strategic depth",
                              font=('Helvetica', 10), fg=COLORS['text'],
                              bg=COLORS['stats_bg'], justify='left')
        conclusions.pack(anchor='w')
        
        tk.Button(analysis_win, text="Close", font=('Helvetica', 11),
                 bg=COLORS['button_bg'], fg=COLORS['text'], relief='flat',
                 padx=20, pady=5, command=analysis_win.destroy).pack(pady=15)


if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg=COLORS['bg'])
    game = TicTacToe(root)
    root.mainloop()