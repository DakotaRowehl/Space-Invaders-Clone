# Dakota Rowehl, 8/10/2019
# Space Invaders, Turtle Python

# Imports
import turtle
import math
import os
import random
import time

# Creating the Window
window = turtle.Screen()
window.bgcolor("black")
window.title("Space Invaders")
window.screensize()
window.setup(width=700, height=700)



# Declaring Global Variables
# Variable declarations are really strange in python to me, I'm more familiar with Java variables
# So I'm playing it safe with a little overkill here.
# It's becoming aparent to me that global variables are a really poor way to do things in Python.
global Score; Score = 0
global last_score; last_score = Score
global Vaderdx; Vaderdx = 0
global temphitcount;
global selected; selected = 0
global death_index;
global lives; lives = 3;
global life_one
global life_two
global life_three
global level; level = 1
global first_level; first_level = True

global tank; tank = turtle.Turtle()
global tank_dx; tank_dx = 16

global tank_shot; tank_shot = turtle.Turtle()
global tank_shot_dy
global tank_shot_state

global invaders; armada = 55; invaders = []
for _ in range(armada): invaders.append(turtle.Turtle())

global invader_shot_one; invader_shot_one = turtle.Turtle()
global invader_shot_one_dy
global invader_shot_one_state

global invader_shot_two; invader_shot_two = turtle.Turtle()
global invader_shot_two_dy
global invader_shot_two_state

global menu_pen; menu_pen = turtle.Turtle()
global norm_btn; norm_btn = turtle.Turtle()
global hard_btn; hard_btn = turtle.Turtle()
global game_pen; game_pen = turtle.Turtle()
global score_pen; score_pen = turtle.Turtle()

def ResetGame():
    global lives; lives = 3;
    global selected; selected = 0
    global Score; Score = 0
    global last_score; last_score = Score
    global level; level = 1


def InitializeGame():
    # Registering our two images for future use.
    # These are taken from Christian Thompsons blog, where he creates a much simpler Space Invaders clone.
    # christianthompson.com/node/45
    turtle.register_shape("player.gif")
    turtle.register_shape("invader.gif")

    #Initializing all the global variables
    global tank_shot_dy; tank_shot_dy = 5
    global tank_shot_state; tank_shot_state = "ready"

    global invader_shot_one_dy; invader_shot_one_dy = -1
    global invader_shot_one_state; invader_shot_one_state = "ready"

    global invader_shot_two_dy; invader_shot_two_dy = -1
    global invader_shot_two_state; invader_shot_two_state = "ready"

    global death_index; death_index = 245
    global temphitcount; temphitcount = 0

    # Initializing the player
    tank.penup()
    tank.shape("player.gif")
    tank.speed(0)
    tank.hideturtle()

    # Initializing the player's projectile
    tank_shot.penup()
    tank_shot.speed(0)
    tank_shot.setheading(90)
    tank_shot.color("white")
    tank_shot.shape("square")
    tank_shot.shapesize(.01, .5)
    tank_shot.setposition(0, -500)
    tank_shot.hideturtle()

    # Creating the Invaders as turtle objects
    turtle.tracer(False)
    for invader in invaders:
        invader.penup()
        invader.shape("invader.gif")
        invader.speed(0)
        invader.hideturtle()
    turtle.tracer(True)
    # I turn off tracing here just to speed up the process.


    # Initializing the first Invader projectile
    invader_shot_one.penup()
    invader_shot_one.speed(0)
    invader_shot_one.setheading(270)
    invader_shot_one.color("white")
    invader_shot_one.shape("square")
    invader_shot_one.shapesize(.01, .5)
    invader_shot_one.hideturtle()


    # and the second Invader projectile
    invader_shot_two.penup()
    invader_shot_two.speed(0)
    invader_shot_two.setheading(270)
    invader_shot_two.color("white")
    invader_shot_two.shape("square")
    invader_shot_two.shapesize(.01, .5)
    invader_shot_two.hideturtle()




