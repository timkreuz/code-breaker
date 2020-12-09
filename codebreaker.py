import tkinter as tk
from numpy import random

# AddFrame
# Position Frame
mainBackground = "#75a3a3"
# solutionBackground = "#94b8b8"
solutionBackground = "#75a3a3"
red = "#ff3300"
yellow = "#ffff00"
green = "#00e600"
blue = "#005ce6"
orange = "#ff9900"
purple = "#cc00cc"
empty = "#b3b3b3"


window = tk.Tk()
window.title("Code Breaker")

# Game

history = []

def getSecretCode():
    secretCode = []
    for _ in range(4): secretCode.append(random.randint(1, 7))
    return secretCode

game = {"solved": False, "guessCount": 0, "guess": [0, 0, 0, 0], "solution": getSecretCode()}
# print(game)

colors = {0: empty, 1: red, 2: orange, 3: yellow, 4: green, 5: blue, 6: purple}


def resetGame():
    game["solved"] = False
    game["guessCount"] = 0
    game["guess"] = [0, 0, 0, 0]
    game["solution"] = getSecretCode()
    # print(game)


def checkCode():
    great = 0
    nice = 0

    for val in range(1,7):
        valNice = 0
        valGreat = 0
        for pos in range(4):
            if game["solution"][pos] == val and game["solution"][pos] == game["guess"][pos]:
                valGreat += 1
        sCount = game["solution"].count(val)
        gCount = game["guess"].count(val)
        if gCount >= sCount:
            valNice = (sCount - valGreat)
        else:
            valNice = (gCount - valGreat)
        great += valGreat
        nice += valNice

    return((great, nice))


def scoreIt():
    score = checkCode()
    game["solved"] = score[0] == 4
    if game["solved"]:
        history.append(game["guessCount"])
        game["guessCount"] = -1
    else:
        game["guessCount"] = game["guessCount"] + 1
        game["guess"] = [0, 0, 0, 0]
    return score


def solveClick(event):
    result = event.widget
    if not game["solved"] and result.row == game["guessCount"]:
        pegs = game["guess"]
        ready = True
        for pos in range(4):
            if pegs[pos] == 0:
                ready = False
        if ready:
            score = scoreIt()
            result.config(text=str(score[0]) + "-" + str(score[1]))
        if game["solved"]:
            displayFinal()
        else:
            nextGuess = window.nametowidget(
                "main.guessFrame-" + str(game["guessCount"]) + ".resultFrame.lbl")
            nextGuess.config(text="Solve")

# Display


def resetDisplay():
    window.nametowidget("main.controlFrame").destroy()
    for row in range(10):
        window.nametowidget("main.guessFrame-" + str(row)).destroy()
    window.nametowidget("main.solutionFrame").destroy()
    addControlFrame(window)
    for row in range(10):
        addGuessFrame(window, row)
    addSolutionFrame(window)


def drawPeg(peg, color):
    peg.create_oval(10, 10, 25, 25, fill=color,
                    outline="#527a7a", width=1)


def pegClick(event):
    peg = event.widget
    if not game["solved"] and peg.row == game["guessCount"]:
        peg.color = ((peg.color + 1) % 7)
        game["guess"][peg.position] = peg.color
        drawPeg(peg, colors[peg.color])


def controlClick(event):
    if game["guessCount"] == -1:
        resetGame()
        resetDisplay()


def displayFinal():
    for pos in range(4):
        peg = window.nametowidget(
            "main.solutionFrame.code.codePeg-" + str(pos))
        peg.color = game["solution"][pos]
        control = window.nametowidget("main.controlFrame.lbl")
        control.config(text="Play Again?")
        drawPeg(peg, colors[peg.color])


def addMainFrame(window):
    main = tk.Frame(master=window, name="main",
                    borderwidth=5, bg=mainBackground)
    label = tk.Label(master=main, name="lbl", text="Code Breaker",
                     height=3, width=40, bg=mainBackground)
    label.pack()
    main.pack(fill=tk.X)


def addLeftFrame(parent, text):
    left = tk.Frame(master=parent, name="left", width=8, bg=solutionBackground)
    label = tk.Label(master=left, name="lbl", text=text,
                     height=2, width=7, bg=solutionBackground)
    label.pack()
    left.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)


def addCodePeg(parent, row, position):
    canvas = tk.Canvas(master=parent, name="codePeg-" + str(position), bd=0,
                       highlightthickness=0, bg=solutionBackground, height=15, width=15)
    drawPeg(canvas, empty)
    canvas.bind('<Button-1>', pegClick)
    setattr(canvas, "row", row)
    setattr(canvas, "position", position)
    setattr(canvas, "color", 0)
    canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)


def addCodeFrame(parent, row):
    code = tk.Frame(master=parent, name="code",
                    width=22, bg=solutionBackground)
    addCodePeg(code, row, 0)
    addCodePeg(code, row, 1)
    addCodePeg(code, row, 2)
    addCodePeg(code, row, 3)
    code.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)


def addResultFrame(parent, text, row):
    resultFrame = tk.Frame(master=parent, name="resultFrame",
                           width=7, bg=solutionBackground)
    label = tk.Label(master=resultFrame, name="lbl", text=text,
                     height=2, width=5, bg=solutionBackground)
    setattr(label, "row", row)
    label.bind('<Button-1>', solveClick)
    label.pack()
    resultFrame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)


def addSolutionFrame(window):
    main = window.nametowidget("main")
    solutionFrame = tk.Frame(master=main, name="solutionFrame",
                             borderwidth=2, relief=tk.GROOVE, bg=solutionBackground)
    addLeftFrame(solutionFrame, "Solution")
    addCodeFrame(solutionFrame, 99)
    addResultFrame(solutionFrame, "", -1)
    solutionFrame.pack(fill=tk.X)


def addControlFrame(window):
    main = window.nametowidget("main")
    controlFrame = tk.Frame(master=main, name="controlFrame",
                            borderwidth=2, relief=tk.GROOVE, bg=solutionBackground)
    label = tk.Label(master=controlFrame, name="lbl", text="Game-" + str(len(history) + 1),
                     height=2, width=10, bg=solutionBackground)
    label.bind('<Button-1>', controlClick)
    label.pack()
    controlFrame.pack(fill=tk.X)


def addGuessFrame(window, row):
    main = window.nametowidget("main")
    guessFrame = tk.Frame(master=main, name="guessFrame-" + str(row),
                          borderwidth=2, relief=tk.GROOVE, bg=solutionBackground)
    addLeftFrame(guessFrame, str(row+1))
    addCodeFrame(guessFrame, row)
    if row == 0:
        message = "Solve"
    else:
        message = ""
    addResultFrame(guessFrame, message, row)
    guessFrame.pack(fill=tk.X)


addMainFrame(window)
addControlFrame(window)
for row in range(10):
    addGuessFrame(window, row)
addSolutionFrame(window)
window.mainloop()
