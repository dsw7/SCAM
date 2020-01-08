import sys
from os import path
from yaml import safe_load
from OpenGL.GL import glClearColor
from OpenGL.GL import glShadeModel
from OpenGL.GL import glMaterialfv
from OpenGL.GL import glLightfv
from OpenGL.GL import glLightf
from OpenGL.GL import glEnable
from OpenGL.GL import glColorMaterial
from OpenGL.GL import GL_SMOOTH
from OpenGL.GL import GL_SPECULAR
from OpenGL.GL import GL_FRONT
from OpenGL.GL import GL_LIGHT0
from OpenGL.GL import GL_LIGHTING
from OpenGL.GL import GL_POSITION
from OpenGL.GL import GL_CONSTANT_ATTENUATION
from OpenGL.GL import GL_LINEAR_ATTENUATION
from OpenGL.GL import GL_QUADRATIC_ATTENUATION
from OpenGL.GL import GL_SHININESS
from OpenGL.GL import GL_COLOR_MATERIAL
from OpenGL.GL import GL_FRONT_AND_BACK
from OpenGL.GL import GL_AMBIENT_AND_DIFFUSE
from OpenGL.GL import GL_DEPTH_TEST

try:
    filepath = path.join(path.dirname(__file__), 'constants.yaml')
    with open(filepath) as constants_file:
        CONSTANTS = safe_load(constants_file)
except FileNotFoundError:
    sys.exit('Missing configuration file!')

LIGHT_X_POS = CONSTANTS['lighting']['light_x_pos']
LIGHT_Y_POS = CONSTANTS['lighting']['light_y_pos']
LIGHT_Z_POS = CONSTANTS['lighting']['light_z_pos']
SHININESS = CONSTANTS['lighting']['shininess']
CONST_ATTENUATION = CONSTANTS['lighting']['const_attenuation']
LINEAR_ATTENUATION = CONSTANTS['lighting']['linear_attenuation']
QUADRATIC_ATTENUATION = CONSTANTS['lighting']['quadratic_attenuation']


def setup_lighting():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glShadeModel(GL_SMOOTH)
    
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialfv(GL_FRONT, GL_SHININESS, SHININESS)
    glLightfv(GL_LIGHT0, GL_POSITION, [LIGHT_X_POS, LIGHT_Y_POS, LIGHT_Z_POS, 0.0])
    
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, CONST_ATTENUATION)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, LINEAR_ATTENUATION)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, QUADRATIC_ATTENUATION)
    
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    
    # Need to enable GL_COLOR_MATERIAL in order to color the GL_POLYGONS
    # glColor3f / GL_POLYGONS will NOT work together
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    
    # GL_DEPTH_TEST performs hidden surface removal
    # What is hidden surface removal?
    #
    # Assume we have two functions that draw objects A and B:
    #
    # mainloop():
    #     glRotatef(1.00, 1.00, 0.00, 0.00)
    #     draw_obj_A()
    #     draw_obj_B()
    #
    # The problem is that object B will always be drawn atop
    # object A which is not realistic for a rotation where eventually
    # A will obscure B. GL_DEPTH_TEST solves this problem.
    glEnable(GL_DEPTH_TEST)
