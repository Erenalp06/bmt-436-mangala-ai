import pygame
import logging


class Mangala:
    def __init__(self, board=None):
        # Mangala oyun tahtasını başlangıç durumu ile başlat veya belirtilen tahta ile başlat.
        if board is None:
            self.board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]  # Başlangıç durumu
        else:
            self.board = board

        self.right_treasure = 6
        self.left_treasure = 13

    def display_board(self):
        # Mangala oyun tahtasının güncel durumunu ekrana yazdır.
        print("         12    11    10    9     8     7")
        print("+-----+-----+-----+-----+-----+-----+-----+-----+")
        print(
            f"|     |  {self.board[12]}  |  {self.board[11]}  |  {self.board[10]}  |  {self.board[9]}  |  {self.board[8]}  |  {self.board[7]}  |     |")
        print(f"| {self.board[13]}   +-----+-----+-----+-----+-----+-----+   {self.board[6]} |")
        print(
            f"|     |  {self.board[0]}  |  {self.board[1]}  |  {self.board[2]}  |  {self.board[3]}  |  {self.board[4]}  |  {self.board[5]}  |     |")
        print("+-----+-----+-----+-----+-----+-----+-----+-----+")
        print("         0     1     2     3     4     5")

        print()

    def is_game_over(self):
        # Oyunun bitip bitmediğini kontrol et, her iki oyuncunun da tarafının boş olup olmadığını kontrol et.
        return all(count == 0 for count in self.board[:6]) or all(count == 0 for count in self.board[7:13])

    def get_valid_moves(self, player):
        # Belirtilen oyuncu için geçerli hamleleri al.
        if player == 1:
            return [i for i in range(6) if self.board[i] > 0]
        elif player == -1:
            return [i for i in range(7, 13) if self.board[i] > 0]

    def make_move(self, move, player):
        # Belirtilen oyuncu için Mangala oyun tahtasında bir hamle yap.
        stones = self.board[move]
        if stones == 1:
            self.board[move] = 0
            move += 1
            self.board[move] += 1
            return
        self.board[move] = 1
        stones -= 1

        current_index = move

        while stones > 0:
            current_index = (current_index + 1) % 14
            if current_index == 6 and player == -1:
                continue
            elif current_index != 13 or player == 1:
                self.board[current_index] += 1
                stones -= 1
            elif current_index == 13 and player == -1:
                self.board[current_index] += 1
                stones -= 1

        ### 2.KURAL ###
        # Eğer son taş, rakibin kuyusundaki taş sayısını çift yapıyorsa, taşları al ve hazineye koy
        if current_index != 6 and current_index != 13 and stones == 0:
            if player == 1 and 6 < current_index < 13:
                if self.board[current_index] % 2 == 0:
                    self.board[6] += self.board[current_index]
                    self.board[current_index] = 0
            elif player == -1 and 0 <= current_index < 6:
                if self.board[current_index] % 2 == 0:
                    self.board[13] += self.board[current_index]
                    self.board[current_index] = 0

        ### 3.KURAL ###
        # Eğer son taş, boş bir kuyuya atılır ve karşısındaki rakip bölgede taş varsa, hem rakibin taşları hem de atılan taş alınır.
        if current_index != 6 and current_index != 13 and stones == 0 and self.board[current_index] == 1:
            opposite_pit_index = 12 - current_index
            if self.board[opposite_pit_index] > 0:
                self.captures_stones(current_index, opposite_pit_index, player)

    def captures_stones(self, current_index, opposite_pit_index, player):
        # Belirtilen indislerden taşları al ve tahtayı güncelle.
        if player == 1:
            self.board[6] += self.board[current_index] + self.board[opposite_pit_index]
        elif player == -1:
            self.board[13] += self.board[current_index] + self.board[opposite_pit_index]
        self.board[current_index] = 0
        self.board[opposite_pit_index] = 0

    def evaluate_board(self):
        # Mangala oyun tahtasının mevcut durumunu değerlendir.
        return self.board[6] - self.board[13]  # Player 1'in taş sayısı - Player 2'nin taş sayısı


