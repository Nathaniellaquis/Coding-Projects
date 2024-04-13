def initialize_board():
    return [[" " for _ in range(3)] for _ in range(3)]

def print_board(board):
    for row in board:
        print("|" + "|".join(row) + "|")
        print("-" * 5)

def get_player_move(board, player):
    valid = False
    while not valid:
        move = input(f"Player {player}, enter your move (row,col): ")
        try:
            row, col = map(int, move.split(','))
            if board[row][col] == " ":
                return row, col
            else:
                print("This cell is already taken.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter row and column as row,col (e.g., 1,2).")

def check_winner(board, player):
    win_conditions = (
        [board[i] for i in range(3)] +
        [[board[i][j] for i in range(3)] for j in range(3)] +
        [[board[i][i] for i in range(3)], [board[i][2-i] for i in range(3)]]
    )
    if any(all(cell == player for cell in line) for line in win_conditions):
        return True
    return False

def check_tie(board):
    return all(all(cell != " " for cell in row) for row in board)

def minimax(board, depth, is_maximizing, player, opponent):
    if check_winner(board, player):
        return 10
    elif check_winner(board, opponent):
        return -10
    elif check_tie(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = player
                    score = minimax(board, depth + 1, False, player, opponent)
                    board[i][j] = " "
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = opponent
                    score = minimax(board, depth + 1, True, player, opponent)
                    board[i][j] = " "
                    best_score = min(score, best_score)
        return best_score

def best_move(board, player, opponent):
    best_score = -float('inf')
    move = (0, 0)
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = player
                score = minimax(board, 0, False, player, opponent)
                board[i][j] = " "
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

def main():
    board = initialize_board()
    human_player = "O"
    ai_player = "X"
    current_player = ai_player  # AI starts

    game_over = False
    while not game_over:
        print_board(board)
        if current_player == human_player:
            row, col = get_player_move(board, human_player)
            board[row][col] = human_player
        else:
            row, col = best_move(board, ai_player, human_player)
            print(f"AI plays {row},{col}")
            board[row][col] = ai_player

        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            game_over = True
        elif check_tie(board):
            print_board(board)
            print("The game is a tie!")
            game_over = True
        else:
            current_player = ai_player if current_player == human_player else human_player

if __name__ == "__main__":
    main()
