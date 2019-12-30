import sys
from os import path
from colorama import Fore, Style
from yaml import safe_load
from .inverse_kinematics import InverseKinematics, NoSolutionError
from .joint_kinematics import TrajectoryGenerator


try:
    consts_file = path.join(path.dirname(__file__), 'constants.yaml')
    with open(consts_file) as constants_file:
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
THETA_1_START = CONSTANTS['kinematics']['theta_1_start']
THETA_2_START = CONSTANTS['kinematics']['theta_2_start']
NET_CYCLES = CONSTANTS['kinematics']['net_cycles']


def print_header():
    print('*' * 60)
    print(Fore.BLUE + 'SCAM - Selective Compliance Autoinjection Manipulator' + Style.RESET_ALL)
    print('Model developed by David S. Weber (\033[36mdsw7@sfu.ca\033[0m)')
    print('Options:')
    print('1. Input C (custom) to input custom (x, y) coordinates.')
    print('2. Input D to use default coordinates.')
    print('3. Input X to exit.')


def get_options_from_user():
    while True:
        option = input('Option: ').lower()
        if option == 'c':   # custom input coordinates
            x_coordinate = float(input('x = '))
            y_coordinate = float(input('y = '))
            type_trajectory = str(input('Trajectory (L / P) = '))
            break
        elif option == 'd': # default input coordinates
            x_coordinate = -0.55
            y_coordinate = -0.55
            type_trajectory = 'L'
            break
        elif option == 'x':
            sys.exit('Exiting... \n' + '*' * 60)
        else:
            print('Invalid option. Try again.')
    return x_coordinate, y_coordinate, type_trajectory


def get_options_main():
    print_header()
    target_x, target_y, type_trajectory = get_options_from_user()
    solution = InverseKinematics(target_x, target_y, L1, L2).get_positive_solution()

    if solution == NoSolutionError:
        sys.exit(Fore.RED + 'Solution does not exist!' + Style.RESET_ALL)
    else:
        theta_1_final, theta_2_final = solution

    trajectory_theta_1 = TrajectoryGenerator(THETA_1_START, theta_1_final, NET_CYCLES)
    trajectory_theta_2 = TrajectoryGenerator(THETA_2_START, theta_2_final, NET_CYCLES)

    if type_trajectory == 'L':
        list_d_theta_1 = trajectory_theta_1.generate_linear_path()
        list_d_theta_2 = trajectory_theta_2.generate_linear_path()
    elif type_trajectory == 'P':
        list_d_theta_1 = trajectory_theta_1.generate_parabolic_path()
        list_d_theta_2 = trajectory_theta_2.generate_parabolic_path()
    else:
        sys.exit('Invalid trajectory type specified.')

    return list_d_theta_1, list_d_theta_2
