import tkinter as tk
from tkinter import font
import random
from tkinter import messagebox as tkMessageBox

boardSize = 10
density = 1
radiusSpace = 1
expandSpace = 1
displayZero = False

"""
Radius 1 = 3x3
Radius 2 = 5x5
2x+1 is Radius to CordSize
(x-1)/2 is CordSize to Radius
etc
"""

class minesweeperLogic(object):
    def __init__(self):
        self.board = {}
        self.mines = 0
        self.mineLocation = set()
        self.flagLocation = set()
        for i in range(boardSize):
            for j in range(boardSize):
                if random.randint(1, boardSize//density) == 1:
                    self.board[(i, j)] = "Mine"
                    self.mines += 1
                    self.mineLocation.add((i, j))
                else:
                    self.board[(i, j)] = "Nothing"

    def radar(self, radius, row, col):
        mineCount = 0
        for i in range(-radius, radius + 1):
            for j in range(-radius, radius + 1):
                try:
                    if self.board[(row + i, col + j)] == "Mine":
                        mineCount += 1
                except KeyError:
                    pass
        return mineCount

class minesweeperBoard(tk.Tk):
    def __init__(self):
        super().__init__()

        self.board = {}
        self.backBoard = {}
        self.logic = minesweeperLogic()

        self.title("Radar Minesweeper")

        self.initDisplay("Minesweeper")
        self.initDisplay(self.logic.mines)
        self.initGrid()

    def initDisplay(self, txt):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text=txt,
            font=font.Font(size=14),
        )
        self.display.pack()

    def initGrid(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        for row in range(boardSize):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=50)
            for col in range(boardSize):
                button = tk.Button(
                    master=grid_frame,
                    text="",
                    fg="black",
                    width=2,
                    height=1,
                    highlightbackground="lightblue",
                    bg = 'gray38'
                )
                self.board[button] = (row, col)
                self.backBoard[(row, col)] = button
                button.grid(
                    row=row,
                    column=col,
                    padx=5,
                    pady=5,
                    sticky="nsew"
                )
                button.bind("<ButtonPress-1>", self.reveal)
                button.bind("<ButtonPress-3>", self.flag)

    def reveal(self, event):
        """Handle a player's move."""
        clicked_btn = event.widget
        row, col = self.board[clicked_btn]
        result = self.logic.board[(row, col)]

        if (row, col) in self.logic.flagLocation:
            return

        if result == "Mine":
            self.gameOver()
        elif result == "Nothing":
            self.revealSpace(row, col)

    def flag(self, event):
        clicked_btn = event.widget
        row, col = self.board[clicked_btn]
        if clicked_btn.cget("text") == "🚩":
            self.logic.flagLocation.remove((row, col))
            clicked_btn.config(fg="black")
            clicked_btn.config(text="")
            return
        if clicked_btn.cget("text") != "":
            return
        clicked_btn.config(fg="red")
        clicked_btn.config(text="🚩")
        self.logic.flagLocation.add((row, col))
        if self.logic.flagLocation == self.logic.mineLocation:
            self.gameOver("You win! Play Again?")


    def revealSpace(self, row, col):
        if row < 0 or col < 0 or row >= boardSize or col >= boardSize:
            return
        if self.backBoard[(row, col)].cget("text") != "":
            return
        space = self.logic.radar(expandSpace, row, col)
        r = self.logic.radar(radiusSpace, row, col)
        self.backBoard[(row, col)].config(text=r)
        self.backBoard[(row, col)].config(bg='ivory2')
        if not(displayZero) and r == 0:
            self.backBoard[(row, col)].config(text=" ")
        if space == 0:
            self.revealSpace(row + 1, col + 1)
            self.revealSpace(row + 1, col - 1)
            self.revealSpace(row + 1, col)
            self.revealSpace(row - 1, col + 1)
            self.revealSpace(row - 1, col - 1)
            self.revealSpace(row - 1, col)
            self.revealSpace(row, col + 1)
            self.revealSpace(row, col - 1)
            return

    def gameOver(self, msg="You lost. Play Again?"):
        for i in self.board.keys():
            omega = self.board[i]
            if self.logic.board[(omega[0], omega[1])] == "Mine" and i.cget("text") == "":
                i.config(fg="blue")
                i.config(text="💣")
        for i in self.logic.flagLocation:
            if self.backBoard[i].cget("text") == "🚩" and i not in self.logic.mineLocation:
                self.backBoard[i].config(fg="pink")
                self.backBoard[i].config(text="X")
        res = tkMessageBox.askyesno("Game Over", msg)

        if res:
            self.destroy()
            startMain()
        else:
            self.destroy()

def startMain():
    board = minesweeperBoard()
    board.mainloop()

if __name__ == '__main__':
    startMain()
