import tkinter as tk

class Board(tk.Tk):

    def __init__(self, init_board, *args, **kwargs):

        # Se inicializa la clase de tk
        tk.Tk.__init__(self, *args, **kwargs)

        # Se salva la meta data
        self.title("Hoppers")
        self.resizable(False, False)
        self.configure(bg="#fff")

        # Variables de tracking
        self.tiles = {}
        self.board = init_board
        self.b_size = len(init_board)

        # Se crean las lables de las columnas y filas
        label_font = "Helvetica 16"
        label_bg = "#fff"
        label_fg = "#333"
        for i in range(self.b_size):

            row_label1 = tk.Label(self, text=i + 1, font=label_font,
                bg=label_bg, fg=label_fg)
            row_label1.grid(row=i + 1, column=0)

            row_label2 = tk.Label(self, text=i + 1, font=label_font,
                bg=label_bg, fg=label_fg)
            row_label2.grid(row=i + 1, column=self.b_size + 2)

            col_label1 = tk.Label(self, text=chr(i + 97), font=label_font,
                bg=label_bg, fg=label_fg)
            col_label1.grid(row=0, column=i + 1)

            col_label2 = tk.Label(self, text=chr(i + 97), font=label_font,
                bg=label_bg, fg=label_fg)
            col_label2.grid(row=self.b_size + 2, column=i + 1)

        # Se crea el grid
        self.canvas = tk.Canvas(self, width=550, height=550, bg="#fff",
            highlightthickness=0)
        self.canvas.grid(row=1, column=1,
            columnspan=self.b_size, rowspan=self.b_size)

        # Label del estado
        self.status = tk.Label(self, anchor="c", font=(None, 16),
            bg="#000000", fg="#fff", text="Turno color negro")
        self.status.grid(row=self.b_size + 3, column=0,
            columnspan=self.b_size + 3, sticky="ewns")

        # Se hace bind de la funcion de dibujo
        self.canvas.bind("<Configure>", self.draw_tiles)
        self.columnconfigure(0, minsize=48)
        self.rowconfigure(0, minsize=48)
        self.columnconfigure(self.b_size + 2, minsize=48)
        self.rowconfigure(self.b_size + 2, minsize=48)
        self.rowconfigure(self.b_size + 3, minsize=48)


    def add_click_handler(self, func):
        self.click_handler = func

    def set_status(self, text):
        self.status.configure(text=text)

    def set_status_color(self, color):
        self.status.configure(bg=color)

    def draw_tiles(self, event=None, board=None):

        if board is not None:
            self.board = board

        # Guardar las propiedades
        self.canvas.delete("tile")
        cell_width = int(self.canvas.winfo_width() / self.b_size)
        cell_height = int(self.canvas.winfo_height() / self.b_size)
        border_size = 5

        # Rehacer los rectangulos
        for col in range(self.b_size):
            for row in range(self.b_size):

                board_tile = self.board[row][col]
                tile_color, outline_color = board_tile.get_tile_colors()

                # se calcula la posicion del pixel
                x1 = col * cell_width + border_size / 2
                y1 = row * cell_height + border_size / 2
                x2 = (col + 1) * cell_width - border_size / 2
                y2 = (row + 1) * cell_height - border_size / 2

                # Se renderiza la casilla
                tile = self.canvas.create_rectangle(x1, y1, x2, y2,
                    tags="tile", width=border_size, fill=tile_color,
                    outline=outline_color)
                self.tiles[row, col] = tile
                self.canvas.tag_bind(tile, "<1>", lambda event, row=row,
                    col=col: self.click_handler(row, col))

        self.draw_pieces()

    def draw_pieces(self, board=None):

        if board is not None:
            self.board = board

        self.canvas.delete("piece")
        cell_width = int(self.canvas.winfo_width() / self.b_size)
        cell_height = int(self.canvas.winfo_height() / self.b_size)
        border_size = 20

        for col in range(self.b_size):
            for row in range(self.b_size):

                # Se calcual la posicion
                x1 = col * cell_width + border_size / 2
                y1 = row * cell_height + border_size / 2
                x2 = (col + 1) * cell_width - border_size / 2
                y2 = (row + 1) * cell_height - border_size / 2

                if self.board[row][col].piece == 2:
                    piece = self.canvas.create_oval(x1, y1, x2, y2,
                        tags="piece", width=0, fill="#E50000")
                elif self.board[row][col].piece == 1:
                    piece = self.canvas.create_oval(x1, y1, x2, y2,
                        tags="piece", width=0, fill="#000000")
                else:
                    continue

                self.canvas.tag_bind(piece, "<1>", lambda event, row=row,
                    col=col: self.click_handler(row, col))

        self.update()


class Tile():

    # Constantes para la meta
    T_NONE = 0
    T_BLACK = 1
    T_RED = 2

    # Constantes de las piezas
    P_NONE = 0
    P_BLACK = 1
    P_RED = 2

    # Constantes de los posibles movimientos
    O_NONE = 0
    O_SELECT = 1
    O_MOVED = 2

    def __init__(self, tile=0, piece=0, outline=0, row=0, col=0):
        self.tile = tile
        self.piece = piece
        self.outline = outline

        self.row = row
        self.col = col
        self.loc = (row, col)

    def get_tile_colors(self):

        # Find appropriate tile color
        tile_colors = [
            ("#0000CD", "#87CEFA"),  # Normal tiles
            ("#A9A9A9", "#696969"),  # Red goal tiles
            ("#ba6262", "#ce9d9d")   # Black goal tiles
        ]
        tile_color = tile_colors[self.tile][(self.loc[0] + self.loc[1]) % 2]

        # Find appropriate outline color
        outline_colors = [
            tile_color,
            "white",  # TODO: Change
            "#1100BB"
        ]
        outline_color = outline_colors[self.outline]

        return tile_color, outline_color

    def __str__(self):
        return chr(self.loc[1] + 97) + str(self.loc[0] + 1)

    def __repr__(self):
        return chr(self.loc[1] + 97) + str(self.loc[0] + 1)

