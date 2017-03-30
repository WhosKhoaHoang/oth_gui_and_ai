#Contains classes that represent pop-up menu items.

import tkinter
import othello
import math


class OthelloMenu(): #Watch out! There's already a class called Menu in the tkinter library
    '''Represents the menu that pops up before a game'''
    
    def __init__(self):
        '''Initializes the state of an Othello game menu.'''
        self._menu_window = tkinter.Tk() #The root window
        self._menu_window.wm_title("Othello Menu")
        self._menu_window.resizable(0,0)
        self._menu_window.geometry('+550+115') #For positioning the window on the screen


        #PROTIP: If you wanna actually see the Frame, you gotta put stuff in it!!!

        #***DIMENSIONS FRAME***
        self._dimension_frame = tkinter.Frame(master=self._menu_window, relief=tkinter.RAISED,
                                              borderwidth=5, background="gray")
        self._dimension_frame.grid(row=0, column=0, sticky=tkinter.N+tkinter.E+tkinter.S+tkinter.W)
        
        
        #NUM_ROWS LABEL
        self._num_rows_text = tkinter.StringVar()
        self._num_rows_text.set("Number of rows:")
        num_rows_label = tkinter.Label(
            master=self._dimension_frame, textvariable=self._num_rows_text, font="arial 15 bold",
            background="gray")
        num_rows_label.grid(row=0, column=0, padx=10, pady=(20,10))
        #NUM_ROWS ENTRY...If I turn this into a option menu, I could probably get rid of some stuff in _on_button_click
        '''
        self._num_rows_entry = tkinter.Entry(
            master=self._dimension_frame, width=20)
        self._num_rows_entry.insert(0, "4")
        self._num_rows_entry.grid(row=0, column=1, padx=10, pady=10,
                                    sticky=tkinter.W+tkinter.E)
        '''
        
        self._num_rows = tkinter.IntVar() 
        self._num_rows.set(4) #why am I getting 0?! I think OptionsMenus contents can only work with strings...
        self._num_rows_menu = tkinter.OptionMenu(self._dimension_frame, self._num_rows,
                                                 4, 6, 8, 10, 12, 14, 16)
        self._num_rows_menu.grid(row=0, column=1, padx=10, pady=2,
                                 sticky=tkinter.W+tkinter.E)


        
        #NUM_COLS LABEL
        self._num_cols_text = tkinter.StringVar()
        self._num_cols_text.set("Number of columns:")
        num_cols_label = tkinter.Label(
            master=self._dimension_frame, textvariable=self._num_cols_text, font="arial 15 bold",
            background="gray")
        num_cols_label.grid(row=1, column=0, padx=10, pady=10)
        #NUM_COLS ENTRY
        '''
        self._num_cols_entry = tkinter.Entry(
            master=self._dimension_frame, width=20)
        self._num_cols_entry.insert(0, "4")
        self._num_cols_entry.grid(row=1, column=1, padx=10, pady=1,
                                  sticky=tkinter.W+tkinter.E)
        '''

        self._num_cols = tkinter.IntVar()
        self._num_cols.set(4)
        self._num_cols_menu = tkinter.OptionMenu(self._dimension_frame, self._num_cols,
                                                 4, 6, 8, 10, 12, 14, 16)
        self._num_cols_menu.grid(row=1, column=1, padx=10, pady=2,
                                 sticky=tkinter.W+tkinter.E)


        #***SELECT COLOR FRAME***
        self._select_color_frame = tkinter.Frame(master=self._menu_window, relief=tkinter.RAISED,
                                                 borderwidth=5, background="gray")
        self._select_color_frame.grid(row=1, column=0,
                                      sticky=tkinter.N+tkinter.E+tkinter.S+tkinter.W)

        #SELECT COLOR LABEL
        self._select_color_label = tkinter.Label(
            master=self._select_color_frame,
            text="Select your color:",
            font="arial 15 bold", background="gray")
        self._select_color_label.grid(row=0, column=0, padx=10, pady=10)

        #BLACK COLOR RADIO BUTTON
        self._player_color = tkinter.StringVar()
        self._player_color.set("B")
        self._black_color = tkinter.Radiobutton(master=self._select_color_frame, text="Black", value="B",
                                                variable=self._player_color, background="gray", font="arial 15")
        self._black_color.grid(row=1,column=0, sticky=tkinter.W, padx=(10,0))

        #WHITE COLOR RADIO BUTTON
        self._white_color = tkinter.Radiobutton(master=self._select_color_frame, text="White", value="W",
                                                variable=self._player_color, background="gray", font="arial 15")
        self._white_color.grid(row=2, column=0, sticky=tkinter.W, padx=(10,0), pady=(0,15))



        #***SELECT OPPONENT FRAME***
        self._select_opp_frame = tkinter.Frame(master=self._menu_window, relief=tkinter.RAISED,
                                               borderwidth=5, background="gray")
        self._select_opp_frame.grid(row=2, column=0,
                                    sticky=tkinter.N+tkinter.E+tkinter.S+tkinter.W)
        self._select_opp_label = tkinter.Label(master=self._select_opp_frame, text="Select CPU opponent:",
                                               font="arial 15 bold", background="gray")
        self._select_opp_label.grid(row=0, column=0, padx=10, pady=10)
        self._cpu_opp = tkinter.StringVar()
        self._cpu_opp.set("Greedy Gary")
        self._opp_menu = tkinter.OptionMenu(self._select_opp_frame, self._cpu_opp,
                                            "Greedy Gary", "Mini Max", "None") #No command option needed. tkinter sees who you selected automatically.
        self._opp_menu.grid(row=0, column=1, padx=10, pady=10)


        
        #***STARTER FRAME***
        #Perhaps it's pointless to specify the dimensions of the Frame since it'll only be as
        #big as its largest widget...
        self._starter_frame = tkinter.Frame(master=self._menu_window, relief=tkinter.RAISED,
                                            borderwidth=5, background="gray")
        self._starter_frame.grid(row=3, column=0,
                                 sticky=tkinter.N+tkinter.E+tkinter.S+tkinter.W)


        #STARTER LABEL
        self._num_rows_label = tkinter.Label(
            master=self._starter_frame, text="Player to make the first move:",
            font="arial 15 bold", background="gray")
        self._num_rows_label.grid(row=0, column=0, padx=10, pady=10)

        #BLACK_START RADIO BUTTON
        self._starter = tkinter.StringVar() #Control variable for the starting player
        self._starter.set("B") #Initialize the value to 1 (the first choice)
        self._black_start = tkinter.Radiobutton(master=self._starter_frame, text="Black", value="B",
                                                variable=self._starter,
                                                background="gray", font="arial 15")
        #Think of the value option as an index value in the category of buttons specified by variable
        self._black_start.grid(row=1,column=0, sticky=tkinter.W, padx=(10,0))
        #WHITE_START RADIO BUTTON
        self._white_start = tkinter.Radiobutton(master=self._starter_frame, text="White", value="W",
                                                variable=self._starter,
                                                background="gray", font="arial 15")
        self._white_start.grid(row=2,column=0, sticky=tkinter.W, padx=(10,0), pady=(0,15))




        #***TOP LEFT PLAYER FRAME***
        self._tlp_frame = tkinter.Frame(master=self._menu_window, relief=tkinter.RAISED,
                                            borderwidth=5, background="gray")
        self._tlp_frame.grid(row=4, column=0,
                             sticky=tkinter.N+tkinter.E+tkinter.S+tkinter.W)


        #TOP_LEFT_PLAYER LABEL
        self._tlp_label = tkinter.Label(
            master=self._tlp_frame, text="Player to be positioned in the top left center square:",
            background="gray", font="arial 15 bold")
        self._tlp_label.grid(row=0, column=0, padx=10, pady=10,
                             sticky=tkinter.N+tkinter.E+tkinter.S+tkinter.W)

        #BLACK_TLP RADIO BUTTON
        self._tlp = tkinter.StringVar()
        self._tlp.set("B")
        self._black_tlp = tkinter.Radiobutton(master=self._tlp_frame, text="Black", value="B", variable=self._tlp,
                                              background="gray")
        self._black_tlp.grid(row=1,column=0, sticky=tkinter.W, padx=(10,0))
        #WHITE_TLP RADIO BUTTON
        self._white_tlp = tkinter.Radiobutton(master=self._tlp_frame, text="White", value="W", variable=self._tlp,
                                              background="gray")
        self._white_tlp.grid(row=2,column=0, sticky=tkinter.W, padx=(10,0), pady=(0,15))


        
        #***WIN METHOD FRAME***
        self._win_method_frame = tkinter.Frame(master=self._menu_window, relief=tkinter.RAISED,
                                               borderwidth=5, background="gray")
        self._win_method_frame.grid(row=5, column=0,
                                    sticky=tkinter.N+tkinter.E+tkinter.S+tkinter.W)


        #WIN_METHOD LABEL
        self._win_method_label = tkinter.Label(
            master=self._win_method_frame, text="Select a victory method:", background="gray", font="arial 15 bold")
        self._win_method_label.grid(row=0, column=0, padx=10, pady=10)

        #MOST TILES RADIO BUTTON
        self._win_method = tkinter.StringVar()
        self._win_method.set(">")
        self._most_tiles = tkinter.Radiobutton(master=self._win_method_frame, text="Player with most tiles wins",
                                               value=">", variable=self._win_method, background="gray", font="arial 15")
        self._most_tiles.grid(row=1, column=0, sticky=tkinter.W, padx=(10,0))
        #LEAST TILES RADIO BUTTON
        self._least_tiles = tkinter.Radiobutton(master=self._win_method_frame, text="Player with least tiles wins",
                                                value="<", variable=self._win_method, background="gray", font="arial 15")
        self._least_tiles.grid(row=2, column=0, sticky=tkinter.W, padx=(10,0), pady=(0,15))



        #OK BUTTON (gridded onto WIN_METHOD frame)
        ok_button=tkinter.Button(
            master=self._win_method_frame, text="OK",
            command=self._on_ok_button, background="gray")
        ok_button.grid(row=3, column=0, padx=10, pady=(25,15))
        
        cancel_button=tkinter.Button(
            master=self._win_method_frame, text="CANCEL",
            command=self._on_cancel_button, background="gray")
        cancel_button.grid(row=3, column=1, padx=5, pady=(25,15))

        #self._num_rows = 0
        #self._num_cols = 0
        self._ok_button_clicked = False
        #Should I have _cancel_button_clicked?
        self._cancel_button_clicked = False
        

    def show(self):
        '''Runs the main loop on the root window.'''
        #self._menu_window.grab_set()
        #self._menu_window.wait_window()
        self._menu_window.mainloop()
        

    def get_num_rows(self)->int:
        '''Gets the number of rows set for a game.'''
        return self._num_rows.get()


    def get_num_cols(self)->int:
        '''Gets the number of columns set for a game.'''
        return self._num_cols.get()


    def get_player_color(self)->str:
        '''Gets the player color set for a game.'''
        return self._player_color.get() #Must call get() on a control variable to get the value!!!


    def get_cpu_opp(self)->str:
        '''Gets the cpu color set for a game.'''
        return self._cpu_opp.get() #Must call get() on a control variable to get the value!!!
    

    def get_starter(self)->str:
        '''Gets the starting player set for a game.'''
        return self._starter.get() #Must call get() on a control variable to get the value!!!


    def get_top_left_player(self)->str:
        '''Gets the top-left player set for a game.'''
        return self._tlp.get()


    def get_win_method(self)->str:
        '''Gets the win method set for a game.'''
        return self._win_method.get()


    def _on_ok_button(self):
        '''Handles the event of the OK button being pressed.'''
        '''
        #Instead of checking for valid input, you can just force the player to input correct values by
        #providing a drop-down menu of values.
        num_rows = int(self._num_rows_entry.get())
        num_cols = int(self._num_cols_entry.get())
        valid_entry = True
        
        if (4 > num_rows > 16) or num_rows % 2 != 0:
            valid_entry = False
            self._num_rows_text.set("Number of rows must be an\neven integer between 4 and 16!")
        if (4 > num_cols > 16) or num_cols % 2 != 0:
            valid_entry = False
            self._num_cols_text.set("Number of columns must be an\neven integer between 4 and 16!")

        if valid_entry:
            self._ok_button_clicked = True
            self._num_rows = int(self._num_rows_entry.get())
            self._num_cols = int(self._num_cols_entry.get())
            #Note how I don't need to set the variables associated with the radio
            #buttons since those would be done automatically in the GUI

            self._menu_window.destroy() #The window will go away but the Menu object will still remain for as
                                         #long as the program is running.
         '''
        self._ok_button_clicked = True

        #FOR TESTING
        #self._menu_window.withdraw()
        #self._menu_window.quit()
        
        self._menu_window.destroy()


    def _on_cancel_button(self):
        '''Handles the event of the Cancel button being pressed.'''
        #self._cancel_button_clicked = True
        #print(self._cancel_button_clicked)
        self._menu_window.destroy()
        

    def was_ok_clicked(self):
        '''Determines if the OK button was pressed'''
        return self._ok_button_clicked



