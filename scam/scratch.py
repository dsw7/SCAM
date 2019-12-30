import sys
from os import path
from colorama import Fore, Style
from utils.joint_kinematics import TrajectoryGenerator
from utils.inverse_kinematics import InverseKinematics, NoSolutionError
from yaml import safe_load


try:
    consts_file = path.join(path.dirname(__file__), 'utils/constants.yaml')
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


coordinate_stack = [[0.5, 0.5]]
while True:
    # using LIFO to get start and target end effector positions
    coordinates_end = list()
    coordinates_end.append(float(input('Target x coordinate: ')))
    coordinates_end.append(float(input('Target y coordinate: ')))
    type_trajectory = input('Trajectory <L/P/None>: ') or 'L'
    coordinate_stack.append(coordinates_end)

    x_c = coordinate_stack[0][0]
    y_c = coordinate_stack[0][1]
    x_f = coordinate_stack[1][0]
    y_f = coordinate_stack[1][1]
    
    object_d_x = TrajectoryGenerator(x_c, x_f, 20)
    object_d_y = TrajectoryGenerator(y_c, y_f, 20)
    
    coordinate_stack.pop(0)

    if type_trajectory == 'L':
        list_d_x = object_d_x.generate_linear_path()
        list_d_y = object_d_y.generate_linear_path()
    elif type_trajectory == 'P':
        list_d_x = object_d_x.generate_parabolic_path()
        list_d_y = object_d_y.generate_parabolic_path()
        
    for dx, dy in zip(list_d_x, list_d_y):
        x_c += dx
        y_c += dy
        solution = InverseKinematics(x_c, y_c, L1, L2).get_positive_solution()
        
        if solution == NoSolutionError:
            sys.exit(Fore.RED + 'Solution does not exist!' + Style.RESET_ALL)
        else:
            theta_1_c, theta_2_c = solution

        print(round(x_c, 4), round(y_c, 4), round(theta_1_c, 4), round(theta_2_c, 4))