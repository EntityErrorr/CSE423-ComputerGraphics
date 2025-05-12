from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random


win_width, win_height = 500, 500


diamond_x = random.randint(-230, 230)
diamond_y = 233
diamond_speed = 1.1


table_x = 0
table_y = -250
table_speed = 42
temp_diamond_speed = 0


scr = 0
table_color = [1, 1, 1]
pause = 0
game_over = False


while True:
    diamond_color = [random.randint(0, 1) for _ in range(3)]
    if any(diamond_color):
        break


def convert_line_zone(x, y, cx, cy, zone):
    dx, dy = x - cx, y - cy
    if zone == 0:
        return x, y
    elif zone == 1:
        return dy + cx, dx + cy
    elif zone == 2:
        return -dy + cx, dx + cy
    elif zone == 3:
        return -dx + cx, dy + cy
    elif zone == 4:
        return -dx + cx, -dy + cy
    elif zone == 5:
        return -dy + cx, -dx + cy
    elif zone == 6:
        return dy + cx, -dx + cy
    else:
        return dx + cx, -dy + cy

def convert_circle_zone(x, y, cx, cy, zone):
    dx, dy = x - cx, y - cy
    if zone == 0:
        return dy + cx, dx + cy
    elif zone == 1:
        return x, y
    elif zone == 2:
        return -dx + cx, dy + cy
    elif zone == 3:
        return -dy + cx, dx + cy
    elif zone == 4:
        return -dy + cx, -dx + cy
    elif zone == 5:
        return -dx + cx, -dy + cy
    elif zone == 6:
        return dx + cx, -dy + cy
    else:
        return dy + cx, -dx + cy

def draw_line(x0, y0, x1, y1, cx, cy, size, zones):
    dx, dy = x1 - x0, y1 - y0
    d = 2 * dy - dx
    incrE = 2 * dy
    incrNE = 2 * (dy - dx)
    x, y = x0, y0

    for z in zones:
        draw_point(*convert_line_zone(x, y, cx, cy, z), size)

    while x < x1:
        if d <= 0:
            d += incrE
        else:
            d += incrNE
            y += 1
        x += 1
        for z in zones:
            draw_point(*convert_line_zone(x, y, cx, cy, z), size)

def draw_circle(x0, y0, x1, y1, radius, cx, cy, size, zones):
    d = 1 - radius
    incrE = 2 * (x1 - x0) + 3
    incrSE = 2 * ((x1 - x0) - (y1 - y0)) + 5
    x, y = x0, y0

    while x < x1:
        if d < 0:
            d += incrE
        else:
            d += incrSE
            y -= 1
        x += 1
        for z in zones:
            draw_point(*convert_circle_zone(x, y, cx, cy, z), size)

def draw_point(x, y, size):
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def display():
    global diamond_x, diamond_y, diamond_speed
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 202, 0, 0, 0, 0, 1, 0)

    # Diamond
    glColor3f(*diamond_color)
    draw_circle(diamond_x + 10, diamond_y + 10, diamond_x + 20, diamond_y, 10, diamond_x, diamond_y, 3, range(8))

    # X Button
    glColor3f(1, 0, 0)
    draw_line(230, 230, 250, 250, 230, 230, 1, [0, 2, 4, 6])

    # Back button
    glColor3f(0, 0, 1)
    draw_line(-250, 230, -230, 250, -250, 230, 1, [0, 7])
    draw_line(-250, 230, -210, 230, -210, 230, 1, [0])

    # Pause/play
    glColor3f(0.8, 0.5, 0)
    if pause == 0:
        draw_line(-30, 230, 0, 220, 220, 0, 1, [5])
        draw_line(0, 240, 30, 240, 250, 0, 1, [5])
    else:
        draw_circle(10, 240, 20, 230, 20, 0, 230, 1, [0, 1, 6, 7])
        draw_line(-30, 220, 10, 220, 220, 0, 1, [5])

    # Table
    glColor3f(*table_color)
    draw_line(table_x, table_y + 20, table_x + 80, table_y + 20, table_x, table_y, 3, [0, 3])
    draw_line(table_x, table_y, table_x + 20, table_y, table_x, table_y, 3, [0, 3])
    draw_line(table_x + 20, table_y, table_x + 80, table_y + 20, table_x, table_y, 3, [0, 3])

    glutSwapBuffers()

def animate():
    global diamond_x, diamond_y, diamond_speed, table_color, scr, game_over, diamond_color

    diamond_y -= diamond_speed

    if diamond_y <= -290 and not game_over:
        table_color[1] = table_color[2] = 0
        print("Game Over\nFinal score:", scr)
        game_over = True
    else:
        if (diamond_x + 20 >= table_x and table_x + 80 >= diamond_x) or (diamond_x - 20 <= table_x and table_x - 80 <= diamond_x):
            if diamond_y - 40 <= table_y and table_y + 40 >= diamond_y:
                diamond_x = random.randint(-230, 230)
                diamond_y = 270
                while True:
                    diamond_color = [random.randint(0, 1) for _ in range(3)]
                    if any(diamond_color):
                        break
                scr += 1
                diamond_speed += 0.2
                print("scr:", scr)
    
    glutPostRedisplay()

def handle_arrow_keys(key, x, y):
    global table_x
    if key == GLUT_KEY_LEFT and table_x > -160:
        table_x -= table_speed
    elif key == GLUT_KEY_RIGHT and table_x < 160:
        table_x += table_speed
    glutPostRedisplay()

def handle_mouse_clicks(button, state, x, y):
    global diamond_speed, table_speed, pause, temp_diamond_speed, game_over, scr, diamond_x, diamond_y, table_color

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if 40 >= y and 280 >= x >= 230:
            if diamond_speed > 0:
                temp_diamond_speed = diamond_speed
                diamond_speed = 0
                table_speed = 0
                pause = 1
            else:
                diamond_speed = temp_diamond_speed
                table_speed = 40
                pause = 0
        elif x < 50 and y < 50:
            diamond_y = 250
            diamond_x = random.randint(-230, 230)
            scr = 0
            table_color[1] = table_color[2] = 1
            table_speed = 40
            diamond_speed = 1
            game_over = False
            print("Starting Over")
        elif x >= 450 and y < 50:
            print("Final score:", scr)
            print("Goodbye!!")
            glutLeaveMainLoop()

    glutPostRedisplay()

def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104, 1, 1, 1000.0)


glutInit()
glutInitWindowSize(win_width, win_height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutCreateWindow(b"Catch the Diamond!")

init()
glutDisplayFunc(display)
glutIdleFunc(animate)
glutSpecialFunc(handle_arrow_keys)
glutMouseFunc(handle_mouse_clicks)
glutMainLoop()
