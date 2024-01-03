import sys
from random import random

import pygame
from pygame.locals import *
import random

pygame.init()
pygame.display.set_icon(pygame.image.load("images/game_icon.png"))

click_sound = pygame.mixer.Sound("images/click.wav")
click_sound.set_volume(0.2)
capture_sound = pygame.mixer.Sound("images/capture.wav")
capture_sound.set_volume(0.2)
win_sound = pygame.mixer.Sound("images/win.wav")
win_sound.set_volume(0.2)

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
brown = (139, 69, 19)

hole_radius = 50
hole_margin = 10
hole_number = 6
stone_number = 4
stone_radius = 10
treasure_width = 100
treasure_height = 200
treasure_margin = 50
font_size = 32
animation_speed = 0.1
difficulty = "kolay"

depth = 3



mangala_board_color = (139, 40, 19)
clock = pygame.time.Clock()


class MangalaV2:
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

        # ## 2.KURAL ###
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

        # ## 3.KURAL ### Eğer son taş, boş bir kuyuya atılır ve karşısındaki rakip bölgede taş varsa, hem rakibin
        # taşları hem de atılan taş alınır.
        if current_index != 6 and current_index != 13 and stones == 0 and self.board[current_index] == 1:
            opposite_pit_index = 12 - current_index
            if self.board[opposite_pit_index] > 0:
                self.captures_stones(current_index, opposite_pit_index, player)

        click_sound.play()

    def captures_stones(self, current_index, opposite_pit_index, player):
        # Belirtilen indislerden taşları al ve tahtayı güncelle.
        if player == 1:
            self.board[6] += self.board[current_index] + self.board[opposite_pit_index]
        elif player == -1:
            self.board[13] += self.board[current_index] + self.board[opposite_pit_index]
        self.board[current_index] = 0
        self.board[opposite_pit_index] = 0

        capture_sound.play()

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
            new_board = MangalaV2(list(board.board))  # Derin kopya oluştur
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
            new_board = MangalaV2(list(board.board))  # Derin kopya oluştur
            new_board.make_move(move, player)
            eval = minimax(new_board, depth - 1, -player, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


def find_best_move(board, depth):
    # Minimax algoritması kullanarak en iyi hamleyi bul.
    valid_moves = board.get_valid_moves(1)
    best_move = -1
    max_eval = float('-inf')

    if difficulty == "zor":
        current_depth = dynamic_depth(board)
    else:
        current_depth = depth  # Diğer zorluk seviyeleri için sabit derinlik

    for move in valid_moves:
        new_board = MangalaV2(list(board.board))
        new_board.make_move(move, 1)
        eval = minimax(new_board, current_depth, -1, float('-inf'), float('inf'))

        if eval > max_eval:
            max_eval = eval
            best_move = move

    return best_move

def dynamic_depth(board):
    # Oyun durumuna göre dinamik derinliği belirle
    player_stones = sum(board.board[:6])
    computer_stones = sum(board.board[7:13])

    if player_stones < computer_stones:
        return 6  # Eğer oyuncunun taşları azsa derinliği artır
    elif player_stones == computer_stones:
        return 5
    else:
        return 4  # Eğer bilgisayarın taşları azsa derinliği azalt



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

    player_area_rect = pygame.Rect(position[0], position[1], 90, 90)

    if player_area_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, (255, 0, 0),
                         (position[0], position[1], 90, 90))  # Change color or add outline for hover effect
    else:
        pygame.draw.rect(screen, (80, 0, 0), (position[0], position[1], 90, 90))

    # Taş Pozisyonları
    stone_coordinates = [(position[0] + 20 + 25 * i, position[1] - 10 + 25 * j) for i in range(3) for j in range(6)]

    pygame.draw.rect(screen, (80, 0, 0), (position[0], position[1], 90, 90))  # Dikdörtgen çizimi
    pygame.draw.circle(screen, (80, 0, 0), (position[0] + 45, position[1] + 95), 45)  # Alt yuvarlak çizimi
    pygame.draw.circle(screen, (80, 0, 0), (position[0] + 45, position[1] - 5), 45)  # Üst yuvarlak çizimi

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
    pygame.draw.rect(screen, mangala_board_color, (5, 175, 790, 200))

    draw_player_area(screen, (700, 230), game_board.board[6], 18)
    draw_player_area(screen, (10, 230), game_board.board[13], 18)

    for i, (kuyu_position, kuyu_index) in enumerate(zip(reversed(kuyu_positions), reversed(range(13)))):
        if i == 6:
            continue
        draw_kuyu(screen, kuyu_position, game_board.board[kuyu_index], 6)

        font = pygame.font.Font(None, 30)

        # Kuyu indisleri 0'dan 6'ya kadar olanlar için altında, 7'den 12'ye kadar olanlar için üstünde yazdırılıyor.
        if i > 6:
            text = font.render(str(kuyu_index), True, (0, 0, 0))
            text_rect = text.get_rect(center=(kuyu_position[0], kuyu_position[1] + 80))
        else:
            text = font.render(str(kuyu_index), True, (0, 0, 0))
            text_rect = text.get_rect(center=(kuyu_position[0], kuyu_position[1] - 80))

        screen.blit(text, text_rect)


