#Contains the classes that represent the AIs for the game.

import time
import othello
from collections import defaultdict
import random

#Not so much greedy as much as randomly picking any available move?...Actually, the algorithm will consider
#all of the available moves and pick the one that would yield the best score, hence greediness.
def greedy_cpu(gamestate, cpu_player, move_processor):
    '''Executes a cpu move based on a greedy algorithm.'''
    while gamestate.get_turn() == cpu_player:
        time.sleep(0.5) #To simulate "thinking"
        valid_moves_lst = _cpu_find_moves(gamestate)
        print("Valid Moves List: ", valid_moves_lst) #Note how valid_moves_lst has "user-friendly" move descriptions (non zero-based numbers)
        if valid_moves_lst == []: #If there are no valid moves, then the CPU can't make a move!
            break

        move_dict = defaultdict(list)
        for move in valid_moves_lst:
            dummy_game = othello.Othello(gamestate.get_num_rows(),
                                         gamestate.get_num_cols(),
                                         gamestate.get_turn(),
                                         gamestate.get_top_left(),
                                         gamestate.get_win_method(),
                                         gamestate.get_board())
            dummy_game.valid_move(move[0], move[1]) #Make the move (for sure it will be valid)
            
            points = dummy_game.get_counts()[0] if gamestate.get_turn == "B"\
                                            else dummy_game.get_counts()[1]
            move_dict[points].append(move)
            
            '''
            #Can also use the evaluation function for mini-max rather than the point difference?
            e_value = minimax_eval(dummy_game)
            move_dict[h_value].append(move)
            '''
            
        
        cpu_move = random.choice(move_dict[max(move_dict.keys())])
        #Choose the next move available that will get the cpu the most choice (randomly choose between all moves
        #that would yield the same number of points)

        print("move_dict: ", move_dict)
        print("cpu_move: ", cpu_move)

        move_processor(cpu_move[0], cpu_move[1])



#PROTIP: Mini-max conducts a HEURISTIC SEARCH -- i.e., a search that will return a best guess of what
#  the best move is. It's a "guess" because we don't have a true idea of how good the move really is.
#  That would require going all the way down to an end-game state (i.e., a terminal state) and evaluating
#  that terminal state, but doing that is often practically infeasible.

#Think: ultimately, we want the cpu to return a move, not some evaluation function value. If anything,
#the evaluation function value should guide the cpu towards the best move
def minimax(gamestate, cpu_player, depth): #Removed the move and move_processor parameters
    #Initially (for the very first call), move would probably be None
    '''Executes a cpu move based on a depth-limited minimax algorithm.'''
    best_move = None
    if depth == 0 or gamestate.get_winner() != " ":
        #print("minimax_eval(gamestate, cpu_player): ", minimax_eval(gamestate, cpu_player))
        return (minimax_eval(gamestate, cpu_player), None) #Don't think I need cpu_player
        #Do I even need to return a move? Yes because minimax is ultimately
        #required to return a move for processing.
        #Think: "this is the move associated with the high evaluation function value
    elif gamestate.get_turn() == cpu_player:
        print("MAXIMIZING PLAYER'S TURN")
        #Thought: the CPU is always the maximizing player. Typically, the maximizing player is the (CPU)
        #player who has the current turn.
        best_val = float("-inf")
        #best_move = None #Could be no best move if no moves were ever available...
        valid_moves_lst = _cpu_find_moves(gamestate)

        if valid_moves_lst == []:
            print("*****EMPTY MOVES ALERT!!!*****")

        '''
        if valid_moves_lst == []:
            #Could be possible that when opp player makes a move, current player
            #ends up not having a move available...
            #Maybe won't need this if I return None as best_move (best_move is set to None at the beginning)...
            return (gamestate, move)
        '''
        for move in valid_moves_lst:
            #Perform the move
            dummy_game = othello.Othello(gamestate.get_num_rows(),
                                         gamestate.get_num_cols(),
                                         gamestate.get_turn(),
                                         gamestate.get_top_left(),
                                         gamestate.get_win_method(),
                                         gamestate.get_board())
                                         #^This final argument is what allows the dummy gamestate to take on the board
                                         #configuration of the current gamestate

            #_draw_console_board(dummy_game) #FOR TESTING
            #print("") #FOR TESTING
            dummy_game.valid_move(move[0], move[1])
            (val, move_made) = minimax(dummy_game, cpu_player, depth-1) #Note how move_made isn't used
            #val = minimax(dummy_game, cpu_player, depth-1, move, move_processor)
            if val > best_val: #perhaps i should handle case where it's equal? don't want AI doing same moves all the time.
                best_move = move
                best_val = val

        return (best_val, best_move)
        #I think you should return move itself because you'd want this function to
        #ultimately return a move, don't you?
        #return best_val

    else:
        print("MINIMIZING PLAYER'S TURN")
        #^For minimizing player
        best_val = float("inf")
        #bast_move = None
        valid_moves_lst = _cpu_find_moves(gamestate)

        '''
        if valid_moves_lst == []:
            #Could be possible that when opp player makes a move, current player
            #ends up not having a move available...
            return (gamestate, move)
        '''
        for move in valid_moves_lst:
            #Perform the move
            dummy_game = othello.Othello(gamestate.get_num_rows(),
                                         gamestate.get_num_cols(),
                                         gamestate.get_turn(),
                                         gamestate.get_top_left(),
                                         gamestate.get_win_method(),
                                         gamestate.get_board())

            dummy_game.valid_move(move[0], move[1])
            (val, move_made) = minimax(dummy_game, cpu_player, depth-1)
            if val < best_val:
                best_move = move
                best_val = val

            
        return (best_val, best_move)


