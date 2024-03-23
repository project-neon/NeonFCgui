import numpy as np
from OpenGL import GL
from PyQt6.QtOpenGL import QOpenGLShaderProgram

from main_window.field_graphics.rendering.render_manager import Renderable, compileShaderProgram, modelFromJSON


def shaderProgram() -> QOpenGLShaderProgram:
    vsh = open("main_window/field_graphics/assets/shaders/VertexShader.vsh").read()
    fsh = open("main_window/field_graphics/assets/shaders/FragmentShader.fsh").read()
    return compileShaderProgram(vsh, fsh)


def gen_color_array(robot_color: list, back_tag_color: list, left_tag_color: list, right_tag_color: list):
    r = robot_color[0]; g = robot_color[1]; b = robot_color[2]
    sr = back_tag_color[0]; sg = back_tag_color[1]; sb = back_tag_color[2]
    sr2 = left_tag_color[0]; sg2 = left_tag_color[1]; sb2 = left_tag_color[2]
    sr3 = right_tag_color[0]; sg3 = right_tag_color[1]; sb3 = right_tag_color[2]
    colors = np.asarray([
        r,g,b, r,g,b, r,g,b, r,g,b, r,g,b, r,g,b,
        sr,sg,sb, sr,sg,sb, sr,sg,sb, sr,sg,sb, sr,sg,sb, sr,sg,sb,
        sr2,sg2,sb2, sr2,sg2,sb2, sr2,sg2,sb2, sr2,sg2,sb2, sr2,sg2,sb2, sr2,sg2,sb2,
        sr3,sg3,sb3, sr3,sg3,sb3, sr3,sg3,sb3, sr3,sg3,sb3, sr3,sg3,sb3, sr3,sg3,sb3,
    ], dtype=np.float32)
    return colors


class Robot(Renderable):
    def __init__(self, robot_color: list, back_tag_color: list, left_tag_color: list, right_tag_color: list):

        template: Renderable = modelFromJSON(open("main_window/field_graphics/assets/models/robot.json").read())[0]

        colors = gen_color_array(robot_color,back_tag_color,left_tag_color,right_tag_color)

        super().__init__(template.vertices, colors, template.shaderProgram)

    def color_accordingly_to_id(self, robot_id: int, team_color=None):
        if team_color is None:
            team_color = [.95, .95, .1]

        if robot_id == 5:
            self.update_color([.1, .1, .1], team_color, [.2, .2, 1.], [.1, .7, .1])
        elif robot_id == 7:
            self.update_color([.1, .1, .1], team_color, [.1, .7, .1], [.9, .5, .6])
        elif robot_id == 8:
            self.update_color([.1, .1, .1], team_color, [.2, .2, 1.], [.9, .5, .8])

    def update_color(self, robot_color: list,back_tag_color: list, left_tag_color: list, right_tag_color: list):
        self.colors = gen_color_array(robot_color,back_tag_color,left_tag_color,right_tag_color)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.colorVBO)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.colors, GL.GL_STATIC_DRAW)
