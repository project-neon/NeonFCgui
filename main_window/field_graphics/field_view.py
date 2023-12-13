"""
Section of the GUI where the field will be displayed.
"""
import math
import typing

from OpenGL import GL
from PyQt6 import QtGui
from PyQt6.QtCore import QTimerEvent
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtWidgets import QLabel, QWidget

from main_window.field_graphics.field_objects.robot import Robot
from main_window.field_graphics.rendering.render_manager import RenderingContext, setupGL


class FieldView(QOpenGLWidget):
    context: RenderingContext = None
    sim_time: int = 0
    rotation = x = y = 0
    scale = .1
    def __init__(self):
        super().__init__()
        self.context = RenderingContext()

        self.setFocusPolicy(self.focusPolicy().StrongFocus)
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
        GL.glClear(GL.GL_DEPTH_BUFFER_BIT | GL.GL_COLOR_BUFFER_BIT)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        self.context.draw(self.sim_time)

    def updateTranslations(self):
        self.context.scale += (self.scale - self.context.scale)/10
        self.context.x += (self.x - self.context.x) / 10
        self.context.y += (self.y - self.context.y) / 10

    def timerEvent(self, event: typing.Optional['QTimerEvent']) -> None:
        self.sim_time += 1
        self.r.rotation = self.sim_time / 350  # <-- TODO remover isso, essa rotação é só pra testes
        self.makeCurrent()
        self.updateTranslations()
        self.update()

    def keyPressEvent(self, event: typing.Optional[QtGui.QKeyEvent]) -> None:
        key = event.key()
        print(key)
        if key == 16777235:
            self.y -= .2
        elif key == 16777234:
            self.x += .2
        elif key == 16777237:
            self.y += .2
        elif key == 16777236:
            self.x -= .2

    def mouseMoveEvent(self, event: typing.Optional[QtGui.QMouseEvent]) -> None:
        super().mouseMoveEvent(event)
        # TODO mover com o mouse

    def wheelEvent(self, event: typing.Optional[QtGui.QWheelEvent]) -> None:
        super().wheelEvent(event)
        self.scale += event.angleDelta().y() / 2400