# Initializing the movement for the player's projectile
def fire_tank_shot():
    global tank_shot_state
    if tank_shot_state == "ready":
        tank_shot_state = "fire"
        x = tank.xcor(); y = tank.ycor()
        tank_shot.setposition(x, y + 10)
        tank_shot.showturtle()

# Initializing the movement for the first invader projectile
def fire_invader_shot_one(invader):
    global invader_shot_one_state
    if invader_shot_one_state == "ready":
        invader_shot_one_state = "fire"
        x = invader.xcor(); y = invader.ycor()
        invader_shot_one.setposition(x, y - 10)
        invader_shot_one.showturtle()

# and for the second
def fire_invader_shot_two(invader):
    global invader_shot_two_state
    if invader_shot_two_state == "ready":
        invader_shot_two_state = "fire"
        x = invader.xcor(); y = invader.ycor()
        invader_shot_two.setposition(x, y - 10)
        invader_shot_two.showturtle()



# Player Movement Functions
def roll_left():
    global tank_dx
    x = tank.xcor(); x -= tank_dx
    if x < -230:
        x = -230
    tank.setx(x)
def roll_right():
    global tank_dx
    x = tank.xcor(); x += tank_dx
    if x > 230:
        x = 230
    tank.setx(x)

turtle.listen()
turtle.onkey(roll_left, "a")
turtle.onkey(roll_right, "d")





# Hit detection function for invader/player collisions, invader/player projectile collisions
def isHit(t1, t2):
    proximity = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    if proximity < 15:
        return True
    else:
        return False

# Hit detection function for projectile on projectile collisions
def isHit2(t1, t2):
    proximity = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    if proximity < 8:
        return True
    else:
        return False

# Hit detection function for invader projectiles on the player
def isHit3(t1, t2):
    proximity = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    if proximity < 12:
        return True
    else:
        return False





# Function for determining whether or not an invader is the lowest in it's column.
def islowest(cy, cx):
    check = 0
    for invader in invaders:
        if cy < invader.ycor() and cx <= invader.xcor() + 5 and cx >= invader.xcor() - 5:
            check += 1
        elif cy > invader.ycor() and cx <= invader.xcor() + 5 and cx >= invader.xcor() - 5:
            check -= 100
    if check >= 0:
        return True
    else:
        return False





# Creating the Menu Screen
def DrawMenu():
    menu_pen.hideturtle()
    menu_pen.penup()
    menu_pen.setposition(-250, -250)
    menu_pen.pendown()
    menu_pen.speed(0)
    menu_pen.color("orange")
    for sides in range(4):
        menu_pen.fd(500)
        menu_pen.lt(90)
    window.bgpic("SpaceInvadersBG.png")
    menu_pen.penup()
    menu_pen.setposition(-245, -248)
    NameString = "Dakota Rowehl"
    menu_pen.write(NameString, False, align="left", font=("Times New Roman", 10, "bold"))
    # Creating the Normal Button
    global norm_btn
    norm_btn.penup()
    norm_btn.setposition(0, -100)
    norm_btn.shape("square")
    norm_btn.shapesize(1.5, 5)
    norm_btn.color("orange")
    norm_btn.stamp()
    norm_btn.hideturtle()
    DifficultyString = "Normal"
    menu_pen.setposition(0, -110)
    menu_pen.color("black")
    menu_pen.write(DifficultyString, False, align="center", font=("Arial", 12, "normal"))
    # Creating the Hard Button
    global hard_btn
    hard_btn.penup()
    hard_btn.setposition(0, -135)
    hard_btn.shape("square")
    hard_btn.shapesize(1.5, 5)
    hard_btn.color("orange")
    hard_btn.stamp()
    hard_btn.hideturtle()
    DifficultyString = "Hard"
    menu_pen.setposition(0, -145)
    menu_pen.color("black")
    menu_pen.write(DifficultyString, False, align="center", font=("Arial", 12, "normal"))


# I'm just calling this function once here to get it going initially
DrawMenu()


# This is the function for writing the score on the screen
def updateScore():
    score_pen.color("orange")
    score_pen.clear()
    score_pen.penup()
    score_pen.setposition(-245, 230)
    score_pen.pendown()
    ScoreString = "Score: %s" %Score
    score_pen.write(ScoreString, False, align="left", font=("Arial", 10, "normal"))




