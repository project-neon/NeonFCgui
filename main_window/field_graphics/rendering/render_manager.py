"""
Responsible for obfuscating most of the most low-level OpenGL calls.
"""

from OpenGL import GL
from PyQt6.QtOpenGL import QOpenGLFramebufferObject, QOpenGLShaderProgram, QOpenGLBuffer, QOpenGLShader
from numpy.core import multiarray


def compileShaderProgram(vertex_shader: str, fragment_shader: str) -> QOpenGLShaderProgram:
    program = QOpenGLShaderProgram()
    vertex = QOpenGLShader(QOpenGLShader.ShaderTypeBit.Vertex)
    fragment = QOpenGLShader(QOpenGLShader.ShaderTypeBit.Fragment)
    if not vertex.compileSourceCode(vertex_shader):
        print("WARNING: FAILED TO COMPILE VERTEX SHADER")
        print("OpenGL version is " + str(GL.glGetString(GL.GL_VERSION)))
        print(vertex.log())
    if not fragment.compileSourceCode(fragment_shader):
        print("WARNING: FAILED TO COMPILE FRAGMENT SHADER")
        print("OpenGL version is " + str(GL.glGetString(GL.GL_VERSION)))
        print(fragment.log())

    program.addShader(vertex)
    program.addShader(fragment)
    if not program.link():
        print("WARNING: FAILED TO BIND SHADER PROGRAM")
        print("OpenGL version is " + str(GL.glGetString(GL.GL_VERSION)))
        print(program.log())
    return program


class Renderable:
    """
    The Renderable class represents any object that may be rendered under a OpenGL context,
    As a OOP quirk, it must handle its own rendering calls, memory allocation
    and external data, such as spatial translations, those features are already
    implemented by the class, however additional vertex attributes and uniforms
    may need to be implemented by subclasses.
    """
    vertexVBO: QOpenGLBuffer = None
    colorVBO: QOpenGLBuffer = None
    vertices: multiarray = None
    colors: multiarray = None
    shaderProgram: QOpenGLShaderProgram = None
    triangles: int = 0
    transformations = {'x': 0, 'y': 0, 'z': 0, 'r': 0}
    shader_uniform_locations = {
        # It is generally considered good practice to store this to minimize GPU calls
        'coordinate_vector_loc': -1,
        'rotation_float_loc': -1,
        'g_coordinate_vector_loc': -1,
        'g_rotation_float_loc': -1,
        'g_scale_float_loc': -1,
        'aspect_ratio_float_loc': -1
    }

    def __init__(self, vertices: multiarray, colors: multiarray, shaderProgram: QOpenGLShaderProgram):
        self.vertices = vertices
        self.colors = colors
        self.shaderProgram = shaderProgram
        self.update_shader_uniform_locations()
        self.triangles = int(len(vertices) / 9)
        self.vertexVBO = QOpenGLBuffer()
        self.vertexVBO.create()
        self.colorVBO = QOpenGLBuffer()
        self.colorVBO.create()
        self.update_vertex_attributes()

    def update_vertex_attributes(self):
        self.vertexVBO.allocate(self.vertices, len(self.vertices) * 3)
        self.colorVBO.allocate(self.colors, len(self.colors) * 3)

    def update_shader_uniform_locations(self):
        self.shader_uniform_locations['g_coordinate_vector_loc'] = self.shaderProgram.uniformLocation(
            'globalTranslation')
        self.shader_uniform_locations['g_rotation_float_loc'] = self.shaderProgram.uniformLocation('globalRotation')
        self.shader_uniform_locations['g_scale_float_loc'] = self.shaderProgram.uniformLocation('globalScale')
        self.shader_uniform_locations['coordinate_vector_loc'] = self.shaderProgram.uniformLocation('coord')
        self.shader_uniform_locations['rotation_float_loc'] = self.shaderProgram.uniformLocation('angle')
        self.shader_uniform_locations['aspect_ratio_float_loc'] = self.shaderProgram.uniformLocation('aspectRatio')

    def pre_render_logic(self):
        GL.glEnableVertexAttribArray(0)
        GL.glEnableVertexAttribArray(1)
        pass

    def post_render_logic(self):
        GL.glDisableVertexAttribArray(0)
        GL.glDisableVertexAttribArray(1)
        pass

    def draw(self, tx, ty, depth, scale, rotation, aspect_ratio, sim_time):
        """
        Draws the object at the currently bound OpenGL Framebuffer object.
        Note that all transformations are meant to be GLOBAL transformations,
        local object transformations may be handled internally.
        """
        self.pre_render_logic()
        self.shaderProgram.setUniformValue(self.shader_uniform_locations['g_coordinate_vector_loc'], tx, ty, depth,
                                           scale)
        self.shaderProgram.setUniformValue(self.shader_uniform_locations['g_rotation_float_loc'], rotation)
        self.shaderProgram.setUniformValue(self.shader_uniform_locations['aspect_ratio_float_loc'], aspect_ratio)
        self.colorVBO.bind()
        self.shaderProgram.setAttributeBuffer(1, GL.GL_FLOAT, 0, 3)
        self.vertexVBO.bind()
        self.shaderProgram.setAttributeBuffer(0, GL.GL_FLOAT, 0, 3)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3 * self.triangles)
        self.post_render_logic()


class RenderingContext:
    objects = []
    transformations = {'x': 0, 'y': 0, 'z': 0, 'scale': 1, 'rotation': 0, 'aspect_ratio': 1}
    framebuffer = None

    def __init__(self, framebuffer: QOpenGLFramebufferObject | None | int = None):
        self.framebuffer = framebuffer

    def set_transformations(self, x=0, y=0, z=0, scale=0, rotation=0):
        self.transformations['x'] = x
        self.transformations['y'] = y
        self.transformations['z'] = z

        self.transformations['scale'] = scale
        self.transformations['rotation'] = rotation

    def set_aspect_ratio(self, aspect_ratio):
        self.transformations['aspect_ratio'] = aspect_ratio

    def draw(self, sim_time):
        for obj in self.objects:
            obj.draw(self.transformations['x'], self.transformations['y'], self.transformations['z'],
                     self.transformations['scale'],
                     self.transformations['rotation'], self.transformations['aspect_ratio'], sim_time)


def setupGL():
    GL.glEnable(GL.GL_DEPTH_TEST)
    GL.glEnable(GL.GL_BLEND)
    GL.glDisable(GL.GL_CULL_FACE)
    GL.glDepthFunc(GL.GL_LESS)
    GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
    GL.glEnable(GL.GL_DEPTH_TEST)
