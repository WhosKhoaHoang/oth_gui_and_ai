#Contains all of the classes corresponding to an othello gamestate.
import math
from collections import namedtuple
from copy import deepcopy




class OthelloInvalidMoveError(Exception):
    """ An exception that represents an invalid move. """
    pass


class Othello:
    """ A class that represents the game state of an Othello game. """

    def __init__(self, num_rows = 4, num_cols = 4,
                 first_mover = "W", top_left = "B",
                 how_to_win = ">", initial_config=[]):
                # initial_config was made for AI Othello to
                # get around pass-by-reference behavior of lists.
        """
        Initializes the game state of an Othello game.
        @num_rows: The number of rows for this Othello game
        @num_cols: The number of columns for this Othello game
        @first_mover: The player who moves first ("W" or "B")
        @top_left: The top-left player in the initial center
                   four-piece layout of this Othello game
        @how_to_win: The method for winning a game (e.g.,
                     most pieces ">" or fewest pieces "<")
        @initial_config: A 2D list representing the initial state
                         of this Othello game (may contain many
                         or fewer pieces than the traditional
                         center four-piece layout)
        type num_rows: int
        type num_cols: int
        type first_mover: str
        type top_left: str
        type how_to_win: str
        type initial_config: list 
        return: None
        rtype: None
        """
        if (4 > num_rows > 16) or num_rows % 2 != 0:
            raise Exception
        else:
            self._num_rows = num_rows
        if (4 > num_cols > 16) or num_cols % 2 != 0:
            raise Exception
        else:
            self._num_cols = num_cols
        if first_mover != "B" and first_mover != "W":
            raise Exception
        else:
            self._turn = first_mover
        if top_left != "B" and top_left != "W":
            raise Exception
        else:
            self._top_left = top_left
        if how_to_win != ">" and how_to_win != "<":
            raise Exception
        else:
            self._how_to_win = how_to_win

        if initial_config == []:
            self._board = self._make_board(num_rows, num_cols, top_left)
        else:
            self._board = deepcopy(initial_config)
            
        self._game_over = False
        self._winner = " "
        self._tl_cell = (0, 0)
        self._tr_cell = (0, num_cols-1)
        self._bl_cell = (num_rows-1, 0)
        self._br_cell = (num_rows-1, num_cols-1)
        self._ls_cells = [(c, 0) for c in range(1, num_rows-1)]
        self._rs_cells = [(c, num_cols-1) for c in range(1, num_rows-1)]
        self._ts_cells = [(0, c) for c in range(1, num_cols-1)]
        self._bs_cells = [(num_rows-1, c) for c in range(1, num_cols-1)]
        #^Note how ranges start from 1 and go to num_rows-1 to avoid corners,
        #which are processed differently

        
    def get_tl_cell(self):
        """
        Returns the top-left cell of the board.
        return: The top-left cell of this Othello game
        rtype: tuple
        """
        return self._tl_cell


    def get_tr_cell(self):
        """
        Returns the top-right cell of the board.
        return: The top-right cell of this Othello game
        rtype: tuple
        """
        return self._tr_cell


    def get_bl_cell(self):
        """
        Returns the bottom-left cell of the board.
        return: The bottom-left cell of this Othello game
        rtype: tuple
        """
        return self._bl_cell


    def get_br_cell(self):
        """
        Returns the bottom-right cell of the board.
        return: The bottom-right cell of this Othello game
        rtype: tuple
        """
        return self._br_cell
    

    def get_num_rows(self):
        """
        Returns the number of rows in an Othello board.
        return: The number of rows in this Othello game
        rtype: int
        """
        return self._num_rows


    def get_num_cols(self):
        """
        Returns the number of columns in an Othello board.
        return: The number of columns in this Othello game
        rtype: int
        """
        return self._num_cols


    def get_board(self):
        """
        Returns a 2D list representation of the Othello board.
        return: A 2D list representaiton of this Othello game
        rtype: list
        """
        return self._board


    def get_turn(self):
        """
        Returns whose turn it is in an Othello game.
        return: The current turn of this Othello game ("B" or "W")
        rtype: str
        """
        return self._turn


    def get_winner(self):
        """
        Returns the winner of the game.
        return: The winner of this game ("B" or "W")
        rtype: str
        """
        return self._winner


    def get_counts(self):
        """
        Returns the count of black and white tiles.
        return: The count of black and white titles in a
                list in the form [black_count, white_count]
        rtype: list
        """
        counts = [0, 0]
        for i in range(self._num_rows):
            for j in range(self._num_cols):
                if self._board[i][j] == "B":
                    counts[0] += 1
                elif self._board[i][j] == "W":
                    counts[1] += 1
        return counts


    #write function for getting how to win, getting top left...
    def get_win_method(self):
        """
        Returns the win method for a game.
        return: The win method for this game (e.g.,
                most pieces ">" or fewest pieces "<")
        rtype: str
        """
        return self._how_to_win


    def get_top_left(self):
        """
        Returns the top left color in the center square.
        return: The top left color in the initial center
                four-piece layout of this Othello game
        type: str
        """
        return self._top_left


    def valid_move(self, row, col):
        """
        Checks the validity of a move and performs the move.
        returns True if move was valid, else returns False.
        @row: The row where a move will be attempted to be performed
        @col: The col where a move will be attempted to be performed
        type row: int
        type col: int
        return: True if the attempted move is valid or False otherwise
        rtype: bool
        """
        if not self._game_over:
            i_row, i_col = row-1, col-1
            #i_row and i_col wil be used to index the board (hence the i)
            (valid, flip_lst) = self._valid_placement(i_row, i_col)
            #print("FOR TESTING. Tiles Flipped: ", flip_lst)
    
            if valid:
                #Big Change: You decided to make determining validity
                #            and flipping separate operations
                self._flip(i_row, i_col, flip_lst)
            else:
                print("\nPlease enter a valid move!")
                return False

            if self._board_is_full():
                self._game_over = True
                self._set_winner()        
           
            self._switch_turn(self._turn)
            if not self._valid_move_exists(): #Check if the other player has any valid moves
                print("\nNo valid moves exist for {0}. {0}'s turn has been skipped".format(self._turn))
                self._switch_turn(self._turn) #Switch turn back to player before skip was determined
                if not self._valid_move_exists(): #Check if the other player has any valid moves
                    print("No valid moves exist for {0}. {0}'s turn has been skipped".format(self._turn))
                    print("No moves exist for either player. GAME OVER")
                    self._game_over = True
                    self._set_winner()
                    return False

            return True
        elif self._game_over:
            print("The game is over. No more moves can be made!")
            #TODO: Replace this^ with an exception later?
            return False


    def _board_is_full(self):
        """
        Determines if the board for this Othello game is full.
        return: True if the board for this Othello game is full
                or False otherwise.
        rtype: bool
        """
        return (self.get_counts()[0] + self.get_counts()[1] == self._num_rows * self._num_cols)


    def _flip(self, i_row, i_col, flip_lst):
        """
        Flips all tiles generated by a tile placement.
        @i_row: The 0-based row of a tile placement
        @i_col: The 0-based col of a tile placement
        @flip_lst: The list of positions of tiles to flip
                   as a result of the given tile placment
        type i_row: int 
        type i_col: int
        type flip_lst: [tuple]
        return: None
        rtype: None
        """
        self._board[i_row][i_col] = self._turn
        for cell in flip_lst:
            self._board[cell[0]][cell[1]] = self._turn
    

    def _valid_placement(self, i_row, i_col):
        """
        Conducts several checks with the given tile placement
        to determine if the placement is valid. If valid, return
        a tuple containing True and a list of cells to flip. 
        Else, return False and an empty list.
        @i_row: The 0-based row of a tile placement
        @i_col: The 0-based col of a tile placement
        type i_row: int 
        type i_col: int
        return: A tuple whose first component is a boolean indicating
                if the given tile placment is valid and whose second
                component is a list of cells to flip as a result of
                the tile placement
        rtype: (bool, [])
        """
        if not self._empty_cell(i_row, i_col):
            return (False, [])
        adj_opp_cells = []

        if (i_row, i_col) == self._tl_cell:
            self._handle_border(i_row, i_col, adj_opp_cells, self._check_ls_corners, "tl")
        elif (i_row, i_col) == self._tr_cell:
            self._handle_border(i_row, i_col, adj_opp_cells, self._check_rs_corners, "tr")
        elif (i_row, i_col) == self._bl_cell:
            self._handle_border(i_row, i_col, adj_opp_cells, self._check_ls_corners, "bl")
        elif (i_row, i_col) == self._br_cell:
            self._handle_border(i_row, i_col, adj_opp_cells, self._check_rs_corners, "br")
        elif (i_row, i_col) in self._ls_cells:
            self._handle_border(i_row, i_col, adj_opp_cells, self._check_ls_and_rs, "ls")
        elif (i_row, i_col) in self._ts_cells:
            self._handle_border(i_row, i_col, adj_opp_cells, self._check_ts_and_bs, "ts")
        elif (i_row, i_col) in self._rs_cells:
            self._handle_border(i_row, i_col, adj_opp_cells, self._check_ls_and_rs, "rs")
        elif (i_row, i_col) in self._bs_cells:
            self._handle_border(i_row, i_col, adj_opp_cells, self._check_ts_and_bs, "bs")
        else:
            self._check_inner_dirs(i_row, i_col, adj_opp_cells)

        #print("\nFOR TESTING. adj_opp_cells: ", adj_opp_cells)

        if adj_opp_cells == []:
            return (False, [])
        else:
            can_place, flip_lst = self._flip_dirs(adj_opp_cells)
            return (can_place, flip_lst)


    def _flip_dirs(self, adj_opp_cells):
        """
        Determines the direction to consider flips for
        each cell in the given dj_opp_cells list.
        @adj_opp_cells: A list of cells that are adjacent
                        and opposite in color to some piece
        type adj_opp_cells: [tuple]
        return: A tuple whose first component is a boolean indicating
                if the given tile placment is valid and whose second
                component is a list of cells to flip as a result of
                the tile placement
        rtype: (bool, [])
        """
        lst = []
        for cell in adj_opp_cells:
            lst.append(self._label_flips(cell[0], cell[1], cell[2]))

        #print("FOR TESTING: lst: ", lst) #FOR TESTING
        lst2 = []
        for e in lst: #lst has elements of the form (boolean, list)
            if e[0] == True:
                lst2.append(e)

        if lst2 == []:
            return (False, lst2)
        else:
            lst3 = []
            for e in lst2:
                for t in e[1]:
                    lst3.append(t)
            return (True, lst3)


    def _label_flips(self, i_row, i_col, direction):
        """
        Considers tiles to be potentially flipped given a direction.
        Returns True and a list of cells to flip if the flip sequence
        is valid. Else, returns False and and empty list.
        @i_row: The 0-based row of a tile placement
        @i_col: The 0-based col of a tile placement
        @direction: The direction in which to carry out
                    tile flips ("n", "ne", "e", "se", "s",
                    "sw", "w", "nw")
        type i_row: int 
        type i_col: int
        type direction: str
        return: A tuple whose first component is a boolean indicating
                if the given tile placment is valid and whose second
                component is a list of cells to flip as a result of
                the tile placement
        rtype: (bool, [])
        """
        vert_move, hori_move = i_row, i_col  #Initially start at the opposing cell
        candidates = []

        #Perhaps could have done if 0 > vert_move > num_rows and 0 > hori_move > num_cols instead!
        while ((self._board[vert_move][hori_move] != self._turn) and not  #This can be True in one of two ways! 
               self._is_dead_end(vert_move, hori_move, direction) and     #   think: "W" or " "
               self._board[vert_move][hori_move] != " "):
            candidates.append((vert_move, hori_move))
            if direction == "n":
                vert_move += 1
            elif direction == "ne":
                hori_move -= 1
                vert_move += 1
            elif direction == "e":
                hori_move -= 1
            elif direction == "se":
                hori_move -= 1
                vert_move -= 1
            elif direction == "s":
                vert_move -= 1
            elif direction == "sw":
                hori_move += 1
                vert_move -= 1
            elif direction == "w":
                hori_move += 1
            elif direction == "nw":
                hori_move += 1
                vert_move += 1
        #Watch out, index can go out of range after several iterations
        #of the loop body, not just once you enter the loop!!!

        ending_cell = self._board[vert_move][hori_move] 
        if ending_cell == self._turn: #If the ending cell is same color, then flip can be done.
            return (True, candidates)
        else:
            return (False, [])


    def _set_winner(self):
        """
        Sets the winner of the game. If the game is a
        draw, then the winner is set to NONE.
        return: None
        rtype: None
        """
        b_count = 0
        w_count = 0

        for i_row in range(self._num_rows):
            for i_col in range(self._num_cols):
                if self._board[i_row][i_col] == "B":
                    b_count += 1
                elif self._board[i_row][i_col] == "W":
                    w_count += 1

        if b_count == w_count:
            self._winner = "NONE"
        elif self._how_to_win == ">":
            self._winner = "B" if b_count > w_count else "W"
        elif self._how_to_win == "<":
            self._winner = "B" if b_count < w_count else "W"


    def _valid_move_exists(self):
        """
        Loops through the game board to determine
        if any valid moves exist.
        return: A list of valid moves
        rtype: [tuple]
        """
        lst = []
        for i_row in range(self._num_rows):
            for i_col in range(self._num_cols):
                if self._valid_placement(i_row, i_col)[0]:
                    lst.append((i_row, i_col))

        return lst != []  #If lst != [], then the list has elements -> valid move(s) exist


    def _handle_border(self, i_row, i_col, adj_opp_cells, check_func, loc):
        """
        Checks for opposing tiles adjacent to cells on the border and
        appends these titles to adj_opp_cells.
        @i_row: The 0-based row of a tile placement
        @i_col: The 0-based col of a tile placement
        @adj_opp_cells: A list of cells that are adjacent
                        and opposite in color to some piece
        @check_func: Any one of the helper functions of this Othello
                     object: _check_ls_corners, _check_rs_corners,
                             _check_ls_and_rs, _check_ts_and_bs
        @loc: A border location (top-side, left-side, right-side, bottom-side)
        type i_row: int
        type i_col: int
        type adj_opp_cells: [tuple]
        type check_func: function
        type loc: str
        return: None
        rtype: None
        """
        check_func(i_row, i_col, adj_opp_cells, loc)
        #check_func will be any of the five functions listed below


    def _check_ls_corners(self, i_row, i_col, adj_opp_cells, loc):
        """
        Checks for opposing tiles adjacent to the left side
        corners (top left and bottom left) of the game board.
        Appends the corresponding cells to adj_opp_cells.
        @i_row: The 0-based row of a tile placement
        @i_col: The 0-based col of a tile placement
        @adj_opp_cells: A list of cells that are adjacent
                        and opposite in color to some piece
        @loc: A border location (tl, tr, bl, br, ts, bs)
        type i_row: int
        type i_col: int
        type adj_opp_cells: [tuple]
        type loc: str
        return: None
        rtype: None
        """
        shift = 1 if loc == "tl" else -1  #either top-left or bottom-left
        opp_player = "B" if self._turn == "W" else "W"

        #Note that loc corresponds to the position of the tile to be placed.
        #Also, the indices correspond to an adjacent opposing cell to be considered.
        #The compass direction corresponds to the direction in which the adjacent opposing
        #cell will be "entered" by the tile to be placed.
        if self._board[i_row+shift][i_col] == opp_player:   #up/down
            if loc == "tl":
                adj_opp_cells.append((i_row+shift, i_col, "n"))
            elif loc == "bl":
                adj_opp_cells.append((i_row+shift, i_col, "s")) 
        if self._board[i_row+shift][i_col+1] == opp_player: #down-diag/up-diag
            if loc == "tl":
                adj_opp_cells.append((i_row+shift, i_col+1, "nw")) 
            elif loc == "bl":
                adj_opp_cells.append((i_row+shift, i_col+1, "sw")) 
        if self._board[i_row][i_col+1] == opp_player:       #right
            adj_opp_cells.append((i_row, i_col+1, "w"))
            

    def _check_rs_corners(self, i_row, i_col, adj_opp_cells, loc):
        """
        Checks for opposing tiles adjacent to the right side
        corners (top right and bottom right) of the game board.
        Appends the corresponding cells to adj_opp_cells.
        @i_row: The 0-based row of a tile placement
        @i_col: The 0-based col of a tile placement
        @adj_opp_cells: A list of cells that are adjacent
                        and opposite in color to some piece
        @loc: A border location (tl, tr, bl, br, ts, bs)
        type i_row: int
        type i_col: int
        type adj_opp_cells: [tuple]
        type loc: str
        return: None
        rtype: None
        """
        shift = 1 if loc == "tr" else -1  #either top-right or bottom-right
        opp_player = "B" if self._turn == "W" else "W"
        
        if self._board[i_row][i_col-1] == opp_player:       #left
            adj_opp_cells.append((i_row, i_col-1, "e"))
        if self._board[i_row+shift][i_col-1] == opp_player: #up-diag/down-diag
            if loc == "tr":
                adj_opp_cells.append((i_row+shift, i_col-1, "ne"))
            elif loc == "br":
                adj_opp_cells.append((i_row+shift, i_col-1, "se"))
        if self._board[i_row+shift][i_col] == opp_player:   #up/down
            if loc == "tr":
                adj_opp_cells.append((i_row+shift, i_col, "n"))
            elif loc == "br":
                adj_opp_cells.append((i_row+shift, i_col, "s"))


    def _check_ls_and_rs(self, i_row, i_col, adj_opp_cells, loc):
        """
        Checks for opposing tiles adjacent to the left and right
        side borders of the game board. Appends the corresponding
        cell to adj_opp_cells.
        @i_row: The 0-based row of a tile placement
        @i_col: The 0-based col of a tile placement
        @adj_opp_cells: A list of cells that are adjacent
                        and opposite in color to some piece
        @loc: A border location (tl, tr, bl, br, ts, bs)
        type i_row: int
        type i_col: int
        type adj_opp_cells: [tuple]
        type loc: str
        return: None
        rtype: None
        """
        shift = 1 if loc == "ls" else -1  #either left side or right side
        opp_player = "B" if self._turn == "W" else "W"

        if self._board[i_row-1][i_col] == opp_player:        #up
            adj_opp_cells.append((i_row-1, i_col, "s"))
        if self._board[i_row-1][i_col+shift] == opp_player:  #up-diag
            if loc == "ls":
                adj_opp_cells.append((i_row-1, i_col+shift, "sw"))
            elif loc == "rs":
                adj_opp_cells.append((i_row-1, i_col+shift, "se"))
        if self._board[i_row][i_col+shift] == opp_player:    #right
            if loc == "ls":
                adj_opp_cells.append((i_row, i_col+shift, "w"))
            elif loc == "rs":
                adj_opp_cells.append((i_row, i_col+shift, "e"))
        if self._board[i_row+1][i_col+shift] == opp_player:  #down-diag
            if loc == "ls":
                adj_opp_cells.append((i_row+1, i_col+shift, "nw"))
            elif loc == "rs":
                adj_opp_cells.append((i_row+1, i_col+shift, "ne"))
        if self._board[i_row+1][i_col] == opp_player:        #down
            adj_opp_cells.append((i_row+1, i_col, "n"))


    def _check_ts_and_bs(self, i_row, i_col, adj_opp_cells, loc):
        """
        Checks for opposing tiles adjacent to the top and bottom side
        borders of the game board. Appends the corresponding cells to
        adj_opp_cells.
        @i_row: The 0-based row of a tile placement
        @i_col: The 0-based col of a tile placement
        @adj_opp_cells: A list of cells that are adjacent
                        and opposite in color to some piece
        @loc: A border location (tl, tr, bl, br, ts, bs)
        type i_row: int
        type i_col: int
        type adj_opp_cells: [tuple]
        type loc: str
        return: None
        rtype: None
        """
        shift = 1 if loc == "ts" else -1  #Either top side or bottom side
        opp_player = "B" if self._turn == "W" else "W"
        
        if self._board[i_row][i_col-1] == opp_player:        #left
            adj_opp_cells.append((i_row, i_col-1, "e"))        
        if self._board[i_row+shift][i_col-1] == opp_player:  #left-diag
            if loc == "ts":
                adj_opp_cells.append((i_row+shift, i_col-1, "ne"))
            elif loc == "bs":
                adj_opp_cells.append((i_row+shift, i_col-1, "se"))
        if self._board[i_row+shift][i_col] == opp_player:    #up/down
            if loc == "ts":
                adj_opp_cells.append((i_row+shift, i_col, "n"))
            elif loc == "bs":
                adj_opp_cells.append((i_row+shift, i_col, "s"))
        if self._board[i_row+shift][i_col+1] == opp_player:  #right-diag
            if loc == "ts":
                adj_opp_cells.append((i_row+shift, i_col+1, "nw"))
            elif loc == "bs":
                adj_opp_cells.append((i_row+shift, i_col+1, "sw"))
        if self._board[i_row][i_col+1] == opp_player:        #right
            adj_opp_cells.append((i_row, i_col+1, "w"))

            
    def _check_inner_dirs(self, i_row, i_col, adj_opp_cells):
        """
        Checks for opposing tiles adjacent to the inner cells of the
        game board and appends these cells to adj_opp_cells.
        @i_row: The 0-based row of a tile placement
        @i_col: The 0-based col of a tile placement
        @adj_opp_cells: A list of cells that are adjacent
                        and opposite in color to some piece
        type i_row: int
        type i_col: int
        type adj_opp_cells: [tuple]
        return: None
        rtype: None
        """
        opp_player = "B" if self._turn == "W" else "W"
        
        if self._board[i_row-1][i_col] == opp_player:      #north, tile to be placed will enter from the south
            adj_opp_cells.append((i_row-1, i_col, "s")) 
        if self._board[i_row-1][i_col+1] == opp_player:    #northeast, tile to be placed will enter from the sw
            adj_opp_cells.append((i_row-1, i_col+1, "sw"))
        if self._board[i_row][i_col+1] == opp_player:      #east, tile to be placed will enter from the west
            adj_opp_cells.append((i_row, i_col+1, "w"))
        if self._board[i_row+1][i_col+1] == opp_player:    #southeast, tile to be placed will enter from the nw
            adj_opp_cells.append((i_row+1, i_col+1, "nw"))
        if self._board[i_row+1][i_col] == opp_player:      #south, tile to be placed will enter from the north
            adj_opp_cells.append((i_row+1, i_col, "n"))
        if self._board[i_row+1][i_col-1] == opp_player:    #southwest, tile to be placed will enter from the ne
            adj_opp_cells.append((i_row+1, i_col-1, "ne"))
        if self._board[i_row][i_col-1] == opp_player:      #west, tile to be placed will enter from the east.
            adj_opp_cells.append((i_row, i_col-1, "e"))
        if self._board[i_row-1][i_col-1] == opp_player:    #northwest, tile to be placed will enter from the se.
            adj_opp_cells.append((i_row-1, i_col-1, "se"))


    #Instead of this _is_dead_end function, couldn't I have just
    #checked if i_row > num_rows, i_row < num_rows, i_col > num_cols,
    #or i_col < num_cols? Hmmm.        
    def _is_dead_end(self, i_row, i_col, direction):
        """
        Determines if the provided row and column is a dead-end.
        @i_row: The 0-based row of a tile placement
        @i_col: The 0-based col of a tile placement
        @direction: The direction in which to carry out
                    tile flips ("n", "ne", "e", "se", "s",
                    "sw", "w", "nw")
        type i_row: int
        type i_col: int
        type direction: str
        return: True if the provided row and column is
                a dead-end or False otherwise.
        rtype: bool
        """
        return (((i_row, i_col) in self._ts_cells and direction == "s") or
                ((i_row, i_col) in self._ts_cells and direction == "se") or
                ((i_row, i_col) in self._ts_cells and direction == "sw") or
                ((i_row, i_col) in self._ls_cells and direction == "e") or
                ((i_row, i_col) in self._ls_cells and direction == "ne") or
                ((i_row, i_col) in self._ls_cells and direction == "se") or
                ((i_row, i_col) in self._bs_cells and direction == "n") or
                ((i_row, i_col) in self._bs_cells and direction == "nw") or
                ((i_row, i_col) in self._bs_cells and direction == "ne") or
                ((i_row, i_col) in self._rs_cells and direction == "w") or
                ((i_row, i_col) in self._rs_cells and direction == "nw") or
                ((i_row, i_col) in self._rs_cells and direction == "sw") or
                ((i_row, i_col) == self._tl_cell and direction == "s") or
                ((i_row, i_col) == self._tl_cell and direction == "se") or
                ((i_row, i_col) == self._tl_cell and direction == "e") or
                ((i_row, i_col) == self._bl_cell and direction == "n") or
                ((i_row, i_col) == self._bl_cell and direction == "ne") or
                ((i_row, i_col) == self._bl_cell and direction == "e") or
                ((i_row, i_col) == self._tr_cell and direction == "w") or
                ((i_row, i_col) == self._tr_cell and direction == "sw") or
                ((i_row, i_col) == self._tr_cell and direction == "s") or
                ((i_row, i_col) == self._br_cell and direction == "w") or
                ((i_row, i_col) == self._br_cell and direction == "nw") or
                ((i_row, i_col) == self._br_cell and direction == "n"))

                
    def _cell_in_boundary(self, i_row, i_col):
        """
        Determines if a given cell is inside of the board's boundaries.
        @i_row: The 0-based row of a tile placement
        @i_col: The 0-based col of a tile placement
        type i_row: int
        type i_col: int
        return: True if the provided row and column is
                a boundary or False otherwise.
        rtype: bool
        """
        return ((i_row, i_col) == self._tl_cell or
                (i_row, i_col) == self._tr_cell or
                (i_row, i_col) == self._bl_cell or
                (i_row, i_col) == self._br_cell or
                (i_row, i_col) in self._ls_cells or
                (i_row, i_col) in self._rs_cells or
                (i_row, i_col) in self._ts_cells or
                (i_row, i_col) in self._bs_cells)


    def _empty_cell(self, i_row, i_col):
        """
        Determines if a given cell is empty.
        @i_row: The 0-based row of a tile placement
        @i_col: The 0-based col of a tile placement
        type i_row: int
        type i_col: int
        return: True if the provided row and column is
                empty or False otherwise.
        rtype: bool
        """
        return self._board[i_row][i_col] == " "


    def _switch_turn(self, cur_player):
        """
        Switches the player turn in an Othello game.
        @cur_player: The current player ("B" or "W")
        return: The opposite color of the current player
        rtype: str
        """
        if cur_player == "W":
            self._turn = "B"
        else:
            self._turn = "W"
            

    def _make_board(self, rows, cols, top_left):
        """
        Constructs a 2D list representation of an Othello game.
        @rows: The number of rows for this Othello game
        @cols: The number of columns for this Othello game
        @top_left: The top-left player in the initial center
                   four-piece layout of this Othello game
        type rows: int
        type cols: int
        type top_left: str 
        return: A 2D list representation of this Othello game
        rtype: list
        """
        board = []
        for i in range(rows):
            board.append([])
            for j in range(cols):
                board[-1].append(" ")

        top_left_row = math.floor(self._num_rows/2)
        top_left_col = math.floor(self._num_cols/2)
        if top_left == "B":
            board[top_left_row-1][top_left_col-1] = top_left
            board[top_left_row-1][top_left_col+1-1] = "W"  
            board[top_left_row+1-1][top_left_col-1] = "W" 
            board[top_left_row+1-1][top_left_col+1-1] = "B" 
        elif top_left == "W":
            board[top_left_row-1][top_left_col-1] = top_left 
            board[top_left_row-1][top_left_col+1-1] = "B"    
            board[top_left_row+1-1][top_left_col-1] = "B"  
            board[top_left_row+1-1][top_left_col+1-1] = "W"

        return board


    def print_board(self):
        """
        Prints the game board of an Othello game.
        This is a useful method for testing.
        return: None
        rtype: None
        """
        for i_row in range(self._num_rows):
            print()
            for i_col in range(self._num_cols):
                if self._board[i_row][i_col] != " ":
                    print(self._board[i_row][i_col], end = " ")
                else:
                    print(".", end = " ")
        print()

