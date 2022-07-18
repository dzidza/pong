import pew
from random import randint

global angles

angles = {0: [1, 1, 0, -1],  # sharp curve (2x)
          1: [1, 1, 0, 0],  # 45 curve
          2: [1, 1, -1, 0],  # slow curve
          3: [0, 1, 0, 0],  # straight
          4: [1, 1, -1, 0],  # slow curve
          5: [1, 1, 0, 0],  # 45 curve
          6: [1, 1, 0, -1]}  # sharp curve (2x)


def setup_values():
    global pow_x
    global pow_y
    global powerup_available
    global x
    global y
    global blink
    global frame
    global p1x
    global p2x
    global p1y
    global p2y
    global p1w
    global p2w
    global dx
    global dy
    global goal
    global direction_x
    global direction_y
    global current_angle
    global powerup_active
    global powerup_end
    global powerup_duration

    powerup_end = -1
    powerup_duration = 60
    powerup_available = False

    current_angle = 4

    direction_x = 1
    direction_y = 1

    x = 2
    y = 2

    blink = True
    frame = 0

    p1x = 4
    p1y = 0
    p1w = 2

    p2x = 4
    p2y = 8
    p2w = 2

    dx = 1  # add random
    dy = 1

    goal = False

def powerup():
    pow_x = randint(0, 7)
    pow_y = randint(3, 4)
    pow = randint(0, 1)
    return pow_x, pow_y, pow

def powerup_large(direction_y):
    global p1w
    global p2w
    if direction_y == 1:
        p1w = 3
    else:
        p2w = 3

def powerup_small(direction_y):
    global p1w
    global p2w
    if direction_y == 1:
        p2w = 1
    else:
        p1w = 1

def undo_powerup():
    global p1w
    global p2w
    p1w = 2
    p2w = 2

def curve(dx, dy, blink):
    if not blink:
        return dx, dy

    angle = angles[current_angle]
    dx = angle[0] * direction_x
    dy = angle[1] * direction_y
    modificator_x = angle[2] * direction_x
    modificator_y = angle[3] * direction_y

    dx = dx + modificator_x if frame % 4 == 0 else dx
    dy = dy + modificator_y if frame % 4 == 0 else dy

    return dx, dy


def credits():
    screen = pew.Pix.from_text("GO", color=None, bgcolor=0, colors=None)
    pew.show(screen)
    pew.tick(1 / 2)


pew.init()
global screen
screen = pew.Pix()

background = pew.Pix.from_iter((
    (0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0),
))

setup_values()

while True:
    if goal == True:
        credits()
        setup_values()
        continue

    keys = pew.keys()
    screen.blit(background)
    screen.pixel(x, y, (3 if blink else 2) + (4 if screen.pixel(x, y) in {2, 7} else 0))


    if powerup_available:
        screen.pixel(pow_x, pow_y, 2)
        if x == pow_x and pow_y == y:
            powerup_end = frame + powerup_duration
            powerup_available = False
            powerup_active = True
            if pow == 0:
                powerup_large(direction_y)
            elif pow == 1:
                powerup_small(direction_y)

    if frame % 100 == 0 and not powerup_available:
        pow_x, pow_y, pow = powerup()
        screen.pixel(pow_x, pow_y, 3)
        powerup_available = True

    if powerup_end == frame:
        undo_powerup()


    dx, dy = curve(dx, dy, blink)

    if y in [0, 7]:
        dy = 0  # GOOOOOOOAL
        dx = 0
        goal = True

    if (y == 1 and x >= p1x and x <= p1x + p1w - 1 and blink) or \
            (y == 6 and x >= p2x and x <= p2x + p2w - 1 and blink):
        dy = dy * -1
        direction_y = direction_y * -1 if dy != 0 else direction_y

        if (x == p2x and y > 4) or (x == p1x and y < 4):
            # print(f'x: {x}, p2x: {p2x}, direction_x: {direction_x}')
            if current_angle == 3:  # straight angle
                direction_x = -1
            current_angle = current_angle - direction_x if current_angle > 0 and not (
                        current_angle == 6 and direction_x == -1) else current_angle
        elif (x == p2x + p2w - 1 and y > 4) or (x == p1x + p1w - 1 and y < 4):
            # print(f'x: {x}, p2x: {p2x}, p2w: {p2w}, direction_x: {direction_x}')
            if current_angle == 3:  # straight angle
                direction_x = 1
            current_angle = current_angle + direction_x if current_angle < 6 and not (
                        current_angle == 0 and direction_x == -1) else current_angle

    if x in [0, 7] and blink:
        dx = dx * -1
        direction_x = direction_x * -1 if dx != 0 else direction_x

    x = x + dx if blink else x
    y = y + dy if blink else y

    screen.box(3, p1x, p1y, width=p1w, height=1)
    screen.box(3, p2x, p2y, width=p2w, height=1)

    if keys & pew.K_UP and p1x != 8 - p1w:
        p1x = p1x + 1
    elif keys & pew.K_LEFT and p1x != 0:
        p1x = p1x - 1

    if keys & pew.K_O and p2x != 8 - p2w:
        p2x = p2x + 1
    elif keys & pew.K_X and p2x != 0:
        p2x = p2x - 1

    blink = not blink
    pew.show(screen)
    pew.tick(1 / 6)
    frame = frame + 1
