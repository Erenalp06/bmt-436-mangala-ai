# a.py

from Mangala import Mangala, find_best_move
import pygame
import sys

class MangalaGUI:
    def __init__(self, mangala):
        pygame.init()  # Pygame başlatılmalı

        self.mangala = mangala
        self.width = 1024
        self.height = 400
        self.board_margin = 20
        self.pit_size = 50
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Mangala Oyunu")

        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()

    def draw_board(self):
        self.screen.fill((255, 255, 255))

        for i in range(14):
            x = self.board_margin + i * (self.pit_size + self.board_margin)
            y = self.height // 2 - self.pit_size // 2

            pygame.draw.rect(self.screen, (0, 0, 0), (x, y, self.pit_size, self.pit_size), 2)

            text = self.font.render(str(self.mangala.board[i]), True, (0, 0, 0))
            text_rect = text.get_rect(center=(x + self.pit_size // 2, y + self.pit_size // 2))
            self.screen.blit(text, text_rect)

        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    clicked_pit = (x - self.board_margin) // (self.pit_size + self.board_margin)
                    if 0 <= clicked_pit < 6 and self.mangala.board[clicked_pit] > 0:
                        self.mangala.make_move(clicked_pit, 1)
                        if self.mangala.is_game_over():
                            print("Oyun bitti! Kazanan: Oyuncu 1")
                            pygame.quit()
                            sys.exit()
                        self.mangala.make_move(find_best_move(self.mangala, depth=3), -1)
                        if self.mangala.is_game_over():
                            print("Oyun bitti! Kazanan: Oyuncu 2")
                            pygame.quit()
                            sys.exit()

            self.draw_board()
            self.clock.tick(30)

if __name__ == "__main__":
    game_board = Mangala()
    mangala_gui = MangalaGUI(game_board)
    mangala_gui.run()
