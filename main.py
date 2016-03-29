#The entry point for the Othello GUI application

import othellogui
import othellomenu

if __name__ == "__main__":
    play_again = False
    menu = othellomenu.OthelloMenu()
    menu.show() #Main loop for the menu kicks in here.

    if menu.was_ok_clicked():
    #Clicking ok should destroy the menu's tkinter window (the tkinter window is destroyed but the menu object isn't)
        while True:
            if play_again:
                menu = othellomenu.OthelloMenu()
                menu.show()
                
            if menu.was_ok_clicked():
                #Instantiate an othello game with the settings given in the menu window.
                app = othellogui.OthelloGUI(menu.get_num_rows(), menu.get_num_cols(),
                             menu.get_player_color(), menu.get_cpu_opp(), menu.get_starter(),
                             menu.get_top_left_player(), menu.get_win_method())
                app.start() #Main loop for the othello game kicks in here.

                if app.did_game_end(): #Control goes to here when game is no longer active.
                    play_again_window = othellomenu.PlayAgain()
                    play_again_window.show()
                    if play_again_window.will_play_again(): #Yes was pressed...
                        play_again = True
                    else: #Else, no was pressed (play_again_window would be destroyed)...
                        break
                else: #Control goes to here if the X button was pressed on the game window.
                    break
            else: #For when cancel is pressed after deciding to play again...
                break
