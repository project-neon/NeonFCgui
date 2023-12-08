from array import array

import numpy as np
from PyQt6.QtOpenGL import QOpenGLShaderProgram

from main_window.field_graphics.rendering.render_manager import Renderable, compileShaderProgram


def shaderProgram() -> QOpenGLShaderProgram:
    vsh = open("main_window/field_graphics/shaders/VertexShader.vsh").read()
    fsh = open("main_window/field_graphics/shaders/FragmentShader.fsh").read()
    return compileShaderProgram(vsh, fsh)


class Robot(Renderable):
    def __init__(self, robotColor: array, stampColor1: array, stampColor2: array):
        vert = np.asarray([-1,-1,0, 1,-1,0, -1,1,0, 1,1,0 , -1,1,0 , 1,-1,0], dtype=np.float32)
        col = np.asarray([0, 0, 0, 0, 0, 0, 0, 0, 0,], dtype=np.float32)
        super().__init__(vert, col, shaderProgram())
