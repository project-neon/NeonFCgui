"""
Section of the GUI where the field will be displayed.
"""
import math
import typing

import numpy as np
from PyQt6 import QtGui
from PyQt6.QtCore import QTimer, QTimerEvent
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtWidgets import QLabel
from OpenGL import GL

from main_window.field_graphics.field_objects import robot
from main_window.field_graphics.field_objects.robot import Robot
from main_window.field_graphics.rendering.render_manager import RenderingContext, setupGL


class FieldView(QOpenGLWidget):
    context: RenderingContext = None
    sim_time: int = 0
    current_scale: float = .1
    current_translation = [0, 0]

    def __init__(self):
        super().__init__()
        self.context = RenderingContext()
        QLabel("<h1>Campo!</h1>", parent=self)

    def initializeGL(self):
        GL.glInitGl42VERSION()
        setupGL()
        GL.glClearColor(.2, .5, .2, 1)
        self.r = Robot([.15, .15, .15], [0, 1, 0], [1, 0, 0])
        self.context.objects.append(self.r)
        self.startTimer(math.ceil(100 / 6))

    def resizeGL(self, w: int, h: int) -> None:
        self.makeCurrent()
        GL.glViewport(0, 0, w, h)
        self.context.set_aspect_ratio(float(w) / float(h))

    def paintGL(self):
        self.context.set_transformations()
        GL.glClear(GL.GL_DEPTH_BUFFER_BIT | GL.GL_COLOR_BUFFER_BIT)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        self.context.draw(self.sim_time)
        # TODO: essa função precisa ser chamada a cada frame e pelo que me parece
        # ela só está atualizando quando a dimenção da janela muda

    def timerEvent(self, a0: typing.Optional['QTimerEvent']) -> None:
        self.sim_time += 1
        self.r.rotation = self.sim_time / 350
        self.makeCurrent()
        self.update()

    def mouseMoveEvent(self, a0: typing.Optional[QtGui.QMouseEvent]) -> None:
        super().mouseMoveEvent(a0)
        x = -(a0.pos().x() - .5 * self.size().width())
        y = -(a0.pos().y() - .5 * self.size().height())
        print("{}:{}".format(x, y))
        self.context.set_transformations(x / 100, y / 100, scale=self.context.scale)

    def wheelEvent(self, a0: typing.Optional[QtGui.QWheelEvent]) -> None:
        super().wheelEvent(a0)
        self.current_scale += a0.angleDelta().y() / 2400
