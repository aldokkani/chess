import sys


class BlockedPathInterface(object):
    @staticmethod
    def is_blocked(current_pos, new_pos, board):
        diffx, diffy = current_pos[0] - new_pos[0], current_pos[1] - new_pos[1]
        rangex, rangey = None, None

        if diffx:
            stepx = int(diffx / abs(diffx))
            rangex = range(new_pos[0] + stepx, current_pos[0], stepx)

        if diffy:
            stepy = int(diffy / abs(diffy))
            rangey = range(new_pos[1] + stepy, current_pos[1], stepy)

        if rangex is None or rangey is None:
            if rangex is not None:
                rangey = [current_pos[1]] * len(rangex)
            elif rangey is not None:
                rangex = [current_pos[0]] * len(rangey)

        for pos in zip(rangex, rangey):
            if pos in board:
                return True
        return False


class Piece(object):
    def __init__(self, name, color):
        self.name = name
        self.color = color
        theme1, theme2 = 'cheq', 'merida'
        self.image = f'images/{theme1}/{color}{name}.png'


class Pawn(Piece, BlockedPathInterface):
    moved = False

    def can_move(self, current_pos, new_pos, board):
        if self.is_blocked(current_pos, new_pos, board):
            return False
        good_white = current_pos[0] == new_pos[0] and self.color == 'White'
        good_black = current_pos[0] == new_pos[0] and self.color == 'Black'

        truthy = list([good_white and current_pos[1] == new_pos[1] + 1])
        truthy.append(good_white and not self.moved and current_pos[1] == new_pos[1] + 2)
        truthy.append(good_black and current_pos[1] + 1 == new_pos[1])
        truthy.append(good_black and not self.moved and current_pos[1] + 2 == new_pos[1])

        if any(truthy):
            self.moved = True
            return True
        return False

    def can_attack(self, current_pos, prey_pos, _board):
        diagonal_move = abs(current_pos[0] - prey_pos[0]) == abs(current_pos[1] - prey_pos[1]) == 1
        if self.color == 'White':
            return diagonal_move and current_pos[1] > prey_pos[1]
        return diagonal_move and current_pos[1] < prey_pos[1]


class Knight(Piece):
    @staticmethod
    def can_move(current_pos, new_pos, _board):
        abs_x = abs(current_pos[0] - new_pos[0])
        abs_y = abs(current_pos[1] - new_pos[1])
        return abs_x == 1 and abs_y == 2 or abs_x == 2 and abs_y == 1

    def can_attack(self, current_pos, prey_pos, board):
        return self.can_move(current_pos, prey_pos, board)


class Bishop(Piece, BlockedPathInterface):
    def can_move(self, current_pos, new_pos, board):
        if self.is_blocked(current_pos, new_pos, board):
            return False

        return abs(current_pos[0] - new_pos[0]) == abs(current_pos[1] - new_pos[1])

    def can_attack(self, current_pos, prey_pos, board):
        return self.can_move(current_pos, prey_pos, board)


class Rook(Piece, BlockedPathInterface):
    def can_move(self, current_pos, new_pos, board):
        if self.is_blocked(current_pos, new_pos, board):
            return False

        return current_pos[0] == new_pos[0] or current_pos[1] == new_pos[1]

    def can_attack(self, current_pos, prey_pos, board):
        return self.can_move(current_pos, prey_pos, board)


class Queen(Piece, BlockedPathInterface):
    def can_move(self, current_pos, new_pos, board):

        if self.is_blocked(current_pos, new_pos, board):
            return False

        truthy = list([current_pos[0] == new_pos[0]])
        truthy.append(current_pos[1] == new_pos[1])
        truthy.append(abs(current_pos[0] - new_pos[0]) == abs(current_pos[1] - new_pos[1]))
        return any(truthy)

    def can_attack(self, current_pos, prey_pos, board):
        return self.can_move(current_pos, prey_pos, board)


class King(Piece):
    @staticmethod
    def can_move(current_pos, new_pos, _board):
        return abs(current_pos[0] - new_pos[0]) in [0, 1] and abs(current_pos[1] - new_pos[1]) in [0, 1]

    def can_attack(self, current_pos, prey_pos, board):
        return self.can_move(current_pos, prey_pos, board)


class PieceFactory(object):
    @staticmethod
    def get_piece(type_, color):
        return getattr(sys.modules[__name__], type_)(type_, color)
