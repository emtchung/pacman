#Emily Chung
#Comp112-05
#Pacman Project

import turtle
import math
import random
import time

"""
3 Goals:

1. Turtle: I use turtles to display the appearance and graphics of the maze, characters, and foods for my game.
2. Flow Control: I am using for and if loops to make sure my game flows smoothly while running. The if loops
    sets the restraints and the for goes through the items in my lists to ensure that the characters and items
    in the game appears and function correctly.
3. Lists: using lists to keep track of coordinates for the pacman and enemies to not cross through the walls
"""

#Background
background=turtle.Screen()
background.bgcolor('black')
background.title ('Pacman Game')
background.setup (600,400)
background.tracer(0)

#Empty Lists
borders = []
ghosts = []
snacks = []
supersnacks = []
autoturns = [(-149, 58), (-101, 58), (91, 58), (139, 58), (-221, 10), (-173, 10), (-101, 10), (91, 10), (163, 10), (211, 10), (-149, -38), (-101, -38), (91, -38), (139, -38)]
forbidden = [(-5,82)]
forbidden2 = [(-5,34)]
den = [(-5,10)]
home = [(-53,10),(-29,10),(19,10)]



#Drawing
class Board(turtle.Turtle):
    def __init__ (self):
        """represents a blue square turtle that will function like a turtle and become the borders of the maze
        """
        turtle.Turtle.__init__(self)
        self.shape('square')
        self.color('blue')
        self.penup()
        self.speed(0)
        
#GameBoard - set up each character resembles a character in the game
board = ['*********************',
         '*pFFF*FFFFFFFFF*FFFp*',
         '*F**F*F*******F*F**F*',
         '*F*FFFFFFFFFFFFFFF*F*',
         '*F*F**F*** ***F**F*F*',
         '*FFFFFF*12 34*FFFFFF*',
         '*F*F**F*******F**F*F*',
         '*F*FFFFFFFFFFFFFFF*F*',
         '*p**F*F*******F*F**F*',
         '*FFFF*FFFFPFFFF*FFpF*',
         '*********************']


def create(gameboard):
    """sig: list -> none
    takes in a list of strings and for each character, it will call turtles to position
    them there to create a gameboard and position the player and enemies at their respective locations
    """
    for row in range(len(gameboard)):
        for column in range (len(gameboard[row])):
            block = gameboard[row][column]
            xcoor = -245 + (column*24)
            ycoor = 130 - (row*24)
            if block == '*':
                draw.goto(xcoor, ycoor)
                draw.stamp()
                borders.append((xcoor, ycoor))
            if block == 'P':
                pacman.goto(xcoor, ycoor)
            if block == 'p':
                supersnacks.append(PacmanPowerup(xcoor, ycoor))
            if block == 'F':
                snacks.append(PacmanFood(xcoor, ycoor))
            if block == '1':
                ghosts.append(Ghost1(xcoor, ycoor))
            if block == '2':
                ghosts.append(Ghost2(xcoor, ycoor))
            if block == '3':
                ghosts.append(Ghost3(xcoor, ycoor))
            if block == '4':
                ghosts.append(Ghost4(xcoor, ycoor))
                

#Characters
class Pacman(turtle.Turtle):
    """represents the pacman/main character in the game that will act like a turtle"""
    def __init__ (self):
        turtle.Turtle.__init__(self)
        self.penup()
        self.speed(1)
        self.color('yellow')
        self.shape('circle')
        self.direction = 'stop'
        self.worth = 0
        
    def __str__(self):
        """when printed, it will print the worth of the pacman"""
        string = str(self.worth)
        return string
    
    def istouching (self, smth):
        """ sig: self, another class, -> True/False
        uses the coordinates of the pacman and other objects around them to check if they will collide"""
        a = self.xcor() - smth.xcor()
        b = self.ycor() - smth.ycor()
        distance = math.sqrt ((a**2) + (b**2))
        if distance < 13:
            return True
        else:
            return False
        
    def spawn(self):
        """tells the pacman to go to original location"""
        self.goto(-5,-86)

   
