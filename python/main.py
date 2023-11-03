import knucklebones.ai as ai
import knucklebones.gamerules as game
import sys

sys.setrecursionlimit(10000) 
    
def main():
    # Initialization of the game
    # first is white, second is black, then column
    board = [[[], [], []], [[], [], []]]
    player = 0  # 0 for white, 1 for black

    winner = None
    turn = 0
    while not winner:
        # Game loop
        print("Turn " + str(turn))
        game.turn(board, player)
        player = (player + 1) % 2
        winner, whitePoints, blackPoints = game.checkWin(board)
        print(board)
        turn += 1
        
    print("The winner is " + game.playerNames[winner] + "!")
    print("Score: " + str(whitePoints) + " - " + str(blackPoints))

main()