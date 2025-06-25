"""
Section of the GUI where the field is displayed.
"""
import math
import typing

from OpenGL import GL
from PyQt6 import QtGui
from PyQt6.QtCore import QTimerEvent
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtWidgets import QLabel

from entities import Match
from field_graphics.field_objects.match.field_match import Match as FieldMatch
from field_graphics.field_objects.ssl_robot_mesh import SSLRobotMesh
from field_graphics.field_objects.vsss_robot_mesh import VSSSRobotMesh
from field_graphics.rendering.objects.animation_manager import AnimationManager
from field_graphics.rendering.objects.rendering_context import RenderingContext
from field_graphics.rendering.render_manager import setupGL


class FieldView(QOpenGLWidget):
    rendering_context: RenderingContext = None
    match_api: Match = None
    match_context: FieldMatch = None
    no_info: bool = True
    isOpenGLInit: bool = False
    sim_time: int = 0
    field_dimentions = None
    rotation = AnimationManager()
    x_translation = AnimationManager(accel_constant=.1, anti_derivative_constant=.2)
    y_translation = AnimationManager(accel_constant=.1, anti_derivative_constant=.2)
    scale = AnimationManager(accel_constant=.15, anti_derivative_constant=.2)

    scroll_level: float = 0
    scroll_wheel_sensibility = 3

    def __init__(self, context: Match):
        super().__init__()
        self.rendering_context = RenderingContext()
        self.scroll_level = 7
        self.setFocusPolicy(self.focusPolicy().StrongFocus)
        self.setMinimumWidth(600)
        self.match_api = context
        # QLabel("<h1>Campo!</h1>", parent=self)

    def initializeGL(self):
        print("Initializing OpenGL Version 4.2")
        GL.glInitGl42VERSION()
        setupGL()
        GL.glClearColor(.2, .5, .2, 1)
        self.startTimer(math.ceil(100 / 6))
        self.isOpenGLInit = True

    def resizeGL(self, w: int, h: int) -> None:
        self.makeCurrent()
        GL.glViewport(0, 0, w, h)
        self.rendering_context.set_aspect_ratio(float(w) / float(h))

    def paintGL(self):
        GL.glClear(GL.GL_DEPTH_BUFFER_BIT | GL.GL_COLOR_BUFFER_BIT)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        self.rendering_context.draw(self.sim_time)

    def update_translations(self, time: float):
        """ Updates global transformations """
        self.scale.goal = math.pow(2, -self.scroll_level)
        self.rendering_context.x = self.x_translation.current
        self.rendering_context.y = self.y_translation.current
        self.rendering_context.scale = self.scale.current
        self.x_translation.update(time)
        self.y_translation.update(time)
        self.scale.update(time)

    def timerEvent(self, event: typing.Optional['QTimerEvent']) -> None:
        if self.match_context is not None:
            self.match_context.update(self.sim_time)
        self.makeCurrent()
        self.update_translations(1)
        self.update()
        if self.no_info and self.match_api.last_update_time !=0: self.no_info = False
        self.sim_time += 1

    def keyPressEvent(self, event: typing.Optional[QtGui.QKeyEvent]) -> None:
        self.updateKey(event.key())
        # print("DEST: " + str(self.x_translation.dest) + "," + str(self.y_translation.dest))

    def updateKey(self, key):
        if key == 16777235:
            self.y_translation.goal -= .2 / self.scale.goal
        elif key == 16777234:
            self.x_translation.goal += .2 / self.scale.goal
        elif key == 16777237:
            self.y_translation.goal += .2 / self.scale.goal
        elif key == 16777236:
            self.x_translation.goal -= .2 / self.scale.goal

    def mouseMoveEvent(self, event: typing.Optional[QtGui.QMouseEvent]) -> None:
        super().mouseMoveEvent(event)
        # TODO mover com o mouse

    def wheelEvent(self, event: typing.Optional[QtGui.QWheelEvent]) -> None:
        super().wheelEvent(event)
        self.scroll_level -= event.angleDelta().y() / (120 * self.scroll_wheel_sensibility)

    def displaySSLModels(self):
        for i in range(0,16):
            test_SSL_R = SSLRobotMesh(i)
            test_SSL_R.y = 340
            test_SSL_R.x = (i * 20) - 160
            self.rendering_context.objects.append(test_SSL_R)
        for i in range(0,16):
            test_SSL_R = SSLRobotMesh(i)
            test_SSL_R.y = 320
            test_SSL_R.x = (i * 20) - 160
            test_SSL_R.set_id(i,False)
            self.rendering_context.objects.append(test_SSL_R)

    def displayVSSSModels(self):
        for i in range(0,20):
            r: VSSSRobotMesh = VSSSRobotMesh([.1, .1, .1], [0, 1, 0], [1, 0, 0], [0, 0, 1])
            r.color_accordingly_to_id(i)
            r.x = i*9 - 85
            r.y = -72
            r.rotation = math.pi
            self.rendering_context.objects.append(r)

    def setupSSL(self):
        from field_graphics.field_objects.match.SSL_match import SSLMatch
        self.match_context = SSLMatch(self)

    def setupVSSS(self):
        from field_graphics.field_objects.match.VSSS_match import VSSSMatch
        self.match_context = VSSSMatch(self)


    def reset(self):
        self.match_context.clear()
        self.rendering_context.objects.clear()