class Ghost1(turtle.Turtle):
    def __init__ (self, xcoor,ycoor):
        """represents a ghost/enemy in the game that will try to eat the pacman and chase it
        """
        turtle.Turtle.__init__(self)
        self.speed(2)
        self.penup()
        self.color('red')
        self.shape('square')
        self.shapesize(stretch_len=0.9)
        self.goto(xcoor,ycoor)
        self.direction = random.choice(['up','down','left','right'])
        self.state = 'normal'
        self.worth = 200

    def move(self):
        """determines how the ghost will move when it interacts with a wall or corner
            and it also checks if the pacman is near so the ghost can chase the pacman or
            if its in the den- uses the coordinates of the ghost"""
        if self.direction == 'up':
            xc = 0
            yc = 24
        elif self.direction == 'down':
            xc = 0
            yc = -24
        elif self.direction == 'left':
            yc = 0
            xc = -24
        elif self.direction == 'right':
            yc = 0
            xc = 24
        elif self.direction == 'stop':
            yc = 0
            xc = 0
        y = self.ycor() + yc
        x = self.xcor() + xc

        if (x,y) in den:
            self.goto(x,y)
            self.direction = 'up'
        if (x,y) in forbidden:
            self.direction = random.choice(['left','right'])
        elif (x,y) in autoturns:
            self.direction = random.choice(['up','down','left','right'])
            self.goto(x,y)
        elif (x,y) not in borders:
            self.goto(x,y)
        else:
            self.direction = random.choice(['up','down','left','right'])

        turtle.ontimer(self.move, t=random.randint(100,200))
        
        if self.pacmanchase(pacman) and self.state == 'normal':
            if pacman.ycor() > self.ycor():
                self.direction = 'up'
            elif pacman.ycor() < self.ycor():
                self.direction = 'down'
            elif pacman.xcor() < self.xcor():
                self.direction = 'left'
            elif pacman.xcor() > self.xcor():
                self.direction = 'right'
                
    def pacmanchase (self, pacman):
        """sig: self, pacman object -> True/False
        checks if the pacman is a certain distance from the ghost"""
        a = self.xcor() - pacman.xcor()
        b = self.ycor() - pacman.ycor()
        distance = math.sqrt ((a**2) + (b**2))
        if distance < 64:
            return True
        else:
            return False
        
    def resetnormal(self):
        """resets the ghost to its original color, position in the board, and state
        """
        self.color('red')
        self.goto(-53,10)
        self.direction == 'up'
        self.state = 'normal'
        
    def resetnoteaten(self):
        """resets the state and color
        """
        self.color('red')
        self.state = 'normal'


class Ghost2(turtle.Turtle):
    def __init__ (self, xcoor,ycoor):
        """represents a ghost/enemy in the game that will try to eat the pacman and chase it
        """
        turtle.Turtle.__init__(self)
        self.speed(2)
        self.penup()
        self.color('orange')
        self.shape('square')
        self.shapesize(stretch_len=0.9)
        self.goto(xcoor,ycoor)
        self.direction = random.choice(['up','down','left','right'])
        self.state = 'normal'
        self.worth = 200

    def move(self):
        """determines how the ghost will move when it interacts with a wall or corner and it also checks
            if the pacman is near so the ghost can chase the pacman - uses the coordinates of the ghost"""
        if self.direction == 'up':
            xc = 0
            yc = 24
        elif self.direction == 'down':
            xc = 0
            yc = -24
        elif self.direction == 'left':
            yc = 0
            xc = -24
        elif self.direction == 'right':
            yc = 0
            xc = 24
        elif self.direction == 'stop':
            yc = 0
            xc = 0
        y = self.ycor() + yc
        x = self.xcor() + xc

        if (x,y) in den:
            self.goto(x,y)
            self.direction = 'up'
        if (x,y) in forbidden:
            self.direction = random.choice(['left','right'])
        elif (x,y) in autoturns:
            self.direction = random.choice(['up','down','left','right'])
            self.goto(x,y)
        elif (x,y) not in borders:
            self.goto(x,y)
        else:
            self.direction = random.choice(['up','down','left','right'])

        turtle.ontimer(self.move, t=random.randint(100,200))
        
        if self.pacmanchase(pacman) and self.state == 'normal':
            if pacman.ycor() > self.ycor():
                self.direction = 'up'
            elif pacman.ycor() < self.ycor():
                self.direction = 'down'
            elif pacman.xcor() < self.xcor():
                self.direction = 'left'
            elif pacman.xcor() > self.xcor():
                self.direction = 'right'
                
    def pacmanchase (self, pacman):
        """sig: self, pacman object -> True/False
        checks if the pacman is a certain distance from the ghost"""
        a = self.xcor() - pacman.xcor()
        b = self.ycor() - pacman.ycor()
        distance = math.sqrt ((a**2) + (b**2))
        if distance < 49:
            return True
        else:
            return False
        
    def resetnormal(self):
        """resets the ghost to its original color, position in the board, and state
        """
        self.color('orange')
        self.goto(-29,10)
        self.direction == random.choice(['left','right'])
        self.state = 'normal'
        
    def resetnoteaten(self):
        """resets the state and color
        """
        self.color('orange')
        self.state = 'normal'


