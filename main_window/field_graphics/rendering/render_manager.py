"""
Responsible for obfuscating most of the most low-level OpenGL calls.
"""
import sys
import json
import numpy as np

from OpenGL import GL
from PyQt6.QtOpenGL import QOpenGLFramebufferObject, QOpenGLShaderProgram, QOpenGLBuffer, QOpenGLShader, \
    QOpenGLVertexArrayObject
from numpy.core import multiarray


def compileShaderProgram(vertex_shader: str, fragment_shader: str) -> QOpenGLShaderProgram:
    """Tries to compile the shader program which the argument strings contain."""
    program = QOpenGLShaderProgram()
    vertex = QOpenGLShader(QOpenGLShader.ShaderTypeBit.Vertex)
    fragment = QOpenGLShader(QOpenGLShader.ShaderTypeBit.Fragment)
    if not vertex.compileSourceCode(vertex_shader):
        print("WARNING: FAILED TO COMPILE VERTEX SHADER")
        print("OpenGL version is " + str(GL.glGetString(GL.GL_VERSION)))
        print(vertex.log())
        print()
    if not fragment.compileSourceCode(fragment_shader):
        print("WARNING: FAILED TO COMPILE FRAGMENT SHADER")
        print("OpenGL version is " + str(GL.glGetString(GL.GL_VERSION)))
        print(fragment.log())
        print()

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
    vertexVBO: int = -1
    colorVBO: int = -1
    vertices: multiarray = None
    colors: multiarray = None
    shaderProgram: QOpenGLShaderProgram = None
    triangle_count: int = 0
    x = 0;
    y = 0;
    z = 0
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
        self.shader_uniform_locations['g_coordinate_vector_loc'] = self.shaderProgram.uniformLocation(
            'globalTranslation')
        self.shader_uniform_locations['g_rotation_float_loc'] = self.shaderProgram.uniformLocation('globalRotation')
        self.shader_uniform_locations['g_scale_float_loc'] = self.shaderProgram.uniformLocation('globalScale')
        self.shader_uniform_locations['coordinate_vector_loc'] = self.shaderProgram.uniformLocation('coord')
        self.shader_uniform_locations['rotation_float_loc'] = self.shaderProgram.uniformLocation('angle')

    def draw(self, tx, ty, scale, rotation, aspect_ratio, sim_time):
        """
        Draws the object at the currently bound OpenGL Framebuffer object.
        Note that all transformations are meant to be GLOBAL transformations,
        local object transformations may be handled internally.
        """
        self.shaderProgram.bind()
        GL.glUniform3f(self.shader_uniform_locations['g_coordinate_vector_loc'], tx, ty, 0)
        GL.glUniform1f(self.shader_uniform_locations['g_rotation_float_loc'], rotation)
        GL.glUniform1f(self.shader_uniform_locations['aspect_ratio_float_loc'], aspect_ratio)
        GL.glUniform1f(self.shader_uniform_locations['g_scale_float_loc'], scale)
        GL.glUniform1f(self.shader_uniform_locations['rotation_float_loc'], self.rotation)
        GL.glUniform3f(self.shader_uniform_locations['coordinate_vector_loc'], self.x, self.y, self.z)

        GL.glEnableVertexAttribArray(0)
        GL.glEnableVertexAttribArray(1)

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.colorVBO)
        self.shaderProgram.setAttributeBuffer(1, GL.GL_FLOAT, 0, 3)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vertexVBO)
        self.shaderProgram.setAttributeBuffer(0, GL.GL_FLOAT, 0, 3)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self.triangle_count * 3)

        GL.glDisableVertexAttribArray(0)
        GL.glDisableVertexAttribArray(1)


def modelFromJSON(data: str):
    jsonobj = json.loads(data)
    objects = jsonobj["objects"]
    models = []

    for obj in objects:
        vertices = obj["vertices"]
        shader = obj["shader"]

        vert_data = []
        color_data = []
        for vertex in vertices:
            vert_data.append(vertex["x"]), vert_data.append(vertex["y"]), vert_data.append(vertex["z"])
            color_data.append(vertex["r"]), color_data.append(vertex["g"]), color_data.append(vertex["b"])
        vertex_sh = open(shader["vertex"]).read()
        fragment_sh = open(shader["fragment"]).read()

        program = compileShaderProgram(vertex_sh, fragment_sh)
        models.append(
            Renderable(np.asarray(vert_data,dtype=np.float32), np.asarray(color_data,dtype=np.float32), program)
        )
    return models


class RenderingContext:
    objects: list[Renderable] = []
    x: float = 0
    y: float = 0
    aspect_ratio: float = 0
    scale: float = .15
    rotation: float = 0

    def __init__(self):
        pass

    def set_transformations(self, x=0, y=0, scale=1, rotation=0):
        self.x = x
        self.y = y
        self.scale = scale
        self.rotation = rotation

    def set_aspect_ratio(self, aspect_ratio):
        self.aspect_ratio = aspect_ratio

    def draw(self, sim_time):
        for obj in self.objects:
            obj.draw(self.x, self.y,
                     self.scale,
                     self.rotation, self.aspect_ratio, sim_time)


def setupGL():
    GL.glEnable(GL.GL_DEPTH_TEST)
    GL.glEnable(GL.GL_BLEND)
    GL.glDisable(GL.GL_CULL_FACE)
    GL.glDepthFunc(GL.GL_LESS)
    GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
    GL.glEnable(GL.GL_DEPTH_TEST)