# This function redraws everything for the game
def DrawGame():
    game_pen.hideturtle()
    game_pen.shape("square")
    game_pen.shapesize(2, 2)
    game_pen.penup()
    game_pen.setposition(-250, -250)
    game_pen.color("orange")
    game_pen.pendown()
    global first_level
    if first_level == False:
        game_pen.speed(0)
    for sides in range(4):
        game_pen.fd(500)
        game_pen.lt(90)
    window.bgpic("BattleBG.png")
    game_pen.speed(0)
    game_pen.penup()
    game_pen.setposition(-255, 260)
    game_pen.pendown()
    game_pen.setheading(270)
    tank.penup()
    global lives
    if lives >= 1:
        tank.setposition(230, 270)
        global life_one
        life_one = tank.stamp()
    if lives >= 2:
        tank.setposition(200, 270)
        global life_two
        life_two = tank.stamp()
    if lives == 3:
        tank.setposition(170, 270)
        global life_three
        life_three = tank.stamp()
    tank.showturtle()
    tank.setposition(0, -220)
    for invader in invaders:
        invader.penup()
    l = 230; j = -220; count = 0
    if level == 2:
        l -= 30
    elif level == 3:
        l -= 60
    for invader in invaders:
        invader.setposition(j, l)
        j += 30
        count += 1
        if count == 11:
            l -= 30
            j = -220
            count = 0
        invader.showturtle()
    updateScore()



# This function just clears the screen of the menu
def ClearScreen():
    turtle.resetscreen()
    # Deletes all drawings and backgrounds, resets turtles to initial state.
    tank.hideturtle()
    for invader in invaders:
        invader.hideturtle()
    window.bgpic("")
    menu_pen.hideturtle()
    game_pen.hideturtle()
    norm_btn.hideturtle()
    hard_btn.hideturtle()
    score_pen.hideturtle()

def flash(turt):
    for _ in range(3):
        turt.stamp()
        turt.fd(45)
        turt.undo()
        turt.clearstamps()
        turt.fd(45)
        turt.undo()

def GameOver():
    game_pen.hideturtle()

    # Drawing GAME OVER
    game_pen.penup()
    game_pen.speed(0)
    game_pen.setposition(0, 20)
    game_pen.shape("square")
    game_pen.shapesize(10.7,1.7)
    game_pen.color("orange")
    game_pen.stamp()
    game_pen.shapesize(10.5,1.5)
    game_pen.color("black")
    game_pen.stamp()
    game_pen.setposition(0,0)
    game_pen.pendown()
    game_pen.color("orange")
    DeathString = "GAME OVER"
    game_pen.write(DeathString, False, align="center", font=("Times New Roman", 25, "bold"))

    # Drawing "Returning to menu in..."
    game_pen.penup()
    game_pen.speed(0)
    game_pen.setposition(0, -20)
    game_pen.shape("square")
    game_pen.shapesize(9.6,1.1)
    game_pen.color("orange")
    game_pen.stamp()
    game_pen.shapesize(9.5,1)
    game_pen.color("black")
    game_pen.stamp()
    game_pen.setposition(0,-30)
    game_pen.pendown()
    game_pen.color("orange")
    i = 10
    while i > 0:
        DelayString = "Returning to Menu...      %s" %i
        game_pen.write(DelayString, False, align="center", font=("Times New Roman", 12, "bold"))
        time.sleep(1)
        game_pen.undo()
        i -= 1

def ReDrawGame(L):
    if L == level:
        GameOver()
        ClearScreen()
        ResetGame()
        DrawMenu()
        turtle.onscreenclick(setdifficulty, btn=1)
    if L < level:
        ClearScreen()
        InitializeGame()
        DrawGame()
        Game()


