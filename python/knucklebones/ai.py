from . import gamerules as game
from copy import deepcopy


def chooseMove(board, player, dice, maxDepth = 3):
    """Returns the best move for the given player on the given board."""
    boardCopy = deepcopy(board)

    possibleMoves = getPossibleMoves(board, player)
    moveScores = createNodes(player, boardCopy, player,
                             maxDepth, dice, possibleMoves)

    return max(moveScores, key=moveScores.get)


def getPossibleMoves(board, player):
    possibleMoves = []

    for idx, column in enumerate(board[player]):
        if len(column) == 3:
            continue
        possibleMoves.append(idx)

    columnsDicts = [{}, {}, {}]
    for column in board[player]:
        columnsDict = {}
        for piece in column:
            if piece in columnsDict:
                columnsDict[piece] += 1
            else:
                columnsDict[piece] = 1
        for piece, count in columnsDict.items():
            columnsDicts[board[player].index(column)][piece] = count

    # Find duplicates
    for idx, column in enumerate(columnsDicts):
        if not idx in possibleMoves:
            continue

        for piece, count in column.items():
            for i in range(idx+1, 3):
                for piece2, count2 in columnsDicts[i].items():
                    if piece == piece2 and count == count2:
                        possibleMoves.remove(idx)
                        break

    return possibleMoves


def minimax(initialPlayer, board, player, maxDepth, depth=0):
    winner, whitePoints, blackPoints = game.checkWin(board)
    if winner == initialPlayer:
        return 1000
    elif winner == (initialPlayer + 1) % 2:
        return -1000
    elif winner == 2:
        return 0

    if depth == maxDepth:
        # print("depth")
        aiPoints = game.calculatePoints(board, initialPlayer)
        enemyPoints = game.calculatePoints(board, (initialPlayer + 1) % 2)
        negation = 1
        if enemyPoints > aiPoints:
            negation = -1
            aiPoints, enemyPoints = enemyPoints, aiPoints
        if enemyPoints == 0:
            if aiPoints == 0:
                return 0
            return max(min(((aiPoints - enemyPoints)**(1.3)) * 4 * negation, 1), -1)
        print("scores")
        print(((aiPoints - enemyPoints)**(1.3) *
              (aiPoints / enemyPoints)**(0.8)) * 4*negation)
        return max(min(((aiPoints - enemyPoints)**(1.3) * (aiPoints / enemyPoints)**(0.8)) * 3*negation, 1000), -1000)

    dicePoints = [0, 0, 0, 0, 0, 0]
    possibleMoves = getPossibleMoves(board, player)
    
    boardCopy = deepcopy(board)

    for dice in range(1, 7):
        moveScores = createNodes(
            initialPlayer, boardCopy, player, maxDepth, dice, possibleMoves, depth + 1)
        bestMove = max(moveScores, key=moveScores.get)
        dicePoints[dice - 1] = moveScores[bestMove]/len(possibleMoves)
        print(dicePoints[dice - 1], dice)
    print(dicePoints, depth)

    return sum(dicePoints)/6


def createNodes(initialPlayer, board, player, maxDepth, dice, possibleMoves, depth=0):
    moveScores = {}
    for possibleMove in possibleMoves:
        boardCopy = deepcopy(board)
        game.makeMove(possibleMove, boardCopy, player, dice)
        moveScores[possibleMove] = minimax(
            initialPlayer, boardCopy, player, maxDepth)
    return moveScores
