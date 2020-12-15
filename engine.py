import chess
import chess.svg
import chess.pgn
import random
import time
from IPython.display import display, Markdown, clear_output

class Player:
    def __init__(self, color):
        self.color = color


class RandomPlayer(Player):
    def move(self, board):
        return random.choice([move for move in board.legal_moves])

class AIPlayer(Player):
    def __init__(self, color):
        self.color = color
        self.depth_limit = 3

    def move(self, board):
        moves = {}
        for move in board.legal_moves: #depth 0
            board.push(move)
            moves[move] = self.evaluate_move(board, 1, -41, 41)
            board.pop()

        best_moves = []
        for key in moves.keys():
            if moves[key] == max(moves.values()):
                best_moves.append(key)
        
        return random.choice(best_moves)
            

    def evaluate_move(self, board, depth, alpha, beta):
        if depth % 2: #if depth is odd ie. minimizing player
            extremepoints = 40
        else:
            extremepoints = -40

        for move in board.legal_moves:
            if depth < self.depth_limit:
                board.push(move)
                if depth % 2: #if depth is odd ie. minimizing player
                    points = self.evaluate_move(board, depth+1, alpha, beta)
                    extremepoints = min(extremepoints, points)
                    beta = min(beta, points)
                    if alpha >= beta: # beta cutoff
                        board.pop()
                        break
                else:
                    points = self.evaluate_move(board, depth+1, alpha, beta)
                    extremepoints = max(extremepoints, points)
                    alpha = max(alpha, points)
                    if beta <= alpha: # alpha cutoff
                        board.pop()
                        break
                board.pop()
            else:
                return self.calculate_material(board)

        return extremepoints
    
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

class HumanPlayer(Player): # Input is unreliable in jupyter, works after a few restarts
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
perspective = chess.WHITE

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
    display(Markdown(chess.svg.board(board, size=400, lastmove=move, orientation=perspective)))

print("\n")
if board.result() == "1-0":
    print("White won on move %d" % move_number)
elif board.result() == "0-1":
    print("Black won on move %d" % move_number)
elif board.result() == "1/2-1/2":
    print("It's a draw on move %d" % move_number)
else:
    print("Something has gone wrong")

print(game, file=open("game.pgn", "w"), end="\n\n")