class Ghost3(turtle.Turtle):
    def __init__ (self, xcoor,ycoor):
        """represents a ghost/enemy in the game that will try to eat the pacman and chase it
        """
        turtle.Turtle.__init__(self)
        self.speed(2)
        self.penup()
        self.color('#E36B89')
        self.shape('square')
        self.shapesize(stretch_len=0.9)
        self.goto(xcoor,ycoor)
        self.direction = random.choice(['up','down','left','right'])
        self.state = 'normal'
        self.worth = 200

    def move(self):
        """determines how the ghost will move when it interacts with a wall or corner and it also
            checks if the pacman is near so the ghost can chase the pacman - uses the coordinates of the ghost"""
        if self.direction == 'up':
            xc = 0
            yc = 24
        elif self.direction == 'down':
            xc = 0
            yc = -24
        elif self.direction == 'left':
            yc = 0
            xc = -24
        elif self.direction == 'right':
            yc = 0
            xc = 24
        elif self.direction == 'stop':
            yc = 0
            xc = 0
        y = self.ycor() + yc
        x = self.xcor() + xc

        if (x,y) in den:
            self.goto(x,y)
            self.direction = 'up'
        if (x,y) in forbidden:
            self.direction = random.choice(['left','right'])
        elif (x,y) in autoturns:
            self.direction = random.choice(['up','down','left','right'])
            self.goto(x,y)
        elif (x,y) not in borders:
            self.goto(x,y)
        else:
            self.direction = random.choice(['up','down','left','right'])

        turtle.ontimer(self.move, t=random.randint(100,200))
        
        if self.pacmanchase(pacman) and self.state == 'normal':
            if pacman.ycor() > self.ycor():
                self.direction = 'up'
            elif pacman.ycor() < self.ycor():
                self.direction = 'down'
            elif pacman.xcor() < self.xcor():
                self.direction = 'left'
            elif pacman.xcor() > self.xcor():
                self.direction = 'right'
                
    def pacmanchase (self, pacman):
        """sig: self, pacman object -> True/False
        checks if the pacman is a certain distance from the ghost"""
        a = self.xcor() - pacman.xcor()
        b = self.ycor() - pacman.ycor()
        distance = math.sqrt ((a**2) + (b**2))
        if distance < 49:
            return True
        else:
            return False
        
    def resetnormal(self):
        """resets the ghost to its original color, position in the board, and state
        """
        self.color('#E36B89')
        self.goto(19, 10)
        self.direction == random.choice(['left','right'])
        self.state = 'normal'
        
    def resetnoteaten(self):
        """resets the state and color
        """
        self.color('#E36B89')
        self.state = 'normal'

class Ghost4(turtle.Turtle):
    def __init__ (self, xcoor,ycoor):
        """represents a ghost/enemy in the game that will try to eat the pacman and chase it
        """
        turtle.Turtle.__init__(self)
        self.speed(2)
        self.penup()
        self.color('#15F4EE')
        self.shape('square')
        self.shapesize(stretch_len=0.9)
        self.goto(xcoor,ycoor)
        self.direction = random.choice(['up','down','left','right'])
        self.state = 'normal'
        self.worth = 200

    def move(self):
        """determines how the ghost will move when it interacts with a wall or corner and it
            also checks if the pacman is near so the ghost can chase the pacman - uses the coordinates of the ghost"""
        if self.direction == 'up':
            xc = 0
            yc = 24
        elif self.direction == 'down':
            xc = 0
            yc = -24
        elif self.direction == 'left':
            yc = 0
            xc = -24
        elif self.direction == 'right':
            yc = 0
            xc = 24
        elif self.direction == 'stop':
            yc = 0
            xc = 0
        y = self.ycor() + yc
        x = self.xcor() + xc

        if (x,y) in den:
            self.goto(x,y)
            self.direction = 'up'
        if (x,y) in forbidden:
            self.direction = random.choice(['left','right'])
        elif (x,y) in autoturns:
            self.direction = random.choice(['up','down','left','right'])
            self.goto(x,y)
        elif (x,y) not in borders:
            self.goto(x,y)
        else:
            self.direction = random.choice(['up','down','left','right'])

        turtle.ontimer(self.move, t=random.randint(100,200))
        
        if self.pacmanchase(pacman) and self.state == 'normal':
            if pacman.ycor() > self.ycor():
                self.direction = 'up'
            elif pacman.ycor() < self.ycor():
                self.direction = 'down'
            elif pacman.xcor() < self.xcor():
                self.direction = 'left'
            elif pacman.xcor() > self.xcor():
                self.direction = 'right'
                
    def pacmanchase (self, pacman):
        """sig: self, pacman object -> True/False
        checks if the pacman is a certain distance from the ghost"""
        a = self.xcor() - pacman.xcor()
        b = self.ycor() - pacman.ycor()
        distance = math.sqrt ((a**2) + (b**2))
        if distance < 49:
            return True
        else:
            return False
        
    def resetnormal(self):
        """resets the ghost to its original color, position in the board, and state
        """
        self.color('#15F4EE')
        self.goto(43, 10)
        self.direction == random.choice(['left','right'])
        self.state = 'normal'
        
    def resetnoteaten(self):
        """resets the state and color
        """
        self.color('#15F4EE')
        self.state = 'normal'

