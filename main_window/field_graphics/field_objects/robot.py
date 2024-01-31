
import numpy as np
from PyQt6.QtOpenGL import QOpenGLShaderProgram

from main_window.field_graphics.rendering.render_manager import Renderable, compileShaderProgram, modelFromJSON


def shaderProgram() -> QOpenGLShaderProgram:
    vsh = open("main_window/field_graphics/assets/shaders/VertexShader.vsh").read()
    fsh = open("main_window/field_graphics/assets/shaders/FragmentShader.fsh").read()
    return compileShaderProgram(vsh, fsh)

class Robot(Renderable):
    def __init__(self, robot_color: list, back_tag_color: list, left_tag_color: list, right_tag_color: list):
        r = robot_color[0]; g = robot_color[1]; b = robot_color[2]
        sr = back_tag_color[0]; sg = back_tag_color[1]; sb = back_tag_color[2]
        sr2 = left_tag_color[0]; sg2 = left_tag_color[1]; sb2 = left_tag_color[2]
        sr3 = right_tag_color[0]; sg3 = right_tag_color[1]; sb3 = right_tag_color[2]
        template: Renderable = modelFromJSON(open("main_window/field_graphics/assets/models/robot.json").read())[0]
        colors = np.asarray([
            r,g,b, r,g,b, r,g,b, r,g,b, r,g,b, r,g,b,
            sr,sg,sb, sr,sg,sb, sr,sg,sb, sr,sg,sb, sr,sg,sb, sr,sg,sb,
            sr2,sg2,sb2, sr2,sg2,sb2, sr2,sg2,sb2, sr2,sg2,sb2, sr2,sg2,sb2, sr2,sg2,sb2,
            sr3,sg3,sb3, sr3,sg3,sb3, sr3,sg3,sb3, sr3,sg3,sb3, sr3,sg3,sb3, sr3,sg3,sb3,
        ], dtype=np.float32)
        super().__init__(template.vertices, colors, template.shaderProgram)

