import sys
import pygame
from yaml import safe_load
from pygame.locals import OPENGL, DOUBLEBUF
from OpenGL.GL import glClear
from OpenGL.GL import GL_COLOR_BUFFER_BIT
from OpenGL.GL import GL_DEPTH_BUFFER_BIT
from utils.view import set_frustum, set_camera_position
from utils.lighting import setup_lighting
from utils.primitives import render_grid
from utils.manipulator import SCAM
from utils.frontend import get_options_main


try:
    with open('utils/constants.yaml') as constants_file:
        CONSTANTS = safe_load(constants_file)
except FileNotFoundError:
    sys.exit('Missing configuration file!')

ANGLE_FOV = CONSTANTS['view']['angle_fov']
WIDTH = CONSTANTS['view']['width']
HEIGHT = CONSTANTS['view']['height']
CLIP_PLANE_NEAR = CONSTANTS['view']['clipping_plane_near']
CLIP_PLANE_FAR = CONSTANTS['view']['clipping_plane_far']
NET_CYCLES = CONSTANTS['kinematics']['net_cycles']


def main():
    d_theta_1, d_theta_2 = get_options_main()
    pygame.init()
    pygame.display.set_caption('SCAM')
    pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF|OPENGL)
    set_frustum(ANGLE_FOV, WIDTH, HEIGHT, CLIP_PLANE_NEAR, CLIP_PLANE_FAR)
    set_camera_position()
    setup_lighting()

    cycle = 0
    theta_1 = 0
    theta_2 = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        if cycle < NET_CYCLES:
            theta_1 += d_theta_1[cycle]
            theta_2 += d_theta_2[cycle]
            cycle += 1


        render_grid()
        SCAM(0, 0, theta_1, theta_2).main()
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == '__main__':
    main()
