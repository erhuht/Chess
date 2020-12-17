from engine import *




whitewin = 0
blackwin = 0
draw = 0
new = 0
old = 0
for i in range(2):
    if i % 2:
        board = chess.Board()
        white = AIPlayer(chess.WHITE)
        black = LegacyAIPlayer(chess.BLACK)
        perspective = chess.WHITE
    else:
        board = chess.Board()
        white = LegacyAIPlayer(chess.WHITE)
        black = AIPlayer(chess.BLACK)
        perspective = chess.BLACK

    while not board.is_game_over():
        if board.turn == chess.WHITE:
            move = white.move(board)
            board.push(move)
        else:
            move = black.move(board)
            board.push(move)

        clear_output(wait=True)
        display(Markdown(chess.svg.board(board, size=400, lastmove=move, orientation=perspective)))

    print("\n")
    if board.result() == "1-0":
        print("White won on move %d" % move_number)
        whitewin += 1
        if i % 2:
            new += 1
        else:
            old += 1
    elif board.result() == "0-1":
        print("Black won on move %d" % move_number)
        blackwin += 1
        if i % 2:
            old += 1
        else:
            new += 1
    elif board.result() == "1/2-1/2":
        print("It's a draw on move %d" % move_number)
        draw += 1
    else:
        print("Something has gone wrong")


print("White: %d, Black: %d, Draw: %d, New: %d, Old: %d" % (whitewin, blackwin, draw, new, old))