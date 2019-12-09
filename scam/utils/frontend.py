import sys
from os import path
from colorama import Fore, Style
from yaml import safe_load
from .inverse_kinematics import InverseKinematics, NoSolutionError


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
            break
        elif option == 'd': # default input coordinates
            x_coordinate = -0.55
            y_coordinate = -0.55
            break
        elif option == 'x':
            sys.exit('Exiting... \n' + '*' * 60)
        else:
            print('Invalid option. Try again.')
    return x_coordinate, y_coordinate


def get_options_main():
    print_header()
    x, y = get_options_from_user()
    solution = InverseKinematics(x, y, L1, L2).get_positive_solution()
    if solution == NoSolutionError:
        sys.exit(Fore.RED + 'Solution does not exist!' + Style.RESET_ALL)
    else:
        theta_1_final, theta_2_final = solution
    d_theta_1 = (theta_1_final - THETA_1_START) / NET_CYCLES
    d_theta_2 = (theta_2_final - THETA_2_START) / NET_CYCLES
    return d_theta_1, d_theta_2
