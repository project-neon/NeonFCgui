from OpenGL import GL
from PyQt6.QtOpenGL import QOpenGLShaderProgram
from numpy.core import multiarray

class Renderable:
    """
    The renderable class is an abstract class that serves as template for any object which may use the OpenGL pipeline.
    """
    def draw(self, tx, ty, scale, rotation, aspect_ratio, sim_time):
        pass
    def update_vertex_attributes(self):
        pass
    def update_shader_uniform_locations(self):
        pass
