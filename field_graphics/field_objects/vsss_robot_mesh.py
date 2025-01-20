import json

import numpy as np
import math
from OpenGL import GL
from PyQt6.QtOpenGL import QOpenGLShaderProgram

from field_graphics.rendering.render_manager import RenderableMesh, compileShaderProgram, modelFromJSON


def shaderProgram() -> QOpenGLShaderProgram:
    vsh = open("field_graphics/assets/shaders/VertexShader.vsh").read()
    fsh = open("field_graphics/assets/shaders/FragmentShader.fsh").read()
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


class VSSSRobotMesh(RenderableMesh):
    def __init__(self, robot_color: list, back_tag_color: list, left_tag_color: list, right_tag_color: list):
        template: RenderableMesh = modelFromJSON(open("field_graphics/assets/models/robot_vsss.json").read())[0]
        colors = gen_color_array(robot_color,back_tag_color,left_tag_color,right_tag_color)
        super().__init__(template.vertices, colors, template.shaderProgram)

    def color_accordingly_to_id(self, robot_id: int, team_yellow: bool = False):
        # FIXME: bandaid solution
        if team_yellow: robot_id += 10
        # FIXME: hardcoded path, plus the func does not actually take the ID into question
        dat = json.loads(open("id_dict.json").read())
        
        robot_id = max(min(robot_id,20),1)
        
        for robot in dat:
            #print(robot)
            if int(robot['id']) == robot_id:
                dat = robot
                break
        
        back_tag = dat["back_tag"]; back_tag = [back_tag["r"],back_tag["g"],back_tag["b"]]
        left_tag = dat["left_tag"]; left_tag = [left_tag["r"],left_tag["g"],left_tag["b"]]
        right_tag = dat["right_tag"]; right_tag = [right_tag["r"],right_tag["g"],right_tag["b"]]
        self.update_color([.1,.1,.1], back_tag, left_tag, right_tag)


    def update_color(self, robot_color: list,back_tag_color: list, left_tag_color: list, right_tag_color: list):
        self.colors = gen_color_array(robot_color,back_tag_color,left_tag_color,right_tag_color)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.colorVBO)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.colors, GL.GL_STATIC_DRAW)
