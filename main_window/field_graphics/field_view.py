"""
Section of the GUI where the field will be displayed.
"""
import math

import numpy as np
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtWidgets import QLabel
from OpenGL import GL

from main_window.field_graphics.field_objects import robot
from main_window.field_graphics.field_objects.robot import Robot
from main_window.field_graphics.rendering.render_manager import RenderingContext, setupGL


class FieldView(QOpenGLWidget):
    context: RenderingContext = None
    sim_time: int = 0

    def __init__(self):
        super().__init__()
        self.context = RenderingContext(self.defaultFramebufferObject())
        QLabel("<h1>Campo!</h1>", parent=self)

    def initializeGL(self):
        GL.glInitGl42VERSION()
        setupGL()
        GL.glClearColor(.2, .5, .2, 1)
        self.context.objects.append(Robot(None, None, None))

    def resizeGL(self, w: int, h: int) -> None:
        # A documentação do PYQT fala pra eu chamar o GLViewport aqui, mas me parece que o próprio PyQT já redimensiona
        # o framebuffer automaticamente, então fica meio redundante na minha opinião
        self.context.set_aspect_ratio(float(w) / float(h))

    def paintGL(self):
        GL.glClear(GL.GL_DEPTH_BUFFER_BIT | GL.GL_COLOR_BUFFER_BIT)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        self.context.draw(self.sim_time)
        self.sim_time += 1
        # TODO: essa função precisa ser chamada a cada frame e pelo que me parece
        # ela só está atualizando quando a dimenção da janela muda
