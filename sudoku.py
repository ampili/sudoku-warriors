import sys

# The 9x9 Sudoku Board (0 represents empty cells)
board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# Keep track of which numbers were part of the starting board so players can't overwrite them
original_board = [row[:] for row in board]

def print_board(bo):
    """Prints the board with nice grid lines."""
    print("\n   1 2 3   4 5 6   7 8 9") # Column numbers
    print(" -------------------------")
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print(" ------+-------+------")
        
        print(f"{i+1} | ", end="") # Row numbers
        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print("| ", end="")
            
            val = bo[i][j]
            display_val = "." if val == 0 else str(val)
            print(display_val + " ", end="")
        print("|")
    print(" -------------------------")

def find_empty(bo):
    """Finds an empty cell (marked as 0)."""
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)
    return None

def is_valid(bo, num, pos):
    """Checks if a number placement is legal according to Sudoku rules."""
    row, col = pos
    
    # Check row
    for j in range(9):
        if bo[row][j] == num and col != j:
            return False
            
    # Check column
    for i in range(9):
        if bo[i][col] == num and row != i:
            return False
            
    # Check 3x3 box
    box_x = col // 3
    box_y = row // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False
                
    return True

def play_game():
    """Main game loop."""
    print("Welcome to Termux Sudoku!")
    
    while True:
        print_board(board)
        
        # Check if board is full (Win Condition)
        if not find_empty(board):
            print("\nCongratulations! You solved the Sudoku puzzle!")
            break
            
        print("\nInstructions: Enter Row, Column, and Number (e.g., 1 3 4) or type 'exit' to quit.")
        user_input = input("Your move: ").strip().lower()
        
        if user_input == 'exit':
            print("Thanks for playing!")
            sys.exit()
            
        try:
            # Parse input numbers
            parts = user_input.split()
            if len(parts) != 3:
                print("Error: Please enter exactly three numbers separated by spaces.")
                continue
                
            r = int(parts[0]) - 1
            c = int(parts[1]) - 1
            num = int(parts[2])
            
            # Validate boundaries
            if not (0 <= r <= 8 and 0 <= c <= 8) or not (1 <= num <= 9):
                print("Error: Rows and Columns must be 1-9. Numbers must be 1-9.")
                continue
                
            # Prevent overwriting original starting clues
            if original_board[r][c] != 0:
                print("Error: You cannot change the starting numbers!")
                continue
                
            # Place the number tentatively
            board[r][c] = num
            
            # Verify if it breaks a rule
            if not is_valid(board, num, (r, c)):
                print("Warning: That move violates Sudoku rules, but it has been placed. Fix it if you get stuck!")
                
        except ValueError:
            print("Error: Invalid characters. Use integers only.")

# Start the game
if __name__ == "__main__":
    play_game()
