from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
import math
import random
import time

# Window and Field Configuration
WIN_WIDTH = 900
WIN_HEIGHT = 700
FIELD_HALF_SIZE = 650
FIELD_EXTRA = 100
field_of_view = 110

# Camera Settings
cam_angle = 0
cam_radius = 700
cam_height = 700

# Game Modes
is_first_person = False
is_cheat = False
cheat_vision = False
game_over = False

# Character State
char_position = [0, 0, 0]
char_angle = 0
char_speed = 12
char_turn_speed = 6
char_life = 5
char_score = 0

# Projectile State
projectiles = []
missed_shots = 0
max_misses = 12
shot_speed = 1.2

# Cheat Mode Timers
last_shot_time = 0
shot_cooldown = 1.2

# Opponent Properties
opponents = []
opponent_scale = 1.0
pulse_timer = 0
opponent_speed = 0.03
initial_opponents = 6

# Weapon mount offset (matching original gun_point)
weapon_mount = [30, 15, 80]


def render_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WIN_WIDTH, 0, WIN_HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for x in text:
        glutBitmapCharacter(font, ord(x))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def render_field():
    glBegin(GL_QUADS)
    for i in range(-FIELD_HALF_SIZE, FIELD_HALF_SIZE + 1, 100):
        for j in range(-FIELD_HALF_SIZE, FIELD_HALF_SIZE + 1, 100):
            if (i + j) % 200 == 0:
                glColor3f(1, 1, 1)
            else:
                glColor3f(0.7, 0.5, 0.95)
            glVertex3f(i, j, 0)
            glVertex3f(i + 100, j, 0)
            glVertex3f(i + 100, j + 100, 0)
            glVertex3f(i, j + 100, 0)

    # Walls: Left, Right, Bottom, Top
    glColor3f(0, 1, 0)
    glVertex3f(-FIELD_HALF_SIZE, -FIELD_HALF_SIZE, 0)
    glVertex3f(-FIELD_HALF_SIZE, FIELD_HALF_SIZE + FIELD_EXTRA, 0)
    glVertex3f(-FIELD_HALF_SIZE, FIELD_HALF_SIZE + FIELD_EXTRA, 100)
    glVertex3f(-FIELD_HALF_SIZE, -FIELD_HALF_SIZE, 100)

    glColor3f(0, 0, 1)
    glVertex3f(FIELD_HALF_SIZE + FIELD_EXTRA, -FIELD_HALF_SIZE, 0)
    glVertex3f(FIELD_HALF_SIZE + FIELD_EXTRA, FIELD_HALF_SIZE + FIELD_EXTRA, 0)
    glVertex3f(FIELD_HALF_SIZE + FIELD_EXTRA, FIELD_HALF_SIZE + FIELD_EXTRA, 100)
    glVertex3f(FIELD_HALF_SIZE + FIELD_EXTRA, -FIELD_HALF_SIZE, 100)

    glColor3f(1, 1, 1)
    glVertex3f(-FIELD_HALF_SIZE, FIELD_HALF_SIZE + FIELD_EXTRA, 0)
    glVertex3f(FIELD_HALF_SIZE + FIELD_EXTRA, FIELD_HALF_SIZE + FIELD_EXTRA, 0)
    glVertex3f(FIELD_HALF_SIZE + FIELD_EXTRA, FIELD_HALF_SIZE + FIELD_EXTRA, 100)
    glVertex3f(-FIELD_HALF_SIZE, FIELD_HALF_SIZE + FIELD_EXTRA, 100)

    glColor3f(0, 1, 1)
    glVertex3f(-FIELD_HALF_SIZE, -FIELD_HALF_SIZE, 0)
    glVertex3f(FIELD_HALF_SIZE + FIELD_EXTRA, -FIELD_HALF_SIZE, 0)
    glVertex3f(FIELD_HALF_SIZE + FIELD_EXTRA, -FIELD_HALF_SIZE, 100)
    glVertex3f(-FIELD_HALF_SIZE, -FIELD_HALF_SIZE, 100)
    glEnd()


