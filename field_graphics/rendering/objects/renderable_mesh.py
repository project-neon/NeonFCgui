from OpenGL import GL
from PyQt6.QtOpenGL import QOpenGLShaderProgram
from numpy.core import multiarray

from field_graphics.rendering.renderable import Renderable
class RenderableMesh (Renderable):
    """
    The RenderableMesh class represents any object that may be rendered under a OpenGL context,
    As a OOP quirk, it must handle its own rendering calls, memory allocation
    and external data, such as spatial translations, those features are already
    implemented by the class, however additional vertex attributes and uniforms
    may need to be implemented by subclasses as needed.
    """
    vertexVBO: int = -1
    colorVBO: int = -1
    vertices: multiarray = None
    colors: multiarray = None
    shaderProgram: QOpenGLShaderProgram = None
    triangle_count: int = 0
    x = 0; y = 0; z = 0
    rotation = 0
    shader_uniform_locations = {
        # It is generally considered good practice to store this to minimize GPU calls
        'coordinate_vector_loc': -1,
        'rotation_float_loc': -1,
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
        self.triangle_count = int(len(vertices) / 9)
        self.vertexVBO = GL.glGenBuffers(1)
        self.colorVBO = GL.glGenBuffers(1)
        self.update_vertex_attributes()

    def update_vertex_attributes(self):
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vertexVBO)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.vertices, GL.GL_STATIC_DRAW)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.colorVBO)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.colors, GL.GL_STATIC_DRAW)

    def update_shader_uniform_locations(self):
        self.shader_uniform_locations['aspect_ratio_float_loc'] = self.shaderProgram.uniformLocation('aspectRatio')
        self.shader_uniform_locations['g_coordinate_vector_loc'] = self.shaderProgram.uniformLocation('globalTranslation')
        self.shader_uniform_locations['g_rotation_float_loc'] = self.shaderProgram.uniformLocation('globalRotation')
        self.shader_uniform_locations['g_scale_float_loc'] = self.shaderProgram.uniformLocation('globalScale')
        self.shader_uniform_locations['coordinate_vector_loc'] = self.shaderProgram.uniformLocation('coord')
        self.shader_uniform_locations['rotation_float_loc'] = self.shaderProgram.uniformLocation('angle')

    def draw(self, tx, ty, scale, rotation, aspect_ratio, sim_time):
        """
        Draws the object at the currently bound OpenGL Framebuffer object.
        Note that all transformations passed as parameters to this function
        are meant to be GLOBAL transformations,
        local object transformations are be handled with internal variables.
        """
        #print('rot render ' + str(self.rotation))
        self.shaderProgram.bind()
        GL.glUseProgram(self.shaderProgram.programId())
        GL.glUniform3f(self.shader_uniform_locations['g_coordinate_vector_loc'], tx, ty, 0)
        GL.glUniform1f(self.shader_uniform_locations['g_rotation_float_loc'], rotation)
        GL.glUniform1f(self.shader_uniform_locations['aspect_ratio_float_loc'], aspect_ratio)
        GL.glUniform1f(self.shader_uniform_locations['g_scale_float_loc'], scale)
        GL.glUniform1f(self.shader_uniform_locations['rotation_float_loc'], self.rotation)
        GL.glUniform3f(self.shader_uniform_locations['coordinate_vector_loc'], self.x, self.y, self.z)

        GL.glEnableVertexAttribArray(0) # Coordinate vertex array
        GL.glEnableVertexAttribArray(1) # Color vertex array

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.colorVBO)
        self.shaderProgram.setAttributeBuffer(1, GL.GL_FLOAT, 0, 3)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vertexVBO)
        self.shaderProgram.setAttributeBuffer(0, GL.GL_FLOAT, 0, 3)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self.triangle_count * 3)

        GL.glDisableVertexAttribArray(0)
        GL.glDisableVertexAttribArray(1)

