from tkinter import *
import random

class Ball(object):
    def __init__(self, data):
        self.cx = data.width/2
        self.cy = data.width/2
        self.r = 10
        self.dx = random.choice([-1, 1])*random.randint(5, 20)
        self.dy = random.choice([-1, 1])*random.randint(5, 10)

    def draw(self, canvas):
        canvas.create_oval(self.cx - self.r, self.cy - self.r, self.cx + self.r,
            self.cy + self.r, fill = "white")

    def bounceY(self):
        self.dy = -self.dy

    def move(self, data):
        self.cx += self.dx
        self.cy += self.dy
        if (self.cy + self.r) >= data.height or (self.cy - self.r) <= 0:
            self.bounceY()

    def score(self, data):
        if (self.cx + self.r <= 0):
            data.AIscore += 1
            return True
        elif (self.cx - self.r >= data.width):
            data.playerScore += 1
            return True
        return False

    def collide(self, data):
        if 0 < (self.cx - self.r) <= 10 and data.paddle.y0 < self.cy < data.paddle.y1:
            self.dx = -self.dx
        if data.width - 10 < (self.cx + self.r) <= data.width \
                and data.AI.paddle.y0 < self.cy < data.AI.paddle.y1:
            self.dx = -self.dx

class Paddle(object):
    def __init__(self, x, y):
        self.x0 = x
        self.y0 = y
        self.x1 = x + 10
        self.y1 = y + 80
        self.color = "white"

    def moveUp(self):
        self.y0 -= 30
        self.y1 -= 30

    def moveDown(self):
        self.y0 += 30
        self.y1 += 30

    def draw(self, canvas):
        canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, fill = self.color)

class AI(object):
    def __init__(self, x, y):
        self.paddle = Paddle(x, y)

    def move(self, data):
        if (not(self.paddle.y0< data.ball.cy < self.paddle.y1)) and data.ball.cy < self.paddle.y0:
            self.paddle.moveUp()
        elif (not(self.paddle.y0 < data.ball.cy < self.paddle.y1)) and data.ball.cy > self.paddle.y0:
            self.paddle.moveDown()

    def draw(self, canvas):
        self.paddle.draw(canvas)

####################################
# customize these functions
####################################

def init(data):
    data.mode = 'start'
    data.paddle = Paddle(0, data.width/2 - 40)
    data.ball = Ball(data)
    data.AI = AI(data.width - 10, data.width/2 - 40)
    data.playerScore = 0
    data.AIscore = 0
    data.timerCounter = 0

def mousePressed(event, data):
    if data.mode == 'start': 
        pass
    elif data.mode == 'game': 
        gameMousePressed(event, data)
    elif data.mode == 'end': 
        pass

def keyPressed(event, data):
    if data.mode == 'start': 
        startKeyPressed(event, data)
    elif data.mode == 'game': 
        gameKeyPressed(event, data)
    elif data.mode == 'end': 
        endKeyPressed(event, data)

def timerFired(data):
    if data.mode == 'start': 
        startTimerFired(data)
    elif data.mode == 'game':
        gameTimerFired(data)
    elif data.mode == 'end':
        pass #nothing to do here

def redrawAll(canvas, data):
    if data.mode == 'start':
        startRedrawAll(canvas, data)
    elif data.mode == 'game':
        gameRedrawAll(canvas, data)
    elif data.mode == 'end':
        endRedrawAll(canvas, data)

########################################
# START MODE
########################################

def startKeyPressed(event, data):
    if event.keysym == 's':
        data.mode = 'game'

def startTimerFired(data):
    data.timerCounter += 1

def startRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill = 'black')
    if data.timerCounter % 5 in [0, 1, 2]:
        canvas.create_text(data.width/2, data.height/2 - 50, text = 'PONG', font = 'System 50',
            fill = 'white')
    canvas.create_text(data.width/2, data.height/2 + 125, text = 'Press "s" to start', 
        fill = 'white', font = 'System 20')

########################################
# GAME MODE
########################################

def gameMousePressed(event, data):
    data.paddle.y0 = event.y
    data.paddle.y1 = event.y + 80

def gameKeyPressed(event, data):
    if event.keysym == "k" and data.paddle.y0 > 0:
        data.paddle.moveUp()
    elif event.keysym == "m" and data.paddle.y1 < data.height:
        data.paddle.moveDown()

def gameTimerFired(data):
    data.ball.move(data)
    data.AI.move(data)
    data.ball.collide(data)
    if data.ball.score(data):
        data.ball = Ball(data)
    if data.playerScore == 10 or data.AIscore == 10:
        data.mode = 'end'

def gameRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill = "black")
    data.paddle.draw(canvas)
    data.ball.draw(canvas)
    data.AI.draw(canvas)
    canvas.create_text(data.width/2, 10, anchor = N, text = "Pong", font = "System 20",
        fill = 'white')
    canvas.create_text(10, 10, text = "score: %d" %data.playerScore, anchor = NW,
        fill = 'white', font = "System 15")
    canvas.create_text(data.width - 10, 10, text = "score %d" %data.AIscore, 
        anchor = NE, fill = 'white', font = 'System 15')

####################################
# END MODE
####################################

def endKeyPressed(event, data):
    if event.keysym == 'r':
        init(data)

def endRedrawAll(canvas, data):
    if data.playerScore == 10:
        canvas.create_rectangle(0, 0, data.width, data.height, fill = "black")
        canvas.create_text(data.width/2, data.height/2 - 50, text = "You win", fill = 'white',
            font = "System 50")
    elif data.AIscore == 10:
        canvas.create_rectangle(0, 0, data.width, data.height, fill = "black")
        canvas.create_text(data.width/2, data.height/2 - 50, text = "You lose", fill = 'white',
            font = "System 50")
    canvas.create_text(data.width/2, data.height/2 + 20, text = 'press "r" to restart',
        fill = 'white', font = 'System 20')

####################################
# RUN FUNCTION
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 50 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Motion>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(600, 600)