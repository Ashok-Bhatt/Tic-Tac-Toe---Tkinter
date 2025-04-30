from tkinter import *
from copy import deepcopy
import os


class GameBoard(Tk):
    
    WINNING_STATES = [[[0,0],[1,1],[2,2]],[[0,2],[1,1],[2,0]],
                      [[0,0],[0,1],[0,2]],[[1,0],[1,1],[1,2]],[[2,0],[2,1],[2,2]],
                      [[0,0],[1,0],[2,0]],[[0,1],[1,1],[2,1]],[[0,2],[1,2],[2,2]]]
    WINDOW_HEIGHT = 300
    WINDOW_WIDTH = 300


    def __init__(self, mode) -> None:
        super().__init__()
        self.game_status = [["","",""],["","",""],["","",""]]
        self.turns = 0
        self.button_list = []
        self.game_is_on = True
        self.create_game_board()
        self.mode = mode        # "mode 0 means vs AI" and "mode 1 means multiplayer game"

    
    def check_winner(self, label):

        winner = self.getWinner(self.game_status)
        winnerText = ""
        if (winner == -1):
            winnerText = "Player 1 won"
        elif (self.mode == 0):
            winnerText = "AI Won"
        else:
            winnerText = "Player 2 won"
        
        if (winner != 0):
            label.configure(text = winnerText, background="black", foreground="white")
            self.game_is_on = False

    
    def getWinner(self, game_status):

        # Example of winning_state: [[0,1],[1,1],[2,1]]
        for winning_state in GameBoard.WINNING_STATES:
            o_won = True
            x_won = True
            for i in range(3):
                x_coord = winning_state[i][0]       # for i=0, x_coord = 0
                y_coord = winning_state[i][1]       # for i=0, y_coord = 1
                element = game_status[x_coord][y_coord]
                if ((element == "") or (element == "X")):
                    o_won = False
                if ((element == "") or (element == "O")):
                    x_won = False

            if x_won:
                # We are returning -1 here because in ai mode x will be player
                return -1
            elif o_won:
                # We are returning 1 here because in ai mode o will be AI and our intention is to make sure Ai wins at all cost
                return 1
        return 0    # No one won
    

    def isTerminal(self, game_status, turn):
        if self.getWinner(game_status) != 0:
            return 1

        return turn == 9
    

    def getMax(self, game_status, turn):

        if self.isTerminal(game_status, turn):
            return self.getWinner(game_status)

        value = -2
        for  x in range(3):
            for y in range(3):
                if self.game_status[x][y] == "":
                    self.game_status[x][y] = "O"
                    player_move = self.getMin(self.game_status, turn+1)
                    self.game_status[x][y] = ""
                    if (player_move > value):
                        value = player_move
                    if (value == 1):
                        return value
    
        return value

    
    def getMin(self, game_status, turn):

        if self.isTerminal(game_status, turn):
            return self.getWinner(game_status)

        value = 2
        for  x in range(3):
            for y in range(3):
                if self.game_status[x][y] == "":
                    game_status[x][y] = "X"
                    # We are considering that AI is playing to maximize thr score
                    ai_move = self.getMax(game_status, turn+1)
                    game_status[x][y] = ""
                    if (ai_move < value):
                        value = ai_move
                    if (value == -1):
                        return value
                
        return value


    def update_board(self, i, j, label):
        
        if (self.game_is_on and self.game_status[i][j] == ""):
            player_symbol = "O" if (self.turns & 1) else "X"
            self.game_status[i][j] = player_symbol
            self.button_list[i*3+j].configure(text=player_symbol)
            self.turns = self.turns + 1
            if self.mode == 0 and self.turns <= 8:
                position = -1
                value = -2
                isFound = False
                for x in range(3):
                    for y in range(3):
                        if self.game_status[x][y] == "":
                            self.game_status[x][y] = "O"
                            player_move = self.getMin(self.game_status, self.turns+1)
                            self.game_status[x][y] =""
                            if (player_move > value):
                                position = x*3+y
                                value = player_move
                            if (value == 1):
                                isFound = True
                                break
                    if isFound:
                        break
                self.game_status[position//3][position%3] = "O"
                self.button_list[position].configure(text="O")
                self.turns = self.turns + 1

            self.update()
            self.check_winner(label)


    def reset_game(self, label):

        label.configure(text="Welcome to Tic Tac Toe", background="white", foreground="black")
        self.turns = 0
        self.game_is_on = True

        # Restarting the game logically
        for buttons in self.button_list:
            buttons.configure(text="")

        # Restarting the game visually
        for i in range(3):
            for j in range(3):
                self.game_status[i][j] = ""
        
        self.update()       # To refresh the screen so that visual changes can be seen


    def create_game_board(self):

        X_MARGIN = (self.winfo_screenwidth() - self.WINDOW_WIDTH)//2
        Y_MARGIN = (self.winfo_screenheight() - self.WINDOW_HEIGHT)//2
        self.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+{X_MARGIN}+{Y_MARGIN}")

        header = Frame(self)
        label = Label(header, text="Welcome to Tic Tac Toe", background="white")
        label.pack(fill=X)
        header.pack(fill=X)

        game_screen = Frame(self, padx=35)
        for i in range(3):
            for j in range(3):
                button = Button(game_screen, text="", height=4, width=8, font="serif 10 bold", command = lambda i=i, j=j:self.update_board(i, j, label))
                button.grid(row=i,column=j)
                self.button_list.append(button)
        game_screen.pack(fill=X)

        button_frame = Frame(self)
        button_frame.pack()

        reset_button = Button(button_frame, text="RESET", height=2, width=15, command = lambda:self.reset_game(label))
        reset_button.grid(row=0, column=0)

        main_menu_button = Button(button_frame, text="Main Menu", height=2, width=15, command = self.main_menu)
        main_menu_button.grid(row=0, column=1)


    def getEmptyCell(self, game_status):
        for i in range(3):
            for j in range(3):
                if game_status[i][j] == "":
                    return i*3+j
    
    def main_menu(self):
        self.destroy()
        os.system("python main.py")