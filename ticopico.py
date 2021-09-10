# Pico-Tico - a Raspberry Pi Pico Powered Tic-Tac-Toe playing Robot
# Kevin McAleer
# September 2021
# Based on Alex Floms Tico Arduino code

from micropython import const
from tft_st7735 import TFT
from time import sleep
from math import acos, cos, sin, atan2, floor, sqrt, pi
from servo import Servo
from random import *
from machine import SPI, Pin, PWM
from sysfont import sysfont

DRAW_HUMAN_MOVE = False
SERIAL_MONITOR_MODE = True

# Servo Pins

LEFT_SERVO_PIN = 5
RIGHT_SERVO_PIN = 6
LIFT_SERVO_PIN = 3

# lift_servo = Servo(minWidth=550, maxWidth=2500, frequency=50)
# left_servo = Servo(minWidth=550, maxWidth=2500, frequency=50)
# right_servo = Servo(minWidth=550, maxWidth=2500, frequency=50)

# Other servo settings
SERVO_LIFT = 1500
# if the pen is not touching the board, this is the value you should change
Z_OFFSET = 525
LIFT0 = 1110 + Z_OFFSET
LIFT1 = 925 + Z_OFFSET
LIFT2 = 735 + Z_OFFSET
LIFT_SPEED = 0.001 # in seconds

lift_servo = PWM(Pin(LIFT_SERVO_PIN))
left_servo = PWM(Pin(LEFT_SERVO_PIN))
right_servo = PWM(Pin(RIGHT_SERVO_PIN))
# left_servo.attach(LEFT_SERVO_PIN)
# right_servo.attach(RIGHT_SERVO_PIN)
lift_servo.freq(50)
lift_servo.duty_u16(LIFT0)

# LCD Pins
TFT_CS = 10
TFT_RST = 8
TFT_DC = 9

spi = SPI(1, baudrate=20000000, polarity=0, phase=0, sck=Pin(10), mosi=Pin(11), miso=None)
tft=TFT(spi,16,17,18)

# Side Servo Calibration
SERVO_LEFT_FACTOR = 690
SERVO_RIGHT_FACTOR = 690

# Zero Position
SERVO_LEFT_NULL = 1950
SERVO_RIGHT_NULL = 815

# Length of arms
L1 = 35.0
L2 = 55.1
L3 = 13.2
L4 = 45.0

# Origin points of left and right servos
O1X = 24.0
O1Y = -25.0
O2X = 49.0
O2Y = -25.0

# Home Cooridinates, where the eraser is
ERASER_X = -11.0
ERASER_Y = 45.5
last_x = ERASER_X
last_y = ERASER_Y

# We will use a list to hold the current state of all the game cells
#  -1 means empty cell
#  0 means O has been drawn
#  1 means X has been drawn

board_values = [-1, -1, -1, -1, -1, -1, -1, -1, -1] 
empty_places = 9

winner = -1

WIN_X = 0
WIN_Y = 80

def setup():
    tft.initr()
    tft.rotation(0)
    tft.fill(aColor=tft.BLACK)
    wink_speed = 0.25

    tft.fillcircle(aPos=[30,30], aRadius=25, aColor=tft.BLUE)
    tft.fillcircle(aPos=[95,30],aRadius=25, aColor=tft.BLUE)
    sleep(wink_speed)
    tft.fillcircle(aPos=[30,30], aRadius=15, aColor=tft.BLACK)
    tft.fillcircle(aPos=[95,30], aRadius=15, aColor=tft.BLACK)
    sleep(wink_speed)
    tft.fillcircle(aPos=[30,30], aRadius=15, aColor=tft.BLUE)
    sleep(wink_speed/2)
    tft.fillcircle(aPos=[30,30], aRadius=15, aColor=tft.BLACK)
    sleep(wink_speed/2)
    tft.fillcircle(aPos=[95,30], aRadius=25, aColor=tft.BLUE)
    sleep(wink_speed/2)
    tft.fillcircle(aPos=[95,30], aRadius=15, aColor=tft.BLACK)
    sleep(wink_speed/2)
    tft.fillcircle(aPos=[30,30], aRadius=15, aColor=tft.BLUE)
    tft.fillcircle(aPos=[95,30], aRadius=15, aColor=tft.BLUE)
    sleep(wink_speed/2)
    tft.fillcircle(aPos=[30,30], aRadius=15, aColor=tft.BLACK)
    tft.fillcircle(aPos=[95,30], aRadius=15, aColor=tft.BLACK)
    sleep(wink_speed)
    tft.text(aPos=[15,80], aString="I'M", aColor=tft.WHITE, aSize=2, nowrap=True, aFont=sysfont)
    tft.text(aPos=[15,100], aString="PICO-TICO", aColor=tft.YELLOW, aSize=2, nowrap=True, aFont=sysfont)