#Pacman Food
class PacmanFood(turtle.Turtle):
    """Represents the food the pacman will eat and will position itself at certain coordinates"""
    def __init__ (self, xcoor,ycoor):
        turtle.Turtle.__init__(self)
        self.speed(0)
        self.penup()
        self.color('pink')
        self.shape('square')
        self.shapesize(stretch_wid=0.2,stretch_len=0.2)
        self.goto(xcoor,ycoor)
        self.worth = 10
        
    def leave(self):
        """will move the turtle to another place on the screen and changes the color so the pacman
           turtle will not bump into it continuously"""
        self.color('black')
        self.goto (700,700)
        self.hideturtle


class PacmanPowerup(turtle.Turtle):
    """Represents the superfood the pacman will eat and will position itself at certain
       coordinates and it will also trigger if the pacman will get its superpower
    """
    def __init__ (self, xcoor,ycoor):
        turtle.Turtle.__init__(self)
        self.speed(0)
        self.penup()
        self.color('pink')
        self.shape('circle')
        self.shapesize(stretch_wid=0.5,stretch_len=0.5)
        self.goto(xcoor,ycoor)
        self.worth = 150
        
    def leave(self):
        """will move the turtle to another place on the screen and changes the color so the
           pacman turtle will not bump into it continuously"""
        self.goto (700,700)
        self.hideturtle

#Movements
def up():
    """sig: none -> none
    helps the pacman turtle move up and not collide with the walls and in the enemies den"""
    pacman.direction='up'
    y = pacman.ycor() + 24
    x = pacman.xcor() + 0
    if (x,y) in forbidden2:
        y = pacman.ycor() - 24
        x = pacman.xcor() + 0
    if (x,y) not in borders:
        pacman.goto(x,y)

def down():
    """sig: none -> none
    helps the pacman turtle move down and not collide with the walls and in the enemies den"""
    pacman.direction='down'
    y = pacman.ycor() - 24
    x = pacman.xcor() + 0
    if (x,y) in forbidden2:
        y = pacman.ycor() + 24
        x = pacman.xcor() + 0
    if (x,y) not in borders:
        pacman.goto(x,y)
        
def left():
    """sig: none -> none
    helps the pacman turtle move left and not collide with the walls and in the enemies den"""
    pacman.direction='left'
    y = pacman.ycor() + 0
    x = pacman.xcor() - 24
    if (x,y) not in borders:
        pacman.goto(x,y)

def right():
    """sig: none -> none
    helps the pacman turtle move right and not collide with the walls and in the enemies den"""
    pacman.direction = 'right'
    y = pacman.ycor() + 0
    x = pacman.xcor() + 24
    if (x,y) not in borders:
        pacman.goto(x,y)

 
#Key Bindings - assigns the keys to the movement functions
background.listen()
background.onkeypress(up,'w')
background.onkeypress(down,'s')
background.onkeypress(left,'a')
background.onkeypress(right,'d')


#Initiation
draw = Board()
pacman = Pacman()
create(board)

#Ghost Movement - a loop so that each ghost can leave the den at a specific time so they don't all leave at the same time
for ghost in ghosts:
    if ghost == ghosts[0]:
        turtle.ontimer(ghost.move, t=random.randint(250,400))
    if ghost == ghosts[1]:
        turtle.ontimer(ghost.move, 3500)
    if ghost == ghosts[2]:
        turtle.ontimer(ghost.move, 6500)
    if ghost == ghosts[3]:
        turtle.ontimer(ghost.move, 8000)


#Scores and Lives
score=pacman
lives = 3

current = turtle.Turtle()
current.speed(0)
current.penup()
current.color('white')
current.goto(-260,-170)
current.pendown()
current.write('Score: {} Lives: {}'.format(score, lives), align='left', font=('Courier',20))
current.hideturtle()


directions=turtle.Turtle()
directions.speed(0)
directions.penup()
directions.color('white')
directions.goto(252,-168)
directions.pendown()
directions.write("Press 'a','s','d','w' to move.".format(score, lives), align='right', font=('Courier',13))
directions.hideturtle()

