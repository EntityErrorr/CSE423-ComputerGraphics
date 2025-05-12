from OpenGL.GL import * 
from OpenGL.GLUT import *
from OpenGL.GLU import * 
import random
import time



#TASK-1

# global vars (window)
w_width = 1280
w_height = 720

# background color
color = [1, 1, 1, 1.0]
border_color = [0, 0, 0, 1.0]

# colors 
lavender = [0.58, 0.44, 0.86, 1.0]
midnight_blue = [0.1, 0.1, 0.44, 1.0]
rose = [0.85, 0.53, 0.58, 1.0] 
moondust = [0.84, 0.84, 0.86, 1.0]
twilight_sky = [0.25, 0.4, 0.6, 1.0]

# points of the house
main_roof_top = [(419, 284), (600, 180), (730, 255)]
main_roof_base = [(435, 304), (600, 208), (714,272)]

side_roof_top = [(648, 336), (758, 226), (861, 329)]
side_roof_base = [(666, 349), (758,257), (850,349)]

left_wall_edge = [(441, 539), (441, 299)]
right_wall_edge = [(836,494),(836,336)]
center_wall_edge = [(680,494),(680,335)]
floor_joint_line = [(441,445),(680,445)]
lower_step_area = [(661, 539), (661, 517),(856, 517), (856, 539)]
upper_step_area = [(674, 517),(674, 494),(843, 494),(843, 517)]
main_entrance_frame = [(720, 494), (720, 350), (797, 350), (797, 494)]
inner_door_frame = [(737, 494), (737, 367), (781, 367), (781, 494)]

window = [(510, 410), (510, 309),(630, 309), (630, 410)]
window_outer_frame = [(500, 420), (500, 300),(640, 300), (640, 420)]

chimney_body = [(474, 253), (474, 200), (533, 200), (533, 218)]
chimney_cap = [(464, 200), (464, 170), (543, 170), (543, 200)]

# for rain
num_rainxs = 120
rainxs = []
rainxs = [{"x": random.randint(0, w_width), "y": random.randint(0, w_height)} for n in range(num_rainxs)]
rainx_speed = 2
rainx_color = [0.5,0.5, 1, 1]

def draw_rainxs():
    global rainxs, rainx_color
    glColor4f(rainx_color[0], rainx_color[1], rainx_color[2], rainx_color[3])
    glLineWidth(3) 
    for i in rainxs:
        glBegin(GL_LINES)
        glVertex2f(i["x"], i["y"])
        glVertex2f(i["x"], i["y"] + 12) 
        glEnd()

def draw_lines(x, y): 
    glColor4f(border_color[0], border_color[1], border_color[2], border_color[3])
      
    glLineWidth(5)  

    glBegin(GL_LINES)
    glVertex2f(x[0], x[1])
    glVertex2f(y[0], y[1])
    glEnd()

def draw_triangle(x, y, z, color,):
    glColor4f(color[0], color[1], color[2], color[3])
    glBegin(GL_TRIANGLES)
    glVertex2f(x[0], x[1])
    glVertex2f(y[0], y[1])
    glVertex2f(z[0], z[1])
    glEnd()


