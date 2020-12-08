# File: Breakout.py
"""
This program (once you have finished it) implements the Breakout game.
"""

from pgl import GWindow, GOval, GRect, GState, GLabel
import random

# Constants

GWINDOW_WIDTH = 360               # Width of the graphics window
GWINDOW_HEIGHT = 600              # Height of the graphics window
N_ROWS = 10                       # Number of brick rows
N_COLS = 10                       # Number of brick columns
BRICK_ASPECT_RATIO = 4 / 1        # Width to height ratio of a brick
BRICK_TO_BALL_RATIO = 3 / 1      # Ratio of brick width to ball size
BRICK_TO_PADDLE_RATIO = 2 / 3     # Ratio of brick to paddle width
BRICK_SEP = 2                     # Separation between bricks
TOP_FRACTION = 0.1                # Fraction of window above bricks
BOTTOM_FRACTION = 0.05            # Fraction of window below paddle
N_BALLS = 3                       # Number of balls in a game
TIME_STEP = 1                  # Time step in milliseconds
INITIAL_Y_VELOCITY = 10.0          # Starting y velocity downward
MIN_X_VELOCITY = 5.0              # Minimum random x velocity
MAX_X_VELOCITY = 15.0              # Maximum random x velocity

# Derived constants

BRICK_WIDTH = (GWINDOW_WIDTH - (N_COLS + 1) * BRICK_SEP) / N_COLS
BRICK_HEIGHT = BRICK_WIDTH / BRICK_ASPECT_RATIO
PADDLE_WIDTH = BRICK_WIDTH / BRICK_TO_PADDLE_RATIO
PADDLE_HEIGHT = BRICK_HEIGHT / BRICK_TO_PADDLE_RATIO
PADDLE_Y = (1 - BOTTOM_FRACTION) * GWINDOW_HEIGHT - PADDLE_HEIGHT
BALL_SIZE = BRICK_WIDTH / BRICK_TO_BALL_RATIO
START_X = 2
START_Y = 75

# Function: breakout

def breakout():
    gw = GWindow(GWINDOW_WIDTH, GWINDOW_HEIGHT)
    gs = GState()



    def bricks():

        START_X = 2
        START_Y = 75
        N_COLS = 10
        N_ROWS = 10
        starting_x = (gw.get_width() - (N_COLS * (BRICK_WIDTH + BRICK_SEP)))
        starting_y = (gw.get_height() - (N_ROWS * (BRICK_HEIGHT + BRICK_SEP)))
        COLORS = ['Red', 'Orange', 'Green',
                  'cyan', 'blue']   
            
        #loops for all the bricks
        for row in range(N_ROWS):
            for col in range(N_COLS):
                x = START_X + col * (BRICK_WIDTH + BRICK_SEP)
                y = START_Y + row * (BRICK_HEIGHT + BRICK_SEP)
                brick = GRect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
                brick.set_filled(True)

                #FIX THIS
                #THE COLOR DEFAULTS ALL TO BLUE, although, EVERY 2 ROWS DOWN SHOULD SWITCH
                for i in range(len(COLORS)):
                    brick.set_color(COLORS[i])
                gw.add(brick)
       
    bricks()
#-------------------------------------------------------------------------------
        

    #CODE FOR THE PADDLE

    def paddle():
        gs.paddle = GRect(150, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT)
        gs.paddle.set_color("Black")
        gs.paddle.set_filled(True)
        gw.add(gs.paddle)

        
    paddle()

#CODE FOR DRAWING THE BALL
    def ball():

        ball_x = 170
        ball_y = 300
        
        gs.ball = GOval(ball_x, ball_y, BALL_SIZE, BALL_SIZE)
        gs.ball.set_color("black")
        gs.ball.set_filled(True)
        gw.add(gs.ball)

    ball()

#CODE FOR VELOCITY OF BALL
    def ball_movement():
        
        gs.vx = random.uniform(MIN_X_VELOCITY, MAX_X_VELOCITY)
        if random.uniform(0, 1) < 0.5:
            gs.vx = -gs.vx

        gs.vy = INITIAL_Y_VELOCITY

    ball_movement()


#CLICK ACTION TO START GAME/ BALL MOVEMENT!
    gs.moving = False
    def click_action(e):
        x = e.get_x()
        y = e.get_y()

        if x <= GWINDOW_WIDTH and x >= 0:
            if y <= GWINDOW_HEIGHT and y >= 0:
                gs.moving = True
                
        
    
#PADDLE FOLLOWING THE MOUSE MOVEMENT (ALONG X)
    def mouse_movement(e):
        mx = e.get_x()
        if (mx - PADDLE_WIDTH/ 2) >= 0 and (mx + PADDLE_WIDTH / 2) <= GWINDOW_WIDTH:
            gs.paddle.set_location(mx - PADDLE_WIDTH / 2, PADDLE_Y)


#Checking for colliding objects
            
    def colliding_objects():
        left_upper = gw.get_element_at(gs.ball.get_x(), gs.ball.get_y())
        left_lower = gw.get_element_at(gs.ball.get_x(), gs.ball.get_y() + BALL_SIZE)
        right_upper = gw.get_element_at(gs.ball.get_x() + BALL_SIZE, gs.ball.get_y())
        right_lower = gw.get_element_at(gs.ball.get_x() + BALL_SIZE, gs.ball.get_y() + \
                                        BALL_SIZE)

        if left_upper != None:
            return left_upper
        if left_lower != None:
            return left_lower
        if right_upper != None:
            return right_upper
        if right_lower != None:
            return right_lower
        else:
            return None


    def GameOverLabel():
        gameover = GLabel("GAME OVER!", GWINDOW_WIDTH / 3 + 5, GWINDOW_HEIGHT / 2)
        gameover.set_color("Red")
        gw.add(gameover)
        

#DEFINING EACH TIME STEP!
    def step():

        global N_BALLS
        if gs.moving:
            collider = colliding_objects()

            if gs.ball.get_x() + BALL_SIZE >= GWINDOW_WIDTH:
                gs.vx *= -1
            if gs.ball.get_x() <= 0:
                gs.vx *= -1
            if gs.ball.get_y() <= 0:
                gs.vy *= -1
            if gs.ball.get_y() + BALL_SIZE >= GWINDOW_HEIGHT:
                gw.remove(gs.ball)
                gs.moving = False
                if N_BALLS > 1:
                    ball()
                    N_BALLS -= 1
                elif N_BALLS == 1:
                    GameOverLabel()
            
            if collider != None:
                if collider == gs.paddle:
                    gs.vy *= -1
                else:
                    gw.remove(collider)
                    gs.vy *= -1

            gs.ball.set_bounds(gs.ball.get_x() + gs.vx, gs.ball.get_y() + gs.vy, BALL_SIZE, BALL_SIZE)

        
    gw.add_event_listener('mousemove', mouse_movement)
    gw.add_event_listener('click', click_action)
    timer = gw.set_interval(step, TIME_STEP)
# Startup code

if __name__ == "__main__":
    breakout()