class PlayAgain:
    '''A class to represent the pop-up that asks the user if they would like to play again.'''

    def __init__(self):
        '''Initializes the state of a "play-again" pop-up menu.'''
        self._dialog_window = tkinter.Tk()
        self._dialog_window.configure(background='gray')
        self._dialog_window.wm_title("")
        self._dialog_window.geometry('+700+400')
        self._dialog_window.resizable(0,0)
        self._play_again = True

        main_frame = tkinter.Frame(master=self._dialog_window, background="gray",
                                   borderwidth=3,relief=tkinter.RAISED)
        main_frame.grid(row=0,column=0)

        play_again_label = tkinter.Label(master=main_frame, text="Play again?",
                                   padx=10, pady=10, background="gray", font="arial 15")
        play_again_label.grid(row=0, column=0)

        buttons_frame = tkinter.Frame(master=main_frame, background="gray")
        buttons_frame.grid(row=1,column=0)
        yes_button = tkinter.Button(master=buttons_frame, text="Yes", command=self._on_yes_pressed)
        yes_button.grid(row=0, column=0, padx=(0,5), pady=(0,10), sticky=tkinter.W)
        no_button = tkinter.Button(master=buttons_frame, text="No", command=self._on_no_pressed)
        no_button.grid(row=0, column=1, padx=(5,0), pady=(0,10), sticky=tkinter.E)

    def show(self):
        '''Runs the main loop on the root window.'''
        #self._dialog_window.grab_set()
        #self._dialog_window.wait_window()
        self._dialog_window.mainloop()

    def _on_yes_pressed(self):
        '''Handles the event of the "Yes" button being pressed.'''
        self._dialog_window.destroy()

    def _on_no_pressed(self):
        '''Handles the event of the "No" button bein pressed.'''
        self._play_again = False
        self._dialog_window.destroy()

    def will_play_again(self):
        '''Returns the player's decision to play again or not.'''
        return self._play_again


if __name__ == "__main__":
    m = OthelloMenu()
    #m.show()
    #pa = PlayAgain()

    #Perhaps I can ultimately have a main function that looks something like this:
    #def main():
        #create Menu object
        #pass data in Menu object to BoardGUI
        #run the BoardGUI
        #Have pop-up at the end of the game asking if user wants to play again
        #Could use a loop for as long as the user says yes...


