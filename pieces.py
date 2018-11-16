import sys


class Piece(object):
    def __init__(self, type_, color):
        self.type = type_
        # If color == True then it's a white piece else it's a black piece.
        self.color = (0, 255, 0) if color else (0, 0, 255)


class Pawn(Piece):
    moved = False

    def can_move(self, current_pos, new_pos):
        good_white = current_pos[0] == new_pos[0] and self.color == (0, 255, 0)
        good_black = current_pos[0] == new_pos[0] and self.color == (0, 0, 255)

        truthy = list([good_white and current_pos[1] == new_pos[1] + 1])
        truthy.append(good_white and not self.moved and current_pos[1] == new_pos[1] + 2)
        truthy.append(good_black and current_pos[1] + 1 == new_pos[1])
        truthy.append(good_black and not self.moved and current_pos[1] + 2 == new_pos[1])

        if any(truthy):
            self.moved = True
            return True
        return False

    def can_attack(self, current_pos, prey_pos):
        diagonal_move = abs(current_pos[0] - prey_pos[0]) == abs(current_pos[1] - prey_pos[1]) == 1
        if self.color == (0, 255, 0):
            return diagonal_move and current_pos[1] > prey_pos[1]
        return diagonal_move and current_pos[1] < prey_pos[1]


class Knight(Piece):
    @staticmethod
    def can_move(current_pos, new_pos):
        abs_x = abs(current_pos[0] - new_pos[0])
        abs_y = abs(current_pos[1] - new_pos[1])
        return abs_x == 1 and abs_y == 2 or abs_x == 2 and abs_y == 1

    def can_attack(self, current_pos, prey_pos):
        return self.can_move(current_pos, prey_pos)


class Bishop(Piece):
    @staticmethod
    def can_move(current_pos, new_pos):
        return abs(current_pos[0] - new_pos[0]) == abs(current_pos[1] - new_pos[1])

    def can_attack(self, current_pos, prey_pos):
        return self.can_move(current_pos, prey_pos)


class Rock(Piece):
    @staticmethod
    def can_move(current_pos, new_pos):
        return current_pos[0] == new_pos[0] or current_pos[1] == new_pos[1]

    def can_attack(self, current_pos, prey_pos):
        return self.can_move(current_pos, prey_pos)


class Queen(Piece):
    @staticmethod
    def can_move(current_pos, new_pos):
        truthy = list([current_pos[0] == new_pos[0]])
        truthy.append(current_pos[1] == new_pos[1])
        truthy.append(abs(current_pos[0] - new_pos[0]) == abs(current_pos[1] - new_pos[1]))
        return any(truthy)

    def can_attack(self, current_pos, prey_pos):
        return self.can_move(current_pos, prey_pos)


class King(Piece):
    @staticmethod
    def can_move(current_pos, new_pos):
        return abs(current_pos[0] - new_pos[0]) in [0, 1] and abs(current_pos[1] - new_pos[1]) in [0, 1]

    def can_attack(self, current_pos, prey_pos):
        return self.can_move(current_pos, prey_pos)


class PieceFactory(object):
    @staticmethod
    def get_piece(type_, color):
        return getattr(sys.modules[__name__], type_)(type_, color)
