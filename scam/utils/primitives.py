import sys
from os import path
from numpy import linspace, sin, cos, pi
from yaml import safe_load
from OpenGL.GL import glColor3f
from OpenGL.GL import glBegin, glEnd
from OpenGL.GL import glVertex3f
from OpenGL.GL import glTranslatef
from OpenGL.GL import glNormal3f
from OpenGL.GL import GL_LINES
from OpenGL.GL import GL_LINE_LOOP
from OpenGL.GL import GL_POLYGON
from OpenGL.GLU import gluNewQuadric
from OpenGL.GLU import gluSphere
from OpenGL.GLU import gluCylinder
from OpenGL.GLU import gluDisk
from OpenGL.GLU import gluQuadricNormals
from OpenGL.GLU import GLU_SMOOTH

try:
    filepath = path.join(path.dirname(__file__), 'constants.yaml')
    with open(filepath) as constants_file:
        CONSTANTS = safe_load(constants_file)
except FileNotFoundError:
    sys.exit('Missing configuration file!')

REF_FRAME_RADIUS = CONSTANTS['primitives']['ref_frame_radius']
REF_FRAME_SLICES = CONSTANTS['primitives']['ref_frame_slices']
REF_FRAME_STACKS = CONSTANTS['primitives']['ref_frame_stacks']
CYLINDER_STACKS = CONSTANTS['primitives']['cylinder_stacks']
CYLINDER_SLICES = CONSTANTS['primitives']['cylinder_slices']

LEFT_GRID = linspace(-1.0, -0.3, 8).tolist()
RIGHT_GRID = linspace(0.3, 1.0, 8).tolist()
GRID_DIMENSIONS = LEFT_GRID + RIGHT_GRID
GRIM_DIMENSIONS_FULL = linspace(-1.0, 1.0, 21).tolist()
OBJ_QUADRIC = gluNewQuadric()
FULL_CIRCLE = [(cos(dt), sin(dt)) for dt in linspace(-pi / 2, 3 * pi / 2, 200)] 
RIGHT_SEMICIRCLE = FULL_CIRCLE[0:101]  # add an extra "point" to prevent underfitted connections
LEFT_SEMICIRCLE = FULL_CIRCLE[99:200]  # add an extra "point" to prevent underfitted connections


def render_grid(full=False):
    """
    Sets a grid in the current viewframe.
    Setting full to False will leave a blank squre inside the grid.
    """
    glColor3f(0.40, 0.40, 0.40)

    if full:
        grid_dim = GRIM_DIMENSIONS_FULL
    else:
        grid_dim = GRID_DIMENSIONS

    # horizontal grid lines
    glBegin(GL_LINES)
    for stack in grid_dim:
        glVertex3f(-1.0, stack, 0.0)
        glVertex3f(1.0, stack, 0.0)
    glEnd()

    # vertical grid lines
    glBegin(GL_LINES)
    for stack in grid_dim:
        glVertex3f(stack, -1.0, 0.0)
        glVertex3f(stack, 1.0, 0.0)
    glEnd()

    glColor3f(1.0, 1.0, 1.0)


def render_reference_frame(radius=REF_FRAME_RADIUS, slices=REF_FRAME_SLICES, stacks=REF_FRAME_STACKS):
    """ Render a green colored sphere that indicates reference frame """
    glColor3f(0.00, 1.00, 0.00)
    gluSphere(OBJ_QUADRIC, radius, slices, stacks)
    glColor3f(1.00, 1.00, 1.00)


def render_circle(x, y, z, radius):
    glBegin(GL_LINE_LOOP)
    for d_theta in linspace(0, 2 * pi, 100):
        a = radius * cos(d_theta) + x
        b = radius * sin(d_theta) + y
        c = z
        glVertex3f(a, b, c)
    glEnd()


gluQuadricNormals(OBJ_QUADRIC, GLU_SMOOTH)
def render_cylinder(radius, height, slices=CYLINDER_SLICES, stacks=CYLINDER_STACKS):
    # cylinder calls glNormal3f() under the hood?
    gluCylinder(OBJ_QUADRIC, radius, radius, height, slices, stacks)  # draw the cylinder
    gluDisk(OBJ_QUADRIC, 0, radius, slices, stacks)  # draw the bottom cap
    glTranslatef(0.00, 0.00, height)                 # translate to top of cylinder
    gluDisk(OBJ_QUADRIC, 0, radius, slices, stacks)  # draw the top cap
    glTranslatef(0.00, 0.00, -height)                # translate back down


