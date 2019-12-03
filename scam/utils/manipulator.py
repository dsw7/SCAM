import sys
from yaml import safe_load
from OpenGL.GL import glPushMatrix
from OpenGL.GL import glRotatef
from OpenGL.GL import glTranslatef
from OpenGL.GL import glBegin
from OpenGL.GL import glEnd
from OpenGL.GL import glVertex3f
from OpenGL.GL import glPopMatrix
from OpenGL.GL import GL_LINES
from .primitives import render_circle
from .primitives import render_reference_frame
from .primitives import render_cube

try:
    with open('utils/constants.yaml') as constants_file:
        CONSTANTS = safe_load(constants_file)
except FileNotFoundError:
    sys.exit('Missing configuration file!')


LENGTH_BASE = CONSTANTS['hardware']['base']['length']
WIDTH_BASE = CONSTANTS['hardware']['base']['width']
HEIGHT_BASE = CONSTANTS['hardware']['base']['height']
HALF_LENGTH_BASE = 0.5 * LENGTH_BASE
HALF_WIDTH_BASE = 0.5 * WIDTH_BASE
RADIUS_FEET = CONSTANTS['hardware']['base']['radius']
HEIGHT_LINK_1 = CONSTANTS['hardware']['link1']['height']
WIDTH_LINK_1 = CONSTANTS['hardware']['link1']['width']
LENGTH_LINK_1 = CONSTANTS['hardware']['link1']['length']
HEIGHT_CUBE_1 = CONSTANTS['hardware']['cube1']['height']
WIDTH_CUBE_1 = CONSTANTS['hardware']['cube1']['width']
LENGTH_CUBE_1 = CONSTANTS['hardware']['cube1']['length']
HEIGHT_LINK_2 = CONSTANTS['hardware']['link2']['height']
WIDTH_LINK_2 = CONSTANTS['hardware']['link2']['width']
LENGTH_LINK_2 = CONSTANTS['hardware']['link2']['length']
HEIGHT_CUBE_2 = CONSTANTS['hardware']['cube2']['height']
WIDTH_CUBE_2 = CONSTANTS['hardware']['cube2']['width']
LENGTH_CUBE_2 = CONSTANTS['hardware']['cube2']['length']
HEIGHT_CUBE_3 = CONSTANTS['hardware']['cube3']['height']
WIDTH_CUBE_3 = CONSTANTS['hardware']['cube3']['width']
LENGTH_CUBE_3 = CONSTANTS['hardware']['cube3']['length']
HEIGHT_LINK_3 = CONSTANTS['hardware']['link3']['height']
WIDTH_LINK_3 = CONSTANTS['hardware']['link3']['width']
LENGTH_LINK_3 = CONSTANTS['hardware']['link3']['length']
HEIGHT_CUBE_4 = CONSTANTS['hardware']['cube4']['height']
WIDTH_CUBE_4 = CONSTANTS['hardware']['cube4']['width']
LENGTH_CUBE_4 = CONSTANTS['hardware']['cube4']['length']
HEIGHT_PROBE = CONSTANTS['hardware']['probe']['height']


class SCAM:
    def __init__(self, x, y, theta_1, theta_2):
        self.x = x
        self.y = y
        self.theta_1 = theta_1
        self.theta_2 = theta_2

    def render_base(self):
        render_reference_frame()
        render_cube(x=0, y=0, z=0.05, length=LENGTH_BASE, width=WIDTH_BASE, height=HEIGHT_BASE)
        render_circle(x=-HALF_LENGTH_BASE, y=-HALF_WIDTH_BASE, z=0, radius=RADIUS_FEET)
        render_circle(x=HALF_LENGTH_BASE, y=-HALF_WIDTH_BASE, z=0, radius=RADIUS_FEET)
        render_circle(x=-HALF_LENGTH_BASE, y=HALF_WIDTH_BASE, z=0, radius=RADIUS_FEET)
        render_circle(x=HALF_LENGTH_BASE, y=HALF_WIDTH_BASE, z=0, radius=RADIUS_FEET)
        glPushMatrix()
        glRotatef(self.theta_1, 0.00, 0.00, 1.00)

    @staticmethod
    def render_first_link():
        glTranslatef(0.00, 0.00, HEIGHT_BASE)
        render_reference_frame()
        render_cube(x=0.00, y=0.00, z=HEIGHT_LINK_1 / 2, length=LENGTH_LINK_1, width=WIDTH_LINK_1, height=HEIGHT_LINK_1)

    @staticmethod
    def render_first_joint():
        glTranslatef(0.00, 0.00, HEIGHT_LINK_1)
        render_reference_frame()
        render_cube(x=0.00, y=0.00, z=HEIGHT_CUBE_1 / 2, length=LENGTH_CUBE_1, width=WIDTH_CUBE_1, height=HEIGHT_CUBE_1)

    @staticmethod
    def render_second_link():
        glTranslatef(LENGTH_CUBE_1 / 2, 0.00, HEIGHT_CUBE_1 / 2)
        render_reference_frame()
        render_cube(x=LENGTH_LINK_2 / 2, y=0.00, z=0.00, length=LENGTH_LINK_2, width=WIDTH_LINK_2, height=HEIGHT_LINK_2)

    @staticmethod
    def render_second_joint():
        glTranslatef(LENGTH_LINK_2, 0.00, 0.00)
        render_reference_frame()
        render_cube(x=LENGTH_CUBE_2 / 2, y=0.00, z=0.00, length=LENGTH_CUBE_2, width=WIDTH_CUBE_2, height=HEIGHT_CUBE_2)

    def render_third_joint(self):
        glTranslatef(LENGTH_CUBE_2 / 2, 0.00, -HEIGHT_CUBE_2 / 2)
        render_reference_frame()
        glRotatef(self.theta_2, 0.00, 0.00, 1.00)
        render_cube(x=0.00, y=0.00, z=-HEIGHT_CUBE_3 / 2, length=LENGTH_CUBE_3, width=WIDTH_CUBE_3, height=HEIGHT_CUBE_3)

    @staticmethod
    def render_third_link():
        glTranslatef(LENGTH_CUBE_3 / 2, 0.00, -HEIGHT_CUBE_3 / 2)
        render_reference_frame()
        render_cube(x=LENGTH_LINK_3 / 2, y=0.00, z=0.00, length=LENGTH_LINK_3, width=WIDTH_LINK_3, height=HEIGHT_LINK_3)

    @staticmethod
    def render_fourth_joint():
        glTranslatef(LENGTH_LINK_3, 0.00, 0.00)
        render_reference_frame()
        render_cube(x=LENGTH_CUBE_4 / 2, y=0.00, z=0.00, length=LENGTH_CUBE_4, width=WIDTH_CUBE_4, height=HEIGHT_CUBE_4)

    @staticmethod
    def render_probe():
        glTranslatef(LENGTH_CUBE_4 / 2, 0.00, -HEIGHT_CUBE_4 / 2)
        render_reference_frame()
        glBegin(GL_LINES)
        glVertex3f(0.00, 0.00, 0.00)
        glVertex3f(0.00, 0.00, -HEIGHT_PROBE)
        glEnd()

    def main(self):
        render_circle(x=self.x, y=self.y, z=0, radius=0.03)
        self.render_base()
        self.render_first_link()
        self.render_first_joint()
        self.render_second_link()
        self.render_second_joint()
        self.render_third_joint()
        self.render_third_link()
        self.render_fourth_joint()
        self.render_probe()
        glPopMatrix()
