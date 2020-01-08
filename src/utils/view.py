from OpenGL.GLU import gluLookAt
from OpenGL.GLU import gluPerspective

def set_frustum(angle_fov, display_width, display_height, clip_near, clip_far):
    aspect_ratio = display_width / display_height
    gluPerspective(angle_fov, aspect_ratio, clip_near, clip_far)

def set_camera_position(position_camera, position_object, rotation_camera):
    gluLookAt(*position_camera, *position_object, *rotation_camera)