def render_cube(x=0, y=0, z=0, length=0.1, width=0.1, height=0.1, show_axis_symmetry=True):
    """
    DSW written cube generation function
    We will translate TO this location using glTranslatef
    The only adjustable parameters are l, w, and h
    """

    # precompute to save on processing power
    half_l = 0.5 * length
    half_w = 0.5 * width
    half_h = 0.5 * height

    # first face
    # ----------
    glBegin(GL_LINE_LOOP)
    glVertex3f(x - half_l, y - half_w, z + half_h) # A
    glVertex3f(x - half_l, y - half_w, z - half_h) # B
    glVertex3f(x - half_l, y + half_w, z - half_h) # C
    glVertex3f(x - half_l, y + half_w, z + half_h) # D
    glEnd()

    # second face
    # -----------
    glBegin(GL_LINE_LOOP)
    glVertex3f(x + half_l, y - half_w, z + half_h) # A
    glVertex3f(x + half_l, y - half_w, z - half_h) # B
    glVertex3f(x + half_l, y + half_w, z - half_h) # C
    glVertex3f(x + half_l, y + half_w, z + half_h) # D
    glEnd()

    # connection lines
    # ----------------

    # A <-> A
    glBegin(GL_LINES)
    glVertex3f(x + half_l, y - half_w, z + half_h)
    glVertex3f(x - half_l, y - half_w, z + half_h)
    glEnd()

    # B <-> B
    glBegin(GL_LINES)
    glVertex3f(x + half_l, y - half_w, z - half_h)
    glVertex3f(x - half_l, y - half_w, z - half_h)
    glEnd()

    # C <-> C
    glBegin(GL_LINES)
    glVertex3f(x + half_l, y + half_w, z - half_h)
    glVertex3f(x - half_l, y + half_w, z - half_h)
    glEnd()

    # D <-> D
    glBegin(GL_LINES)
    glVertex3f(x + half_l, y + half_w, z + half_h)
    glVertex3f(x - half_l, y + half_w, z + half_h)
    glEnd()

    if show_axis_symmetry:
        # a red line depicting the reference frame location
        glColor3f(1.00, 0.00, 0.00)
        glBegin(GL_LINES)
        glVertex3f(x + half_l, y, z)
        glVertex3f(x - half_l, y, z)
        glEnd()
        glColor3f(1.00, 1.00, 1.00)


def render_cuboid(x=0, y=0, z=0, length=0.1, width=0.1, height=0.1):
    """
    Draws a cuboid with fill and proper lighting.
    Proper lighting is achieved using an internal call to glNormal3f()
    where a normal vector is passed into the function. I believe the normal
    vector must be of unit magnitude.

    i.e.:
    glBegin(GL_POLYGON)
    glNormal3f(0.0, 0.0, 1.0)  # note that this vector is normal to the below plane
    glVertex3f( 1.0,  1.0, 0.0)
    glVertex3f( 1.0, -1.0, 0.0)
    glVertex3f(-1.0, -1.0, 0.0)
    glVertex3f(-1.0,  1.0, 0.0)
    glEnd()
    """
    # precompute to save on processing power
    half_w = 0.5 * width

    # first face
    # ----------
    glBegin(GL_POLYGON)
    glNormal3f(-1.0, 0.0, 0.0)
    glVertex3f(x, y - half_w, z)
    glVertex3f(x, y + half_w, z)
    glVertex3f(x, y + half_w, z + height)
    glVertex3f(x, y - half_w, z + height)
    glEnd()

    # last face
    # ----------
    glBegin(GL_POLYGON)
    glNormal3f(1.0, 0.0, 0.0)
    glVertex3f(x + length, y - half_w, z)
    glVertex3f(x + length, y + half_w, z)
    glVertex3f(x + length, y + half_w, z + height)
    glVertex3f(x + length, y - half_w, z + height)
    glEnd()

    # side "tube"
    glBegin(GL_POLYGON)
    glNormal3f(0.0, 1.0, 0.0)
    glVertex3f(x, y + half_w, z)
    glVertex3f(x, y + half_w, z + height)
    glVertex3f(x + length, y + half_w, z + height)
    glVertex3f(x + length, y + half_w, z)
    glEnd()

    glBegin(GL_POLYGON)
    glNormal3f(0.0, -1.0, 0.0)
    glVertex3f(x, y - half_w, z)
    glVertex3f(x, y - half_w, z + height)
    glVertex3f(x + length, y - half_w, z + height)
    glVertex3f(x + length, y - half_w, z)
    glEnd()

    glBegin(GL_POLYGON)
    glNormal3f(0.0, 0.0, 1.0)
    glVertex3f(x, y + half_w, z + height)
    glVertex3f(x, y - half_w, z + height)
    glVertex3f(x + length, y - half_w, z + height)
    glVertex3f(x + length, y + half_w, z + height)
    glEnd()

    glBegin(GL_POLYGON)
    glNormal3f(0.0, 0.0, -1.0)
    glVertex3f(x, y - half_w, z)
    glVertex3f(x, y + half_w, z)
    glVertex3f(x + length, y + half_w, z)
    glVertex3f(x + length, y - half_w, z)
    glEnd()


