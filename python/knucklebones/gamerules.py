import random
from . import ai
from copy import deepcopy

playerNames = ["White", "Black", "Draw"]


def turn(board, player):
    # Turn of the game
    # Roll the dice
    dice = rollDice()
    print("Dice: " + str(dice))

    if player == 0:
        while True:
            try:
                move = int(input(f"{playerNames[player]}'s move: ")) - 1
            except ValueError:
                print("Invalid move!")
                continue
            # Check if the move is valid
            if not checkMove(move, board, player):
                print("Invalid move!")
                continue
            break
    else:
        boardCopy = deepcopy(board)
        move = ai.chooseMove(boardCopy, player, dice, maxDepth=1)
        print(f"{playerNames[player]}'s move: {move + 1}")

    # Make the move
    makeMove(move, board, player, dice)


def rollDice():
    dice = random.randint(1, 6)
    return dice


def checkMove(move, board, player):
    if not move in [0, 1, 2]:
        return False
    if len(board[player][move]) == 3:
        return False
    return True


def checkWin(board):
    # Check if the game is over
    if not ((len(board[0][0]) == 3 and len(board[0][1]) == 3 and len(board[0][2]) == 3) or (len(board[1][0]) == 3 and len(board[1][1]) == 3 and len(board[1][2]) == 3)):
        # Game is not over
        return None, None, None

    # Game is over
    whitePoints = calculatePoints(board, 0)
    blackPoints = calculatePoints(board, 1)

    if whitePoints > blackPoints:
        winner = 0
    elif blackPoints > whitePoints:
        winner = 1
    else:
        winner = 2

    return winner, whitePoints, blackPoints


def calculatePoints(board, player):
    points = 0
    for column in board[player]:
        pcsDict = {}
        for piece in column:
            if piece in pcsDict:
                pcsDict[piece] += 1
            else:
                pcsDict[piece] = 1
        for piece, count in pcsDict.items():
            points += piece * count ** 2
    return points


def makeMove(move, board, player, dice):
    board[player][move].append(dice)

    while True:
        if dice in board[(player + 1) % 2][move]:
            board[(player + 1) % 2][move].remove(dice)
        else:
            break
