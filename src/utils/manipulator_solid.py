import sys
from yaml import safe_load
from OpenGL.GL import glPushMatrix
from OpenGL.GL import glRotatef
from OpenGL.GL import glTranslatef
from OpenGL.GL import glBegin
from OpenGL.GL import glEnd
from OpenGL.GL import glVertex3f
from OpenGL.GL import glPopMatrix
from OpenGL.GL import glColor3f
from OpenGL.GL import GL_LINES
from .primitives import render_cuboid, render_cylinder, render_link

try:
    with open('utils/constants.yaml') as constants_file:
        CONSTANTS = safe_load(constants_file)
except FileNotFoundError:
    sys.exit('Missing configuration file!')

PRIMITIVE = CONSTANTS['hardware_solid_rendering']
BASE_LENGTH = PRIMITIVE['base']['length']
BASE_WIDTH = PRIMITIVE['base']['width']
BASE_HEIGHT = PRIMITIVE['base']['height']
STEP_1_RADIUS = PRIMITIVE['stepper_1']['radius']
STEP_1_HEIGHT = PRIMITIVE['stepper_1']['height']
BUSH_1_RADIUS = PRIMITIVE['bushing_1']['radius']
BUSH_1_HEIGHT = PRIMITIVE['bushing_1']['height']
AXLE_1_RADIUS = PRIMITIVE['axle_1']['radius']
AXLE_1_HEIGHT = PRIMITIVE['axle_1']['height']
LINK_1_LENGTH = PRIMITIVE['link_1']['length']
LINK_1_RADIUS = PRIMITIVE['link_1']['width']
LINK_1_HEIGHT = PRIMITIVE['link_1']['height']
STEP_2_RADIUS = PRIMITIVE['stepper_2']['radius']
STEP_2_HEIGHT = PRIMITIVE['stepper_2']['height']
AXLE_2_RADIUS = PRIMITIVE['axle_2']['radius']
AXLE_2_HEIGHT = PRIMITIVE['axle_2']['height']
LINK_2_LENGTH = PRIMITIVE['link_2']['length']
LINK_2_RADIUS = PRIMITIVE['link_2']['width']
LINK_2_HEIGHT = PRIMITIVE['link_2']['height']
STEP_3_RADIUS = PRIMITIVE['stepper_3']['radius']
STEP_3_HEIGHT = PRIMITIVE['stepper_3']['height']


class SCAMSolidRendering:
    def __init__(self, x, y, theta_1, theta_2):
        self.x = x
        self.y = y
        self.theta_1 = theta_1
        self.theta_2 = theta_2

    @staticmethod
    def render_base():
        glPushMatrix()
        render_cuboid(x=-BASE_LENGTH / 2, length=BASE_LENGTH, width=BASE_WIDTH, height=BASE_HEIGHT)

    @staticmethod
    def render_first_actuator():
        glTranslatef(0.00, 0.00, BASE_HEIGHT)                           # translate from base to actuator top
        glColor3f(0.40, 0.40, 0.40)                                     # make actuator dark gray
        render_cylinder(radius=STEP_1_RADIUS, height=STEP_1_HEIGHT)     # draw first actuator
        glColor3f(1.00, 1.00, 1.00)                                     # revert back to default color
        glTranslatef(0.00, 0.00, STEP_1_HEIGHT)                         # translate from base to actuator top
        render_cylinder(radius=BUSH_1_RADIUS, height=BUSH_1_HEIGHT)     # draw first bushing
        render_cylinder(radius=AXLE_1_RADIUS, height=AXLE_1_HEIGHT)     # draw first axle

    def render_first_link(self):
        glTranslatef(0.00, 0.00, AXLE_1_HEIGHT)                         # translate to actuator tip of first axle
        glPushMatrix()                                                  # isolate the first rotation
        glRotatef(self.theta_1, 0.0, 0.0, 1.0)                          # the first rotation
        glColor3f(0.75, 0.75, 0.75)                                     # make first link silver
        render_link(r=LINK_1_RADIUS, h=LINK_1_HEIGHT, l=LINK_1_LENGTH)  # the first link

    @staticmethod
    def render_second_actuator():
        glTranslatef(LINK_1_LENGTH, 0.00, 0.00)                         # translate to end of first link
        glColor3f(0.40, 0.40, 0.40)                                     # make second actuator dark gray
        render_cylinder(radius=STEP_2_RADIUS, height=STEP_2_HEIGHT)     # draw second actuator
        glColor3f(1.00, 1.00, 1.00)                                     # revert back to default color
        glTranslatef(0.00, 0.00, STEP_2_HEIGHT)                         # translate to top of second stepper
        render_cylinder(radius=AXLE_2_RADIUS, height=AXLE_2_HEIGHT)     # draw second axle

    def render_second_link(self):
        glTranslatef(0.00, 0.00, AXLE_2_HEIGHT)                         # translate to tip of second axle
        glColor3f(0.75, 0.75, 0.75)                                     # make second link silver
        glPushMatrix()                                                  # isolate the second rotation
        glRotatef(self.theta_2, 0.0, 0.0, 1.0)                          # the second rotation
        render_link(r=LINK_2_RADIUS, h=LINK_2_HEIGHT, l=LINK_2_LENGTH)  # the second link

    @staticmethod
    def render_third_actuator():
        glTranslatef(LINK_2_LENGTH, 0.00, 0.00)                         # translate to end of second link
        glColor3f(0.40, 0.40, 0.40)                                     # make actuator dark gray
        render_cylinder(radius=STEP_3_RADIUS, height=STEP_3_HEIGHT)     # draw third actuator

    @staticmethod
    def render_vertical_line():
        glColor3f(1.00, 1.00, 1.00)
        glBegin(GL_LINES)
        glVertex3f(0.00, 0.00, 0.25)
        glVertex3f(0.00, 0.00, -0.75)
        glEnd()

    def main(self):
        glColor3f(1.00, 1.00, 1.00)
        self.render_base()
        self.render_first_actuator()
        self.render_first_link()
        self.render_second_actuator()
        self.render_second_link()
        self.render_third_actuator()
        self.render_vertical_line()
        glPopMatrix()
        glPopMatrix()
        glPopMatrix()
