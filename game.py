from engine import AIPlayer, LegacyAIPlayer, RandomPlayer, HumanPlayer
import chess
import chess.svg
import chess.pgn
from IPython.display import display, Markdown, clear_output
from math import ceil
import sys

board = chess.Board()
white = {'a':AIPlayer, 'h':HumanPlayer, 'r':RandomPlayer, 'l':LegacyAIPlayer}[sys.argv[1]](chess.WHITE)
black = {'a':AIPlayer, 'h':HumanPlayer, 'r':RandomPlayer, 'l':LegacyAIPlayer}[sys.argv[2]](chess.BLACK)
perspective = {'w':chess.WHITE, 'b':chess.BLACK}[sys.argv[3]]

move_number = 0
game = chess.pgn.Game()
node = game
while not board.is_game_over():
    move_number += 1
    if board.turn == chess.WHITE:
        move = white.move(board)
        board.push(move)
    else:
        move = black.move(board)
        board.push(move)
    node = node.add_variation(move)

    clear_output(wait=True)
    if board.is_check():
        if board.turn == chess.WHITE:
            display(Markdown(chess.svg.board(board, size=400, lastmove=move, orientation=perspective, check=board.king(chess.WHITE))))
        else:
            display(Markdown(chess.svg.board(board, size=400, lastmove=move, orientation=perspective, check=board.king(chess.BLACK))))
    else:
        display(Markdown(chess.svg.board(board, size=400, lastmove=move, orientation=perspective)))
    

print("\n")
if board.result() == "1-0":
    print("White won on move %d" % ceil(move_number/2))
elif board.result() == "0-1":
    print("Black won on move %d" % ceil(move_number/2))
elif board.result() == "1/2-1/2":
    print("It's a draw on move %d" % ceil(move_number/2))
else:
    print("Something has gone wrong")

print(game, file=open("game.pgn", "w"), end="\n\n")