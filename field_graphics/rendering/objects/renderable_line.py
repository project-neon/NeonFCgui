from OpenGL import GL
from PyQt6.QtOpenGL import QOpenGLShaderProgram
from numpy.core import multiarray

from field_graphics.rendering.renderable import Renderable


class RenderableLine(Renderable):
    """
    The RenderableLine class represents a dinamically alocated Renderable, that of course is a line.
    By being dinamically alocated it allows for faster data transfer than the RenderableMesh class, which is statially alocated.
    This class is made mostly for pathfinding visualization, which may require intensive shape-changing.
    """

    vertex_VBO: int = -1
    color_VBO: int = -1
    vertices: multiarray = None
    colors: multiarray = None
    shaderProgram: QOpenGLShaderProgram = None
    x = 0; y = 0; z = 0

    shader_uniform_locations = {
        'coordinate_vector_loc': -1,
        'g_coordinate_vector_loc': -1,
        'g_rotation_float_loc': -1,
        'g_scale_float_loc': -1,
        'aspect_ratio_float_loc': -1
    }

    def __init__(self, vertices: multiarray, colors: multiarray, shader_program: QOpenGLShaderProgram):
        self.vertices = vertices
        self.colors = colors
        self.shaderProgram = shader_program
        self.update_shader_uniform_locations()
        self.line_count = len(vertices)/3 - 3 # FIXME ?
        self.vertexVBO = GL.glGenBuffers(1)
        self.colorVBO = GL.glGenBuffers(1)
        self.update_vertex_attributes()
        self.update_line_buffer()
        pass

    def update_vertex_attributes(self):
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.colorVBO)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.colors, GL.GL_STATIC_DRAW)
        pass

    def update_shader_uniform_locations(self):
        self.shader_uniform_locations['aspect_ratio_float_loc'] = self.shaderProgram.uniformLocation('aspectRatio')
        self.shader_uniform_locations['g_coordinate_vector_loc'] = self.shaderProgram.uniformLocation('globalTranslation')
        self.shader_uniform_locations['coordinate_vector_loc'] = self.shaderProgram.uniformLocation('coord')
        self.shader_uniform_locations['g_rotation_float_loc'] = self.shaderProgram.uniformLocation('globalRotation')
        self.shader_uniform_locations['g_scale_float_loc'] = self.shaderProgram.uniformLocation('globalScale')

    def update_line_buffer(self, buffer: multiarray = None):
        if not buffer is None: self.vertices = buffer
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vertexVBO)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.vertices, GL.GL_STATIC_DRAW)
        self.line_count = len(self.vertices) - 1
        pass

    def draw(self, tx, ty, scale, rotation, aspect_ratio, sim_time):

        self.shaderProgram.bind()
        GL.glUseProgram(self.shaderProgram.programId())
        GL.glUniform3f(self.shader_uniform_locations['g_coordinate_vector_loc'], tx, ty, 0)
        GL.glUniform3f(self.shader_uniform_locations['coordinate_vector_loc'], self.x, self.y, self.z)
        GL.glUniform1f(self.shader_uniform_locations['g_rotation_float_loc'], 0)
        GL.glUniform1f(self.shader_uniform_locations['aspect_ratio_float_loc'], aspect_ratio)
        GL.glUniform1f(self.shader_uniform_locations['g_scale_float_loc'], scale)

        GL.glEnableVertexAttribArray(0)
        GL.glEnableVertexAttribArray(1)

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.colorVBO)
        self.shaderProgram.setAttributeBuffer(1, GL.GL_FLOAT, 0, 3)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vertexVBO)
        self.shaderProgram.setAttributeBuffer(0, GL.GL_FLOAT, 0, 3)

        GL.glDrawArrays(GL.GL_LINE_STRIP, 0, self.line_count * 3)

        GL.glDisableVertexAttribArray(0)
        GL.glDisableVertexAttribArray(1)

