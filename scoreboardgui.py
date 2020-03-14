#Contains the class for the scoreboard GUI.
import tkinter
import othello

class ScoreBoardGUI(tkinter.Frame):
    
    def __init__(self, root, gamestate, *args, **kwargs):
        """
        Initializes the state of a ScoreBoardGUI object.
        @root: The root window of the GUI
        @gamestate: The game state of an othello game
                    represented by a 2-D list.
        type root: tkinter.Tk
        type gamestate: list
        *args: Arbitary count of positional arguments
        **args: Arbitary count of keyword arguments
        return: None
        rtype: None
        """
        tkinter.Frame.__init__(self, root, *args, **kwargs)

        #Note how the master of all these labels is self -- i.e., the Frame itSELF.
        #In the act of extending, we're essentially adding stuff onto a Frame.

        self._turn_text = tkinter.StringVar()
        self._turn_text.set("{}'s turn to move".format("BLACK" if gamestate.get_turn()=="B" else "WHITE"))
        self._turn_indicator = tkinter.Label(master=self,
                                    textvariable=self._turn_text,
                                    background="gray", font="Arial 15 bold")
        self._turn_indicator.pack(side=tkinter.TOP)

        self._black_score_text = tkinter.StringVar()
        self._black_score_text.set("Black Score: {}".format(gamestate.get_counts()[0]))
        self._black_score = tkinter.Label(master=self, textvariable=self._black_score_text, background="gray")
        self._black_score.pack()

        self._white_score_text = tkinter.StringVar()
        self._white_score_text.set("White Score: {}".format(gamestate.get_counts()[1]))
        self._white_score = tkinter.Label(master=self, textvariable=self._white_score_text, background="gray")
        self._white_score.pack(side=tkinter.BOTTOM)

        
    def update_turn_label(self, gamestate):
        """
        Updates the label indicating whose turn it is.
        @gamestate: The game state of an othello game
                    represented by a 2-D list.
        type gamestate: list
        return: None
        rtype: None
        """
        self._turn_text.set("{}'s turn to move".format("BLACK" if gamestate.get_turn()=="B" else "WHITE"))


    def update_score_label(self, gamestate):
        """
        Updates the label indicating the scores.
        @gamestate: The game state of an othello game
                    represented by a 2-D list.
        type gamestate: list
        return: None
        rtype: None
        """
        self._black_score_text.set("Black Score: {}".format(gamestate.get_counts()[0]))
        self._white_score_text.set("White Score: {}".format(gamestate.get_counts()[1]))


    def indicate_invalid(self, gamestate):
        """
        Creates a label to notify the player of an invalid move.
        @gamestate: The game state of an othello game
                    represented by a 2-D list.
        type gamestate: list
        return: None
        rtype: None
        """
        self._turn_text.set("{}'s move invalid. Try again.".format\
                            ("BLACK" if gamestate.get_turn()=="B" else "WHITE"))


    def indicate_result(self, gamestate):
        """
        Creates a label to show the results of a completed game.
        @gamestate: The game state of an othello game
                    represented by a 2-D list.
        type gamestate: list
        return: None
        rtype: None
        """
        if gamestate.get_winner() != "NONE":
            self._turn_text.set("GAME OVER! The winner is {}".format\
                            ("BLACK" if gamestate.get_winner()=="B" else "WHITE"))
        else:
            self._turn_text.set("GAME OVER! The game is a draw")
        self.update_score_label(gamestate)

        
