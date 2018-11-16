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

    def move_piece(self, pos):
        x = math.floor(pos[0] / 100 % 10)
        y = math.floor(pos[1] / 100 % 10)
        print(x, y, x + y)

        if (x, y) in self.pieces_on_board and self.piece_to_move:
            piece = self.pieces_on_board[self.piece_to_move]
            prey = self.pieces_on_board[(x, y)]
            attack_itself_or_team = self.piece_to_move == (x, y) or piece.color == prey.color
            if not attack_itself_or_team and piece.can_attack(self.piece_to_move, (x, y)):
                # Clear the new square
                self.draw_square((x, y))

                self.draw_piece(piece, (x, y))
                self.pieces_on_board.update({(x, y): piece})

                # Clear the old square
                self.draw_square(self.piece_to_move)
                self.pieces_on_board.pop(self.piece_to_move)

            self.piece_to_move = None

        elif (x, y) in self.pieces_on_board:
            self.piece_to_move = (x, y)
        elif self.piece_to_move:
            piece = self.pieces_on_board[self.piece_to_move]
            if piece.can_move(self.piece_to_move, (x, y)):
                self.draw_piece(piece, (x, y))
                self.pieces_on_board.update({(x, y): piece})
                # Clear the old square
                self.draw_square(self.piece_to_move)
                self.pieces_on_board.pop(self.piece_to_move)

            self.piece_to_move = None

    def draw_square(self, pos):
        if pos[1] % 2:
            color = self.colors['white'] if pos[0] % 2 else self.colors['black']
        else:
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
