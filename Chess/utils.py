from position import Position
from piece import WHITE, BLACK
from exceptions import *

def str_repr(pos):
    return chr(ord('a') + pos[1]) + chr(ord('1') + pos[0])


def nbr_repr(pos):
    return ( ord(pos[1]) - ord('1'), ord(pos[0]) - ord('a'))

def possibleMovesPawn(self):
    move_forward = Position( (1, 0))
    move_left = move_forward.add(Position( (0, -1)))
    move_right = move_forward.add(Position( (0, 1)))
    if self.color == WHITE:
        possible_moves = [self.position.add(move_forward), self.position.add(move_left), self.position.add(move_right)]
        if self.firstMove:
            double = Position((2, 0))
            possible_moves.append(self.position.add(double) )
    else:
        possible_moves = [self.position.sub(move_forward), self.position.sub(move_left), self.position.sub(move_right)]
        if self.firstMove:
            double = Position((2, 0))
            possible_moves.append(self.position.sub(double))
    return possible_moves

def isObstructedPawn(piece, target, whitePieces, blackPieces):
    passive_pieces = whitePieces if piece.color == BLACK else blackPieces
    pieces = whitePieces + blackPieces
    if piece.color == WHITE:
        forward = piece.position.add(Position((1, 0)))
        double_forward = forward.add(Position( (1, 0) ))
        left = piece.position.add(Position((1, -1)))
        right = piece.position.add(Position((1, 1)))
    else:
        forward = piece.position.sub(Position((1, 0)))
        double_forward = forward.sub(Position((1, 0)))
        left = piece.position.sub(Position((1, -1)))
        right = piece.position.sub(Position((1, 1)))
    move = Position(target)
    if move == forward:
        for piece in pieces:
            if piece.position == forward:
                return True
    if move == double_forward:
        for piece in pieces:
            if piece.position == forward:
                return True
        for piece in pieces:
            if piece.position == double_forward:
                return True
    if move == left:
        for piece in passive_pieces:
            if piece.position == left:
                break
        else:
            return True
    if move == right:
        for piece in passive_pieces:
            if piece.position == right:
                break
        else:
            return True
    return False

def validatePawnMove(piece, target):
    if not piece.isPossibleMove(target):
        raise ImpossibleMoveException(piece, target)
    if isPawnTargetBlocked(piece, target):
        raise ImpossibleMoveException(piece, target)

def isPawnTargetBlocked(piece, target):
    if isTargetSameColor(piece, target) or isTargetObstructed(piece, target):
        return True
    else:
        return False

def isTargetSameColor(piece, target, white_pieces, black_pieces):
    return piece.isSameColor(target, white_pieces, black_pieces)

def isTargetObstructed(piece, target, white_pieces, black_pieces):
    return piece.isObstructed(target, white_pieces, black_pieces)