def draw():
    #background
    draw_triangle(center_wall_edge[1], side_roof_base[1], right_wall_edge[1], midnight_blue)
    draw_triangle(left_wall_edge[0], left_wall_edge[1], (center_wall_edge[0][0], left_wall_edge[0][1]), midnight_blue)
    draw_triangle(left_wall_edge[1],main_roof_base[2], (center_wall_edge[0][0], left_wall_edge[0][1]), midnight_blue)
    draw_triangle(main_roof_base[0], main_roof_base[1], main_roof_base[2], midnight_blue)

    draw_triangle(center_wall_edge[0],center_wall_edge[1], right_wall_edge[0], midnight_blue)
    draw_triangle(center_wall_edge[1], right_wall_edge[1], right_wall_edge[0], midnight_blue)

    # chimney_body
    draw_triangle(chimney_body[0], chimney_body[1], chimney_body[2], midnight_blue)
    draw_triangle(chimney_body[0], chimney_body[2], chimney_body[3], midnight_blue)

    # color of roof
    draw_triangle(main_roof_top[0], main_roof_top[1], main_roof_base[1], rose)
    draw_triangle(main_roof_top[0], main_roof_base[1], main_roof_base[0], rose)
    draw_triangle(main_roof_top[1], main_roof_top[2], main_roof_base[2], rose)
    draw_triangle(main_roof_top[1], main_roof_base[2], main_roof_base[1], rose)

    draw_triangle(side_roof_top[0], side_roof_top[1], side_roof_base[1], rose)
    draw_triangle(side_roof_top[0], side_roof_base[1], side_roof_base[0], rose)
    draw_triangle(side_roof_top[1], side_roof_top[2], side_roof_base[2], rose)
    draw_triangle(side_roof_top[1], side_roof_base[2], side_roof_base[1], rose)

    # roof (upper)
    draw_lines(main_roof_top[0], main_roof_top[1])
    draw_lines(main_roof_top[1], main_roof_top[2])
    draw_lines(main_roof_base[0], main_roof_base[1])
    draw_lines(main_roof_base[1], main_roof_base[2])
    draw_lines(main_roof_base[0], main_roof_top[0])
    # roof (lower)
    draw_lines(side_roof_top[0], side_roof_top[1])
    draw_lines(side_roof_top[1], side_roof_top[2])
    draw_lines(side_roof_base[0], side_roof_base[1])
    draw_lines(side_roof_base[1], side_roof_base[2])
    draw_lines(side_roof_base[0], side_roof_top[0])
    draw_lines(side_roof_base[2], side_roof_top[2])


    # botom left
    draw_triangle(left_wall_edge[0], floor_joint_line[0], floor_joint_line[1], lavender)
    draw_triangle(left_wall_edge[0], floor_joint_line[1],(floor_joint_line[1][0], left_wall_edge[0][1]),lavender)

    # borders
    draw_lines(left_wall_edge[0], left_wall_edge[1])
    draw_lines(left_wall_edge[0], lower_step_area[0])
    draw_lines(right_wall_edge[0], right_wall_edge[1])
    draw_lines(center_wall_edge[0], center_wall_edge[1])
    draw_lines(floor_joint_line[0], floor_joint_line[1])


    # for stair
    draw_triangle(lower_step_area[0], lower_step_area[1], lower_step_area[2], twilight_sky)
    draw_triangle(lower_step_area[0], lower_step_area[2], lower_step_area[3], twilight_sky)
    draw_lines(lower_step_area[0], lower_step_area[1])
    draw_lines(lower_step_area[1], lower_step_area[2])
    draw_lines(lower_step_area[2], lower_step_area[3])
    draw_lines(lower_step_area[0], lower_step_area[3])
    
    draw_triangle(upper_step_area[0], upper_step_area[1], upper_step_area[2], twilight_sky)
    draw_triangle(upper_step_area[0], upper_step_area[2], upper_step_area[3], twilight_sky)
    draw_lines(upper_step_area[0], upper_step_area[1])
    draw_lines(upper_step_area[1], upper_step_area[2])
    draw_lines(upper_step_area[2], upper_step_area[3])
    draw_lines(upper_step_area[0], upper_step_area[3])
    


    # for main_entrance_frame
    draw_triangle(main_entrance_frame[0], main_entrance_frame[1], main_entrance_frame[2], lavender)
    draw_triangle(main_entrance_frame[0], main_entrance_frame[2], main_entrance_frame[3], rose)
    draw_lines(main_entrance_frame[0], main_entrance_frame[1])
    draw_lines(main_entrance_frame[1], main_entrance_frame[2])
    draw_lines(main_entrance_frame[2], main_entrance_frame[3])
    draw_lines(main_entrance_frame[0], main_entrance_frame[3])
    

    # main_entrance_frame (small)
    draw_triangle(inner_door_frame[0], inner_door_frame[1], inner_door_frame[2], moondust)
    draw_triangle(inner_door_frame[0], inner_door_frame[2], inner_door_frame[3], moondust)
    draw_lines(inner_door_frame[0], inner_door_frame[1])
    draw_lines(inner_door_frame[1], inner_door_frame[2])
    draw_lines(inner_door_frame[2], inner_door_frame[3])
    draw_lines(inner_door_frame[0], inner_door_frame[3])

    # border (window)
    draw_triangle(window_outer_frame[0], window_outer_frame[1], window_outer_frame[2], lavender)
    draw_triangle(window_outer_frame[0], window_outer_frame[2], window_outer_frame[3], rose)

    # color (window)
    draw_triangle(window[0], window[1], window[2], moondust)
    draw_triangle(window[0], window[2], window[3], moondust)

    # 1st window
    draw_lines(window[0], window[1])
    draw_lines(window[1], window[2])
    draw_lines(window[2], window[3])
    draw_lines(window[0], window[3])

    # border (window)
    draw_lines(window_outer_frame[0], window_outer_frame[1])
    draw_lines(window_outer_frame[1], window_outer_frame[2])
    draw_lines(window_outer_frame[2], window_outer_frame[3])
    draw_lines(window_outer_frame[0], window_outer_frame[3])

    # tint (window)
    draw_triangle((window[0][0] + 10, window[0][1] - 10),(window[1][0]+10, window[1][1]+10),(window[3][0]-50, window[3][1]-10), color)

    # chimney_body
    draw_lines(chimney_body[0], chimney_body[1])
    draw_lines(chimney_body[1], chimney_body[2])
    draw_lines(chimney_body[2], chimney_body[3])

    # chimney_body (top)
    draw_triangle(chimney_cap[0], chimney_cap[1], chimney_cap[2], rose)
    draw_triangle(chimney_cap[0], chimney_cap[2], chimney_cap[3], rose)
    draw_lines(chimney_cap[0], chimney_cap[1])
    draw_lines(chimney_cap[1], chimney_cap[2])
    draw_lines(chimney_cap[2], chimney_cap[3])
    draw_lines(chimney_cap[0], chimney_cap[3])

    draw_rainxs()