def configure_camera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(field_of_view, float(WIN_WIDTH)/WIN_HEIGHT, 0.1, 2000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if is_first_person:
        rad = math.radians(char_angle)
        eye_x = char_position[0] + weapon_mount[0]/2 * math.sin(rad) - weapon_mount[1]*math.cos(rad)
        eye_y = char_position[1] - weapon_mount[0]/2 * math.cos(rad) - weapon_mount[1]*math.sin(rad)
        eye_z = char_position[2] + weapon_mount[2] + 20
        if cheat_vision:
            cx = eye_x + math.sin(rad)*100
            cy = eye_y + math.cos(rad)*100
            cz = eye_z
        else:
            cx = eye_x - math.sin(-rad)*100
            cy = eye_y - math.cos(-rad)*100
            cz = eye_z
        gluLookAt(eye_x, eye_y, eye_z, cx, cy, cz, 0, 0, 1)
    else:
        rad = math.radians(cam_angle)
        x = cam_radius * math.sin(rad)
        y = cam_radius * math.cos(rad)
        z = cam_height
        gluLookAt(x, y, z, 0, 0, 0, 0, 0, 1)


def render_character():
    glPushMatrix()
    glTranslatef(*char_position)
    glRotatef(char_angle, 0, 0, 1)
    if game_over:
        glRotatef(-90, 1, 0, 0)

    # Legs
    glColor3f(0,0,1)
    gluCylinder(gluNewQuadric(),5,10,50,10,10)
    glTranslatef(30,0,0)
    gluCylinder(gluNewQuadric(),5,10,50,10,10)

    # Body
    glTranslatef(-15,0,70)
    glColor3f(85/255,108/255,47/255)
    glutSolidCube(40)

    # Head
    glTranslatef(0,0,40)
    glColor3f(0,0,0)
    gluSphere(gluNewQuadric(),20,10,10)

    # Left Arm
    glTranslatef(20,-60,-30)
    glRotatef(-90,1,0,0)
    glColor3f(254/255,223/255,188/255)
    gluCylinder(gluNewQuadric(),4,8,50,10,10)

    # Right Arm
    glRotatef(90,1,0,0)
    glTranslatef(-40,0,0)
    glRotatef(-90,1,0,0)
    gluCylinder(gluNewQuadric(),4,8,50,10,10)

    # Gun (exact original offsets)
    glRotatef(90,1,0,0)
    glTranslatef(20,-40,0)
    glRotatef(-90,1,0,0)
    glColor3f(192/255,192/255,192/255)
    gluCylinder(gluNewQuadric(),1,10,80,10,10)

    glPopMatrix()


def render_projectile(x,y,z):
    glPushMatrix()
    glTranslatef(x,y,z)
    glRotatef(-90,1,0,0)
    glColor3f(1,0,0)
    glutSolidCube(10)
    glPopMatrix()


def shoot_projectile():
    global projectiles
    rad = math.radians(char_angle+45)
    if is_first_person:
        x = char_position[0] + weapon_mount[0]*math.sin(rad) - weapon_mount[1]*math.cos(rad)
        y = char_position[1] - weapon_mount[0]*math.cos(rad) - weapon_mount[1]*math.sin(rad)
        z = char_position[2] + weapon_mount[2]
    else:
        ang = math.radians(char_angle-90)
        x = char_position[0] + weapon_mount[0]*math.cos(ang) - weapon_mount[1]*math.sin(ang)
        y = char_position[1] + weapon_mount[0]*math.sin(ang) + weapon_mount[1]*math.cos(ang)
        z = char_position[2] + weapon_mount[2]
    projectiles.append([x,y,z,char_angle])


def update_projectiles():
    global projectiles,missed_shots,game_over
    to_remove=[]
    for p in projectiles:
        rad=math.radians(p[3]-90)
        p[0]+=shot_speed*math.cos(rad)
        p[1]+=shot_speed*math.sin(rad)
        if abs(p[0])>FIELD_HALF_SIZE+FIELD_EXTRA or abs(p[1])>FIELD_HALF_SIZE:
            to_remove.append(p)
            missed_shots+=1
            print(f"Missed: {missed_shots}")
    for p in to_remove:
        projectiles.remove(p)
    if missed_shots>=max_misses:
        game_over=True


def detect_hits():
    global char_score,projectiles,opponents
    for p in projectiles[:]:
        for o in opponents[:]:
            dx,dy=p[0]-o[0],p[1]-o[1]
            if math.hypot(dx,dy)<60:
                char_score+=1
                projectiles.remove(p)
                opponents.remove(o)
                spawn_opponents(1)
                break


def spawn_opponents(count=initial_opponents):
    for _ in range(count):
        x=random.uniform(-FIELD_HALF_SIZE+100,FIELD_HALF_SIZE-100)
        y=random.uniform(-FIELD_HALF_SIZE+100,FIELD_HALF_SIZE-100)
        while abs(x-char_position[0])<200:
            x=random.uniform(-FIELD_HALF_SIZE+100,FIELD_HALF_SIZE-100)
        while abs(y-char_position[1])<200:
            y=random.uniform(-FIELD_HALF_SIZE+100,FIELD_HALF_SIZE-100)
        opponents.append([x,y,0])


def render_opponent(x,y,z):
    glPushMatrix()
    glTranslatef(x,y,z+35)
    glColor3f(1,0,0)
    gluSphere(gluNewQuadric(),35*opponent_scale,10,10)
    glTranslatef(0,0,50)
    glColor3f(0,0,0)
    gluSphere(gluNewQuadric(),15*opponent_scale,10,10)
    glPopMatrix()


def update_opponents():
    global opponents,char_life,game_over
    for o in opponents[:]:
        dx,dy=char_position[0]-o[0],char_position[1]-o[1]
        dist=math.hypot(dx,dy)
        if dist<50:
            char_life-=1
            print(f"Life left: {char_life}")
            if char_life<=0:
                game_over=True
                opponents.clear()
                projectiles.clear()
                return
            opponents.remove(o)
            spawn_opponents(1)
        else:
            ang=math.atan2(dy,dx)
            o[0]+=opponent_speed*math.cos(ang)
            o[1]+=opponent_speed*math.sin(ang)


def update_pulse():
    global pulse_timer,opponent_scale
    pulse_timer+=0.01
    opponent_scale=1.0+0.5*math.sin(pulse_timer)


def find_closest_opponent():
    return min(opponents,key=lambda o:math.hypot(char_position[0]-o[0],char_position[1]-o[1]))


def calculate_opponent_angles():
    return [((math.degrees(math.atan2(o[1]-char_position[1],o[0]-char_position[0]))+90)%360) for o in opponents]


def cheat_rotate_aim():
    global char_angle,last_shot_time
    if not opponents: return
    angles=calculate_opponent_angles()
    char_angle=(char_angle+char_turn_speed/10)%360
    for ang in angles:
        diff=abs((char_angle-ang+540)%360-180)
        if diff<2 and time.time()-last_shot_time>shot_cooldown:
            shoot_projectile()
            last_shot_time=time.time()
            break


def cheat_target_closest():
    global char_angle,last_shot_time
    if not opponents: return
    o=find_closest_opponent()
    target=(math.degrees(math.atan2(o[1]-char_position[1],o[0]-char_position[0]))+90)%360
    diff=(target-char_angle+540)%360-180
    if abs(diff)>char_turn_speed:
        char_angle+=char_turn_speed/10 if diff>0 else -char_turn_speed/10
    else:
        char_angle=target
        if time.time()-last_shot_time>shot_cooldown:
            shoot_projectile()
            last_shot_time=time.time()


def handle_mouse(button,state,x,y):
    global is_first_person,char_turn_speed
    if button==GLUT_LEFT_BUTTON and state==GLUT_DOWN and not game_over:
        shoot_projectile()
    if button==GLUT_RIGHT_BUTTON and state==GLUT_DOWN and not game_over:
        is_first_person=not is_first_person
        char_turn_speed=3 if is_first_person else 6


def handle_keyboard(key,a,b):
    global char_angle,char_position,game_over,is_cheat,cheat_vision,missed_shots,char_life,char_score,projectiles,opponents,cam_angle,cam_radius,cam_height
    x,y,z=char_position
    if not game_over:
        if key==b'w': x-=char_speed*math.sin(math.radians(-char_angle)); y-=char_speed*math.cos(math.radians(char_angle))
        if key==b's': x+=char_speed*math.sin(math.radians(-char_angle)); y+=char_speed*math.cos(math.radians(char_angle))
        if key==b'a': char_angle+=char_turn_speed
        if key==b'd': char_angle-=char_turn_speed
        if key==b'c': is_cheat=not is_cheat
        if key==b'v' and is_first_person and is_cheat: cheat_vision=not cheat_vision
    if key==b'r':
        game_over=False; is_first_person=False; is_cheat=False; cheat_vision=False
        char_position[:] = [0,0,0]; char_angle=0; char_life=5; char_score=0; missed_shots=0
        projectiles.clear(); opponents.clear(); cam_angle=0; cam_radius=700; cam_height=700
        spawn_opponents()
    x=max(-FIELD_HALF_SIZE,min(x,FIELD_HALF_SIZE+FIELD_EXTRA))
    y=max(-FIELD_HALF_SIZE,min(y,FIELD_HALF_SIZE+FIELD_EXTRA))
    char_position[:]=[x,y,z]


def handle_special_keys(key,a,b):
    global cam_angle,cam_radius,cam_height
    if key==GLUT_KEY_UP: cam_height-=10; cam_radius-=10
    if key==GLUT_KEY_DOWN: cam_height+=10; cam_radius+=10
    if key==GLUT_KEY_LEFT: cam_angle-=5
    if key==GLUT_KEY_RIGHT: cam_angle+=5


def display_scene():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glViewport(0,0,WIN_WIDTH,WIN_HEIGHT)
    configure_camera(); render_field(); render_character()
    if not game_over:
        if is_cheat: cheat_rotate_aim()
        for o in opponents: render_opponent(*o)
        for p in projectiles: render_projectile(p[0],p[1],p[2])
        render_text(10,WIN_HEIGHT-30,f"Life: {char_life}")
        render_text(10,WIN_HEIGHT-60,f"Score: {char_score}")
        render_text(10,WIN_HEIGHT-90,f"Missed: {missed_shots}")
    else:
        render_text(10,WIN_HEIGHT-30,f"Game Over! Score: {char_score}")
        render_text(10,WIN_HEIGHT-60,'Press "R" to Restart')
    glutSwapBuffers()


def game_loop():
    if not game_over:
        update_opponents(); update_pulse(); update_projectiles(); detect_hits()
    glutPostRedisplay()


def main():
    glutInit(); glutInitDisplayMode(GLUT_DOUBLE|GLUT_RGB|GLUT_DEPTH)
    glutInitWindowSize(WIN_WIDTH,WIN_HEIGHT); glutInitWindowPosition(100,50)
    glutCreateWindow(b"Bullet Frenzy Refactored")
    glEnable(GL_DEPTH_TEST)
    spawn_opponents()
    glutDisplayFunc(display_scene); glutIdleFunc(game_loop)
    glutKeyboardFunc(handle_keyboard); glutSpecialFunc(handle_special_keys)
    glutMouseFunc(handle_mouse)
    glutMainLoop()

if __name__=="__main__":
    main()
