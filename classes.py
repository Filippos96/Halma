from tkinter import *
from tkinter import ttk

SQUARE_SIZE = 50
BOARD_SIZE = 8
CAMP_SIZE = 4
OFFSETS = [-1,0,1]
MODIFIED_SPACES = {}
WHITE_PIECES = {}
BLACK_PIECES = {}
HILITE=None
NO_HILITE_FILL ="white"
HILITE_FILL = "blue"
root = Tk()

class Board:
    def __init__(self, row_num, col_num):
        self.square_dict={}
        self.adjacent = [
                        (row_num + row_offset, col_num+col_offset) 
                         for row_offset in OFFSETS 
                         for col_offset in OFFSETS
                         if row_offset != 0 or col_offset != 0 
                         ]
        self.row_num = row_num
        self.col_num = col_num
          
        self.canvas_object = Canvas(root, width=SQUARE_SIZE, height=SQUARE_SIZE)
        self.canvas_object.grid(row=self.row_num, column=self.col_num)
        self.oval_id = None
        
        if row_num+col_num < CAMP_SIZE:
            self.draw_oval()
            self.canvas_object.tag_bind(self.oval_id, "<Button-1>", self.oval_click)
        
    def reset(self):
        self.canvas_object.delete(self.rect_id)
    def oval_clicked(self,event):
        print("oval clicke")
    def rect_click(self,event):
        print("clicked rect")
    
class Square:
    
    last_clicked = None  # Class attribute to track the last clicked piece

    def __init__(self, row_num, col_num):
        self.adjacent = [
                        (row_num + row_offset, col_num+col_offset) 
                         for row_offset in OFFSETS 
                         for col_offset in OFFSETS
                         if row_offset != 0 or col_offset != 0 
                         ]
        self.row_num = row_num
        self.col_num = col_num
          
        self.canvas_object = Canvas(root, width=SQUARE_SIZE, height=SQUARE_SIZE)
        self.canvas_object.grid(row=self.row_num, column=self.col_num)
        self.oval_id = None
        
        if row_num+col_num < CAMP_SIZE:
            self.draw_oval()
            self.canvas_object.tag_bind(self.oval_id, "<Button-1>", self.oval_click)
    
    def reset(self):
        self.canvas_object.configure(bg="lightgray")
        
    def draw_rect(self):
        self.canvas_object.configure(bg="black")
        MODIFIED_SPACES[(self.row_num,self.col_num)] = self
        
    def draw_oval(self):
        self.oval_id = self.canvas_object.create_oval(0, 0, SQUARE_SIZE, SQUARE_SIZE, fill=NO_HILITE_FILL)
    
    def oval_click(self, event):
        if Square.last_clicked:
            Square.last_clicked.canvas_object.itemconfigure(Square.last_clicked.oval_id, fill=NO_HILITE_FILL, width=0)

        for square in MODIFIED_SPACES.values():
            square.reset()
        for space in self.adjacent:
            square = square_dict.get(space,None)
            if square.oval_id is None:
                square.draw_rect()
        self.highlite_oval()
    def highlite_oval(self):
        HILITE = self
        HILITE.canvas_object.itemconfigure(HILITE.oval_id, fill=HILITE_FILL, width=2)
        
        Square.last_clicked = self  # Update the last clicked piece
        
    

square_dict = {}
for row_num in range(BOARD_SIZE):
    for col_num in range(BOARD_SIZE):
        square_dict [(row_num,col_num)]=Square(row_num, col_num)

root.mainloop()


def remove_oval(self):
    pass
def get_possible(self, iteration=1):
    if iteration== 1:
        self.list_of_movers=[]
    for direction in self.adjavent:
        adj_square = self.board.square_dict.get(direction)
        after_pos = [pos*2 for pos in direction]
        one_after = self.board.square_dict.get(after_pos)
        after_empty = one_after.oval_id is None
        if adj_square.oval_id is None:
            if iteration == 1: 
                self.list_of_moves.append(direction)
        elif after_empty and after_pos not in self.list_of_moves:
            self.list_of_moves
            
            
PLAYERS = [
    ("white", 0),
    ("black", N-1)
]

#Give the distance from goal to every square a score and just add whatever the 
#square a piece is on has for score to the score