def iterate():
    global w_width, w_height
    glViewport(0, 0, w_width, w_height) 
    glMatrixMode(GL_PROJECTION)  
    glLoadIdentity()       
    glOrtho(0, w_width, w_height, 0, 0.0, 1.0) 
    glMatrixMode(GL_MODELVIEW)   
    glLoadIdentity()            


def show_screen():
    global color

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) 
    glLoadIdentity()   

    # setup related properties
    iterate()
       
    draw()
    glutSwapBuffers()



def animation():
    global rainxs

    for x in rainxs:
        x["y"] += rainx_speed  
        if x["y"] > w_height:  
            x["y"] = 0
            x["x"] = random.randint(0, w_width) 

    glutPostRedisplay()

def press_key(key, x, y):
    print("x: ", x, "y: ", y)
    global color, border_color, rainx_color

    if key == b"m":
        
        color[0] += 0.25
        color[1] += 0.25
        color[2] += 0.25
        if color[0] >= 1 or color[1] >= 1 or color[2] >= 1:
            color = [1,1,1, 1.0]

        border_color[0] -= 0.35
        border_color[1] -= 0.35
        border_color[2] -= 0.35
        if border_color[0] <= 0 or border_color[1] <= 0 or border_color[2] <= 0:
            border_color = [0,0,0, 1.0]
        
        #rainx color for white backgrounds
        if color[0] >.25 and color[1] >.25 and color[2] >.25:
            rainx_color = [0.5,0.5, 1, 1.0]

    if key == b"n":
        
        color[0] -= 0.25
        color[1] -= 0.25
        color[2] -= 0.25
        if color[0] <= 0 or color[1] <= 0 or color[2] <= 0:
            color = [0,0,0, 1.0]

        
        border_color[0] += 0.35
        border_color[1] += 0.35
        border_color[2] += 0.35
        if border_color[0] >= 1 or border_color[1] >= 1 or border_color[2] >= 1:
            border_color = [1,1,1, 1.0]
        
        #Special border + rainx for black background
        if color == [0,0,0, 1.0]:
            border_color = [0,0,0, 1.0]
            rainx_color = [173/255, 216/255, 230/255, 1.0]
        
        


    glClearColor(color[0], color[1], color[2], color[3]) 
    glutPostRedisplay()
    
def special_press_key(key, x, y):
    global rainxs, rainx_speed
    if key == GLUT_KEY_LEFT:

        # rain (to the left)
        for x in rainxs:
            x["x"] -= 5
            x["y"] += rainx_speed 


    elif key == GLUT_KEY_RIGHT:
        # rain (to the right)
        for x in rainxs:
            x["x"] += 5
            x["y"] += rainx_speed
    
    glutPostRedisplay()

def mouse_button(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        print("Left mouse clicked at", x, y)
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        print("Right mouse clicked at", x, y)

    glutPostRedisplay()



glutInit()    
glutInitDisplayMode(GLUT_RGBA) 
glutInitWindowSize(w_width, w_height) 
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"House in Rainfall")
glClearColor(color[0], color[1], color[2], color[3]) 
glutDisplayFunc(show_screen)


glutIdleFunc(animation)
glutKeyboardFunc(press_key)
glutSpecialFunc(special_press_key)
glutMouseFunc(mouse_button)


