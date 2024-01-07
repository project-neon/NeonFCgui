
import numpy as np
from PyQt6.QtOpenGL import QOpenGLShaderProgram

from main_window.field_graphics.rendering.render_manager import Renderable, compileShaderProgram


def shaderProgram() -> QOpenGLShaderProgram:
    vsh = open("main_window/field_graphics/assets/shaders/VertexShader.vsh").read()
    fsh = open("main_window/field_graphics/assets/shaders/FragmentShader.fsh").read()
    return compileShaderProgram(vsh, fsh)

DEFAULT_TAG_DEPTH = -.1
CORNER_DIST = .27
class Robot(Renderable): #TODO: pegar as dimenções certas
    def __init__(self, robotColor: list, stampColor1: list, stampColor2: list):
        r = robotColor[0]; g = robotColor[1]; b = robotColor[2]; dfd = DEFAULT_TAG_DEPTH; cd = CORNER_DIST
        sr = stampColor1[0]; sg = stampColor1[1]; sb = stampColor1[2];
        sr2 = stampColor2[0]; sg2 = stampColor2[1]; sb2 = stampColor2[2];
        vert = np.asarray([
            -1,-1,0, 1,-1,0, -1,1,0, 1,1,0, -1,1,0, 1,-1,0,  # quadrado preto
            -1+cd,cd/2,dfd, 1-cd,cd/2,dfd, -1+cd,1-cd,dfd, 1-cd,1-cd,dfd, -1+cd,1-cd,dfd ,1-cd,cd/2,dfd,  # quadrado de cima
            -1+cd,-1+cd,dfd, 1-cd,-1+cd,dfd, -1+cd,-cd/2,dfd, 1-cd,-cd/2,dfd, -1+cd,-cd/2,dfd ,1-cd,-1+cd,dfd  # quadrado de baixo
        ], dtype=np.float32)
        col = np.asarray([r, g, b, r, g, b, r, g, b, r, g, b, r, g, b, r, g, b,
                          sr,sg,sb,sr,sg,sb,sr,sg,sb,sr,sg,sb,sr,sg,sb,sr,sg,sb,
                          sr2,sg2,sb2,sr2,sg2,sb2,sr2,sg2,sb2,sr2,sg2,sb2,sr2,sg2,sb2,sr2,sg2,sb2,
                          ], dtype=np.float32)
        super().__init__(vert, col, shaderProgram())