# This function contains the MAINLOOP of the game
def Game():

    turtle.onkey(fire_tank_shot, "space")

    # Again, I plan on getting rid of all the global variables, but I'm new to python so I'm accepting these call blocks
    global death_index; global tank_shot_state; global invader_shot_two_dy
    global Vaderdx; global invader_shot_one_state; global invader_shot_one_dy
    global Score; global invader_shot_two_state; global game_pen;
    global temphitcount; global last_score; global tank_dx; global lives
    global life_three; global life_two; global life_one; global level
    invader_kills = 0; death_list = []; landing = False; isBreak = False
    temp_level = level; initial_Vaderdx = Vaderdx

    while True:

        # To prevent the screen from refreshing after every turtle operation.
        turtle.tracer(False)

        # Loop for all invader functionality
        for k, invader in enumerate(invaders):
            x = invader.xcor()
            x += Vaderdx
            # Preventing dead invaders from moving left and right.
            for i in death_list:
                if i == k:
                    x = invader.xcor()
            invader.setx(x)


            # Moving the invaders back and down after hitting a wall
            if (invader.xcor() > 230 and invader.xcor() < 250 and invader.ycor() < 250) or (invader.xcor() < -230 and invader.xcor() > -250 and invader.ycor() < 250):
                Vaderdx *= -1
                for w, i in enumerate(invaders):
                    y = i.ycor()
                    y -= 10
                    # Preventing dead invaders from traveling down.
                    for z in death_list:
                        if z == w:
                            y = i.ycor()
                    i.sety(y)

            # Firing the invader projectiles
            q = random.randrange(10)
            if (invader.xcor() <= tank.xcor() + 70 and invader.xcor() >= tank.xcor() -70) and islowest(invader.ycor(), invader.xcor()) and invader.xcor() > -250:
                fire_invader_shot_one(invader)
            elif q <= 2 and islowest(invader.ycor(), invader.xcor()) and invader.xcor() > -250:
                fire_invader_shot_two(invader)


            # Collision Detection for the player projectile and the invaders
            if isHit(tank_shot, invader):
                # Moving dead invaders off screen
                Score += 5
                temphitcount += 1
                invader_kills += 1
                if temphitcount > 3:
                    death_index -= 25
                    temphitcount = 1
                if temphitcount == 1:
                    invader.setposition(-320, death_index)
                if temphitcount == 2:
                    invader.setposition(-295, death_index)
                if temphitcount == 3:
                    invader.setposition(-270, death_index)
                # Removing turtles from their lists, turning them off
                #del invaders[k]

                # Instead I added the invaders to a death list, and checked, using enumerate, to prevent them from moving.
                death_list.append(k)



                # Reset the player projectile
                tank_shot_state = "ready"
                tank_shot.hideturtle()
                tank_shot.setposition(0, -400)

                # Increasing the horizontal speed of the invaders based on the number killed.
                if invader_kills == 20:
                    Vaderdx *= 1
                if invader_kills == 42:
                    Vaderdx *= 1
                if invader_kills == 49:
                    Vaderdx *= 1.5
                if invader_kills == 52:
                    Vaderdx *= 1.25
                if invader_kills == 53:
                    Vaderdx *= 1.25
                if invader_kills == 54:
                    Vaderdx *= 1.5
                if invader_kills == 55:
                    global first_level
                    first_level = False
                    level += 1
                    if level > 3:
                        level = 1
                    if lives < 3:
                        lives += 1
                    isBreak = True
                    break

            # Hit detection for the invaders landing, or for a player/invader collision, GAME OVER
            if (isHit(tank, invader) or invader.ycor() < -220) and landing == False:
                landing = True
                Vaderdx = 0
                isBreak = True
                break

            # Collision detection for the invader projectile hits on the player
            if isHit3(tank, invader_shot_two):
                # Reseting the projectile
                invader_shot_two_state = "ready"
                invader_shot_two.sety(700)
                invader_shot_two.hideturtle()

                # Death animation
                x = tank.xcor(); y = tank.ycor(); turtle.tracer(True)
                vdx = Vaderdx; Vaderdx = 0; invader_shot_one_dy = 0; invader_shot_two_dy = 0; tank_dx = 0;
                game_pen.penup()
                game_pen.setposition(x, y)
                game_pen.speed(1)
                game_pen.color("black")
                flash(game_pen)
                lives -= 1;
                if lives == 2:
                    tank.clearstamp(life_three)
                elif lives == 1:
                    tank.clearstamp(life_two)
                elif lives == 0:
                    tank.clearstamp(life_one)
                Vaderdx = vdx; invader_shot_one_dy = -1; invader_shot_two_dy = -1; tank_dx = 16
                turtle.tracer(False)
            if isHit3(tank, invader_shot_one):
                # Reseting the projectile
                invader_shot_one_state = "ready"
                invader_shot_one.sety(700)
                invader_shot_one.hideturtle()

                # Death animation
                x = tank.xcor(); y = tank.ycor(); turtle.tracer(True)
                vdx = Vaderdx; Vaderdx = 0; invader_shot_one_dy = 0; invader_shot_two_dy = 0; tank_dx = 0;
                game_pen.penup()
                game_pen.setposition(x, y)
                game_pen.speed(1)
                game_pen.color("black")
                flash(game_pen)
                lives -= 1;
                if lives == 2:
                    tank.clearstamp(life_three)
                elif lives == 1:
                    tank.clearstamp(life_two)
                elif lives == 0:
                    tank.clearstamp(life_one)
                Vaderdx = vdx; invader_shot_one_dy = -1; invader_shot_two_dy = -1; tank_dx = 16
                turtle.tracer(False)


            # Collision detection for opposing projectiles
            if isHit2(tank_shot, invader_shot_one):
                tank_shot_state = "ready"
                invader_shot_one_state = "ready"
                tank_shot.hideturtle()
                invader_shot_one.hideturtle()
                tank_shot.sety(-400)
                invader_shot_one.sety(400)
            if isHit2(tank_shot, invader_shot_two):
                tank_shot_state = "ready"
                invader_shot_two_state = "ready"
                tank_shot.hideturtle()
                invader_shot_two.hideturtle()
                tank_shot.sety(-400)
                invader_shot_two.sety(400)

        if isBreak or lives == -1:
            death_list.clear()
            Vaderdx = initial_Vaderdx
            ReDrawGame(temp_level)
            break

        # Projectile Motion
        if tank_shot_state == "fire":
            y = tank_shot.ycor()
            y += tank_shot_dy
            tank_shot.sety(y)
            if tank_shot.ycor() > 220:
                tank_shot_state = "ready"
                tank_shot.hideturtle()
        if invader_shot_one_state == "fire":
            y = invader_shot_one.ycor()
            y += invader_shot_one_dy
            invader_shot_one.sety(y)
            if invader_shot_one.ycor() < -220:
                invader_shot_one_state = "ready"
                invader_shot_one.sety(-400)
                invader_shot_one.hideturtle()
        if invader_shot_two_state == "fire":
            y = invader_shot_two.ycor()
            y += invader_shot_two_dy
            invader_shot_two.sety(y)
            if invader_shot_two.ycor() < -220:
                invader_shot_two_state = "ready"
                invader_shot_two.sety(-400)
                invader_shot_two.hideturtle()

        if Score > last_score:
            updateScore()
        last_score = Score

        # To refresh the screen at the end of each loop.
        turtle.update()

# This is a call for a function to decide if the main loop terminated due to a game over or due to the player advancing rounds






# This function assigns values for the two different difficulty levels, and also calls the game function
def setdifficulty(x, y):
    global Vaderdx
    global selected
    if x >= -50 and x <= 50 and y >= -150 and y <= -90:
        if y <= -90 and y >= -120 and selected == 0:
            turtle.onscreenclick(None)
            selected = 1
            Vaderdx = 1
            ClearScreen()
            InitializeGame()
            DrawGame()
            Game()
        elif y <= -120 and y >= -150 and selected == 0:
            turtle.onscreenclick(None)
            selected = 1
            Vaderdx = 1.2
            ClearScreen()
            InitializeGame()
            DrawGame()
            Game()
    else:
        Vaderdx = 0
    return selected



turtle.onscreenclick(setdifficulty, btn=1)








turtle.mainloop()