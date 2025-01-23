"""
Responsible for obfuscating most of the most lower-level OpenGL calls.
"""
import json

import numpy as np
from OpenGL import GL
from PIL import Image
from PyQt6.QtOpenGL import QOpenGLShaderProgram, QOpenGLShader

from field_graphics.rendering.objects.renderable_mesh import RenderableMesh


def compileShaderProgram(vertex_shader: str, fragment_shader: str) -> QOpenGLShaderProgram | None:
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
        print()
        return None

    return program


def loadTexture(path: str) -> int:
    """Loads a texture object from an image file in the specified path and returns its OpenGL qualified name"""
    img = Image.open(path)
    # data = numpy.fromstring(str(img), numpy.uint8)
    w, h = img.size
    by = img.tobytes("raw", "RGBA", 0, -1)

    texture_id = GL.glGenTextures(1)
    GL.glBindTexture(GL.GL_TEXTURE_2D, texture_id)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST)
    GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, w, h, 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, by)
    GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
    return texture_id



def modelFromJSON(data: str):
    jsonobj = json.loads(data)
    objects = jsonobj["objects"]
    models = []

    for obj in objects:
        vertices = obj["vertices"]
        shader = obj["shader"]
        vert_data = []
        color_data = []
        uniforms = shader["uniforms"]

        for vertex in vertices:
            vert_data.append(vertex["x"]), vert_data.append(vertex["y"]), vert_data.append(vertex["z"])
            color_data.append(vertex["r"]), color_data.append(vertex["g"]), color_data.append(vertex["b"])
        vertex_sh = open(shader["vertex"]).read()
        fragment_sh = open(shader["fragment"]).read()
        program = compileShaderProgram(vertex_sh, fragment_sh)

        GL.glUseProgram(program.programId())
        for uniform in uniforms:
            uniform_type = uniform["type"] #TODO: support all data types
            loc = GL.glGetUniformLocation(program.programId(), uniform["name"])
            if uniform_type == "int": GL.glUniform1i(loc, int(uniform["v0"]))
            elif uniform_type == "float": GL.glUniform1f(loc, float(uniform["v0"]))
            elif uniform_type == "vec2": GL.glUniform2f(loc, float(uniform["v0"]), float(uniform["v1"]))
            elif uniform_type == "vec3": GL.glUniform3f(loc, float(uniform["v0"]), float(uniform["v1"]), float(uniform["v2"]))
            elif uniform_type == "vec4": GL.glUniform4f(loc, float(uniform["v0"]), float(uniform["v1"]), float(uniform["v2"]), float(uniform["v3"]))
        models.append(
            RenderableMesh(np.asarray(vert_data, dtype=np.float32), np.asarray(color_data, dtype=np.float32), program)
        )
    return models


def setupGL():
    """"Sets up the OpenGL default environment properties"""
    GL.glEnable(GL.GL_DEPTH_TEST)
    GL.glEnable(GL.GL_BLEND)
    GL.glDisable(GL.GL_CULL_FACE)
    GL.glDepthFunc(GL.GL_LESS)
    # GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
    GL.glBlendFuncSeparate(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA, GL.GL_ONE, GL.GL_ZERO);