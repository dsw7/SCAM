from OpenGL.GLU import gluLookAt
from OpenGL.GLU import gluPerspective

def set_frustum(angle_fov, display_width, display_height, clip_near, clip_far):
    aspect_ratio = display_width / display_height
    gluPerspective(angle_fov, aspect_ratio, clip_near, clip_far)

def set_camera_position():
    position_camera = (0.00, -3.00, 2.00)
    position_object = (0.00, 0.00, 0.00)
    rotation_camera = (0.00, 1.00, 0.00)
    gluLookAt(*position_camera, *position_object, *rotation_camera)
