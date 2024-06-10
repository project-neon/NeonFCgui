import numpy as np
from PyQt6.QtOpenGL import QOpenGLShaderProgram

from field_graphics.rendering.objects.renderable_mesh import RenderableMesh
from field_graphics.rendering.render_manager import compileShaderProgram, modelFromJSON


def shaderProgram() -> QOpenGLShaderProgram:
    vsh = open("field_graphics/assets/shaders/VertexShader.vsh").read()
    fsh = open("field_graphics/assets/shaders/CutCircleFragmentShader.fsh").read()
    return compileShaderProgram(vsh, fsh)


def gen_color_array(robot_id):
    data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    return np.asarray(data)


class SSLRobotMesh(RenderableMesh):
    def __init__(self, id):
        template: RenderableMesh = modelFromJSON(open("field_graphics/assets/models/robot_ssl.json").read())[0]
        colors = gen_color_array(id)
        super().__init__(template.vertices, colors, template.shaderProgram)