def draw_kuyu(screen, position, n, stone_count):
    font = pygame.font.Font(None, 30)
    pygame.draw.circle(screen, (80, 0, 0), position, 45)

    kuyu_rect = pygame.Rect(position[0] - 45, position[1] - 45, 90, 90)


    if kuyu_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.circle(screen, (255, 0, 0), position, 45)  # Change color or add outline for hover effect
    else:
        pygame.draw.circle(screen, (80, 0, 0), position, 45)

    stone_count_kuyu = 6

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

def display_transparent_text(text, font_size, position, screen):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(midbottom=position)
    text_surface.set_alpha(128)  # Set alpha value for transparency (0: fully transparent, 255: fully opaque)
    screen.blit(text_surface, text_rect)

def start_screen(screen):
    # Arka plan resmi
    background = pygame.image.load("images/background.jpg")
    screen.blit(background, (0, 0))

    # Başlık fontu
    title_font = pygame.font.Font(None, 120)
    title_text = title_font.render("MANGALA", True, black)
    title_rect = title_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))

    # Başla butonu fontu (daha büyük)
    button_font = pygame.font.Font(None, 80)
    button_text = button_font.render("Başla", True, white)

    # Ayarlanabilir buton boyutları
    button_width = 200
    button_height = 80

    button_rect = pygame.Rect((screen.get_width() - button_width) // 2, (screen.get_height() - button_height) // 2 + 80, button_width, button_height)

    # Hesaplanan konum için text'in merkezi
    text_rect = button_text.get_rect(center=button_rect.center)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if button_rect.collidepoint(mouse_x, mouse_y):
                    return

        # Başlık ve butonu ekrana çiz
        screen.blit(title_text, title_rect)
        pygame.draw.rect(screen, mangala_board_color, button_rect, border_radius=10)
        screen.blit(button_text, text_rect)

        pygame.display.flip()


def select_difficulty(screen):
    global difficulty
    difficulty_selected = False
    while not difficulty_selected:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 200 <= mouse_x <= 600:
                    if 200 <= mouse_y <= 300:
                        global depth
                        depth = 3
                        difficulty = "kolay"
                        difficulty_selected = True
                    elif 320 <= mouse_y <= 420:
                        depth = 4
                        difficulty = "orta"
                        difficulty_selected = True
                    elif 440 <= mouse_y <= 540:
                        depth = 5
                        difficulty = "zor"
                        difficulty_selected = True

        draw_difficulty_screen(screen)
        pygame.display.flip()
        pygame.time.delay(50)


def draw_difficulty_screen(screen):
    background = pygame.image.load("images/background.jpg")
    screen.fill(black)
    screen.blit(background, (0, 0))

    font_large = pygame.font.Font(None, 55)  # Font boyutunu 60 olarak değiştirildi
    font = pygame.font.Font(None, 60)

    # Renkler
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)

    # Metin renkleri
    text_color = black

    text_prompt = font_large.render("LÜTFEN BİR ZORLUK SEVİYESİ SEÇİNİZ", True, text_color)
    text_easy = font.render("KOLAY", True, text_color)
    text_medium = font.render("ORTA", True, text_color)
    text_hard = font.render("ZOR", True, text_color)

    # Dikdörtgen renkleri
    rect_color_easy = red
    rect_color_medium = green
    rect_color_hard = blue

    rect_prompt = pygame.Rect(50, 50, 900, 100)
    rect_easy = pygame.Rect(200, 200, 400, 100)
    rect_medium = pygame.Rect(200, 320, 400, 100)
    rect_hard = pygame.Rect(200, 440, 400, 100)

    border_radius = 20

    pygame.draw.rect(screen, (163, 255, 20), rect_easy, border_radius=border_radius)
    pygame.draw.rect(screen, (241, 195, 15), rect_medium, border_radius=border_radius)
    pygame.draw.rect(screen, (247, 121, 22), rect_hard, border_radius=border_radius)

    # İcon eklemeleri
    icon_size = (80, 80)
    icon_easy = pygame.image.load("images/icon_easy.png")
    icon_medium = pygame.image.load("images/icon_medium.png")
    icon_hard = pygame.image.load("images/icon_hard.png")

    icon_easy = pygame.transform.scale(icon_easy, icon_size)
    icon_medium = pygame.transform.scale(icon_medium, icon_size)
    icon_hard = pygame.transform.scale(icon_hard, icon_size)

    # Metinleri ve ikonları aynı düzen içinde hizala
    text_offset = 20  # İkon ve metin arasındaki boşluk
    icon_offset = 10  # İkon ile düğme arasındaki boşluk

    # Prompt metni
    screen.blit(text_prompt, (rect_prompt.centerx - text_prompt.get_width() // 1.6, rect_prompt.centery))

    # KOLAY düğmesi
    screen.blit(text_easy, (rect_easy.x + (rect_easy.width - text_easy.get_width() - icon_size[0] - text_offset - icon_offset) // 2,
                            rect_easy.centery - text_easy.get_height() // 2))
    screen.blit(icon_easy, (rect_easy.x + (rect_easy.width - icon_size[0] - icon_offset), rect_easy.centery - icon_size[1] // 2))

    # ORTA düğmesi
    screen.blit(text_medium, (rect_medium.x + (rect_medium.width - text_medium.get_width() - icon_size[0] - text_offset - icon_offset) // 2,
                              rect_medium.centery - text_medium.get_height() // 2))
    screen.blit(icon_medium, (rect_medium.x + (rect_medium.width - icon_size[0] - icon_offset), rect_medium.centery - icon_size[1] // 2))

    # ZOR düğmesi
    screen.blit(text_hard, (rect_hard.x + (rect_hard.width - text_hard.get_width() - icon_size[0] - text_offset - icon_offset) // 2,
                            rect_hard.centery - text_hard.get_height() // 2))
    screen.blit(icon_hard, (rect_hard.x + (rect_hard.width - icon_size[0] - icon_offset), rect_hard.centery - icon_size[1] // 2))

    pygame.display.flip()



def main():

    timer_duration = 5000  # 20 seconds in milliseconds
    current_timer = timer_duration
    timer_running = False


    timer_font = pygame.font.Font(None, 36)
    timer_text_color = (0, 0, 0)

    screen_width = 800
    screen_height = 600

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Mangala Oyunu")
    background = pygame.image.load("images/background.jpg")
    pygame.mixer.music.load("images/music.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)

    start_screen(screen)

    select_difficulty(screen)

    font = pygame.font.Font(None, 90)

    game_board = MangalaV2()
    game_over = False
    current_player = -1

    print("Mangala Oyunu")
    print("Başlangıç Durumu:")
    game_board.display_board()

    dragging = False
    drag_start_x = 0
    volume = 0.2
    muted = False
    sound_on_icon = pygame.image.load("images/sound_on.png")
    sound_off_icon = pygame.image.load("images/sound_off.png")

    icon_size = (35, 35)

    sound_on_icon = pygame.transform.scale(sound_on_icon, icon_size)
    sound_off_icon = pygame.transform.scale(sound_off_icon, icon_size)

    timer_running = True
    current_timer = timer_duration

    clock = pygame.time.Clock()
    while not game_over:
        elapsed_time = clock.tick(60)
        screen.fill(black)
        screen.blit(background, (0, 0))

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
                                win_sound.play()
                            else:
                                print("PC Sırası")
                            # Oyuncu 1'in hamlesi sonrasında bilgisayarın hamlesi yapılıyor

                            player2_move = find_best_move(game_board, depth)
                            game_board.make_move(player2_move, player=1)

                            current_player = -1
                            print("Oyuncu 2'nin Hamlesi: %d" % player2_move)
                            print("Oyun Tahtası:\n%s" % str(game_board.display_board()))
                            if game_board.is_game_over():
                                game_over = True
                                if game_board.board[6] > game_board.board[13]:
                                    print("Oyun Bitti! PC Kazandı!")
                                    win_sound.play()
                                elif game_board.board[6] < game_board.board[13]:
                                    print("Oyun Bitti! Oyuncu Kazandı!")
                                    win_sound.play()
                                win_sound.play()
                            else:
                                print("Oyuncu 1 Sırası")
                            current_timer = timer_duration
                if 50 <= mouse_x <= 250 and 550 <= mouse_y <= 570:
                    dragging = True  # Slider'ı tutma başladı
                    drag_start_x = mouse_x
                    volume = pygame.mixer.music.get_volume()
                elif 8 <= mouse_x <= 40 and 540 <= mouse_y <= 570:
                    muted = not muted
                    if muted:
                        pygame.mixer.music.set_volume(0.0)
                    else:
                        pygame.mixer.music.set_volume(volume)
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    volume = min(1.0, volume + 0.1)
                    pygame.mixer.music.set_volume(volume)
                elif event.key == K_DOWN:
                    volume = max(0.0, volume - 0.1)
                    pygame.mixer.music.set_volume(volume)
            elif event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                if dragging:

                    volume = max(0.0, min(1.0, (mouse_x - 50) / 200.0))
                    pygame.mixer.music.set_volume(volume)
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False

        # Zamanlayıcıyı güncelle
        if timer_running:
            elapsed_time = pygame.time.Clock().tick(60)
            current_timer -= elapsed_time
            if current_timer <= 0:

                if current_player == -1:
                    player_moves = game_board.get_valid_moves(current_player)
                    if player_moves:
                        random_move = random.choice(player_moves)
                        game_board.make_move(random_move, current_player)
                        print("Oyuncu 1'in Hamlesi: %d" % random_move)
                        print("Oyun Tahtası:\n%s" % str(game_board.display_board()))
                    # Sırayı bir sonraki oyuncuya geçir
                    current_player = 1
                else:
                    # Sıra oyuncu 2'nin (PC) hamlesi
                    current_player = -1
                    player2_move = find_best_move(game_board, depth)

                    game_board.make_move(player2_move, player=1)

                    print("Oyuncu 2'nin Hamlesi: %d" % player2_move)
                    print("Oyun Tahtası:\n%s" % str(game_board.display_board()))

                    if game_board.is_game_over():
                        game_over = True
                        print("Oyun Bitti! PC Kazandı!")
                        win_sound.play()
                    else:
                        print("Oyuncu 1 Sırası")
                    # Zamanlayıcıyı mevcut oyuncu için sıfırla
                    current_timer = timer_duration

        pygame.time.delay(0)  # Zamanlayıcı hızını kontrol etmek için küçük bir gecikme ekle


        timer_text = timer_font.render(f"Time left: {current_timer // 1000} seconds", True, timer_text_color)
        timer_text_rect = timer_text.get_rect(center=(screen_width // 2, 30))
        screen.blit(timer_text, timer_text_rect)


        pygame.draw.rect(screen, (255, 255, 255), (50, 540, 200, 20), border_radius=10)
        pygame.draw.rect(screen, mangala_board_color, (50, 540, int(volume * 200), 20), border_radius=10)


        if muted:
            screen.blit(sound_off_icon, (50 - sound_off_icon.get_width() - 10, 532))
        else:
            screen.blit(sound_on_icon, (50 - sound_on_icon.get_width() - 10, 532))


        draw_board(screen, game_board)

        display_transparent_text("MANGALA", 100, (screen_width // 2, screen_height - 100), screen)

        pygame.display.flip()
        pygame.time.Clock().tick(60)


    pygame.quit()


if __name__ == "__main__":
    main()
