import tkinter as tk
import random

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.root.configure(bg="#1a1a1a")
        self.root.resizable(False, False)
        
        # Game parameterscm
        self.GRID_SIZE = 20
        self.GRID_WIDTH = 20
        self.GRID_HEIGHT = 15
        self.CANVAS_WIDTH = self.GRID_WIDTH * self.GRID_SIZE
        self.CANVAS_HEIGHT = self.GRID_HEIGHT * self.GRID_SIZE
        self.SPEED = 100  # ms between moves
        
        # Game state
        self.snake = [(5, 5), (4, 5), (3, 5)]  # Head at (5,5)
        self.food = self.spawn_food()
        self.direction = (1, 0)  # Moving right
        self.next_direction = (1, 0)
        self.score = 0
        self.game_over = False
        self.high_score = 0
        
        # Top frame for score
        top_frame = tk.Frame(root, bg="#1a1a1a")
        top_frame.pack(pady=5)
        
        self.score_label = tk.Label(top_frame, text=f"Score: {self.score}", 
                                   font=("Arial", 14, "bold"), 
                                   bg="#1a1a1a", fg="#00ff00")
        self.score_label.pack(side=tk.LEFT, padx=10)
        
        self.high_score_label = tk.Label(top_frame, text=f"High Score: {self.high_score}", 
                                        font=("Arial", 14, "bold"), 
                                        bg="#1a1a1a", fg="#ffaa00")
        self.high_score_label.pack(side=tk.LEFT, padx=10)
        
        # Canvas
        self.canvas = tk.Canvas(root, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT,
                               bg="#000000", highlightthickness=2, highlightbackground="#00ff00")
        self.canvas.pack(pady=10)
        
        # Bottom frame for controls
        bottom_frame = tk.Frame(root, bg="#1a1a1a")
        bottom_frame.pack(pady=10)
        
        self.status_label = tk.Label(bottom_frame, text="Use Arrow Keys or WASD to Move | Press R to Reset", 
                                    font=("Arial", 10), bg="#1a1a1a", fg="#cccccc")
        self.status_label.pack()
        
        reset_btn = tk.Button(bottom_frame, text="Reset Game", font=("Arial", 11),
                             bg="#ff4444", fg="white", command=self.reset_game, padx=10)
        reset_btn.pack(pady=5)
        
        # Keyboard bindings
        self.root.bind("<Up>", lambda e: self.change_direction((0, -1)))
        self.root.bind("<Down>", lambda e: self.change_direction((0, 1)))
        self.root.bind("<Left>", lambda e: self.change_direction((-1, 0)))
        self.root.bind("<Right>", lambda e: self.change_direction((1, 0)))
        
        # WASD controls
        self.root.bind("w", lambda e: self.change_direction((0, -1)))
        self.root.bind("W", lambda e: self.change_direction((0, -1)))
        self.root.bind("s", lambda e: self.change_direction((0, 1)))
        self.root.bind("S", lambda e: self.change_direction((0, 1)))
        self.root.bind("a", lambda e: self.change_direction((-1, 0)))
        self.root.bind("A", lambda e: self.change_direction((-1, 0)))
        self.root.bind("d", lambda e: self.change_direction((1, 0)))
        self.root.bind("D", lambda e: self.change_direction((1, 0)))
        
        # Reset key
        self.root.bind("r", lambda e: self.reset_game())
        self.root.bind("R", lambda e: self.reset_game())
        
        # Start game loop
        self.game_loop()
    
    def spawn_food(self):
        while True:
            food = (random.randint(0, self.GRID_WIDTH - 1), 
                   random.randint(0, self.GRID_HEIGHT - 1))
            if food not in self.snake:
                return food
    
    def change_direction(self, new_direction):
        # Prevent reversing into itself
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.next_direction = new_direction
    
    def game_loop(self):
        if not self.game_over:
            self.update_game()
            self.draw_game()
            self.root.after(self.SPEED, self.game_loop)
        else:
            self.show_game_over()
    
    def update_game(self):
        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        
        # Check wall collision
        if (new_head[0] < 0 or new_head[0] >= self.GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= self.GRID_HEIGHT):
            self.game_over = True
            return
        
        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            return
        
        # Move snake
        self.snake.insert(0, new_head)
        
        # Check food collision
        if new_head == self.food:
            self.score += 10
            self.score_label.config(text=f"Score: {self.score}")
            self.food = self.spawn_food()
            # Speed up slightly
            if self.SPEED > 50:
                self.SPEED -= 2
        else:
            self.snake.pop()
    
    def draw_game(self):
        self.canvas.delete("all")
        
        # Draw snake
        for segment in self.snake:
            x, y = segment
            x1 = x * self.GRID_SIZE + 1
            y1 = y * self.GRID_SIZE + 1
            x2 = x1 + self.GRID_SIZE - 1
            y2 = y1 + self.GRID_SIZE - 1
            
            if segment == self.snake[0]:  # Head
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="#00ff00", outline="#00cc00")
            else:  # Body
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="#00aa00", outline="#008800")
        
        # Draw food
        x, y = self.food
        x1 = x * self.GRID_SIZE + 1
        y1 = y * self.GRID_SIZE + 1
        x2 = x1 + self.GRID_SIZE - 1
        y2 = y1 + self.GRID_SIZE - 1
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="#ff0000", outline="#cc0000")
    
    def show_game_over(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.high_score_label.config(text=f"High Score: {self.high_score}")
        
        self.status_label.config(text=f"Game Over! Final Score: {self.score} | Press R or Click Reset to Play Again", 
                                fg="#ff4444")
    
    def reset_game(self):
        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False
        self.SPEED = 100
        self.score_label.config(text=f"Score: {self.score}")
        self.status_label.config(text="Use Arrow Keys or WASD to Move | Press R to Reset", fg="#cccccc")
        self.game_loop()

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
