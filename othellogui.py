#Contains the class for the othello board GUI.

_INITIAL_CELL_WIDTH = 60  #Default is 60 pixels
_INITIAL_CELL_HEIGHT = 60 #Defauly is 60 pixels

import tkinter, othello, scoreboardgui, math, random, time, othelloai
from collections import defaultdict
from copy import deepcopy

class OthelloGUI:
    def __init__(self, num_rows=4, num_cols=4, hum_player="B", cpu_opp="Greedy Gary",
                 first_mover="B", top_left="B", how_to_win=">"):
        '''Initializes all the attributes of a BoardGUI object.'''

        self._root = tkinter.Tk()
        self._root.configure(background='black')
        self._root.wm_title("Othello")
        self._root.geometry('+550+150')
        self._game_active = True
        self._game_ended = False
        self._first_mover = first_mover
        self._cpu_made_first_move = False
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._top_left = top_left   #For AI Othello
        self._hum_player = hum_player   #For AI Othello
        self._cpu_player = "W" if hum_player == "B" else "B"   #For AI Othello
        self._cpu_opp = cpu_opp
        self._how_to_win = how_to_win   #For AI Othello
        self._corner_mappings = dict()   #For AI Othello
        self._gamestate = othello.Othello(num_rows, num_cols, first_mover, top_left, how_to_win)

        
        self._canvas = tkinter.Canvas(master=self._root, height=_INITIAL_CELL_HEIGHT*num_rows,
                                      width=_INITIAL_CELL_WIDTH*num_cols, background="darkgreen",
                                      borderwidth=5, relief=tkinter.RAISED)
        self._canvas.configure(highlightbackground="gray")
        self._canvas.grid(row=1, column=0, padx=30,pady=30,
                    sticky=tkinter.N+tkinter.S+tkinter.W+tkinter.E)
        
        self._scoreboard = scoreboardgui.ScoreBoardGUI(self._root, self._gamestate, background="gray",
                                                       borderwidth=5, relief=tkinter.RAISED)
        self._scoreboard.grid(row=0, column=0,
                               sticky=tkinter.N+tkinter.S+tkinter.W+tkinter.E, padx=20, pady=(20,0))
                               #Pass one of the padding options a tuple to indicate different paddings
                               #for (top, bottom) for pady or (left, right) for padx directions.
        
        self._root.rowconfigure(1, weight=1)
        self._root.columnconfigure(0, weight=1)
        self._canvas.bind("<Configure>", self._on_canvas_resize)
        self._canvas.bind("<Button-1>", self._on_canvas_click)
        self._canvas.bind("<Motion>", self._on_mouse_motion)
        self._scoreboard.bind("<Button-1>", self._on_scoreboard_click)
        self._scoreboard.bind("<Motion>", self._on_mouse_motion)


    def start(self):
        '''Runs the mainloop on the root window.'''
        self._root.mainloop()


    #TODO: Figure out why there's also a call to the AI for mouse motion event...
    # - Ah, so that the CPU could make a move when they go first.
    def _on_mouse_motion(self, event):
        '''An event handler that process motion over the canvas.'''
        if self._first_mover == self._cpu_player and not self._cpu_made_first_move:
            if self._cpu_opp == "Greedy Gary":
                othelloai.greedy_cpu(self._gamestate, self._cpu_player, self._process_move)
            elif self._cpu_opp == "Mini Max":
                while self._gamestate.get_turn() == self._cpu_player and self._gamestate.get_winner() == " ":
                    #FOCUS HERE
                    #result = othelloai.minimax(self._gamestate, self._cpu_player, 3)
                    result = othelloai.minimax_abp(self._gamestate, self._cpu_player,
                                                   float("-inf"), float("inf"), 3)
                    if result[1] != None:
                        self._process_move(result[1][0], result[1][1])
        self._draw_board()
        #Must draw_board() here to take effect. When you had this code in the __init__ funciton, note how
        #draw_board() is automatically called upon the window appearing!
        self._cpu_made_first_mode = True


    def _on_canvas_resize(self, event):
        '''An event handler that processes window resizes.'''
        self._draw_board()


    def _on_scoreboard_click(self, event):
        '''Destroys the game window upon a click of the scoreboard Frame.'''
        if not self._game_active:
            self._game_ended = True
            self._root.destroy()


    def _draw_board(self):
        '''Draws the lines and tiles corresponding to a particular Othello game state.'''
        self._canvas.delete(tkinter.ALL)
        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()

        self._draw_lines(canvas_width, canvas_height)
        
        corners = self._get_corners(canvas_width, canvas_height)
        new_corner_mappings = self._get_mappings(corners, "corners")
        
        self._draw_circles(new_corner_mappings)


    def _draw_lines(self, canvas_width, canvas_height):
        '''Draws the lines on the board.'''
        #DRAW VERTICAL LINES
        delta_x = 0
        for col in range(1, self._num_cols):
            self._canvas.create_line(canvas_width*(1/self._num_cols) + delta_x, 0,
                                     canvas_width*(1/self._num_cols) + delta_x, canvas_height, width=3)
            delta_x += canvas_width*(1/self._num_cols) #increment by width of a cell
            
        #DRAW HORIZONTAL LINES
        delta_y = 0
        for row in range(1, self._num_rows):
            #The idea is that we jump down the number of pixels equal to _CELL_HEIGHT for each row...
            #NOTE: In general, 1/(whatever) is a single unit of (whatever)
            self._canvas.create_line(0, canvas_height*(1/self._num_rows) + delta_y, #left starting point (x, y)
                                    canvas_width, canvas_height*(1/self._num_rows) + delta_y, width=3) #right endpoint (x, y)
            delta_y += canvas_height*(1/self._num_rows) #increment by height of a cell


    def _on_canvas_click(self, event):
        '''An event handler that processes left mouse button clicks.'''
        if self._game_active:
            if self._cpu_opp == "None":
                self._player_move(event)
            else:
                if self._gamestate.get_turn() == self._hum_player:
                    self._player_move(event) #Human moves
                if self._gamestate.get_turn() == self._cpu_player:
                    if self._cpu_opp == "Greedy Gary":
                        othelloai.greedy_cpu(self._gamestate, self._cpu_player, self._process_move)
                    elif self._cpu_opp == "Mini Max":
                        #print("CHANGE DEPTH BACK TO 3 WHEN DONE TESTING!")
                        while self._gamestate.get_turn() == self._cpu_player and\
                              self._gamestate.get_winner() == " ":
                            #FOCUS HERE
                            #result = othelloai.minimax(self._gamestate, self._cpu_player, 3)
                            result = othelloai.minimax_abp(self._gamestate, self._cpu_player,
                                                           float("-inf"), float("inf"), 3)
                            #Handle case where result[1] == None?
                            if result[1] != None:
                                self._process_move(result[1][0], result[1][1])
                            #else:
                            #    self._game_ended = True
                            #Hmm...program is crashing when a game is over rather than exiting properly.
                            #Probably happens when white makes the final move...yup, that's the problem.
        else:
            self._game_ended = True
            self._root.destroy() #Click on canvas to get rid of window after a completed game
            
    
    def _player_move(self, event):
        #Maybe I could use a while loop here too instead of having if sttements in _on_canvas_click?
        '''Executes a human player's move'''
        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()
        
        corners = self._get_corners(canvas_width, canvas_height)
        midpoint_mappings = self._get_mappings(corners, "midpoints")
        self._corner_mappings = self._get_mappings(corners, "corners")
        #Made this an instance variable so I wouldn't have to pass it around to self._process_move?

        nearest_cell = self._find_nearest_cell(event, midpoint_mappings)
        self._process_move(nearest_cell[0]+1, nearest_cell[1]+1)


    def _process_move(self, row, col):
        '''Processes a move executed by either the player or CPU.'''
        if self._gamestate.valid_move(row, col) and self._game_active:
        #^If move is valid...
            print("FOR TESTING. Move Made: ", (row, col))
            self._scoreboard.update_turn_label(self._gamestate)
            self._scoreboard.update_score_label(self._gamestate)
            if self._gamestate.get_winner() != " ":
                self._scoreboard.indicate_result(self._gamestate)
                self._game_active = False #Perhaps you only need to use self._gamestate.get_winner() rather than this variable?
        elif not self._gamestate.valid_move(row, col) and self._gamestate.get_winner() != " ":
        #^Handles case when both players no longer have valid moves before board is full..
            self._scoreboard.indicate_result(self._gamestate)
            self._game_active = False          
        elif not self._gamestate.valid_move(row, col) and self._game_active:
        #^If invalid move was made...
            self._scoreboard.indicate_invalid(self._gamestate)

        self._draw_circles(self._corner_mappings)
        self._root.update() #this is for the CPU in case they make multiple moves

    
    def _find_nearest_cell(self, event, midpoint_mappings):
        '''Finds the nearest cell to a mouse click made on the game board.'''
        min_dist = float("inf")
        nearest_cell = (0, 0)
        for item in midpoint_mappings.items():
            dist = math.sqrt((event.x-item[1][0])**2 + (event.y-item[1][1])**2)
            if dist < min_dist:
                nearest_cell = (item[0][0], item[0][1])
                min_dist = dist
                
        return nearest_cell


    def _draw_circles(self, corner_mappings): #Note how the TL and BR corners are needed to draw circles (ovals)
        '''Takes a mapping of cell positions to top left and bottom right corners and draws circles
           according to how they are arranged for a particular gamestate.'''
        for (i, j) in corner_mappings:
            if self._gamestate.get_board()[i][j] == "B":
                self._canvas.create_oval(corner_mappings[(i,j)][0][0]+8, corner_mappings[(i,j)][0][1]+8,
                                         corner_mappings[(i,j)][1][0]-8, corner_mappings[(i,j)][1][1]-8, fill="black", width=3)
            elif self._gamestate.get_board()[i][j] == "W":
                self._canvas.create_oval(corner_mappings[(i,j)][0][0]+8, corner_mappings[(i,j)][0][1]+8,
                                         corner_mappings[(i,j)][1][0]-8, corner_mappings[(i,j)][1][1]-8, fill="white", width=3)
        

    def _get_corners(self, canvas_width, canvas_height):
        '''Genereates a list where each elements is a list of tuples whoses components
           are the top-left and bottom-right corners of a cell. An element is created
           for each cell on the board.'''
        cur_corner_x = 0
        cur_corner_y = 0
        corners = []
        for row in range(self._num_rows):
            for col in range(self._num_cols):
                top_left = (cur_corner_x, cur_corner_y) 
                #top_right = (cur_corner_x + canvas_width*(1/self._num_cols), cur_corner_y)
                #bottom_left = (cur_corner_x, cur_corner_y + canvas_height*(1/self._num_rows))
                bottom_right = (cur_corner_x + canvas_width*(1/self._num_cols), 
                                cur_corner_y + canvas_height*(1/self._num_rows))
                corners.append([top_left, bottom_right])
                cur_corner_x += canvas_width*(1/self._num_cols)
            cur_corner_x = 0 #push x all the way back to the left of the canvas
            cur_corner_y += canvas_height*(1/self._num_rows)

        return corners


    def _get_mappings(self, corners, mode):
        '''Takes a list of the top left and bottom right corners of all the squares on the
           board and maps these corners to their corresponding (i,j)th cell (if mode is "corners")
           or maps the midpoint between these corners to the corresponding (i,j)th cell (if mode is
           "midpoints"). The mapping is represented as a dictionary.'''
        mappings = dict() #recall that dictionaries are not ordered!!!!
        k = 0
        for i in range(self._num_rows):
            for j in range(self._num_cols):
                if mode == "corners":
                    mappings[(i,j)] = corners[k]
                elif mode == "midpoints":
                    mappings[(i,j)] = ((corners[k][0][0]+corners[k][1][0])/2,
                                              (corners[k][0][1]+corners[k][1][1])/2)
                k += 1
                
        return mappings
    

    def did_game_end(self):
        '''Returns a boolean indicating if the current othello game has ended.'''
        return self._game_ended


#For testing
if __name__ == "__main__":
    #game = OthelloGUI(4, 4, "B", "Greedy Gary", "W", "B", ">")
    game = OthelloGUI(8, 8, "W", "Mini Max", "W", "W", ">")
    #game = OthelloGUI(8, 8, "B", "None", "W", "W", ">")
    game.start()
