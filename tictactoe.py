
#Tic Tac Toe Player
#By: Victor Osunji


import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    # Returns starting state of the board.
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    # Returns player who has the next turn on a board.
    # Initialize counter for X and O
    
    counterX = 0
    counterO = 0
    
    # Count how many X and O there are in the board
    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column] == X:
                counterX += 1
            if board[row][column] == O:
                counterO += 1

    # If there are more X then O, next turn is O
    if counterX > counterO:
        return O
    # If there is O == X, next turn is X
    else:
        return X


def moves(board):
    
    # Returns set of all possible moves (i, j) available on the board.
    # i = row of the move (0, 1, or 2) 
    # j = cell in the row (0, 1, or 2) 
    
    # Create a empty set of all possible moves
    AllPossibleMoves = set()

    # Possible moves are any cells that are empty
    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column] == EMPTY:
                AllPossibleMoves.add((row,column))

    # Return the set
    return AllPossibleMoves


def result(board, move):
    
    # Returns the board that results from making move (i, j) on the board.
    
    # If move is not a open move for the board, raise an exception.
    if move not in moves(board):
        raise Exception('move is not a valid move for the board!')

    # makes a deep copy of the board first before making any changes.
    board_copy = copy.deepcopy(board)

    # returns board state with updated board
    x, y = move
    board_copy[x][y] = player(board)
    return board_copy


# checks horizontally if X or O has won
def checkRow(board,player):
    for row in range(len(board)):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True
    return False


# Checks vertically if X or O has won
def checkColumn(board,player):
    for column in range(len(board)):
        if board[0][column] == player and board[1][column] == player and board[2][column] == player:
            return True
    return False


# checks diagonally if X or O has won
def checkTopDiagonal(board,player):
    count = 0
    for row in range(len(board)):
        for column in range(len(board[row])):
            if row == column and board[row][len(board) - row - 1] == player:
                count += 1
    return count == 3


# One can win the game with three of their moves in a row diagonally.
def checkBottomDiagonal(board,player):
    count = 0
    for row in range(len(board)):
        for column in range(len(board[row])):
            if row == column and board[row][column] == player:
                count += 1
    return count == 3    


def winner(board):
    
    # Returns the winner X, O or, None.
    
    # If X won, return X. 
    if checkRow(board,X) or checkColumn(board,X) or checkBottomDiagonal(board,X) or checkTopDiagonal(board,X):
        return X 
    
    # If O won, return O.
    elif checkRow(board,O) or checkColumn(board,O) or checkBottomDiagonal(board,O) or checkTopDiagonal(board,O):
        return O

    # If game is in progress, or a tie, return None
    else:
        return None


def terminal(board):
    
    # Returns True if game is over, else False
    
    # If the game is over, return True
    if winner(board) == X:
        return True
    if winner(board) == O:
        return True
    
    # If there are still empty cells, return False
    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column] == EMPTY:
                return False

    # If there game was a tie, return True
    return True


def utility(board):
    
    # Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    
    # If X won the game, the utility is 1. 
    if winner(board) == X:
        return 1
    # If O won the game, the utility is -1. 
    elif winner(board) == O:
        return -1
    # If the game has is a tie, the utility is 0.
    else:
        return 0


def max_value(board):
    v = -math.inf
    if terminal(board):
        return utility(board)
    for move in moves(board):
        v = max(v, min_value(result(board, move)))
    return v


def min_value(board):
    v = math.inf
    if terminal(board):
        return utility(board)
    for move in moves(board):
        v = min(v, max_value(result(board, move)))
    return v

def minimax(board):
    
    # If the board is a terminal board, return None.
    if terminal(board):
        return None
    
    # Case of player is X
    elif player(board) == X:
        plays = []
        # Loop over the moves to get the max value for X and min value for O
        for move in moves(board):
            # Add in plays a tuple with the min_value and the moves that results to its value
            plays.append([min_value(result(board,move)), move])
        # Reverse sort for the plays list and get the move that should take
        return sorted(plays, key=lambda x: x[0], reverse=True)[0][1]
    
    # Case of player is O
    elif player(board) == O:
        plays = []
        for move in moves(board):
            # Add in plays a tuple with the max_value and the moves that results to its value
            plays.append([max_value(result(board,move)), move])
        # Reverse sort for the plays list and get the move that should take
        return sorted(plays, key=lambda x: x[0])[0][1]