#Removed the move and move_processor parameters
def minimax_abp(gamestate, cpu_player, alpha, beta, depth):
    #Initially (for the very first call), move would probably be None
    """
    Executes a cpu move based on a depth-limited
    minimax algorithm with alpha-beta pruning.
    @gamestate: The game state of an Othello game
    @cpu_player: The color of the CPU player ("B" or "W")
    @alpha: The maximum lower bound for an AB-prune
    @beta: The minimum upper bound for an AB-prune
    type gamestate: list
    type cpu_player: str
    type alpha: float
    type beta: float
    return: A tuple containing the best score for an
            evaluated gamestate, the move associated
            with that evaluated gamestate, the alpha
            value, and the beta value.
    """

    print("ALPHA-BETA PRUNING IN EFFECT")
    #Note that the same gamestate object is passed through the
    #minimax game tree and it keeps track of whose turn it is
    #throughout the traversal.

    best_move = None
    if depth == 0 or gamestate.get_winner() != " ":
        #print("minimax_eval(gamestate, cpu_player): ", minimax_eval(gamestate, cpu_player))
        return (minimax_eval(gamestate, cpu_player), None, alpha, beta)
        #. Don't think I actually need cpu_player
        #. Do I even need to return a move? Yes because minimax is ultimately
        #  required to return a move for processing.
        #  Think: "this is the move associated with the high evaluation function value

    if gamestate.get_turn() == cpu_player:
        print("MAXIMIZING PLAYER'S TURN")
        #Note that the root of a minimax game tree corresponds to the maximizing player.
        #Thus, the CPU player is always the maximizing player since minimax is initiated/
        #called on behalf of the CPU player when its their turn.

        best_val = float("-inf")
        #best_move = None #Could be no best move if no moves were ever available...
        valid_moves_lst = _cpu_find_moves(gamestate)

        if valid_moves_lst == []:
            print("*****EMPTY MOVES ALERT!!!*****")

        '''
        if valid_moves_lst == []:
            #Could be possible that when opp player makes a move,
            #current player ends up not having a move available...
            #Maybe won't need this if I return None as best_move
            #(best_move is set to None at the beginning)...
            return (gamestate, move)
        '''
        for move in valid_moves_lst:
            dummy_game = othello.Othello(gamestate.get_num_rows(),
                                         gamestate.get_num_cols(),
                                         gamestate.get_turn(),
                                         gamestate.get_top_left(),
                                         gamestate.get_win_method(),
                                         gamestate.get_board())
                                         #^This final argument is what allows
                                         # the dummy gamestate to take on the board
                                         # configuration of the current gamestate

            #_draw_console_board(dummy_game) #FOR TESTING
            #Perform the move
            dummy_game.valid_move(move[0], move[1])
            (val, move_made, alpha, beta) = minimax_abp(dummy_game, cpu_player,
                                                        alpha, beta, depth-1)
            #Note how move_made isn't used...

            #val = minimax(dummy_game, cpu_player, depth-1, move, move_processor)
            # Perhaps I should also handle case where it's equal? don't want
            # AI doing same moves all the time.
            if val > best_val:
                best_move = move
                best_val = val

            if best_val >= alpha:
                alpha = best_val

            if beta <= alpha:
                break
    else:
        print("MINIMIZING PLAYER'S TURN")
        best_val = float("inf")
        #bast_move = None
        valid_moves_lst = _cpu_find_moves(gamestate)

        '''
        if valid_moves_lst == []:
            #Could be possible that when opp player makes a move,
            #current player ends up not having a move available...
            return (gamestate, move)
        '''
        for move in valid_moves_lst:
            dummy_game = othello.Othello(gamestate.get_num_rows(),
                                         gamestate.get_num_cols(),
                                         gamestate.get_turn(),
                                         gamestate.get_top_left(),
                                         gamestate.get_win_method(),
                                         gamestate.get_board())

            #Perform the move
            dummy_game.valid_move(move[0], move[1])
            (val, move_made, alpha, beta) = minimax_abp(dummy_game, cpu_player,
                                                        alpha, beta, depth-1)
            if val < best_val:
                best_move = move
                best_val = val

            if best_val <= beta:
                alpha = best_val

            if beta <= alpha:
                break


    return (best_val, best_move, alpha, beta)


