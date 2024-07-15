"""
Section of the GUI where the field will be displayed.
"""
import math
import random
import typing

import numpy
import numpy as np
from OpenGL import GL
from PyQt6 import QtGui
from PyQt6.QtCore import QTimerEvent
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtWidgets import QLabel

from entities import Match
from field_graphics.field_objects import vss_robot_mesh
from field_graphics.field_objects.ssl_robot_mesh import SSLRobotMesh
from field_graphics.field_objects.vss_robot_mesh import VSSRobotMesh
from field_graphics.field_objects.text import Text
from field_graphics.rendering.objects.animation_manager import AnimationManager
from field_graphics.rendering.objects.renderable_line import RenderableLine
from field_graphics.rendering.render_manager import setupGL, modelFromJSON, RenderableMesh
from field_graphics.rendering.objects.rendering_context import RenderingContext


class FieldView(QOpenGLWidget):
    context: RenderingContext = None
    no_info: bool = True
    sim_time: int = 0
    rotation = AnimationManager()
    x_translation = AnimationManager(accel_constant=.1, anti_derivative_constant=.2)
    y_translation = AnimationManager(accel_constant=.1, anti_derivative_constant=.2)
    scale = AnimationManager(accel_constant=.15, anti_derivative_constant=.2)

    scroll_level: float = 0
    scroll_wheel_sensibility = 3

    def __init__(self, context: Match):
        super().__init__()
        self.ball = None
        self.r1 = self.r2 = self.r3 = None
        self.context = RenderingContext()
        self.scroll_level = 7
        self.setFocusPolicy(self.focusPolicy().StrongFocus)
        self.match = context
        QLabel("<h1>Campo!</h1>", parent=self)

    def initializeGL(self):
        # Aqui tem muita coisa de teste, TODO: remover isso... eventualmente...
        GL.glInitGl42VERSION()
        setupGL()
        GL.glClearColor(.2, .5, .2, 1)

        self.r1: VSSRobotMesh = VSSRobotMesh([.1, .1, .1], [0, 1, 0], [1, 0, 0], [0, 0, 1])
        self.r2: VSSRobotMesh = VSSRobotMesh([.1, .1, .1], [0, 1, 0], [1, 0, 0], [0, 0, 1])
        self.r3: VSSRobotMesh = VSSRobotMesh([.1, .1, .1], [0, 1, 0], [1, 0, 0], [0, 0, 1])

        self.r1.rotation = math.pi/2
        self.r2.rotation = -math.pi/6
        self.r3.rotation = math.pi * (9.5/3)

        self.r1.color_accordingly_to_id(5)
        self.r2.color_accordingly_to_id(7)
        self.r3.color_accordingly_to_id(8)

        self.context.objects.append(self.r1)
        self.context.objects.append(self.r2)
        self.context.objects.append(self.r3)

        field = modelFromJSON(open("field_graphics/assets/models/field_vsss.json").read())

        for obj in field:
            # obj.x = 75; obj.y = 65
            self.context.objects.append(obj)

        self.test_SSL_R = SSLRobotMesh(0)
        self.test_SSL_R.y = 10

        self.context.objects.append(self.test_SSL_R)

        for i in range(0,20):
            r: VSSRobotMesh = VSSRobotMesh([.1, .1, .1], [0, 1, 0], [1, 0, 0], [0, 0, 1])
            r.color_accordingly_to_id(i)
            r.x = i*9 - 85
            r.y = -72
            r.rotation = math.pi
            self.context.objects.append(r)

        #Text("Socorro","field_graphics/assets/bitmaps/Arial Bold_1024.bmp")
        robot_text_1 = Text("#05", "field_graphics/assets/bitmaps/Arial Bold_1024.bmp", size=6, tracking=self.r1, anchor=(10, 0))
        robot_text_2 = Text("#07", "field_graphics/assets/bitmaps/Arial Bold_1024.bmp", size=6, tracking=self.r2, anchor=(10, 0))
        robot_text_3 = Text("#08", "field_graphics/assets/bitmaps/Arial Bold_1024.bmp", size=6, tracking=self.r3, anchor=(10, 0))

        self.context.objects.append(robot_text_1)
        self.context.objects.append(robot_text_2)
        self.context.objects.append(robot_text_3)

        self.ball = modelFromJSON(open("field_graphics/assets/models/ball.json").read())[0]
        self.context.objects.append(self.ball)

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

    def update_robot_coord(self, robot_id: int, model: RenderableMesh):
        r = self.match.fetch_robot_by_id(robot_id)
        model.x = r.robot_pos[0] * 100 - 75 # TODO mudar pra dimensões do campo grande
        model.y = r.robot_pos[1] * 100 - 65
        model.rotation = -r.robot_pos[2] + math.pi/2


    def timerEvent(self, event: typing.Optional['QTimerEvent']) -> None:

        if self.no_info:
            self.r1.x = math.sin(self.sim_time/100) * 20
            self.r1.y = math.cos(self.sim_time/100) * 20

            self.r2.x = math.sin(self.sim_time/100 + math.pi * 4/3) * 20
            self.r2.y = math.cos(self.sim_time/100 + math.pi * 4/3) * 20

            self.r3.x = math.sin(self.sim_time/100 + math.pi * 2/3) * 20
            self.r3.y = math.cos(self.sim_time/100 + math.pi * 2/3) * 20

            self.r1.rotation += (1/100)
            self.r2.rotation += (1/100)
            self.r3.rotation += (1/100)

        else:
            self.update_robot_coord(5,self.r1)
            self.update_robot_coord(7,self.r2)
            self.update_robot_coord(8,self.r3)

            ball = self.match.ball
            self.ball.x = ball.ball_pos[0] * 100 - 75; self.ball.y = ball.ball_pos[1] * 100 - 65

        self.sim_time += 1

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
