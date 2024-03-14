from tkinter import *
from tkinter import ttk

SQUARE_SIZE = 50
BOARD_SIZE = 8
CAMP_SIZE = 4
OFFSETS = [-1, 0, 1]
PIECES_DICT = {}
# PLAYER=[
#     ("white", 0),
#     ("black", N-1)
# ]


root = Tk()
selected_piece = None
previous_piece =None

GOALS = {'white': [], 'black': []}

        

class GameBoard(Canvas):
    def __init__(self, root):
        super().__init__(root, width=SQUARE_SIZE*BOARD_SIZE, height=SQUARE_SIZE*BOARD_SIZE)
        self.grid()
        self.squares = []
        self.current_player = 'white'
        for row_num in range(BOARD_SIZE):
            row = []
            for col_num in range(BOARD_SIZE):
                color = "grey"
                square_id = self.create_rectangle(col_num * SQUARE_SIZE, row_num * SQUARE_SIZE, 
                                                  (col_num + 1) * SQUARE_SIZE, (row_num + 1) * SQUARE_SIZE, fill=color)
                row.append(square_id)
                self.tag_bind(square_id, "<Button-1>", self.move)
            self.squares.append(row)
        for y_col in range(BOARD_SIZE):
            for x_col in range(BOARD_SIZE):
                if y_col + x_col < CAMP_SIZE:
                    PIECES_DICT[(y_col, x_col)] = Pawn(self, y_col, x_col, "black")
                    GOALS['white'].append((BOARD_SIZE - 1 - y_col, BOARD_SIZE - 1 - x_col))

                if (BOARD_SIZE - 1 - y_col) + (BOARD_SIZE - 1 - x_col) < CAMP_SIZE:
                    PIECES_DICT[(y_col, x_col)] = Pawn(self, y_col, x_col, "white")
                    GOALS['black'].append((BOARD_SIZE - 1 - y_col, BOARD_SIZE - 1 - x_col))

    def switch_player(self):
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        print(f"It's now {self.current_player}'s turn.")
    
    def move(self, event):
        global selected_piece
        global previous_piece
        if selected_piece and selected_piece.color == self.current_player:
            col_num, row_num = event.x // SQUARE_SIZE, event.y // SQUARE_SIZE
            selected_piece.col_num, selected_piece.row_num = col_num, row_num
            selected_piece.redraw()
            selected_piece.reset_moves_shown()
            previous_piece = selected_piece
            selected_piece = None
            calculate_score(GOALS, PIECES_DICT)
            self.switch_player() 
        elif selected_piece and selected_piece.color != self.current_player:
            print(f"It's not {selected_piece.color}'s turn.")


class Pawn:
    def __init__(self, board, row_num, col_num, color):
        self.board = board
        self.row_num = row_num
        self.col_num = col_num
        self.color = color
        
        self.update_adjacent()
        self.oval_id = self.board.create_oval(self.col_num * SQUARE_SIZE, self.row_num * SQUARE_SIZE, 
                                              (self.col_num + 1) * SQUARE_SIZE, (self.row_num + 1) * SQUARE_SIZE, fill=self.color)
        self.board.tag_bind(self.oval_id, "<Button-1>", self.select_pawn)
    
    def __repr__(self):
        return f"{self.color} {self.oval_id}"

    def select_pawn(self, event):
        global selected_piece
        selected_piece = self
        self.visited_spaces = []
        self.update_adjacent()
        update_pieces_dict()
        self.calculate_possible_moves(self.col_num, self.row_num)
        self.show_possible_moves()
        
    def redraw(self):
        self.board.coords(self.oval_id, self.col_num * SQUARE_SIZE, self.row_num * SQUARE_SIZE, 
                          (self.col_num + 1) * SQUARE_SIZE, (self.row_num + 1) * SQUARE_SIZE)

    def show_possible_moves(self):
        for adjacent_x, adjacent_y in self.adjacent:
            if (adjacent_x, adjacent_y) not in PIECES_DICT.keys() and 0 <= adjacent_x < BOARD_SIZE and 0 <= adjacent_y < BOARD_SIZE:
                self.board.itemconfig(self.board.squares[adjacent_x][adjacent_y], fill="blue")

    def reset_moves_shown(self):
        for row_num in range(BOARD_SIZE):
            for col_num in range(BOARD_SIZE):
                if (row_num, col_num) not in PIECES_DICT.keys():
                    self.board.itemconfig(self.board.squares[row_num][col_num], fill="grey")
    
    def update_adjacent(self):
        self.adjacent = [
            (self.row_num + row_offset, self.col_num + col_offset)
            for row_offset in OFFSETS
            for col_offset in OFFSETS
            if row_offset != 0 or col_offset != 0
        ]
    
    def calculate_possible_moves(self, pos_x, pos_y):
        self.visited_spaces.append((pos_x,pos_y))
        for pos_x, pos_y in self.adjacent:
            if (pos_x, pos_y) in PIECES_DICT.keys():
                # Calculate the difference between the adjacent square and the current piece
                direction_x = pos_x - self.row_num
                direction_y = pos_y - self.col_num
                # Find the square directly opposite the adjacent square
                opposite_x = pos_x + direction_x
                opposite_y = pos_y + direction_y
                # Append the new coordinates to the list of possible moves
                if (opposite_x, opposite_y) not in self.visited_spaces and (opposite_x, opposite_y) not in PIECES_DICT.keys():
                    self.adjacent.append((opposite_x, opposite_y))
                    return self.calculate_possible_moves(opposite_x, opposite_y)


def update_pieces_dict():
    keys_to_remove = [
        key for key, piece in PIECES_DICT.items() 
        if piece.col_num == selected_piece.col_num and piece.row_num == selected_piece.row_num
    ]
    for key in keys_to_remove:
        del PIECES_DICT[key]
        
    if previous_piece:  
        PIECES_DICT[(previous_piece.row_num, previous_piece.col_num)] = previous_piece
 
def calculate_distance(pos_x, pos_y, goal_x, goal_y):
    distance_x = abs(pos_x - goal_x)
    distance_y = abs(pos_y - goal_y)
    distance = max(distance_x, distance_y)
    return distance


def calculate_score(goal_positions, pieces_dict):
    scores = {}
    for color in ['white', 'black']:
        scores[color] = 0
        for piece in pieces_dict.values():
            if piece.color == color:
                
                for goal in goal_positions[color]:
                    goal_x, goal_y = goal
                    scores[color] += calculate_distance(piece.row_num, piece.col_num, goal_x, goal_y)
    print(scores)
    return scores
    #pieces dict / coords
    #seperate white from black
    #assign goal position for white and black
    #for every color piece, calculate 



board = GameBoard(root)
root.mainloop()

