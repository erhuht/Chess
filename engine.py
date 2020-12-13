import chess
import chess.svg
import random
import time
from IPython.display import display, Markdown, clear_output

class Player:
    def __init__(self, color):
        self.color = color


class RandomPlayer(Player):
    def move(self, board):
        time.sleep(0.5)
        return random.choice([move for move in board.legal_moves])

class AIPlayer(Player):
    def __init__(self, color):
        self.color = color
        self.depth_limit = 3

    def move(self, board):
        moves = {}
        for move in board.legal_moves:
            board.push(move)
            moves[move] = self.evaluate_move(board, 1)
            board.pop()

        best_moves = []
        for key in moves.keys():
            if moves[key] == max(moves.values()):
                best_moves.append(key)
        
        return random.choice(best_moves)
            

    def evaluate_move(self, board, depth):
        if depth % 2: #if depth is odd ie. minimizing player
            points = 40
        else:
            points = -40

        for move in board.legal_moves:
            if depth < self.depth_limit:
                board.push(move)
                if depth % 2: #if depth is odd ie. minimizing player
                    points = min(points, self.evaluate_move(board, depth+1))
                else:
                    points = max(points, self.evaluate_move(board, depth+1))
                board.pop()
            else:
                return self.calculate_material(board)

        return points
    
    def calculate_material(self, board):
        material = 0
        material += len(board.pieces(chess.PAWN, self.color))*1
        material += len(board.pieces(chess.KNIGHT, self.color))*3
        material += len(board.pieces(chess.BISHOP, self.color))*3
        material += len(board.pieces(chess.ROOK, self.color))*5
        material += len(board.pieces(chess.QUEEN, self.color))*9
        material -= len(board.pieces(chess.PAWN, not self.color))*1
        material -= len(board.pieces(chess.KNIGHT, not self.color))*3
        material -= len(board.pieces(chess.BISHOP, not self.color))*3
        material -= len(board.pieces(chess.ROOK, not self.color))*5
        material -= len(board.pieces(chess.QUEEN, not self.color))*9

        return material

class HumanPlayer(Player):
    def move(self, board):
        while True:
            try:
                move = board.parse_san(input("Move: "))
            except ValueError:
                print("Invalid move")
            else:
                return move
        

board = chess.Board()
white = HumanPlayer(chess.WHITE)
black = AIPlayer(chess.BLACK)


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
    display(Markdown(chess.svg.board(board, size=400, lastmove=move)))

print("\n")
if board.result() == "1-0":
    print("White won on move %d" % move_number)
elif board.result() == "0-1":
    print("Black won on move %d" % move_number)
elif board.result() == "1/2-1/2":
    print("It's a draw on move %d" % move_number)
else:
    print("Something has gone wrong")