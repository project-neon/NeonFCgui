import numpy as np
from OpenGL import GL
from PyQt6.QtOpenGL import QOpenGLShaderProgram

from field_graphics.rendering.objects.renderable_mesh import RenderableMesh
from field_graphics.rendering.render_manager import compileShaderProgram, modelFromJSON


def shaderProgram() -> QOpenGLShaderProgram:
    vsh = open("field_graphics/assets/shaders/VertexShader.vsh").read()
    fsh = open("field_graphics/assets/shaders/SSLRobotFragmentShader.fsh").read()
    return compileShaderProgram(vsh, fsh)

class SSLRobotMesh(RenderableMesh):

    isYellow: bool = False

    def __init__(self, id: int):
        template: RenderableMesh = modelFromJSON(open("field_graphics/assets/models/robot_ssl.json").read())[0]
        super().__init__(template.vertices, np.asarray([0,0,0,0,0,0,0,0,0,0,0,0],dtype=np.float32), template.shaderProgram)
        self.set_id(id)

    def set_id(self, id: int, yellow = True):
        self.id = id
        GL.glUseProgram(self.shaderProgram.programId())
        GL.glUniform1i(
            GL.glGetUniformLocation(self.shaderProgram.programId(),"id"),
            self.id
        )
        self.isYellow = yellow
        if not yellow: 
            GL.glUniform1i(GL.glGetUniformLocation(self.shaderProgram.programId(),"team"), 0)
        else:
            GL.glUniform1i(GL.glGetUniformLocation(self.shaderProgram.programId(),"team"), 1)