def window(x,y,width,height, title:str):
    tft.fillrect(aStart=[x,y], aSize=[width, height], aColor=tft.WHITE)
    tft.fillrect(aStart=[x+1,y+1], aSize=[width-1, 10], aColor=tft.GRAY)
    tft.rect(aStart=[x,y], aSize=[width, height], aColor=tft.GRAY)
    tft.fillrect(aStart=[x+2,y+2], aSize=[6, 6], aColor=tft.PURPLE)
    
    tft.hline(aStart=[x+10, y+3],aLen=width-14, aColor=tft.BLACK)
    tft.hline(aStart=[x+10, y+5],aLen=width-14, aColor=tft.BLACK)
    tft.hline(aStart=[x+10, y+7],aLen=width-14, aColor=tft.BLACK)

    tft.fillrect(aStart=[x+3,y+12], aSize=[width-8, height-34], aColor=tft.BLACK)

    # tft.text(aPos=[x+10, y+2], aString=title, aColor=tft.RED, aFont=sysfont, aSize=1)

def draw_click_start_message():
    """ Draws the Click Start message """
    
    # tft.rect(aStart=[0,90], aSize=[130,100], aColor=tft.BLACK)
    tft.text(aPos=[20,130], aString="Press S", aColor=tft.YELLOW, aFont=sysfont, nowrap=True)
    tft.text(aPos=[20,140], aString="to Start", aColor=tft.YELLOW, aFont=sysfont, nowrap=True)
    # draw_frame()
    sleep(0.250)

def print_menu():
    print("--==MAIN MENU==--")
    print("==S== Start Game")
    print("==E== Erase")
    print("==F== Draw Frame")
    print("==H== Go Home")

def draw_frame():
    lift(LIFT2)
    sleep_value = 0.1
    v1 = [50,110]
    v2 = [70,110]
    h1 = [45,115]
    h2 = [45,135]

    # Vertical
    draw_to(30,10)
    tft.vline(aStart=v1, aLen=30, aColor=tft.WHITE)
    tft.vline(aStart=v2, aLen=30, aColor=tft.WHITE)
    tft.hline(aStart=h1, aLen=30, aColor=tft.WHITE)
    tft.hline(aStart=h2, aLen=30, aColor=tft.WHITE)
    sleep(sleep_value)
    # draw
    lift(LIFT0)
    draw_to(25, 50)
    lift(LIFT2)
    draw_to(47, 10)
    sleep(sleep_value)
    lift(LIFT0)
    draw_to(45, 50)
    lift(LIFT2)

    # Horizontal
    draw_to(10,23)
    
    lift(LIFT0)
    draw_to(60,23)
    lift(LIFT2)
    draw_to(10, 35)
    lift(LIFT0)
    draw_to(60, 35)
    lift(LIFT2)

def go_home():
    lift_servo.duty_u16(800)
    left_servo.duty_u16(1633)
    right_servo.duty_u16(2289)
    
    lift(LIFT2 - 100) # Lift all the way up
    draw_to(ERASER_X, ERASER_Y)
    lift(LIFT0)
    sleep(0.1)
    # print("Homed")


