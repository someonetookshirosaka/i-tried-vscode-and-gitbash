import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("400x500")
        self.root.configure(bg="#2c3e50")
        
        # Game variables
        self.board = [''] * 9  # 0-8 represents the 9 squares
        self.human = 'X'
        self.ai = 'O'
        self.game_over = False
        
        # Title label
        title_label = tk.Label(root, text="Tic Tac Toe", font=("Arial", 24, "bold"), 
                              bg="#2c3e50", fg="#ecf0f1")
        title_label.pack(pady=10)
        
        # Status label
        self.status_label = tk.Label(root, text="You are X, AI is O. Your turn!", 
                                     font=("Arial", 12), bg="#2c3e50", fg="#3498db")
        self.status_label.pack(pady=5)
        
        # Game frame
        game_frame = tk.Frame(root, bg="#2c3e50")
        game_frame.pack(pady=10)
        
        # Create buttons for grid
        self.buttons = []
        for i in range(9):
            btn = tk.Button(game_frame, text="", font=("Arial", 20, "bold"),
                           width=5, height=2, bg="#34495e", fg="white",
                           command=lambda idx=i: self.on_button_click(idx))
            row = i // 3
            col = i % 3
            btn.grid(row=row, column=col, padx=5, pady=5)
            self.buttons.append(btn)
        
        # Reset button
        reset_btn = tk.Button(root, text="Reset Game", font=("Arial", 12),
                             bg="#e74c3c", fg="white", command=self.reset_game)
        reset_btn.pack(pady=10)
    
    def on_button_click(self, index):
        if self.board[index] == '' and not self.game_over:
            self.board[index] = self.human
            self.update_button(index)
            
            # Check if human won
            if self.check_winner(self.human):
                self.status_label.config(text="You won! 🎉", fg="#2ecc71")
                self.game_over = True
                return
            
            # Check for draw
            if '' not in self.board:
                self.status_label.config(text="It's a Draw! 🤝", fg="#f39c12")
                self.game_over = True
                return
            
            # AI turn
            self.status_label.config(text="AI is thinking...", fg="#f39c12")
            self.root.after(500, self.ai_move)
    
    def ai_move(self):
        # Simple AI: Try to win, block human win, or take random spot
        move = self.find_winning_move(self.ai)
        
        if move is None:
            move = self.find_winning_move(self.human)  # Block human
        
        if move is None:
            move = self.find_best_move()  # Take center or random
        
        if move is not None:
            self.board[move] = self.ai
            self.update_button(move)
        
        # Check if AI won
        if self.check_winner(self.ai):
            self.status_label.config(text="AI won! Better luck next time! 🤖", fg="#e74c3c")
            self.game_over = True
            return
        
        # Check for draw
        if '' not in self.board:
            self.status_label.config(text="It's a Draw! 🤝", fg="#f39c12")
            self.game_over = True
            return
        
        self.status_label.config(text="Your turn!", fg="#3498db")
    
    def find_winning_move(self, player):
        """Find a move that would result in a win"""
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
        
        for combo in winning_combinations:
            values = [self.board[i] for i in combo]
            if values.count(player) == 2 and values.count('') == 1:
                return combo[values.index('')]
        
        return None
    
    def find_best_move(self):
        """Find best available move (prefer center, then corners, then random)"""
        # Prefer center
        if self.board[4] == '':
            return 4
        
        # Then corners
        corners = [0, 2, 6, 8]
        available_corners = [c for c in corners if self.board[c] == '']
        if available_corners:
            return random.choice(available_corners)
        
        # Then any empty spot
        available = [i for i in range(9) if self.board[i] == '']
        return random.choice(available) if available else None
    
    def check_winner(self, player):
        """Check if the given player has won"""
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
        
        for combo in winning_combinations:
            if all(self.board[i] == player for i in combo):
                return True
        return False
    
    def update_button(self, index):
        """Update button display"""
        player = self.board[index]
        self.buttons[index].config(text=player, state="disabled")
        
        if player == self.human:
            self.buttons[index].config(fg="#3498db")
        else:
            self.buttons[index].config(fg="#e74c3c")
    
    def reset_game(self):
        """Reset the game"""
        self.board = [''] * 9
        self.game_over = False
        self.status_label.config(text="You are X, AI is O. Your turn!", fg="#3498db")
        
        for btn in self.buttons:
            btn.config(text="", state="normal", fg="white")

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()