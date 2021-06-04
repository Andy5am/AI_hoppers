import sys
import time
import math

from board import Board, Tile


class Hoppers():

    def __init__(self, b_size=8, t_limit=60, c_player=Tile.P_RED):

        # Se crea el tablero
        board = [[None] * b_size for _ in range(b_size)]
        for row in range(b_size):
            for col in range(b_size):

                if row + col < 4:
                    element = Tile(2, 2, 0, row, col)
                elif row + col > 2 * (b_size - 3):
                    element = Tile(1, 1, 0, row, col)
                else:
                    element = Tile(0, 0, 0, row, col)

                board[row][col] = element

        # Variables
        self.b_size = b_size
        self.t_limit = t_limit
        self.c_player = c_player
        self.board_view = Board(board)
        self.board = board
        self.current_player = Tile.P_BLACK
        self.selected_tile = None
        self.valid_moves = []
        self.computing = False
        self.total_plies = 0

        self.ply_depth = 3
        self.ab_enabled = True

        self.r_goals = [t for row in board
                        for t in row if t.tile == Tile.T_RED]
        self.g_goals = [t for row in board
                        for t in row if t.tile == Tile.T_BLACK]

        self.board_view.set_status_color("#E50000" if
            self.current_player == Tile.P_RED else "#000000")

        if self.c_player == self.current_player:
            self.AI_Move()

        self.board_view.add_click_handler(self.tile_clicked)
        self.board_view.draw_tiles(board=self.board)  # Se recarga el tablero

        self.board_view.mainloop()  # Tkinter loop

    def tile_clicked(self, row, col):

        if self.computing: 
            return

        new_tile = self.board[row][col]

        # Si se selecciona una piza
        if new_tile.piece == self.current_player:

            self.outline_tiles(None)  #Se reinicia el outline

            # Se resaltan los espacios en los que puede jugar
            new_tile.outline = Tile.O_MOVED
            self.valid_moves = self.get_moves(new_tile,
                self.current_player)
            self.outline_tiles(self.valid_moves)

            # Se actualiza el tablero
            self.board_view.set_status("Pieza `" + str(new_tile) + "` seleccionada")
            self.selected_tile = new_tile

            self.board_view.draw_tiles(board=self.board)  # Se refresa el tablero

        # Si ya seleccionamos una pieza y va a mover
        elif self.selected_tile and new_tile in self.valid_moves:

            self.outline_tiles(None)  # reinicia outline
            self.move_piece(self.selected_tile, new_tile)  # Se mueve la pieza

            # Se actualiza el estado
            self.selected_tile = None
            self.valid_moves = []
            self.current_player = (Tile.P_RED
                if self.current_player == Tile.P_BLACK else Tile.P_BLACK)

            self.board_view.draw_tiles(board=self.board)  # Se refresca el tablero

            #Si hay un ganador
            winner = self.verify_winner()
            if winner:
                self.board_view.set_status("Gano el " + ("negro"
                    if winner == Tile.P_BLACK else "rojo"))
                self.current_player = None

            elif self.c_player is not None:
                self.AI_Move()

        else:
            self.board_view.set_status("Movimiento invalido")

    def minimax(self, depth, player_to_max, max_time, a=float("-inf"),
                b=float("inf"), maxing=True, prunes=0, boards=0):

        if depth == 0 or self.verify_winner() or time.time() > max_time:
            return self.utility_distance(player_to_max), None, prunes, boards

        # Se buscan los movimientos
        best_move = None
        if maxing:
            best_val = float("-inf")
            moves = self.get_possible_moves(player_to_max)
        else:
            best_val = float("inf")
            moves = self.get_possible_moves((Tile.P_RED
                    if player_to_max == Tile.P_BLACK else Tile.P_BLACK))

        for move in moves:
            for to in move["to"]:

                # Por si no hay tiempo
                if time.time() > max_time:
                    return best_val, best_move, prunes, boards

                # Mover pieza
                piece = move["from"].piece
                move["from"].piece = Tile.P_NONE
                to.piece = piece
                boards += 1

                val, _, new_prunes, new_boards = self.minimax(depth - 1,
                    player_to_max, max_time, a, b, not maxing, prunes, boards)
                prunes = new_prunes
                boards = new_boards

                # Se regresa la pieza
                to.piece = Tile.P_NONE
                move["from"].piece = piece

                if maxing and val > best_val:
                    best_val = val
                    best_move = (move["from"].loc, to.loc)
                    a = max(a, val)

                if not maxing and val < best_val:
                    best_val = val
                    best_move = (move["from"].loc, to.loc)
                    b = min(b, val)

                if self.ab_enabled and b <= a:
                    return best_val, best_move, prunes + 1, boards

        return best_val, best_move, prunes, boards

    def AI_Move(self):

        current_turn = (self.total_plies // 2) + 1
        print("Turno IA")
        sys.stdout.flush()

        # Se calcula la jugada
        self.computing = True
        self.board_view.update()
        max_time = time.time() + self.t_limit

        # se hace minimax
        start = time.time()
        _, move, prunes, boards = self.minimax(self.ply_depth,
            self.c_player, max_time)
        end = time.time()

        # Se mueve la pieza
        self.outline_tiles(None)  # se resetean los outlines
        move_from = self.board[move[0][0]][move[0][1]]
        move_to = self.board[move[1][0]][move[1][1]]
        self.move_piece(move_from, move_to)

        self.board_view.draw_tiles(board=self.board)  # Refresca el tablero

        winner = self.verify_winner()
        if winner:
            self.board_view.set_status("Gano el " + ("negro"
                if winner == Tile.P_BLACK else "rojo"))
            self.board_view.set_status_color("#212121")
            self.current_player = None
            self.current_player = None


        else:  
            self.current_player = (Tile.P_RED
                if self.current_player == Tile.P_BLACK else Tile.P_BLACK)

        self.computing = False
        print()

    def get_possible_moves(self, player=1):

        moves = []  # Posibles movimientos
        for col in range(self.b_size):
            for row in range(self.b_size):

                curr_tile = self.board[row][col]

                # ignorar elementos que no importan
                if curr_tile.piece != player:
                    continue

                move = {
                    "from": curr_tile,
                    "to": self.get_moves(curr_tile, player)
                }
                moves.append(move)

        return moves

    def get_moves(self, tile, player, moves=None, adj=True):

        if moves is None:
            moves = []

        row = tile.loc[0]
        col = tile.loc[1]

        # Lista de lugares validos
        valid_tiles = [Tile.T_NONE, Tile.T_BLACK, Tile.T_RED]
        if tile.tile != player:
            valid_tiles.remove(player)  
        if tile.tile != Tile.T_NONE and tile.tile != player:
            valid_tiles.remove(Tile.T_NONE) 

        # Movimientos adyacentes
        for col_delta in range(-1, 2):
            for row_delta in range(-1, 2):

                # Se ven los lugares

                new_row = row + row_delta
                new_col = col + col_delta

                
                if ((new_row == row and new_col == col) or
                    new_row < 0 or new_col < 0 or
                    new_row >= self.b_size or new_col >= self.b_size):
                    continue

                new_tile = self.board[new_row][new_col]
                if new_tile.tile not in valid_tiles:
                    continue

                if new_tile.piece == Tile.P_NONE:
                    if adj:  
                        moves.append(new_tile)
                    continue

                # Saltos

                new_row = new_row + row_delta
                new_col = new_col + col_delta

                
                if (new_row < 0 or new_col < 0 or
                    new_row >= self.b_size or new_col >= self.b_size):
                    continue

                new_tile = self.board[new_row][new_col]
                if new_tile in moves or (new_tile.tile not in valid_tiles):
                    continue

                if new_tile.piece == Tile.P_NONE:
                    moves.insert(0, new_tile)  # priorizar saltos
                    self.get_moves(new_tile, player, moves, False)

        return moves

    def move_piece(self, from_tile, to_tile):

        if from_tile.piece == Tile.P_NONE or to_tile.piece != Tile.P_NONE:
            self.board_view.set_status("Moviemiento invalido")
            return

        # Se mueve la pieza
        to_tile.piece = from_tile.piece
        from_tile.piece = Tile.P_NONE

        # Outline actualizado
        to_tile.outline = Tile.O_MOVED
        from_tile.outline = Tile.O_MOVED

        self.total_plies += 1

        self.board_view.set_status_color("#000000" if
            self.current_player == Tile.P_RED else "#E50000")
        self.board_view.set_status("Se movió la pieza de`" + str(from_tile) +
            "` a `" + str(to_tile) + "`, " + ('Le toca al ' + "negro" if
            self.current_player == Tile.P_RED else "Le toca al rojo"))

    def verify_winner(self):

        if all(g.piece == Tile.P_BLACK for g in self.r_goals):
            return Tile.P_BLACK
        elif all(g.piece == Tile.P_RED for g in self.g_goals):
            return Tile.P_RED
        else:
            return None

    def outline_tiles(self, tiles=[], outline_type=Tile.O_SELECT):

        if tiles is None:
            tiles = [j for i in self.board for j in i]
            outline_type = Tile.O_NONE

        for tile in tiles:
            tile.outline = outline_type

    def utility_distance(self, player):

        def point_distance(p0, p1):
            return math.sqrt((p1[0] - p0[0])**2 + (p1[1] - p0[1])**2)

        value = 0

        for col in range(self.b_size):
            for row in range(self.b_size):

                tile = self.board[row][col]

                if tile.piece == Tile.P_BLACK:
                    distances = [point_distance(tile.loc, g.loc) for g in
                                 self.r_goals if g.piece != Tile.P_BLACK]
                    value -= max(distances) if len(distances) else -50

                elif tile.piece == Tile.P_RED:
                    distances = [point_distance(tile.loc, g.loc) for g in
                                 self.g_goals if g.piece != Tile.P_RED]
                    value += max(distances) if len(distances) else -50

        if player == Tile.P_RED:
            value *= -1

        return value


if __name__ == "__main__":

    hoppers = Hoppers()
