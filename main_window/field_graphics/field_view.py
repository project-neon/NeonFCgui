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
    aspect_ratio: float = 1
    def __init__(self):
        super().__init__()

        self.context = RenderingContext(self.defaultFramebufferObject())
        QLabel("<h1>Campo!</h1>", parent=self)

    def initializeGL(self):
        GL.glInitGl42VERSION()
        setupGL()
        pass

    def resizeGL(self, w: int, h: int) -> None:
        # A documentação do PYQT fala pra eu chamar o GLViewport aqui, mas me parece que o próprio PyQT já redimensiona
        # o framebuffer automaticamente, então fica meio redundante na minha opinião
        self.aspect_ratio = float(w) / float(h)
        pass


    def paintGL(self):
        GL.glClear(GL.GL_DEPTH_BUFFER_BIT | GL.GL_COLOR_BUFFER_BIT)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        self.context.draw(self.sim_time)
        self.sim_time += 1
        # TODO: essa função precisa ser chamada a cada frame e pelo que me parece
        # ela só está atualizando quando a dimenção da janela muda
        GL.glClearColor(math.sin(self.sim_time / 14.643) / 2 + .5,
                        math.cos(self.sim_time / 23.32) / 2 + .5,
                        math.cos(self.sim_time / 43.4) / 2 + .5, 0)

        if self.sim_time == 1:
            # !! TESTES !!! TODO REMOVER VVV --- VVV
            self.local_vertex_location_test_VBO = GL.glGenBuffers(1)
            self.local_vertex_color_test_VBO = GL.glGenBuffers(1)
            self.shader = robot.shaderProgram()
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.local_vertex_location_test_VBO)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, np.asarray([.2,-.2,0, -.2,-.2,0, 0,.2,0], dtype=np.float32), GL.GL_STATIC_DRAW)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.local_vertex_color_test_VBO)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, np.asarray([1,0,0 , 0,1,0 , 0,0,1], dtype=np.float32),GL.GL_STATIC_DRAW)
            # self.r = Robot(0, 0, 0)
            # self.context.objects.append(self.r)

        self.shader.bind()
        GL.glUniform1f(self.shader.uniformLocation("angle"), self.sim_time / 20)
        GL.glUniform1f(self.shader.uniformLocation("aspectRatio"), self.aspect_ratio)

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.local_vertex_location_test_VBO)
        GL.glEnableVertexAttribArray(0)
        GL.glEnableVertexAttribArray(1)
        self.shader.setAttributeBuffer(0, GL.GL_FLOAT, 0, 3)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.local_vertex_color_test_VBO)
        self.shader.setAttributeBuffer(1, GL.GL_FLOAT, 0, 3)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.local_vertex_location_test_VBO)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)
        GL.glDisableVertexAttribArray(1)
        GL.glDisableVertexAttribArray(0)