#Note that we're ultimatrly not just looking at the score to be gained with this evaluation function
def minimax_eval(gamestate, cpu_player):
    #Also say that if the CPU's piece is in the cornrers, then have it contribute a lot to the score?
    #Work something in here like...if the move causes the opponent to not be able to make a move on the
    #next turn, then definitely take it?
    
    score = 0
    score += gamestate.get_counts()[0]-gamestate.get_counts()[1] if cpu_player == "B" else\
           gamestate.get_counts()[1]-gamestate.get_counts()[0]  #Should I associate a heighter "weight" with this?

    #If the move would lead to the CPU getting a corner piece, then heavily consider it
    corners = [gamestate.get_tl_cell(), gamestate.get_tr_cell(),
               gamestate.get_bl_cell(), gamestate.get_br_cell()]
    for row in gamestate.get_board():
        for col in row:
            if col == "cpu_player" and (row, col) in corners:
                score += 10

    return score
    
    '''
    return gamestate.get_counts()[0]-gamestate.get_counts()[1] if cpu_player == "B" else\
           gamestate.get_counts()[1]-gamestate.get_counts()[0]
    '''
    #The maximizing player should be first in the difference expression. This is because the maximizing player
    #would want to have the largest number of pieces on the board (and the minimizing player would want it so that
    #the maximizing player has the fewest pieces on the board)
    
    #Can't I also just return the number of points of the player for which the evaluation function is called?


def _cpu_find_moves(gamestate):
    '''Loops through the gameboard to find valid moves and returns a list of
       those valid moves.'''
    valid_moves_lst = []
    for i_row in range(gamestate.get_num_rows()):
        for i_col in range(gamestate.get_num_rows()):
            if gamestate._valid_placement(i_row, i_col)[0]:
                valid_moves_lst.append((i_row+1, i_col+1))

    return valid_moves_lst



#USED FOR TESTING OUT OTHELLO AI
def _draw_console_board(gamestate):
    for i_row in range(gamestate.get_num_rows()):
        print()
        for i_col in range(gamestate.get_num_cols()):
            if gamestate.get_board()[i_row][i_col] != " ":
                print(gamestate.get_board()[i_row][i_col], end = " ")
            else:
                print(".", end = " ") 
