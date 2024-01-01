from textwrap import indent


class Mangala:
    def __init__(self, board=None):
        if board is None:
            self.board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]  # Başlangıç durumu
        else:
            self.board = board

    def display_board(self):

        print("         12    11    10    9     8     7")
        print("+-----+-----+-----+-----+-----+-----+-----+-----+")
        print(f"|     |  {self.board[12]}  |  {self.board[11]}  |  {self.board[10]}  |  {self.board[9]}  |  {self.board[8]}  |  {self.board[7]}  |     |")
        print(f"| {self.board[13]}   +-----+-----+-----+-----+-----+-----+   {self.board[6]} |")
        print(f"|     |  {self.board[0]}  |  {self.board[1]}  |  {self.board[2]}  |  {self.board[3]}  |  {self.board[4]}  |  {self.board[5]}  |     |")
        print("+-----+-----+-----+-----+-----+-----+-----+-----+")
        print("         0     1     2     3     4     5")


        print()

    def is_game_over(self):
        return all(count == 0 for count in self.board[:6]) or all(count == 0 for count in self.board[7:13])

    def get_valid_moves(self, player):
        if player == 1:
            return [i for i in range(6) if self.board[i] > 0]
        elif player == -1:
            return [i for i in range(7, 13) if self.board[i] > 0]

    def make_move(self, move, player):
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
        if player == 1:
            self.board[6] += self.board[current_index] + self.board[opposite_pit_index]
        elif player == -1:
            self.board[13] += self.board[current_index] + self.board[opposite_pit_index]
        self.board[current_index] = 0
        self.board[opposite_pit_index] = 0

    def evaluate_board(self):
        return self.board[6] - self.board[13]  # Player 1'in taş sayısı - Player 2'nin taş sayısı

def print_minimax_steps(board, depth, player, alpha, beta, move):
    indent = ' ' * (5 - depth)  # Derinlik kadar boşluk ekleyerek görselleştirme yapar
    print(f"{indent}Depth {depth}, Player {player}, Move {move}")
    print(f"{indent}Alpha: {alpha}, Beta: {beta}")
    board.display_board()
    print()


def minimax(board, depth, player, alpha, beta):
    if depth == 0 or board.is_game_over():
        eval_value = board.evaluate_board()
        print_minimax_steps(board, depth, player, alpha, beta, None)
        print(f"{indent}Evaluated: {eval_value}")
        return eval_value

    valid_moves = board.get_valid_moves(player)

    if player == 1:  # Maximize
        max_eval = float('-inf')
        for move in valid_moves:
            new_board = Mangala(list(board.board))
            new_board.make_move(move, player)
            eval = minimax(new_board, depth - 1, -player, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
            print_minimax_steps(board, depth, player, alpha, beta, move)
        return max_eval

    else:  # Minimize
        min_eval = float('inf')
        for move in valid_moves:
            new_board = Mangala(list(board.board))
            new_board.make_move(move, player)
            eval = minimax(new_board, depth - 1, -player, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
            print_minimax_steps(board, depth, player, alpha, beta, move)
        return min_eval


def find_best_move(board, depth):
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


def main():
    # Oyunun başlangıcı
    game_board = Mangala()
    game_over = False

    print("Mangala Oyunu")
    print("Başlangıç Durumu:")
    game_board.display_board()

    start_game = input("Oyunu başlatmak için 'b' tuşuna basın: ")
    if start_game.lower() != 'b':
        print("Geçersiz giriş. Oyun başlatılamadı.")
        return

    while not game_over:
        # Oyuncu 1'in hamlesi
        try:
            player1_move = int(input("Oyuncu 1, taş seçin (7-12): "))
        except ValueError:
            print("Geçersiz giriş. Lütfen bir tam sayı girin.")
            continue
        game_board.make_move(player1_move, -1)
        print(f"Oyuncu 1 hamlesi: {player1_move}")
        game_board.display_board()

        if game_board.is_game_over():
            print("Oyun bitti! Kazanan: Oyuncu 1")
            break

        # Oyuncu 2'nin hamlesi
        player2_move = find_best_move(game_board, depth=2)
        game_board.make_move(player2_move, 1)
        print(f"Oyuncu 2 hamlesi: {player2_move}")
        game_board.display_board()

        if game_board.is_game_over():
            print("Oyun bitti! Kazanan: Oyuncu 2")
            break

if __name__ == "__main__":
    main()
