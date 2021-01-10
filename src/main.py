import sys
from os import path
from yaml import safe_load
from colorama import Fore, Style
from OpenGL.GL import glClear
from OpenGL.GL import GL_COLOR_BUFFER_BIT
from OpenGL.GL import GL_DEPTH_BUFFER_BIT
from pygame import init, quit as pygame_quit, QUIT
from pygame.locals import OPENGL, DOUBLEBUF
from pygame.display import set_caption, set_mode, flip
from pygame.event import get
from pygame.time import wait
from utils.joint_kinematics import TrajectoryGenerator
from utils.inverse_kinematics import InverseKinematics, NoSolutionError
from utils.view import set_frustum, set_camera_position
from utils.lighting import setup_lighting
from utils.primitives import render_grid
from utils.manipulator import SCAM
from utils.manipulator_solid import SCAMSolidRendering

try:
    CONSTS_FILE = path.join(path.dirname(__file__), 'utils/constants.yaml')
    with open(CONSTS_FILE) as constants_file:
        CONSTANTS = safe_load(constants_file)
except FileNotFoundError:
    sys.exit('Missing configuration file!')

LENGTH_CUBE_1 = CONSTANTS['hardware']['cube1']['length']
LENGTH_LINK_2 = CONSTANTS['hardware']['link2']['length']
LENGTH_CUBE_2 = CONSTANTS['hardware']['cube2']['length']
LENGTH_CUBE_3 = CONSTANTS['hardware']['cube3']['length']
LENGTH_LINK_3 = CONSTANTS['hardware']['link3']['length']
LENGTH_CUBE_4 = CONSTANTS['hardware']['cube4']['length']
L1 = LENGTH_CUBE_1 / 2 + LENGTH_LINK_2 + LENGTH_CUBE_2 / 2
L2 = LENGTH_CUBE_3 / 2 + LENGTH_LINK_3 + LENGTH_CUBE_4 / 2

ANGLE_FOV = CONSTANTS['view']['angle_fov']
WIDTH = CONSTANTS['view']['width']
HEIGHT = CONSTANTS['view']['height']
CLIP_PLANE_NEAR = CONSTANTS['view']['clipping_plane_near']
CLIP_PLANE_FAR = CONSTANTS['view']['clipping_plane_far']
NET_CYCLES = CONSTANTS['kinematics']['net_cycles']
TYPE_RENDERING = CONSTANTS['rendering_type']['solid']
POSITION_CAMERA = CONSTANTS['view']['camera_position']
POSITION_OBJECT = CONSTANTS['view']['object_position']
ROTATION_CAMERA = CONSTANTS['view']['camera_rotation']

def loop(x_position, y_position, list_d_x, list_d_y):
    cycle = 0
    while True:
        for event in get():
            if event.type == QUIT:
                pygame_quit()
                sys.exit()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        if cycle < NET_CYCLES:
            x_position += list_d_x[cycle]
            y_position += list_d_y[cycle]
            cycle += 1

        solution = InverseKinematics(x_position, y_position, L1, L2).get_positive_solution()
        if solution == NoSolutionError:
            sys.exit(Fore.RED + 'Solution does not exist!' + Style.RESET_ALL)
        else:
            theta_1, theta_2 = solution

        render_grid()

        if TYPE_RENDERING:
            SCAMSolidRendering(0, 0, theta_1, theta_2).main()
        else:
            SCAM(0, 0, theta_1, theta_2).main()

        flip()
        wait(10)

def main():
    type_trajectory = input('Input a trajectory type: <L/P/None>: ') or 'L'
    x_start = input('Start x position (or press Enter to select default value): ') or 0.5
    y_start = input('Start y position (or press Enter to select default value): ') or 0.5
    x_end = input('End x position (or press Enter to select default value): ') or 0.5
    y_end = input('End y position (or press Enter to select default value): ') or -0.95
    print('Rendering...')

    init()
    set_caption('SCAM')
    set_mode((WIDTH, HEIGHT), DOUBLEBUF|OPENGL)
    set_frustum(ANGLE_FOV, WIDTH, HEIGHT, CLIP_PLANE_NEAR, CLIP_PLANE_FAR)
    set_camera_position(POSITION_CAMERA, POSITION_OBJECT, ROTATION_CAMERA)
    setup_lighting()

    trajectory_x = TrajectoryGenerator(float(x_start), float(x_end), NET_CYCLES)
    trajectory_y = TrajectoryGenerator(float(y_start), float(y_end), NET_CYCLES)

    if type_trajectory == 'P':
        list_d_x = trajectory_x.generate_parabolic_path()
        list_d_y = trajectory_y.generate_parabolic_path()
    else:
        list_d_x = trajectory_x.generate_linear_path()
        list_d_y = trajectory_y.generate_linear_path()

    loop(x_start, y_start, list_d_x, list_d_y)

if __name__ == '__main__':
    main()
