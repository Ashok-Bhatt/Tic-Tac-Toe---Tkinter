from tkinter import *
from gameboard import GameBoard


class gameMode(Tk):
    
    WINDOW_HEIGHT = 300
    WINDOW_WIDTH = 300


    def __init__(self) -> None:
        super().__init__()
        self.createGameModeSelectionWindow()


    def createGameModeSelectionWindow(self):
        X_MARGIN = (self.winfo_screenwidth() - self.WINDOW_WIDTH)//2
        Y_MARGIN = (self.winfo_screenheight() - self.WINDOW_HEIGHT)//2
        self.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+{X_MARGIN}+{Y_MARGIN}")

        label = Label(self, text="Choose Game Mode", font=("Helvetica", 16))
        label.pack(pady=20)

        button_frame = Frame(self)
        button_frame.pack(expand=True)

        vs_ai_button = Button(button_frame, text="Versus AI", font=("Helvetica", 14), width=15, command = lambda:self.start_game(0))
        vs_ai_button.pack(pady=10)

        multiplayer_button = Button(button_frame, text="Multiplayer", font=("Helvetica", 14), width=15, command = lambda:self.start_game((1)))
        multiplayer_button.pack(pady=10)


    def start_game(self, mode):
        self.destroy()
        gb = GameBoard(mode)
        gb.mainloop()