def sq(value:float):
    """ Returns the square of a number """
    return value * value

def set_xy(t_x:float, t_y:float):
    # print("set_xy, x:",t_x, "y:",t_y)

    sleep(0.001)
    dx, dy, c = 1.0, 1.0, 1.0
    a1, a2, hx, hy = 1.0, 1.0, 1.0, 1.0

    dx = t_x - O1X
    dy = t_y - O1Y

    # print("dx:", dx, "dy:", dy)

    # polar length (c) and angle (a1)
    c = sqrt(sq(dx) + sq(dy))
    # print("c: (sqrt):", c)

    a1 = atan2(dy, dx)
    a2 = return_angle(L1, L2, c)
    left_servo.duty_u16(floor(((a2 + a2 - pi) * SERVO_LEFT_FACTOR) + SERVO_LEFT_NULL))

    # Calculate joinr arm point for triangle of the right servo arm
    a2 = return_angle(L2, L1, c)
    hx = t_x + L3 * cos(((a1 - a2) + 0.621) + pi)
    hy = t_y + L3 * sin(((a1 - a2) + 0.621) + pi)

    # Calculate triangle betwen pen joints, servo_right and arm joint

    dx = hx - O2X
    dy = hy - O2Y
    # print("dx:", dx, "dy:", dy)    
    # c = sqrt((dx * dx) + (dy * dy))
    c = sqrt(sq(dx) + sq(dy))
    a1 = atan2(dy, dx)
    a2 = return_angle(L1, L4, c)

    right_servo.duty_u16(floor((a1 - a2) * SERVO_RIGHT_FACTOR) + SERVO_RIGHT_NULL)

def draw_to(p_x:float, p_y:float):
    global last_x, last_y
    dx =0.0
    dy =0.0
    c =0.0
    i =0

    # dx, dy of new point
    dx = p_x - last_x
    dy = p_y - last_y
    # path length in mm, times 4 equals steps per mm
    c = floor(7 * sqrt(dx * dx + dy * dy))

    # print("c: before", c)
    if (c < 1): 
        c = 1
    
    # print("c:", c)
    for i in range (c):
        # draw line point by point
        # print("drawing line", last_x, i, dx, last_y, dy, c)
        set_xy(last_x + (i * dx / c), last_y + (i * dy / c))

    last_x = p_x
    last_y = p_y

def return_angle(a:float, b:float, c:float):
    """ Returns the cosine rule for angle between c and a"""
    # print("a:", a, "b:", b, "c:",c)
    # acos_a_value = ((a * a) + (c * c) - (b * b)) / (2 * (a * c))
    acos_a_value = ((a**2 + c**2) - (b**2)) / (2 * a*c)

    # assert(acos_a_value) >= -1
    # assert(acos_a_value) <= 1
    # print("acos_a_value:", acos_a_value)
    return acos(acos_a_value)

def lift(lift:float):
    
    global SERVO_LIFT
    if SERVO_LIFT >= lift:
        # print("SERVO_LIFT >= lift", SERVO_LIFT, "lift:", lift)
        while SERVO_LIFT >= lift:
            # print("SERVO_LIFT >= lift", SERVO_LIFT, "lift:", lift)
            SERVO_LIFT -= 1
            lift_servo.duty_u16(SERVO_LIFT)
            sleep(LIFT_SPEED)
    else:
        # print("SERVO_LIFT = ", SERVO_LIFT, "Lift:", lift)
        while (SERVO_LIFT <= lift):
            # print("SERVO_LIFT = ", SERVO_LIFT, "Lift:", lift)
            SERVO_LIFT += 1
            lift_servo.duty_u16(SERVO_LIFT)
            sleep(LIFT_SPEED)

def bogenUZS(bx:float, by:float, radius:float, start:int, end:int, sqee:float):
    inkr = -0.05
    count = 0

    while (start + count) > end:
        draw_to(sqee * radius * cos(start + count) + bx, radius * sin(start + count) + by)
        count += inkr

