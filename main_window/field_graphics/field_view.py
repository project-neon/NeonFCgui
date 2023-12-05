"""
Section of the GUI where the field will be displayed.
"""

from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtWidgets import QLabel
from OpenGL import GL
from PyQt6.QtOpenGL import QOpenGLFunctions_4_1_Core as GLF, QOpenGLFramebufferObject

from main_window.field_graphics.render_manager import RenderingContext, setupGL


class FieldView(QOpenGLWidget):
    context = None
    sim_time = 0

    def __init__(self):
        super().__init__()
        self.context = RenderingContext()
        QLabel("<h1>Campo!</h1>", parent=self)

    def initializeGL(self):
        GL.glInitGl42VERSION()
        GL.glClearColor(0, .7, 0, 0)
        setupGL()
        pass

    def paintGL(self):
        self.makeCurrent()
        self.context.draw(self.sim_time)
        self.sim_time += 1
        pass