def render_link(x=0.0, y=0.0, r=0.1, h=0.1, l=0.2):
    """
    Draws a "pill shaped" link with fill and proper lighting.
    Proper lighting is achieved using an internal call to glNormal3f()
    where a normal vector is passed into the function. I believe the normal
    vector must be of unit magnitude.

    i.e.:
    glBegin(GL_POLYGON)
    glNormal3f(0.0, 0.0, 1.0)  # note that this vector is normal to the below plane
    glVertex3f( 1.0,  1.0, 0.0)
    glVertex3f( 1.0, -1.0, 0.0)
    glVertex3f(-1.0, -1.0, 0.0)
    glVertex3f(-1.0,  1.0, 0.0)
    glEnd()
    """

    # draw right side half washer
    # ==========================================
    xy = []
    for dtheta in LEFT_SEMICIRCLE:
        xy.append((r * dtheta[0] + x, r * dtheta[1] + y))

    # draw bottom half circle
    glBegin(GL_POLYGON)
    glNormal3f(0.0, 0.0, -1.0)
    for coords in xy:
        glVertex3f(*coords, 0.0)
    glEnd()

    # draw top half circle
    glBegin(GL_POLYGON)
    glNormal3f(0.0, 0.0, 1.0)
    for coords in xy:
        glVertex3f(*coords, h)
    glEnd()

    # draw circular strip
    # there may be a bug here
    glBegin(GL_POLYGON)
    for coords in xy:
        glNormal3f(coords[0] / r, coords[1] / r, 0)
        glVertex3f(*coords, 0.0)
        glVertex3f(*coords, h)
    glEnd()

    # draw middle core
    # ==========================================
    glBegin(GL_POLYGON)
    glNormal3f(0.0, 1.0, 0.0)
    glVertex3f(x, y + r, 0.0)         # B
    glVertex3f(x, y + r, 0.0 + h)     # C
    glVertex3f(x + l, y + r, 0.0 + h) # G
    glVertex3f(x + l, y + r, 0.0)     # F
    glEnd()

    glBegin(GL_POLYGON)
    glNormal3f(0.0, -1.0, 0.0)
    glVertex3f(x, y - r, 0.0)         # A
    glVertex3f(x, y - r, 0.0 + h)     # D
    glVertex3f(x + l, y - r, 0.0 + h) # H
    glVertex3f(x + l, y - r, 0.0)     # E
    glEnd()

    glBegin(GL_POLYGON)
    glNormal3f(0.0, 0.0, 1.0)
    glVertex3f(x, y + r, 0.0 + h)     # C
    glVertex3f(x, y - r, 0.0 + h)     # D
    glVertex3f(x + l, y - r, 0.0 + h) # H
    glVertex3f(x + l, y + r, 0.0 + h) # G
    glEnd()

    glBegin(GL_POLYGON)
    glNormal3f(0.0, 0.0, -1.0)
    glVertex3f(x, y - r, 0.0)         # A
    glVertex3f(x, y + r, 0.0)         # B
    glVertex3f(x + l, y + r, 0.0)     # E
    glVertex3f(x + l, y - r, 0.0)     # F
    glEnd()

    # draw left side half washer
    # ==========================================
    xy2 = []
    for dtheta in RIGHT_SEMICIRCLE:
        xy2.append((r * dtheta[0] + x, r * dtheta[1] + y))

    glTranslatef(x + l, 0.0, 0.0)

    # draw bottom half circle
    glBegin(GL_POLYGON)
    glNormal3f(0.0, 0.0, -1.0)
    for coords in xy2:
        glVertex3f(*coords, 0.0)
    glEnd()

    # draw top half circle
    glBegin(GL_POLYGON)
    glNormal3f(0.0, 0.0, 1.0)
    for coords in xy2:
        glVertex3f(*coords, h)
    glEnd()

    # draw circular strip
    # there may be a bug here
    glBegin(GL_POLYGON)
    for coords in xy2:
        glNormal3f(coords[0] / r, coords[1] / r, 0)
        glVertex3f(*coords, 0.0)
        glVertex3f(*coords, h)
    glEnd()

    glTranslatef(x - l, 0.0, 0.0)