def bogenGZS(bx:float, by:float, radius:float, start:int, end:int, sqee:float):
    inkr = 0.05
    count = 0

    while (start+count) <= end:
        draw_to(sqee * radius * cos(start+ count)+bx, radius * sin(start+count)+ by)
        count += inkr

def draw_x(bx:float, by:float):
    bx = bx -1
    by = by -1
    # Go
    draw_to(bx, by+1)
    # Draw
    lift(LIFT0)
    draw_to(bx + 10, by + 10)
    # Go
    lift(LIFT2)
    draw_to(bx + 10, by)
    # Draw
    lift(LIFT0)
    draw_to(bx, by + 10)
    lift(LIFT1)

def draw_zero(bx:float, by:float):
    draw_to(bx + 6, by + 3)
    lift(LIFT0)
    bogenGZS(bx + 3.5, by + 5, 5, -0.8, 6.7, 0.5)
    lift(LIFT1)

def erase():
    """ Wipes the game board of any marker pen """
    go_home()
    lift(LIFT0)
    draw_to(70, ERASER_Y)
    draw_to(5, ERASER_Y)

    draw_to(70, 34)
    draw_to(0, 34)
    draw_to(70, 34)

    draw_to(0, 26)
    draw_to(70, 20)

    draw_to(0, 20)
    draw_to(70, 5)

    draw_to(10, 15)
    draw_to(40, 30)

    draw_to(ERASER_X, ERASER_Y)
    lift(LIFT2 - 100)
    print("Erase complete")

def draw_move(move):
    if move == 0:
        draw_frame()
    if move == 1:
        draw_x(15, 40)
    if move == 2:
        draw_x(15, 25)
    if move == 3:
        draw_x(15, 10)
    if move == 4:
        draw_x(30, 40)
    if move == 5:
        draw_x(30, 25)
    if move == 6:
        draw_x(30, 15)
    if move == 7:
        draw_x(50, 40)
    if move == 8: 
        draw_x(50 ,25)
    if move == 9:
        draw_x(50, 10)
    if move == 11:
        draw_zero(15, 40)
    if move == 12:
        draw_zero(15, 25)
    if move == 13:
        draw_zero(15, 10)
    if move == 14:
        draw_zero(30, 40)
    if move == 15:
        draw_zero(30, 25)
    if move == 16:
        draw_zero(30, 10)
    if move == 17:
        draw_zero(50, 40)
    if move == 18:
        draw_zero(50, 25)
    if move == 19:
        draw_zero(50, 10)
    
    if move == 99:
        draw_to(5, 0)

    # Get out of the way
    lift(LIFT2)
    draw_to(10,10)


def record_move(move:int):
    global empty_places, board_values
    if (move >= 1) and (move <= 9):
        board_values[move -1] = 1
        empty_places -= 1
    if (move >= 11) and (move <= 19):
        board_values[move -11] = 0
        empty_places -= 1

def draw():
    """ The Game was a draw"""
    x, y, w, h = 0, 80, 130, 100
    window(x,y,w,h,"Draw")
    tft.text(aPos=[x+35,y+42], aString="-=DRAW=-", aColor=tft.WHITE, aFont=sysfont)
    print("Nobody won - Game was a draw.")

def player_wins():
    # tft.fillrect(aStart=[0,80], aSize=[130,100], aColor=tft.BLACK)
    x, y, w, h = 0, 80, 130, 100
    window(x,y,w,h,"Winner")
    tft.text(aPos=[x+35,y+32], aString="-=YOU=-", aColor=tft.WHITE, aFont=sysfont)
    tft.text(aPos=[x+35,y+42], aString="-=WIN=-", aColor=tft.WHITE, aFont=sysfont)
    
