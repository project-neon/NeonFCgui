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
from main_window.field_graphics.field_objects.text import Text
from main_window.field_graphics.rendering.render_manager import RenderingContext, setupGL, modelFromJSON
from main_window.field_graphics.rendering.animation_manager import AnimationManager


class FieldView(QOpenGLWidget):
    context: RenderingContext = None
    sim_time: int = 0
    rotation = AnimationManager()
    x_translation = AnimationManager(accel_constant=.1, anti_derivative_constant=.2)
    y_translation = AnimationManager(accel_constant=.1, anti_derivative_constant=.2)
    scale = AnimationManager(accel_constant=.15, anti_derivative_constant=.2)

    scroll_level: float = 0
    scroll_wheel_sensibility = 3

    def __init__(self):
        super().__init__()
        self.context = RenderingContext()
        self.scroll_level = 7
        self.setFocusPolicy(self.focusPolicy().StrongFocus)
        QLabel("<h1>Campo!</h1>", parent=self)

    def initializeGL(self):
        # Aqui tem muita coisa de teste, TODO: remover isso... eventualmente...
        GL.glInitGl42VERSION()
        setupGL()
        GL.glClearColor(.2, .5, .2, 1)
        self.r = Robot([.1, .1, .1], [0, 1, 0], [1, 0, 0], [0, 0, 1])
        self.context.objects.append(self.r)
        field = modelFromJSON(open("main_window/field_graphics/assets/models/field_vsss.json").read())
        for obj in field:
            self.context.objects.append(obj)

        text = Text("#01", "main_window/field_graphics/assets/bitmaps/Bahnschrift SemiBold_1024.bmp", size=6, tracking=self.r, anchor=(10, 0))
        self.context.objects.append(text)

        self.startTimer(math.ceil(100 / 6))

    def resizeGL(self, w: int, h: int) -> None:
        self.makeCurrent()
        GL.glViewport(0, 0, w, h)
        self.context.set_aspect_ratio(float(w) / float(h))

    def paintGL(self):
        GL.glClear(GL.GL_DEPTH_BUFFER_BIT | GL.GL_COLOR_BUFFER_BIT)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        self.context.draw(self.sim_time)

    def update_translations(self, time: float):
        self.scale.dest = math.pow(2, -self.scroll_level)
        self.context.x = self.x_translation.current
        self.context.y = self.y_translation.current
        self.context.scale = self.scale.current
        self.x_translation.update(time)
        self.y_translation.update(time)
        self.scale.update(time)

    def timerEvent(self, event: typing.Optional['QTimerEvent']) -> None:
        self.sim_time += 1
        #self.r.rotation = self.sim_time / 350  # <-- TODO remover isso, essa rotação é só pra testes
        self.r.x = math.sin(self.sim_time/200) * 80
        self.r.y = math.cos(self.sim_time/200) * 40

        self.r.rotation = self.sim_time/25

        self.makeCurrent()
        self.update_translations(1)
        self.update()

    def keyPressEvent(self, event: typing.Optional[QtGui.QKeyEvent]) -> None:
        self.updateKey(event.key())
        # print("DEST: " + str(self.x_translation.dest) + "," + str(self.y_translation.dest))

    def updateKey(self, key):
        if key == 16777235:
            self.y_translation.dest -= .2 / self.scale.dest
        elif key == 16777234:
            self.x_translation.dest += .2 / self.scale.dest
        elif key == 16777237:
            self.y_translation.dest += .2 / self.scale.dest
        elif key == 16777236:
            self.x_translation.dest -= .2 / self.scale.dest

    def mouseMoveEvent(self, event: typing.Optional[QtGui.QMouseEvent]) -> None:
        super().mouseMoveEvent(event)
        # TODO mover com o mouse
        # Como faz

    def wheelEvent(self, event: typing.Optional[QtGui.QWheelEvent]) -> None:
        super().wheelEvent(event)
        self.scroll_level -= event.angleDelta().y() / (120 * self.scroll_wheel_sensibility)
