"""
Section of the GUI where the field will be displayed.
"""
import math
import typing

from OpenGL import GL
from PyQt6 import QtGui
from PyQt6.QtCore import QTimerEvent
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtWidgets import QLabel

from entities import Match
from main_window.field_graphics.field_objects.robot import Robot
from main_window.field_graphics.field_objects.text import Text
from main_window.field_graphics.rendering.animation_manager import AnimationManager
from main_window.field_graphics.rendering.render_manager import RenderingContext, setupGL, modelFromJSON


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

        self.r1: Robot = Robot([.1, .1, .1], [0, 1, 0], [1, 0, 0], [0, 0, 1])
        self.r2: Robot = Robot([.1, .1, .1], [0, 1, 0], [1, 0, 0], [0, 0, 1])
        self.r3: Robot = Robot([.1, .1, .1], [0, 1, 0], [1, 0, 0], [0, 0, 1])

        self.r1.rotation = math.pi/2
        self.r2.rotation = -math.pi/6
        self.r3.rotation = math.pi * (9.5/3)

        self.r1.color_accordingly_to_id(5)
        self.r2.color_accordingly_to_id(7)
        self.r3.color_accordingly_to_id(8)

        self.context.objects.append(self.r1)
        self.context.objects.append(self.r2)
        self.context.objects.append(self.r3)

        field = modelFromJSON(open("main_window/field_graphics/assets/models/field_vsss.json").read())

        for obj in field:
            self.context.objects.append(obj)

        #Text("Socorro","main_window/field_graphics/assets/bitmaps/Arial Bold_1024.bmp")
        robot_text_1 = Text("#05", "main_window/field_graphics/assets/bitmaps/Arial Bold_1024.bmp", size=6, tracking=self.r1, anchor=(10, 0))
        robot_text_2 = Text("#07", "main_window/field_graphics/assets/bitmaps/Arial Bold_1024.bmp", size=6, tracking=self.r2, anchor=(10, 0))
        robot_text_3 = Text("#08", "main_window/field_graphics/assets/bitmaps/Arial Bold_1024.bmp", size=6, tracking=self.r3, anchor=(10, 0))

        self.context.objects.append(robot_text_1)
        self.context.objects.append(robot_text_2)
        self.context.objects.append(robot_text_3)

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
        self.no_info = self.match.last_update_time == 0
        if self.no_info: # TODO: remover
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
            r_5 = self.match.fetch_robot_by_id(5)
            r_7 = self.match.fetch_robot_by_id(7)
            r_8 = self.match.fetch_robot_by_id(8)

            self.r1.x = r_5.robot_pos[0]; self.r1.y = r_5.robot_pos[1]; self.r1.rotation = r_5.robot_pos[2]
            self.r2.x = r_7.robot_pos[0]; self.r2.y = r_7.robot_pos[1]; self.r2.rotation = r_7.robot_pos[2]
            self.r3.x = r_8.robot_pos[0]; self.r3.y = r_8.robot_pos[1]; self.r3.rotation = r_8.robot_pos[2]


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