def pico_tico_wins():
    x, y, w, h = 0, 80, 130, 100
    window(x,y,w,h,"Winner")
    tft.text(aPos=[x+25,y+32], aString="-=PICO-TICO=-", aColor=tft.WHITE, aFont=sysfont)
    tft.text(aPos=[x+25,y+42], aString="   -=WINS=-   ", aColor=tft.WHITE, aFont=sysfont)

def check_winner_col(col, player):
    global winner
    # Row
    if (board_values[(col-1)*3] == player) and (board_values[(col-1) * 3 + 1] == player) and (board_values[(col - 1) * 3 + 1] == player) and (board_values[(col -1) * 3 + 2] == player):
        print("--== Winner Col ==--")
        print(player)
        if(player==0):
           player_wins()
        else:
            pico_tico_wins()
        draw_to(55 -20 * (4 - col - 1), 10)
        # Draw
        lift(LIFT0)
        draw_to(55 - 20 * (4 - col -1), 50)
        lift(LIFT2)

        winner = player

def check_winner_row(row:int, player:int):
    global winner
    # row
    if (board_values[row -1] == player) and (board_values[row + 3 -1] == player) and (board_values[row + 6 -1] == player):
        print("--== Winner ROW ==--")
        print(player)
        if player==0:
            player_wins()
        else:
            pico_tico_wins()
        draw_to(10, 43 - 14 * (row - 1))
        # Draw
        lift(LIFT0)
        draw_to(60,43 - 13 * (row -1))
        lift(LIFT2)

        winner = player

def reply_move():
    rand_empty_place = randrange(empty_places) + 1
    empty_places_found = 0
    for i in range(0,9):
        if board_values[i] == -1:
            # We found an empty place
            empty_places_found += 1
            if empty_places_found == rand_empty_place:
                draw_move(i + 1)
                record_move(i + 1)
                print("Replying to: ")
                print(i+1)

def check_winner_diag(diag:int, player:int):
    global winner
    # check which diagonal
    if diag == 1:
        if (board_values[1 -1] == player) and (board_values[5 -1] == player) and (board_values[9 - 1] == player):
            print("--== Winner DIAGONAL 1 ==--")
            print(player)
            if player==0:
                player_wins()
            else:
                pico_tico_wins()
            draw_to(60,10)
            lift(LIFT0)
            draw_to(15,45)
            lift(LIFT2)

            winner = player
    else:
        if (board_values[7 - 1] == player) and (board_values[5-  1] == player) and (board_values[3 - 1] == player):
            print("--== Winner Diagonal 2 ==0--")
            print(player)
            if player == 0:
                player_wins()
            else:
                pico_tico_wins()
            draw_to(10,10)
            lift(LIFT0)
            draw_to(60,50)
            lift(LIFT2)
            winner = player

def print_board():
    """ Print the board to the console """
    board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
    count = 0
    for cell in board_values:
        if cell == -1: 
            board[count] = " "
        if cell == 1: 
            board[count] = "X"
        if cell == 0: 
            board[count] = "O"
        count += 1
   
    print(" Current Game Board  |  ID Number of the cells")
    print(" ",board[9-1], "|", board[6-1], "|", board[3-1],  "       9 | 6 | 3")
    print(" ---+---+---      ---+---+---")
    print(" ",board[8-1], "|", board[5-1], "|", board[2-1],  "       8 | 5 | 2")
    print(" ---+---+---      ---+---+---")
    print(" ",board[7-1], "|", board[4-1], "|", board[1-1],  "       7 | 4 | 1 ")
    print("")

