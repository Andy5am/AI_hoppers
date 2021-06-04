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
            self.current_player == Tile.P_RED else "#007F00")

        if self.c_player == self.current_player:
            self.AI_Move()

        self.board_view.add_click_handler(self.tile_clicked)
        self.board_view.draw_tiles(board=self.board)  # Se recarga el tablero

        self.board_view.mainloop()  # Tkinter loop



if __name__ == "__main__":

    hoppers = Hoppers()
