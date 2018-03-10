"""
class: GameRules
"""
import position
import piece
import exceptions


class GameRules:
    """ GameRules contain game logic, present chess pieces, colors and position. It transforms chessboard positions
    given as 'a1' to Position. Position is used for game logic."""
    def __init__(self):
        self.white_pieces = []
        self.black_pieces = []
        self.position = position.Position
        self.setupInitialPosition()
        self.pieces = self.white_pieces + self.black_pieces

    def setupInitialPosition(self):
        self.white_pieces += [piece.Pawn(self.position(col + '2'), piece.Piece.WHITE, 'pawn') for col in 'abcdefgh']
        self.white_pieces.append(piece.Rook(self.position('a' + '1'), piece.Piece.WHITE, 'rook'))
        self.white_pieces.append(piece.Knight(self.position('b' + '1'), piece.Piece.WHITE, 'knight'))
        self.white_pieces.append(piece.Bishop(self.position('c' + '1'), piece.Piece.WHITE, 'bishop'))
        self.white_pieces.append(piece.Queen(self.position('d' + '1'), piece.Piece.WHITE, 'queen'))
        self.white_pieces.append(piece.King(self.position('e' + '1'), piece.Piece.WHITE, 'king'))
        self.white_pieces.append(piece.Bishop(self.position('f' + '1'), piece.Piece.WHITE, 'bishop'))
        self.white_pieces.append(piece.Knight(self.position('g' + '1'), piece.Piece.WHITE, 'knight'))
        self.white_pieces.append(piece.Rook(self.position('h' + '1'), piece.Piece.WHITE, 'rook'))

        self.black_pieces += [piece.Pawn(self.position(col + '7'), piece.Piece.BLACK, 'pawn') for col in 'abcdefgh']
        self.black_pieces.append(piece.Rook(self.position('a' + '8'), piece.Piece.BLACK, 'rook'))
        self.black_pieces.append(piece.Knight(self.position('b' + '8'), piece.Piece.BLACK, 'knight'))
        self.black_pieces.append(piece.Bishop(self.position('c' + '8'), piece.Piece.BLACK, 'bishop'))
        self.black_pieces.append(piece.Queen(self.position('d' + '8'), piece.Piece.BLACK, 'queen'))
        self.black_pieces.append(piece.King(self.position('e' + '8'), piece.Piece.BLACK, 'king'))
        self.black_pieces.append(piece.Bishop(self.position('f' + '8'), piece.Piece.BLACK, 'bishop'))
        self.black_pieces.append(piece.Knight(self.position('g' + '8'), piece.Piece.BLACK, 'knight'))
        self.black_pieces.append(piece.Rook(self.position('h' + '8'), piece.Piece.BLACK, 'rook'))

    def applyGameRules(self, color, start, target):
        start = self.position(start)
        target = self.position(target)
        active_piece, passive_pieces = self.getActivePieceAndPassivePieces(color, start)
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

        active_piece.position = target
        self.removeCapturedPiece(passive_pieces, target)

    def removeCapturedPiece(self, passive_pieces, target):
        for i, passive_piece in enumerate(passive_pieces):
            if passive_piece.position == target:
                del passive_pieces[i]
                break

    def getActivePieceAndPassivePieces(self, color, start):
        active_pieces, passive_pieces = (self.white_pieces, self.black_pieces) if color == piece.Piece.WHITE else (
            self.black_pieces, self.white_pieces)
        for active_piece in active_pieces:
            if active_piece.position == start:
                return active_piece, passive_pieces
        else:
            raise exceptions.PieceNotFoundException(color, start)

    def pawnRules(self, active_piece, target, direction):
        # Rule 1
        forward_move = self.pawnMoveForwardRule(active_piece, target, direction)
        # Rule 2
        capture = self.pawnMoveCapture(active_piece, target, direction)
        # Rule 3 addera fler regler. Till exempel an passant.
        # check rules
        if not forward_move and not capture:
            raise exceptions.ImpossibleMoveException(active_piece, target)

    def pawnMoveCapture(self, active_piece, target, direction):
        test_distance = active_piece.position.add(direction)
        if not target == test_distance:
            return False
        passive_pieces = self.white_pieces if active_piece.color == piece.Piece.BLACK else self.black_pieces
        for passive_piece in passive_pieces:
            if passive_piece.position == target:
                passive_pieces.remove(passive_piece)
                return True
        return False

    def pawnMoveForwardRule(self, active_piece, target, direction):
        if not target.getColumn() == active_piece.position.getColumn():
            return False
        pawn_base_row = self.position('a2') if active_piece.color == piece.Piece.WHITE else self.position('a7')
        if target.sub(direction) == active_piece.position:
            forward_move = self.moveDirection(active_piece, target, direction)
        elif target.sub(direction).sub(direction).getRow() == pawn_base_row.getRow():
            forward_move = self.moveDirection(active_piece, target, direction)
        else:
            forward_move = False
        return forward_move

    def rookRules(self, active_piece, target, direction):
        # rule 1
        prev_target = target.sub(direction)
        directions = [self.position(( 1, 0)), self.position( ( 0, 1)), self.position( (-1, 0)), self.position( (0, -1))]
        if direction in directions:
            move_to_adjacent_of_target = self.moveDirection(active_piece, prev_target, direction)
        else:
            move_to_adjacent_of_target = False
        # rule 2
        attacking_target = self.moveAttacking(active_piece, target)
        if not move_to_adjacent_of_target or not attacking_target:
            raise exceptions.ImpossibleMoveException(active_piece, target)

    def knightRules(self, active_piece, target, direction):
        #rule 1
        start = active_piece.position
        possible_moves = []
        possible_moves.append(start.add(self.position( (1, 2))))
        possible_moves.append(start.add(self.position( (-1, 2))))
        possible_moves.append(start.add(self.position( (-1, -2))))
        possible_moves.append(start.add(self.position( (1, -2))))
        possible_moves.append(start.add(self.position( (2, 1))))
        possible_moves.append(start.add(self.position( (-2, 1))))
        possible_moves.append(start.add(self.position( (-2, -1))))
        possible_moves.append(start.add(self.position( (2, -1))))
        if target in possible_moves:
            attacking_target = self.moveAttacking(active_piece, target)
        else:
            attacking_target = False
        # check rules
        if not attacking_target:
            raise exceptions.ImpossibleMoveException(active_piece, target)

    def bishopRules(self, active_piece, target, direction):
        # rule 1
        prev_target = target.sub(direction)
        directions = [self.position( (1, 1)), self.position( (-1, 1)), self.position( (-1, -1)), self.position( (1, -1))]
        if direction in directions:
            move_to_adjacent_of_target = self.moveDirection(active_piece, prev_target, direction)
        else:
            move_to_adjacent_of_target = False
        # rule 2
        attacking_target = self.moveAttacking(active_piece, target)
        # check rules
        if not move_to_adjacent_of_target or not attacking_target:
            raise exceptions.ImpossibleMoveException(active_piece, target)

    def queenRules(self, active_piece, target, direction):
        # rule 1
        prev_target = target.sub(direction)
        move_to_adjacent_of_target = self.moveDirection(active_piece, prev_target, direction)
        #rule 2
        attacking_target = self.moveAttacking(active_piece, target)
        # check rules
        if not move_to_adjacent_of_target or not attacking_target:
            raise exceptions.ImpossibleMoveException(active_piece, target)

    def kingRules(self, active_piece, target, direction):
        # rule 1
        attacking_target = self.moveAttacking(active_piece, target)
        # check rules
        if not attacking_target:
            raise exceptions.ImpossibleMoveException(active_piece, target)

    def moveAttacking(self, active_piece, target):
        active_pieces = self.white_pieces if active_piece.color == piece.Piece.WHITE else self.black_pieces
        for active_piece in active_pieces:
            if active_piece.position == target:
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

    def __str__(self):
        squares = {str(p.position): p.getName() for p in self.white_pieces + self.black_pieces}
        s = '  A B C D E F G H \n'
        for row in '87654321':
            s += row + ' '
            s += ' '.join(squares.get(column + row, '#') for column in 'abcdefgh')
            s += '\n'
        return s
