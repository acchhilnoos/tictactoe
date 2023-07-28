import random

game_board = [[0,0,0],
              [0,0,0],
              [0,0,0]]
# such that any square is given by board[row][column]

Move = tuple[int, int]
ROW = 0
COLUMN = 1
# such that any square is given by (row, column)

def check_win(board:list[list[int]], player:int) -> bool:
    """
    Determines whether the given player has won on the given board.
    Returns the winning player's number, otherwise 0.
    """
    # check rows
    for row in board:
        if row[0] == row[1] == row[2] == player:
            return True

    # check columns
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] == player:
            return True

    # check diagonals
    if board[0][0] == board[1][1] == board[2][2] == player or board[0][2] == board[1][1] == board[2][0] == player:
        return True

    return False

def player_move(board:list[list[int]], player:int) -> bool:
    """
    Allows the given player to make a move on the given board.
    Returns True if the move was successful, otherwise False.
    """
    try:
        row = int(input("Choose a row (1-3): ")) - 1
        column = int(input("Choose a column (1-3): ")) - 1
        if board[row][column] == 0:
            board[row][column] = player
            show_board(board)
            return True
        else:
            print("Square not available.")
            return False
    except ValueError:
        print("Invalid input.")
        return False
    except IndexError:
        print("Invalid input.")
        return False

def cpu_move(board:list[list[int]]) -> None:
    """
    Allows the CPU to make a move on the given board.
    """
    scores = {}

    for i, row in enumerate(board):
        for j, square in enumerate(row):
            if square == 0:
                scores[(i, j)] = minimax(board, (i, j), 3)

    move = [y for y in scores if scores[y] == max([scores[x] for i,x in enumerate(scores)])][0]
    
    print(scores)
    print(f"CPU move: {move}")
    board[move[ROW]][move[COLUMN]] = 3
    show_board(board)

def minimax(board:list[list[int]], move:Move, player:int) -> int:
    trial = [x for x in board[0]], [y for y in board[1]], [z for z in board[2]]

    if player == 3:
        mini = 2
        trial[move[ROW]][move[COLUMN]] = 3

        if check_win(trial, 3) == True:
            return 1
        elif 0 not in trial[0] and 0 not in trial[1] and 0 not in trial[2]:
            return 0
        else:
            for i, row in enumerate(trial):
                for j, square in enumerate(row):
                    if square == 0:
                        mini = min(mini, minimax(trial, (i,j), 1))
            return mini
    else:
        maxi = -2
        trial[move[ROW]][move[COLUMN]] = 1

        if check_win(trial, 1) == True:
            return -1
        elif not 0 in trial[0] and not 0 in trial[1] and not 0 in trial[2]:
            return 0
        else:
            for i, row in enumerate(trial):
                for j, square in enumerate(row):
                    if square == 0:
                        maxi = max(maxi, minimax(trial, (i,j), 3))
            return maxi

def show_board(board:list[list[int]]) -> None:
    """
    Displays the current game board.
    """
    labels = {0:" ", 1:"X", 2:"O", 3:"O"}
    print("   |   |   ")
    print(f" {labels[board[0][0]]} | {labels[board[0][1]]} | {labels[board[0][2]]} ")
    print("___|___|___")
    print("   |   |   ")
    print(f" {labels[board[1][0]]} | {labels[board[1][1]]} | {labels[board[1][2]]} ")
    print("___|___|___")
    print("   |   |   ")
    print(f" {labels[board[2][0]]} | {labels[board[2][1]]} | {labels[board[2][2]]} ")
    print("   |   |   ")
    print("\n")

def play(board:list[list[int]]) -> None:
    """
    Play Tic-Tac-Toe with PvP and CPU options.
    """

    board = [[0,0,0],[0,0,0],[0,0,0]]
    
    # gamemode selection
    gamemode = input(("(1) 2p or (2) CPU (3) Exit: "))
    while not gamemode.isdigit() or int(gamemode) < 1 or int(gamemode) > 3:
        print("Invalid input.")
        gamemode = input(("(1) 2p (2) CPU (3) Exit: "))
    gamemode = int(gamemode)

    # PvP
    if gamemode == 1:
        player = 0
        while (0 in board[0] or 0 in board[1] or 0 in board[2]):
            pnum = player % 2 + 1
            
            success = False
            while success != True:
                success = player_move(board, pnum)

            if check_win(board, pnum) == True:
                print(f"Player {pnum} wins.")
                return
            
            player += 1

    # CPU
    elif gamemode == 2:
        player = random.randint(1,2)
        if player == 2:
            cpu_move(board)
            
        while (0 in board[0] or 0 in board[1] or 0 in board[2]):
            success = False
            while success != True:
                success = player_move(board, 1)

            if check_win(board, 1) == True:
                print("Player wins.")
                return

            if (0 in board[0] or 0 in board[1] or 0 in board[2]):
                cpu_move(board)

                if check_win(board, 3) == True:
                    print("CPU wins.")
                    return

    else:
        raise KeyboardInterrupt

    print("Draw.")

while True:
    try:
        play(game_board)
    except KeyboardInterrupt:
        print("Bye.")
        break
