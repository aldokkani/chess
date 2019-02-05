import pygame
import math
from pieces import *


class Chess(object):
    colors = {
        "black": (100, 100, 100),
        "white": (255, 255, 255),
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255)
    }
    pieces_on_board = {}
    piece_to_move = None
    kings_pos = {
        "White": (4, 7),
        "Black": (4, 0)
    }
    king_in_check = None

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption('PyChess')
        self.screen.fill((224, 224, 224))

        self.board = pygame.Surface((800, 800)).convert()
        self.draw_board()

        self.init_setup()

        self.screen.blit(self.board, (0, 0))
        pygame.display.flip()

    def draw_board(self):
        x, y = 0, 0
        for i in range(8 * 8):
            self.draw_square((x, y))
            x += 1
            if (i + 1) % 8 == 0:
                y += 1
                x = 0

    def run(self):
        # Event loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.move_piece(event.pos)

            self.screen.blit(self.board, (0, 0))
            pygame.display.flip()

    def highlight_square(self, pos, color):
        self.draw_square(pos, color)
        self.draw_piece(self.pieces_on_board[pos], pos)

    def update_kings_pos(self, king_color, pos):
        self.kings_pos[king_color] = pos
        self.king_in_check = None

    def king_is_safe(self, piece, pos):
        if self.king_in_check == self.piece_to_move:
            return True
        self.pieces_on_board.update({pos: piece})
        for position, p in self.pieces_on_board.items():
            if p.color != piece.color:
                if p.can_attack(position, self.king_in_check, self.pieces_on_board):
                    self.pieces_on_board.pop(pos)
                    return False

        self.highlight_square(self.king_in_check, color=None)
        self.king_in_check = None
        return True

    def put_king_in_check(self, king_pos):
        self.highlight_square(king_pos, color=self.colors['red'])
        self.king_in_check = king_pos

    def make_a_move(self, piece, pos):
        if self.king_in_check is not None and not self.king_is_safe(piece, pos):
            self.highlight_square(self.piece_to_move, color=None)
            return

        # Update king's pos
        if piece.name == 'King':
            self.update_kings_pos(piece.color, pos)
        # Check if king is in check
        opposite_king_pos = self.kings_pos['Black' if piece.color == 'White' else 'White']
        if piece.can_attack(pos, opposite_king_pos, self.pieces_on_board):
            self.put_king_in_check(opposite_king_pos)

        # Clear the new square and update it with the move
        self.draw_square(pos)
        self.draw_piece(piece, pos)
        self.pieces_on_board.update({pos: piece})

        # Clear the old square
        self.draw_square(self.piece_to_move)
        self.pieces_on_board.pop(self.piece_to_move)

    def move_piece(self, pos):
        x = math.floor(pos[0] / 100 % 10)
        y = math.floor(pos[1] / 100 % 10)
        print(x, y, x + y)

        if (x, y) in self.pieces_on_board:
            if self.piece_to_move:
                piece = self.pieces_on_board[self.piece_to_move]
                prey = self.pieces_on_board[(x, y)]
                attack_itself_or_team = self.piece_to_move == (x, y) or piece.color == prey.color
                if not attack_itself_or_team and piece.can_attack(self.piece_to_move, (x, y), self.pieces_on_board):
                    self.make_a_move(piece, (x, y))
                else:
                    self.highlight_square(self.piece_to_move, color=None)
                self.piece_to_move = None
            else:
                self.highlight_square((x, y), color=self.colors['green'])
                self.piece_to_move = (x, y)

        elif self.piece_to_move:
            piece = self.pieces_on_board[self.piece_to_move]
            if piece.can_move(self.piece_to_move, (x, y), self.pieces_on_board):
                self.make_a_move(piece, (x, y))

            else:
                self.highlight_square(self.piece_to_move, color=None)
            self.piece_to_move = None

    def draw_square(self, pos, color=None):
        if pos[1] % 2 and not color:
            color = self.colors['white'] if pos[0] % 2 else self.colors['black']
        elif not color:
            color = self.colors['black'] if pos[0] % 2 else self.colors['white']

        cell = pygame.Surface((100, 100))

        cellpos = cell.get_rect()
        cellpos.x = pos[0] * 100
        cellpos.y = pos[1] * 100

        cell.fill(color)
        cell = cell.convert()
        self.board.blit(cell, cellpos)

    def draw_piece(self, piece, pos):
        image = pygame.image.load(piece.image).convert_alpha()
        imagepos = image.get_rect()
        imagepos.centerx = pos[0] * 100 + 50
        imagepos.centery = pos[1] * 100 + 50
        self.board.blit(image, imagepos)

    def init_setup(self):
        pieces = ['Rook', 'Knight', 'Bishop', 'Queen', 'King', 'Bishop', 'Knight', 'Rook']

        for i, p in enumerate(pieces):
            black_piece = PieceFactory.get_piece(p, 'Black')
            black_pawn = PieceFactory.get_piece('Pawn', 'Black')
            white_piece = PieceFactory.get_piece(p, 'White')
            white_pawn = PieceFactory.get_piece('Pawn', 'White')

            self.draw_piece(black_piece, (i, 0))
            self.draw_piece(black_pawn, (i, 1))
            self.draw_piece(white_pawn, (i, 6))
            self.draw_piece(white_piece, (i, 7))

            self.pieces_on_board.update({(i, 0): black_piece})
            self.pieces_on_board.update({(i, 1): black_pawn})
            self.pieces_on_board.update({(i, 6): white_pawn})
            self.pieces_on_board.update({(i, 7): white_piece})


if __name__ == '__main__':
    Chess().run()