end = turtle.Turtle()
end.speed(0)
end.penup()
end.color('white')
end.goto(0,0)
end.hideturtle()

#SuperFruit Power
def weak():
    """sig: none -> none
    creates a weak state for the ghosts and makes each ghosts' state be weak and change their color"""
    weak.has_been_called = True 
    for ghost in ghosts:
        ghost.color('light blue')
        ghost.state = 'weak'
      
def normal():
    """sig:none -> none
    returns to normal mode and goes through a loop to make each ghost reset to its original state"""
    for ghost in ghosts:
        ghost.resetnoteaten()

timelimit = 5 #a time limit for the superfruit
weak.has_been_called = False

#Enemy Timed Movement after Death
def dead():
    """sig: none->none
    tells python if a function has been called"""
    dead.has_been_called = True
    
timelimit2 = 6 #a time limit for how long the ghosts can stay in the den
dead.has_been_called = False

#Game Running
while True:
    #a loop that checks if the pacman collides with the food so that it can change the score and remove the snack from the board and list
    for food in snacks:
        if pacman.istouching(food):
            pacman.worth += food.worth
            current.clear()
            current.write('Score: {} Lives: {}'.format(score, lives), align='left', font=('Courier',20))
            food.leave()
            snacks.remove(food)

    #a loop that checks if the pacman collides with the superfood so that it can change the score and remove the snack from the board and list + trigger the pacmans superpower to eat the ghosts and change the ghosts state
    for food in supersnacks:
        if pacman.istouching(food):
            pacman.worth += food.worth
            current.clear()
            current.write('Score: {} Lives: {}'.format(score, lives), align='left', font=('Courier',20))
            food.leave()
            supersnacks.remove(food)
            weak()
            start1 = time.time()

    #a loop that changes the colors of the ghosts and see how long time has passed so the superpower ends        
    if weak.has_been_called:
        elapsed = int(time.time()-start1)
        if elapsed > (timelimit - 3):
            for ghost in ghosts:
                if ghost.state == 'weak' and (elapsed % 2) == 0:
                    ghost.color('white')
                elif ghost.state == 'weak' and (elapsed % 2) != 0:
                    ghost.color('light blue')
        if elapsed > timelimit:
            normal()
            weak.has_been_called = False

    #a loop that checks if the ghosts are interacting with the pacman and changes the score if it does -- checks if certain states are true to determine if the score will increase or decrease 
    for ghost in ghosts:
        if pacman.istouching(ghost) and ghost.state == 'normal':
            lives -= 1
            time.sleep(1)
            for ghost in ghosts:
                ghost.resetnormal()
                ghost.direction = 'stop'
                start2 = time.time()
                dead()
            pacman.worth -= ghost.worth
            pacman.spawn()
            pacman.direction = 'stop'
            current.clear()
            current.write('Score: {} Lives: {}'.format(score, lives), align='left', font=('Courier',20))
        elif pacman.istouching(ghost) and ghost.state == 'weak':
            pacman.worth += ghost.worth
            ghost.resetnormal()
            current.clear()
            current.write('Score: {} Lives: {}'.format(score, lives), align='left', font=('Courier',20))

    #a loop that makes the ghosts move and leave the den at a certain time when the pacman dies        
    if dead.has_been_called:
        elapsed2 = int(time.time()-start2)
        if elapsed2 < timelimit2:
            for ghost in ghosts:
                if ghost == ghosts[0] and elapsed2 == 0:
                    ghost.direction = 'right'
                if ghost == ghosts[1] and elapsed2 == 2:
                    ghost.direction = 'right'
                if ghost == ghosts[2] and elapsed2 == 4:
                    ghost.direction = 'left'
                if ghost == ghosts[3] and elapsed2 == 5:
                    ghost.direction = 'left'
        if elapsed2 > timelimit2:
            dead.has_been_called = False

    #end screen - tells the score and if the player won or lost        
    if lives == 0:
        time.sleep(1)
        turtle.clearscreen()
        background.bgcolor('black')
        end.pendown()
        end.write('No more lives! \nScore: {}'.format(score), align ='center', font=('Courier',30))
        time.sleep(2)
        turtle.bye()
    
    elif len(snacks) == 0 and len(supersnacks) == 0:
        time.sleep(1)
        turtle.clearscreen()
        background.bgcolor('black')
        end.pendown()
        end.write('Congrats. You won!\nScore: {}'.format(score), align = 'center', font=('Courier',30))
        time.sleep(2)
        turtle.bye()
    
    background.update()
