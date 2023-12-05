"""
Section of the GUI where the field will be displayed.
"""
import math

from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtWidgets import QLabel
from OpenGL import GL

from main_window.field_graphics.field_objects.robot import Robot
from main_window.field_graphics.rendering.render_manager import RenderingContext, setupGL


class FieldView(QOpenGLWidget):
    context = None
    sim_time = 0

    def __init__(self):
        super().__init__()
        self.context = RenderingContext(self.defaultFramebufferObject())
        QLabel("<h1>Campo!</h1>", parent=self)

    def initializeGL(self):
        GL.glInitGl42VERSION()
        GL.glClearColor(0, .7, 0, 0)
        setupGL()
        pass

    def paintGL(self):
        self.makeCurrent()
        GL.glClear(GL.GL_DEPTH_BUFFER_BIT | GL.GL_COLOR_BUFFER_BIT)
        self.context.draw(self.sim_time)
        self.sim_time += 1
        # TODO: essa função precisa ser chamada a cada frame e pelo que me parece
        # ela só está atualizando quando a dimenção da janela muda
        GL.glClearColor(math.sin(self.sim_time/74.643)/2 + .5,
                        math.cos(self.sim_time/344.32)/2 + .5,
                        math.cos(self.sim_time/137.4)/2 + .5, 0)
        #if self.sim_time == 4:
        #    self.context.objects.append(Robot(0, 0, 0))
        #pass
