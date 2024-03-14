from tkinter import *

SQUARE_SIZE = 50
BOARD_SIZE = 8
CAMP_SIZE = 4
OFFSETS = [-1, 0, 1]
PIECES_DICT = {}

root = Tk()

class GameBoard:
    def __init__(self):
        self.pawn_dict = {
            "white": {},
            "black": {}
        }

        self.initialize_board(BOARD_SIZE)
        self.initialize_pawns(BOARD_SIZE, CAMP_SIZE)
        self.controller = None
    
    def set_controller(self, controller):
        self.controller = controller

    def create_pawn(self, x, y, color, pawn_id=None):
        return Pawn(x,y,color,pawn_id)
    
    def initialize_pawns(self, board_size, camp_size):
        pawn_id = 0
        for x in range(board_size):
            for y in range(board_size):
                if x + y < camp_size:
                    pawn_id += 1
                    self.pawn_dict["white"][pawn_id] = self.create_pawn(x, y, "white", pawn_id)
                if (board_size - 1 - x) + (board_size - 1 - y) < CAMP_SIZE:
                    pawn_id += 1
                    self.pawn_dict["black"][pawn_id] = self.create_pawn(x, y, "black", pawn_id)
        print(f"model pawns {self.pawn_dict}")
    def initialize_board(self, board_size):
        self.board_coords = [(row_num, col_num) for row_num in range(board_size) for col_num in range(board_size)]
    
    def get_pawn(pawn):
        pass
    
class View(Canvas):
    def __init__(self, root):
        super().__init__(root, width=400, height=400)
        self.pack()
        self.controller = None
        self.board_squares = {}
        self.pawn_dict = {
            "white": {},
            "black": {}
        }
        self.pawn_dict2 = []
        self.previously_clicked_oval_id_and_color = None
        
    def draw_board(self, board_coords):
        for x, y in board_coords:
            square_id = self.create_rectangle(x * SQUARE_SIZE, y * SQUARE_SIZE,
                                            x * SQUARE_SIZE + SQUARE_SIZE, y * SQUARE_SIZE + SQUARE_SIZE, fill="gray")
            self.board_squares[(x, y)] = square_id
            self.tag_bind(square_id, "<Button-1>", lambda event, x=x, y=y: self.highlight_square(x, y, "blue"))

    def highlight_square(self, x, y, color):
        self.reset_squares()
        board_squares = self.board_squares.get((x, y))
        if board_squares:
            self.itemconfig(board_squares, fill=color)
    
    def set_controller(self, controller):
        self.controller = controller
            
    def draw_pawn(self, pawn):
        oval_id = self.create_oval(
            pawn.x * SQUARE_SIZE, pawn.y * SQUARE_SIZE, 
            pawn.x * SQUARE_SIZE + SQUARE_SIZE, pawn.y * SQUARE_SIZE + SQUARE_SIZE, 
            fill=pawn.color
        )
        
        #self.pawn_dict[pawn.color][pawn.pawn_id] = oval_id
        
        self.tag_bind(oval_id, "<Button-1>", lambda event, pawn_id=pawn.pawn_id: self.select_pawn(oval_id, "blue", pawn))

    def highlight_pawn(self, oval_id, highlight_color): 
        #Reset previous pawn       
        if self.previously_clicked_oval_id_and_color:
            id, color = self.previously_clicked_oval_id_and_color
            self.itemconfig(tagOrId=id, fill=color)
        color = self.itemcget(oval_id, 'fill')
        self.previously_clicked_oval_id_and_color = (oval_id, color)
        #Highlights new pawn
        self.itemconfig(tagOrId=oval_id, fill=highlight_color)
    
    def select_pawn(self, oval_id, highlight_color, pawn):
        self.highlight_pawn(oval_id, highlight_color)
        self.send_pawn(pawn)
    
    def select_square(self):
        pass
    
    def draw_pawns(self, pawn_dict):
        for color in pawn_dict.keys():
            for pawn_id, pawn in pawn_dict[color].items():
                self.draw_pawn(pawn)
                self.pawn_dict[color][pawn_id] = pawn
        print(f"view pawns {self.pawn_dict}")

    def reset_squares(self):
        for square in self.board_squares.values():
            self.itemconfig(square, fill="gray")
    
    def send_pawn(self,pawn):
        self.controller.send_pawn(pawn)
    
    def send_square(self, square):
        pass
            
class Controller:
    def __init__(self, view, game_board):
        self.view = view
        self.game_board = game_board #Board and pawns are created 
        self.view.set_controller(self) #connect controller in view for communication
        self.game_board.set_controller(self) #connect controller in model for communication
        self.view.draw_board(self.game_board.board_coords) #Draws in view from information in model
        self.view.draw_pawns(self.game_board.pawn_dict) #Draw pawns created in model, draw in view

        
    def get_board_coords(self):
        return self.game_board.board_coords
    
    def send_pawn(self,pawn):
        game_board.get_pawn(pawn)
    
class Pawn:
    def __init__(self, row_num, col_num, color, pawn_id=None):
        self.x = row_num
        self.y = col_num
        self.color = color
        self.pawn_id = pawn_id
    
    def __repr__(self):
        return f"{self.pawn_id}, {self.x, self.y}, {self.color}"

game_board = GameBoard()
view = View(root)
controller = Controller(view, game_board)

root.mainloop()