def start_game():
    global winner, empty_places
    print("====GAME IS ON====")
    x,y,width, height = 0, 80, 130, 100

    window(x,y,width,height, "LETS GO")
    # tft.fillrect(aStart=[0,80], aSize=[130,100], aColor=tft.BLACK)
    tft.text(aPos=[x+10,y+20], aString="GAME", aFont=sysfont, aColor=tft.WHITE)
    tft.text(aPos=[x+10,y+40], aString="IS", aFont=sysfont, aColor=tft.WHITE)
    tft.text(aPos=[x+10,y+60], aString="ON", aFont=sysfont, aColor=tft.WHITE)
    sleep(0.5)

    print("Erasing")
    erase()

    print("Drawing Frame")
    draw_frame()
    sleep(1)

    print("Pico-Tico is making the first move")
    draw_move(5)
    record_move(5)

    # as long as the game is running we need to repeat this loop
    while (winner == -1) and (empty_places > 0):
        # print("Winner", winner, "empty places", empty_places)
        
        print_board()
        print("Human, enter your move(1-9")

        x, y, w, h = 0, 80, 130, 100
        window(x,y,w,h,"Your move")
        # tft.fillrect(aStart=[0,80], aSize=[130,100],aColor=tft.BLACK)
        tft.text(aPos=[x+10,y+32], aString="YOUR", aColor=tft.RED, aFont=sysfont)
        tft.text(aPos=[x+10,y+42], aString="MOVE", aColor=tft.RED, aFont=sysfont)
        move_to = 0
        tft.fillcircle(aPos=[30,30],aRadius=15, aColor=tft.RED)
        tft.fillcircle(aPos=[95,30],aRadius=15, aColor=tft.BLACK)

        if SERIAL_MONITOR_MODE:
            move_to = int(input(">"))
        
        # check the move_to value is valid
        if (move_to > 0) and (move_to < 10):
            if board_values[move_to -1] == -1:
                print("Moving to: ", move_to)

                if DRAW_HUMAN_MOVE:
                    draw_move(move_to + 10)
                
                # Record the move
                record_move(move_to + 10)

                for n in range(1,3):
                    check_winner_row(n,0)
                    check_winner_col(n,0)
                    # check_winner_row(2,0)
                    # check_winner_row(3,0)

                    # check_winner_col(1,0)
                    # check_winner_col(2,0)
                    # check_winner_col(3,0)

                check_winner_diag(1,0)
                check_winner_diag(2,0)

                if (winner == -1) and (empty_places > 0):
                    # clean text area

                    x, y, w, h = 0, 80, 130, 100
                    window(x,y,w,h,"Your move")
                    tft.text(aPos=[x+10,y+32], aString="PICO-TICO", aColor=tft.WHITE, aFont=sysfont)
                    tft.text(aPos=[x+10,y+42], aString="MOVE", aColor=tft.WHITE, aFont=sysfont)
                    tft.fillcircle(aPos=[30,30],aRadius=15, aColor=tft.BLACK)
                    tft.fillcircle(aPos=[95,30], aRadius=15, aColor=tft.YELLOW)
                    reply_move()

                for n in range(1,3):
                    check_winner_row(n,1)
                    check_winner_col(n,1)
                    # check_winner_row(2,1)
                    # check_winner_row(3,1)

                    # check_winner_col(1,1)
                    # check_winner_col(2,1)
                    # check_winner_col(3,1)

                check_winner_diag(1,1)
                check_winner_diag(2,1)
            
            else:
                print("Already taken!")

                x, y, w, h = 0, 80, 130, 100
                window(x,y,w,h,"Your move")
                tft.text(aPos=[x+10,y+32], aString="PLACE", aColor=tft.RED, aFont=sysfont)
                tft.text(aPos=[x+10,y+42], aString="TAKEN", aColor=tft.RED, aFont=sysfont)
                sleep(0.25)
            if (winner == -1) and (empty_places == 0):
                draw()
    print_board()
    go_home()

# main loop
setup()
draw_click_start_message()
while True:
    
    print_menu()
    user_input = input("> ")
    user_input = user_input.upper()

    if user_input not in ['S','E','F','H']:
        print("===WRONG INPUT===")
    else:
        if user_input=='H':
            go_home()
        if user_input=="E":
            erase()
        if user_input=="F":
            draw_frame()
        else:
            start_game()

    # Reset Game Variables
    winner = -1
    empty_places = 9

    # clear the board
    for _ in range(9):
        board_values[_] = -1

print("end or program")