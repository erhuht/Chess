from engine import AIPlayer, LegacyAIPlayer, RandomPlayer, HumanPlayer
import chess
import chess.svg
import chess.pgn
from IPython.display import display, Markdown, clear_output
from math import ceil
import sys



whitewin = 0
blackwin = 0
draw = 0
p1 = 0
p2 = 0
for i in range(int(sys.argv[3])):
    if i % 2:
        board = chess.Board()
        white = {'a':AIPlayer, 'r':RandomPlayer, 'l':LegacyAIPlayer}[sys.argv[2]](chess.WHITE)
        black = {'a':AIPlayer, 'r':RandomPlayer, 'l':LegacyAIPlayer}[sys.argv[1]](chess.BLACK)
        perspective = chess.BLACK
    else:
        board = chess.Board()
        white = {'a':AIPlayer, 'r':RandomPlayer, 'l':LegacyAIPlayer}[sys.argv[1]](chess.WHITE)
        black = {'a':AIPlayer, 'r':RandomPlayer, 'l':LegacyAIPlayer}[sys.argv[2]](chess.BLACK)
        perspective = chess.WHITE
    
    move_number = 0
    while not board.is_game_over():
        move_number += 1
        if board.turn == chess.WHITE:
            move = white.move(board)
            board.push(move)
        else:
            move = black.move(board)
            board.push(move)

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
        whitewin += 1
        if i % 2:
            p2 += 1
        else:
            p1 += 1
    elif board.result() == "0-1":
        print("Black won on move %d" % ceil(move_number/2))
        blackwin += 1
        if i % 2:
            p1 += 1
        else:
            p2 += 1
    elif board.result() == "1/2-1/2":
        print("It's a draw on move %d" % ceil(move_number/2))
        draw += 1
    else:
        print("Something has gone wrong")

display(Markdown(""" White | Black | Draw | Player 1 (%s) | Player 2 (%s)
 :---: |:---: |:---: |:---: |:---:  
 %d | %d | %d | %d | %d """ % ({'a':"AI", 'r':"Random", 'l':"Legacy AI"}[sys.argv[1]], {'a':"AI", 'r':"Random", 'l':"Legacy AI"}[sys.argv[1]], whitewin, blackwin, draw, p1, p2)))