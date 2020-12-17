import chess
import chess.svg
import chess.pgn
import random
import time
from IPython.display import display, Markdown, clear_output
from math import ceil

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
        self.OUTER_CENTER = chess.SquareSet([chess.C3, chess.D3, chess.E3, chess.F3, chess.F4, chess.F5, chess.F6, chess.E6, chess.D6, chess.C6, chess.C5, chess.C4])

    def move(self, board):
        moves = {}
        for move in board.legal_moves: #depth 0
            board.push(move)
            moves[move] = self.evaluate_move(board, 1, float("-inf"), float("inf"))
            board.pop()

        best_moves = []
        for key in moves.keys():
            if moves[key] == max(moves.values()):
                best_moves.append(key)
        
        chosen_move = random.choice(best_moves)
        if board.is_castling(chosen_move):
            self.castled = True
        return chosen_move
            

    def evaluate_move(self, board, depth, alpha, beta):
        if depth % 2: #if depth is odd ie. minimizing player
            extremepoints = float("inf")
        else:
            extremepoints = float("-inf")

        if depth < self.depth_limit and (not board.is_game_over()):
            for move in board.legal_moves:
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
            return self.evaluate_position(board)

        return extremepoints

    def evaluate_position(self, board): # 0 = even situation
        points = self.calculate_material(board)


        #Occupy center
        points += (len(board.pieces(chess.PAWN, self.color) & chess.SquareSet(chess.BB_CENTER)) - len(board.pieces(chess.PAWN, not self.color) & chess.SquareSet(chess.BB_CENTER)))*30
        points += (len(board.pieces(chess.KNIGHT, self.color) & chess.SquareSet(chess.BB_CENTER)) - len(board.pieces(chess.PAWN, not self.color) & chess.SquareSet(chess.BB_CENTER)))*30
        points += (len(board.pieces(chess.KNIGHT, self.color) & self.OUTER_CENTER) - len(board.pieces(chess.KNIGHT, not self.color) & self.OUTER_CENTER))*25
        points += (len(board.pieces(chess.BISHOP, self.color) & self.OUTER_CENTER) - len(board.pieces(chess.BISHOP, not self.color) & self.OUTER_CENTER))*25

        #Knight on rim
        points -= len(board.pieces(chess.KNIGHT, self.color) & chess.SquareSet(chess.BB_FILE_A | chess.BB_FILE_H))*25

        #advancing pawns
        if self.color == chess.WHITE:
            points += len(board.pieces(chess.PAWN, self.color) & chess.SquareSet(chess.BB_RANK_7))*50
        else:
            points += len(board.pieces(chess.PAWN, self.color) & chess.SquareSet(chess.BB_RANK_2))*50

        #Castling
        if self.color == chess.WHITE:
            if len(board.pieces(chess.ROOK, self.color) & chess.SquareSet(chess.BB_RANK_1)) > 1:
                if not (chess.square_file(board.king(self.color)) < min([chess.square_file(square) for square in board.pieces(chess.ROOK, self.color)]) or chess.square_file(board.king(self.color)) > max([chess.square_file(square) for square in board.pieces(chess.ROOK, self.color)])):
                    if not board.has_castling_rights(self.color):
                        points -= 20
                else:
                    points += 20
        else:
            if len(board.pieces(chess.ROOK, self.color) & chess.SquareSet(chess.BB_RANK_8)) > 1:
                if not (chess.square_file(board.king(self.color)) < min([chess.square_file(square) for square in board.pieces(chess.ROOK, self.color)]) or chess.square_file(board.king(self.color)) > max([chess.square_file(square) for square in board.pieces(chess.ROOK, self.color)])):
                    if not board.has_castling_rights(self.color):
                        points -= 20
                else:
                    points += 20

        #Purposefully at the end:
        if board.is_game_over():
            if board.result() == "1/2-1/2":
                if points > 250:
                    points -= 200
                elif points < -250:
                    points += 200
            elif (board.result() == "1-0" and self.color == chess.WHITE) or (board.result() == "0-1" and self.color == chess.BLACK):
                points += 20000
            elif (board.result() == "1-0" and self.color == chess.BLACK) or (board.result() == "0-1" and self.color == chess.WHITE): #just to be sure
                points -= 20000

        return points

        #Castle x (needs work)
        #Occupy center x
        #Own piece-square tables?
        #Game phases?
        #Connect Rooks?
        #avoid draw x
        #Knight on rim x

        #move ordering:
        #captures
        #number of legal move for opponent
        #check

        #endgames

    def calculate_material(self, board):
        material = 0
        material += len(board.pieces(chess.PAWN, self.color))*100
        material += len(board.pieces(chess.KNIGHT, self.color))*320
        material += len(board.pieces(chess.BISHOP, self.color))*330
        material += len(board.pieces(chess.ROOK, self.color))*500
        material += len(board.pieces(chess.QUEEN, self.color))*900
        material -= len(board.pieces(chess.PAWN, not self.color))*100
        material -= len(board.pieces(chess.KNIGHT, not self.color))*320
        material -= len(board.pieces(chess.BISHOP, not self.color))*330
        material -= len(board.pieces(chess.ROOK, not self.color))*500
        material -= len(board.pieces(chess.QUEEN, not self.color))*900

        return material

class LegacyAIPlayer(AIPlayer):
    def move(self, board):
        moves = {}
        for move in board.legal_moves: #depth 0
            board.push(move)
            moves[move] = self.evaluate_move(board, 1, float("-inf"), float("inf"))
            board.pop()

        best_moves = []
        for key in moves.keys():
            if moves[key] == max(moves.values()):
                best_moves.append(key)
        
        chosen_move = random.choice(best_moves)
        if board.is_castling(chosen_move):
            self.castled = True
        return chosen_move
            

    def evaluate_move(self, board, depth, alpha, beta):
        if depth % 2: #if depth is odd ie. minimizing player
            extremepoints = float("inf")
        else:
            extremepoints = float("-inf")

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
white = AIPlayer(chess.WHITE)
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
    print("White won on move %d" % ceil(move_number/2))
elif board.result() == "0-1":
    print("Black won on move %d" % ceil(move_number/2))
elif board.result() == "1/2-1/2":
    print("It's a draw on move %d" % ceil(move_number/2))
else:
    print("Something has gone wrong")

print(game, file=open("game.pgn", "w"), end="\n\n")