def minimax(board, depth, player, alpha, beta):
    # Minimax algoritmasını uygulayarak bir oyuncu için en iyi hamleyi bul.
    if depth == 0 or board.is_game_over():
        return board.evaluate_board()

    valid_moves = board.get_valid_moves(player)

    if player == 1:  # Maximize
        max_eval = float('-inf')
        for move in valid_moves:
            new_board = Mangala(list(board.board))  # Derin kopya oluştur
            new_board.make_move(move, player)
            eval = minimax(new_board, depth - 1, -player, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval

    else:  # Minimize
        min_eval = float('inf')
        for move in valid_moves:
            new_board = Mangala(list(board.board))  # Derin kopya oluştur
            new_board.make_move(move, player)
            eval = minimax(new_board, depth - 1, -player, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


def find_best_move(board, depth):
    # Belirli bir derinlikte Minimax algoritması kullanarak en iyi hamleyi bul.
    valid_moves = board.get_valid_moves(1)
    best_move = -1
    max_eval = float('-inf')

    for move in valid_moves:
        new_board = Mangala(list(board.board))
        new_board.make_move(move, 1)
        eval = minimax(new_board, depth - 1, -1, float('-inf'), float('inf'))
        if eval > max_eval:
            max_eval = eval
            best_move = move

    return best_move

# Kuyu koordinatlarını bir liste içinde tanımla
kuyu_positions = [
    (165, 325), (260, 325), (355, 325),
    (450, 325), (545, 325), (640, 325),
    (743, 280),
    (640, 225), (545, 225), (450, 225),
    (355, 225), (260, 225), (165, 225),
    (53, 277)

]

kuyu_positions = [kuyu_positions[i] for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]]


def get_clicked_kuyu(mouse_x, mouse_y):
    for i, (kuyu_x, kuyu_y) in enumerate(kuyu_positions):
        if kuyu_x - 45 < mouse_x < kuyu_x + 45 and kuyu_y - 45 < mouse_y < kuyu_y + 45:
            return i
    return None

def draw_player_area(screen, position, n, stone_count):
    font = pygame.font.Font(None, 30)

    # Taş Pozisyonları
    stone_coordinates = [(position[0] + 20 + 25 * i, position[1] - 10 + 25 * j) for i in range(3) for j in range(6)]

    pygame.draw.rect(screen, (80, 0, 0), (position[0], position[1], 90, 90))  # Dikdörtgen çizimi
    pygame.draw.circle(screen, (80, 0, 0), (position[0] + 45, position[1] + 100), 45)  # Alt yuvarlak çizimi
    pygame.draw.circle(screen, (80, 0, 0), (position[0] + 45, position[1]), 45)  # Üst yuvarlak çizimi

    if n > stone_count:
        text = font.render(str(n), True, (255, 255, 255))
        text_rect = text.get_rect(center=(position[0] + 45, position[1] + 70))
        screen.blit(text, text_rect)
    else:
        # Rengi değiştirecek taş sayısı belirleniyor
        change_color_count = min(n, stone_count)

        # Belirlenen taş sayısı kadar rengi değiştiriliyor
        for i in range(change_color_count):
            pygame.draw.circle(screen, (255, 255, 255), stone_coordinates[i], 10)

        # Diğer taşlar aynı renkte çiziliyor
        for i in range(change_color_count, stone_count):
            pygame.draw.circle(screen, (80, 0, 0), stone_coordinates[i], 10)




def draw_board(screen, game_board):
    pygame.draw.rect(screen, (139, 40, 19), (5, 175, 790, 200))

    draw_player_area(screen, (700, 230), game_board.board[6], 18)
    draw_player_area(screen, (10, 230), game_board.board[13], 18)

    for i, (kuyu_position, kuyu_index) in enumerate(zip(reversed(kuyu_positions), reversed(range(13)))):
        if i == 6:
            continue
        draw_kuyu(screen, kuyu_position, game_board.board[kuyu_index], 6)

        font = pygame.font.Font(None, 30)

        # Kuyu indisleri 0'dan 6'ya kadar olanlar için altında, 7'den 12'ye kadar olanlar için üstünde yazdırılıyor.
        if i > 6:
            text = font.render(str(kuyu_index), True, (255, 255, 255))
            text_rect = text.get_rect(center=(kuyu_position[0], kuyu_position[1] + 80))
        else:
            text = font.render(str(kuyu_index), True, (255, 255, 255))
            text_rect = text.get_rect(center=(kuyu_position[0], kuyu_position[1] - 80))

        screen.blit(text, text_rect)



def draw_kuyu(screen, position, n, stone_count):
    font = pygame.font.Font(None, 30)
    pygame.draw.circle(screen, (80, 0, 0), position, 45)

    stone_count_kuyu = 6
    # Adjust the calculations for stone positions
    stone_positions = [(position[0] - 15 + 30 * i, position[1] - 25 + 25 * j) for i in range(2) for j in range(3)]

    if n > stone_count_kuyu:
        text = font.render(str(n), True, (255, 255, 255))
        text_rect = text.get_rect(center=position)
        screen.blit(text, text_rect)
    else:
        change_color_count_kuyu = min(n, stone_count_kuyu)

        for i in range(change_color_count_kuyu):
            pygame.draw.circle(screen, (255, 255, 255), stone_positions[i], 10)

        for i in range(change_color_count_kuyu, stone_count_kuyu):
            pygame.draw.circle(screen, (80, 0, 0), stone_positions[i], 10)
def main():
    pygame.init()

    screen_width = 800
    screen_height = 600

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Mangala Oyunu")

    font = pygame.font.Font(None, 90)

    game_board = Mangala()
    game_over = False
    current_player = -1

    print("Mangala Oyunu")
    print("Başlangıç Durumu:")
    game_board.display_board()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                print("Mouse Pozisyonu: (%d, %d)" % (mouse_x, mouse_y))
                clicked_kuyu = get_clicked_kuyu(mouse_x, mouse_y)
                if clicked_kuyu is not None:
                    if current_player == -1 and 6 < clicked_kuyu < 13:
                        valid_moves = game_board.get_valid_moves(player=-1)
                        if clicked_kuyu in valid_moves:
                            game_board.make_move(clicked_kuyu, player=-1)
                            current_player = 1
                            print("Oyuncu 1'in Hamlesi: %d" % clicked_kuyu)
                            print("Oyun Tahtası:\n%s" % str(game_board.display_board()))
                            if game_board.is_game_over():
                                game_over = True
                                print("Oyun Bitti! Oyuncu 1 Kazandı!")
                            else:
                                print("PC Sırası")
                            # Oyuncu 1'in hamlesi sonrasında bilgisayarın hamlesi yapılıyor
                            player2_move = find_best_move(game_board, depth=5)
                            game_board.make_move(player2_move, player=1)
                            current_player = -1
                            print("Oyuncu 2'nin Hamlesi: %d" % player2_move)
                            print("Oyun Tahtası:\n%s" % str(game_board.display_board()))
                            if game_board.is_game_over():
                                game_over = True
                                print("Oyun Bitti! PC Kazandı!")
                            else:
                                print("Oyuncu 1 Sırası")

        draw_board(screen, game_board)
        pygame.display.update()
        pygame.time.Clock().tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
