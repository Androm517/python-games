"""
class: GameRules
"""
from position import Position
from piece import Pawn, Rook, Knight, Bishop, Queen, King, WHITE, BLACK
from exceptions import *


class GameRules:
    def __init__(self, white_pieces=None, black_pieces=None):
        self.white_pieces = white_pieces
        self.black_pieces = black_pieces
        self.pieces = self.white_pieces + self.black_pieces

    def setupInitialPosition(self):
        self.white_pieces += [Pawn(col + '2', WHITE, 'pawn') for col in 'abcdefgh']
        self.white_pieces.append(Rook('a' + '1', WHITE, 'rook'))
        self.white_pieces.append(Knight('b' + '1', WHITE, 'knight'))
        self.white_pieces.append(Bishop('c' + '1', WHITE, 'bishop'))
        self.white_pieces.append(Queen('d' + '1', WHITE, 'queen'))
        self.white_pieces.append(King('e' + '1', WHITE, 'king'))
        self.white_pieces.append(Bishop('f' + '1', WHITE, 'bishop'))
        self.white_pieces.append(Knight('g' + '1', WHITE, 'knight'))
        self.white_pieces.append(Rook('h' + '1', WHITE, 'rook'))

        self.black_pieces += [Pawn(col + '7', BLACK, 'pawn') for col in 'abcdefgh']
        self.black_pieces.append(Rook('a' + '8', BLACK, 'rook'))
        self.black_pieces.append(Knight('b' + '8', BLACK, 'knight'))
        self.black_pieces.append(Bishop('c' + '8', BLACK, 'bishop'))
        self.black_pieces.append(Queen('d' + '8', BLACK, 'queen'))
        self.black_pieces.append(King('e' + '8', BLACK, 'king'))
        self.black_pieces.append(Bishop('f' + '8', BLACK, 'bishop'))
        self.black_pieces.append(Knight('g' + '8', BLACK, 'knight'))
        self.black_pieces.append(Rook('h' + '8', BLACK, 'rook'))

    def applyGameRules(self, active_piece, target):
        target = Position(target)
        direction = active_piece.position.unitVector(target)
        if active_piece.name == 'pawn':
            self.pawnRules(active_piece, target, direction)
        elif active_piece.name == 'rook':
            self.rookRules(active_piece, target, direction)
        elif active_piece.name == 'knight':
            self.knightRules(active_piece, target, direction)
        elif active_piece.name == 'bishop':
            self.bishopRules(active_piece, target, direction)
        elif active_piece.name == 'queen':
            self.queenRules(active_piece, target, direction)
        elif active_piece.name == 'king':
            self.kingRules(active_piece, target, direction)

    def pawnRules(self, active_piece, target, direction):
        # Rule 1
        forward_move = self.pawnMoveForwardRule(active_piece, target, direction)
        # Rule 2
        capture = self.pawnMoveCapture(active_piece, target, direction)
        # Rule 3 addera fler regler. Till exempel an passant.
        # check rules
        if not forward_move and not capture:
            raise ImpossibleMoveException(active_piece, target)

    def pawnMoveCapture(self, active_piece, target, direction):
        test_distance = active_piece.position.add(direction)
        if not target == test_distance:
            return False
        pieces = self.white_pieces if active_piece.color == BLACK else self.black_pieces
        for piece in pieces:
            if piece.position == target:
                pieces.remove(piece)
                return True
        return False

    def pawnMoveForwardRule(self, active_piece, target, direction):
        if not target.getColumn() == active_piece.position.getColumn():
            return False
        return self.moveDirection(active_piece, target, direction)

    def rookRules(self, active_piece, target, direction):
        # rule 1
        prev_target = target.sub(direction)
        directions = [Position(( 1, 0)), Position( ( 0, 1)), Position( (-1, 0)), Position( (0, -1))]
        if direction in directions:
            move_to_adjacent_of_target = self.moveDirection(active_piece, prev_target, direction)
        else:
            move_to_adjacent_of_target = False
        # rule 2
        attacking_target = self.moveAttacking(active_piece, target)
        if not move_to_adjacent_of_target or not attacking_target:
            raise ImpossibleMoveException(active_piece, target)

    def knightRules(self, active_piece, target, direction):
        #rule 1
        start = active_piece.position
        possible_moves = []
        possible_moves.append(start.add(Position( (1, 2))))
        possible_moves.append(start.add(Position( (-1, 2))))
        possible_moves.append(start.add(Position( (-1, -2))))
        possible_moves.append(start.add(Position( (1, -2))))
        possible_moves.append(start.add(Position( (2, 1))))
        possible_moves.append(start.add(Position( (-2, 1))))
        possible_moves.append(start.add(Position( (-2, -1))))
        possible_moves.append(start.add(Position( (2, -1))))
        if target in possible_moves:
            attacking_target = self.moveAttacking(active_piece, target)
        else:
            attacking_target = False
        # check rules
        if not attacking_target:
            raise ImpossibleMoveException(active_piece, target)

    def bishopRules(self, active_piece, target, direction):
        # rule 1
        prev_target = target.sub(direction)
        directions = [Position( (1, 1)), Position( (-1, 1)), Position( (-1, -1)), Position( (1, -1))]
        if direction in directions:
            move_to_adjacent_of_target = self.moveDirection(active_piece, prev_target, direction)
        else:
            move_to_adjacent_of_target = False
        # rule 2
        attacking_target = self.moveAttacking(active_piece, target)
        # check rules
        if not move_to_adjacent_of_target or not attacking_target:
            raise ImpossibleMoveException(active_piece, target)

    def queenRules(self, active_piece, target, direction):
        # rule 1
        prev_target = target.sub(direction)
        move_to_adjacent_of_target = self.moveDirection(active_piece, prev_target, direction)
        #rule 2
        attacking_target = self.moveAttacking(active_piece, target)
        # check rules
        if not move_to_adjacent_of_target or not attacking_target:
            raise ImpossibleMoveException(active_piece, target)

    def kingRules(self, active_piece, target, direction):
        # rule 1
        attacking_target = self.moveAttacking(active_piece, target)
        # check rules
        if not attacking_target:
            raise ImpossibleMoveException(active_piece, target)

    def moveAttacking(self, active_piece, target):
        pieces = self.white_pieces if active_piece.color == WHITE else self.black_pieces
        for piece in pieces:
            if piece.position == target:
                return False
        return True

    def moveDirection(self, active_piece, target, direction):
        step = active_piece.position
        while not step == target:
            step = step.add(direction)
            if step.isPositionOutsideBoard():
                return False
            for piece in self.pieces:
                if piece.position == step:
                    return False
        return True
