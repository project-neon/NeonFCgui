import numpy as np

from PyQt6.QtOpenGL import QOpenGLShaderProgram

from main_window.field_graphics.rendering.render_manager import Renderable, compileShaderProgram



class Robot(Renderable):
    def __init__(self, robotColor, stampColor1, stampColor2):
        vert = np.asarray([-1, -1, 0, 1, -1, 0, -1, 1, 0, 1, -1, 0, -1, 1, 0, 1, 1, 0], dtype=np.float32)
        col = np.asarray([0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1], dtype=np.float32)
        vsh = open("shaders/VertexShader.vsh").read()
        fsh = open("shaders/FragmentShader.fsh").read()
        shader = compileShaderProgram(vsh,fsh)
        super().__init__(vert, col, shader)