glutMainLoop()  



#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------



#TASK-2



screen_width = 1280
screen_height = 720


boundary = [(100, 620), (100, 100), (1180, 100), (1180, 620)]
x_limit = 1180
y_limit = 620
x_start = 100
y_start = 100


motion_directions = [(-1, 1), (1, 1), (1, -1), (-1, -1)]
speed = 0.2
upper_speed = 100
lower_speed = 0.05
paused = False
flashing_enabled = False
flash_flag = False
last_flash_time = time.time()
flash_interval = 0.3
dot_radius = 12


background_color = [1, 1, 1, 1.0]
dark_color = [0, 0, 0, 1.0]
bouncing_dots = []


class BouncingDot:
    def __init__(self, xpos, ypos, tone, move_vector):
        self.posX = xpos
        self.posY = ypos
        self.original_color = tone[:]
        self.current_color = tone[:]
        self.move_vector = move_vector

    def toggle_flash(self):
        if self.current_color == self.original_color:
            self.current_color = [0.0, 0.0, 0.0, 1.0]
        else:
            self.current_color = self.original_color[:]


def plot_dot(x, y, rgba):
    global dot_radius
    glColor4f(*rgba)
    glPointSize(dot_radius)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def draw_box(c1, c2, c3, c4, col):
    glColor4f(*col)
    glBegin(GL_TRIANGLES)
    glVertex2f(*c1)
    glVertex2f(*c2)
    glVertex2f(*c3)
    glVertex2f(*c1)
    glVertex2f(*c3)
    glVertex2f(*c4)
    glEnd()


def render_scene():
    draw_box(boundary[0], boundary[1], boundary[2], boundary[3], dark_color)
    for dot in bouncing_dots:
        plot_dot(dot.posX, dot.posY, dot.current_color)
    if flashing_enabled:
        handle_blinking()


def setup_camera():
    glViewport(0, 0, screen_width, screen_height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, screen_width, screen_height, 0, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def render_frame():
    global background_color
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_camera()
    render_scene()
    glutSwapBuffers()


def update_positions():
    global bouncing_dots, x_limit, y_limit, x_start, y_start, speed, paused
    if not paused:
        for dot in bouncing_dots:
          
            speed = max(lower_speed, min(speed, upper_speed))

            next_x = dot.posX + dot.move_vector[0] * speed
            next_y = dot.posY + dot.move_vector[1] * speed


            if next_x >= x_limit or next_x <= x_start:
                dot.move_vector = (-dot.move_vector[0], dot.move_vector[1])
                dot.posX = max(x_start, min(x_limit, next_x))
            else:
                dot.posX = next_x

            if next_y >= y_limit or next_y <= y_start:
                dot.move_vector = (dot.move_vector[0], -dot.move_vector[1])
                dot.posY = max(y_start, min(y_limit, next_y))
            else:
                dot.posY = next_y

    glutPostRedisplay()


def key_input(key, x, y):
    global paused, flashing_enabled
    if key == b' ':
        paused = not paused
        flashing_enabled = False
    glutPostRedisplay()


def arrow_input(key, x, y):
    global speed, paused
    if not paused:
        if key == GLUT_KEY_UP:
            speed += 0.1
        elif key == GLUT_KEY_DOWN:
            speed -= 0.1
    glutPostRedisplay()


def handle_blinking():
    global flash_flag, last_flash_time, flash_interval, bouncing_dots
    now = time.time()
    if now - last_flash_time >= flash_interval:
        for dot in bouncing_dots:
            dot.toggle_flash()
        flash_flag = not flash_flag
        last_flash_time = now


def mouse_click(button, state, mx, my):
    global bouncing_dots, x_limit, y_limit, x_start, y_start, paused, flash_flag, flashing_enabled
    if not paused:
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            flashing_enabled = True
        elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
            if x_start < mx < x_limit and y_start < my < y_limit:
                random_rgba = [random.random(), random.random(), random.random(), 1.0]
                direction = random.choice(motion_directions)
                new_dot = BouncingDot(mx, my, random_rgba, direction)
                bouncing_dots.append(new_dot)
    glutPostRedisplay()



glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(screen_width, screen_height)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"Amazing Box")
glClearColor(*background_color)
glutDisplayFunc(render_frame)
glutIdleFunc(update_positions)
glutKeyboardFunc(key_input)
glutSpecialFunc(arrow_input)
glutMouseFunc(mouse_click)
glutMainLoop()
