from tkinter import *
from tkinter import ttk

SQUARE_SIZE = 50
BOARD_SIZE = 8
CAMP_SIZE = 4
OFFSETS = [-1,0,1]
PIECES_DICT = {}

root = Tk()

selected_piece = None


class Square:
    def __init__(self, row_num, col_num, color):
        self.row_num = row_num
        self.col_num = col_num
        self.color=color
        self.adjacent = [
                        (row_num + row_offset, col_num+col_offset) 
                         for row_offset in OFFSETS 
                         for col_offset in OFFSETS
                         if row_offset != 0 or col_offset != 0 
                         ]
        
        self.canvas_object = Canvas(root, width=SQUARE_SIZE, height=SQUARE_SIZE)
        self.canvas_object.grid(row=self.row_num, column=self.col_num)
        self.oval_id = self.canvas_object.create_oval(0, 0, SQUARE_SIZE, SQUARE_SIZE, fill=self.color)
        self.canvas_object.tag_bind(self.oval_id, "<Button-1>", self.move)

    
    def get_coords(self):
        print(f"clicked: {self.col_num}, {self.row_num}")
        return (self.col_num, self.row_num)
        
    def __repr__(self) -> str:
        return f"x: {self.col_num} y: {self.row_num} color: {self.color}"
    
    def move(self, event):
        global selected_piece
        if selected_piece:
            # Store old coordinates for later deletion from PIECES_DICT
            old_coords = (selected_piece.col_num, selected_piece.row_num)
            
            selected_piece.col_num, selected_piece.row_num = self.col_num, self.row_num
            
            # Update PIECES_DICT
            del PIECES_DICT[old_coords]
            PIECES_DICT[(self.col_num, self.row_num)] = selected_piece

            selected_piece.redraw()
            selected_piece = None  # Clear the selected piece

class Board:
    def __init__(self, BOARD_SIZE):
        self.board_size = BOARD_SIZE
        board_space = {}
        for row_num in range(self.board_size):
            for col_num in range(self.board_size):
                Square(row_num, col_num, "grey")
                
class Pawn(Square):
    def __init__(self, row_num, col_num, color):
        super().__init__(row_num, col_num, color)
        self.selected = False
        self.canvas_object.tag_bind(self.oval_id, "<Button-1>", self.select_pawn)

    
    def select_pawn(self, event):
        global selected_piece
        selected_piece = self
        self.reset_moves_shown()
        self.show_possible_moves() 
        
    def show_possible_moves(self):
        self.possible_moves_coords = []
        for adjacent_x, adjacent_y in self.adjacent:
            if (adjacent_x, adjacent_y) not in PIECES_DICT.keys() and adjacent_x >= 0 and adjacent_y >=0:
                self.possible_moves_coords.append(Square(adjacent_x, adjacent_y, color="blue"))
        print(self)

    def reset_moves_shown(self):
        for coords in PIECES_DICT:
            y_col, x_col = coords
            Square(y_col, x_col, color="grey")
    
    def redraw(self):
        self.canvas_object.delete(self.oval_id)
        self.oval_id = self.canvas_object.create_oval(0, 0, SQUARE_SIZE, SQUARE_SIZE, fill=self.color)
        self.canvas_object.tag_bind(self.oval_id, "<Button-1>", self.select_pawn)
                
    


        

board = Board(BOARD_SIZE)
for y_col in range(BOARD_SIZE):
    for x_col in range(BOARD_SIZE):
        if y_col+x_col < CAMP_SIZE:
            PIECES_DICT[(y_col, x_col)] = Pawn(y_col, x_col, "black")


root.mainloop()