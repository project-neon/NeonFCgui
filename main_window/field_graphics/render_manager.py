"""
Responsible for obfuscating most of the most low-level OpenGL calls.
"""

from OpenGL import GL
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtGui import QOpenGLContext
from PyQt6.QtWidgets import QApplication
from PyQt6.QtOpenGL import QOpenGLFunctions_4_1_Core as GLF, QOpenGLFramebufferObject


class Renderable:
    # The Renderable class represents any object that may be rendered under a OpenGL context,
    # As a OOP quirk, it must handle its own rendering calls and memory allocation
    # And external data, such as spatial translations must be provided by the external context.

    vertexVBO = None
    colorVBO = None
    vertices = None
    colors = None
    shaderProgram = None

    transformations = {'x': 0, 'y': 0, 'rotation': 0}
    shader_uniform_locations = {
        # It is generally considered good practice to store this to minimize GPU calls
        'coordinate_vector_loc': -1,
        'rotation_float_loc': -1,
        'scale_float_loc': -1
    }

    def __init__(self, vertices, colors, shaderProgram):
        self.vertices = vertices
        self.colors = colors
        self.shaderProgram = shaderProgram

    def pre_render_logic(self):
        # in case additional buffer objects need their attributes enabled for access before rendering
        pass

    def post_render_logic(self):
        # disable buffer objects after rendering
        pass

    def draw(self, tx, ty, scale, rotation, aspect_ratio, sim_time):
        """
        Draws the object at the currently bound OpenGL Framebuffer object.
        Note that all transformations are meant to be GLOBAL transformations,
        local object transformations may be handled internally.
        """
        pass


class RenderingContext:
    objects = []
    transformations = {'x': 0, 'y': 0, 'scale': 1, 'rotation': 0}
    framebuffer = None

    def __init__(self, framebuffer: QOpenGLFramebufferObject):
        self.framebuffer = framebuffer

    def set_transformations(self, x=0, y=0, scale=0, rotation=0):
        self.transformations['x'] = x
        self.transformations['y'] = y
        self.transformations['scale'] = scale
        self.transformations['rotation'] = rotation

    def draw(self, sim_time):
        self.framebuffer.bind()
        GL.glClear(GLC.GL_DEPTH_BUFFER_BIT | GLC.GL_COLOR_BUFFER_BIT)
        for obj in self.objects:
            obj.pre_render_logic()
            obj.draw(self.transformations['x'], self.transformations['y'], self.transformations['scale'],
                     self.transformations['rotation'], sim_time)
            obj.post_render_logic()


def setupGL():
    GL.glInitGl41VERSION()
    GL.glEnable(GL.GL_DEPTH_TEST)
    GL.glEnable(GL.GL_BLEND)
    GL.glDisable(GL.GL_CULL_FACE)
    GL.glDepthFunc(GL.GL_LESS)
    GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
    GL.glEnable(GL.GL_DEPTH_TEST)
