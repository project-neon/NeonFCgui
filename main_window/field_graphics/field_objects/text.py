import math

from PIL import Image
import numpy
import numpy as np

from main_window.field_graphics.field_objects import robot
from main_window.field_graphics.rendering.render_manager import Renderable, loadTexture, compileShaderProgram
from OpenGL import GL


class Text(Renderable):
    texture_id = -1
    texture_coordinates_VBO = -1
    texture_coors = []

    def __init__(self, display: str, texture_directory: str, color=None, size=1, fixed_rotation=False, tracking: Renderable | None = None, anchor: tuple = (0, 0)):

        if color is None:
            color = [1, 1, 1, 1]
        self.display = display
        self.texture_directory = texture_directory
        self.color = color
        self.tracking = tracking
        self.fixed_rotation = fixed_rotation
        self.anchor = anchor

        vertices = []
        colors = []

        i = 0.0

        for act in display:
            pos: int = ord(act) - 32
            bmp_x: int = pos % 16
            bmp_y: int = math.floor(pos / 16)

            wspc_c = i / 2 - display.__len__() / 4

            vertices.append(wspc_c);      vertices.append(-.5); vertices.append(-.8)  # --
            vertices.append(wspc_c + .5); vertices.append(-.5); vertices.append(-.8)  # +-
            vertices.append(wspc_c);      vertices.append(.5);  vertices.append(-.8)  # -+

            vertices.append(wspc_c);      vertices.append(.5);  vertices.append(-.8)  # -+
            vertices.append(wspc_c + .5); vertices.append(-.5); vertices.append(-.8)  # +-
            vertices.append(wspc_c + .5); vertices.append(.5);  vertices.append(-.8)  # ++

            # Sampla os as coordenadas da textura com base no sistema de coordenadas do OpenGL
            # Assumindo que o bitmap seja de 16 * 16 caracteres, o que já é suficiente pro alfabeto ASCII
            # da lingua portuguesa
            
            txs_x_b = bmp_x / 16;       txs_y_e = 1 - (bmp_y / 16)
            txs_x_e = txs_x_b + 1 / 32; txs_y_b = txs_y_e - 1 / 16

            self.texture_coors.append(txs_x_b); self.texture_coors.append(txs_y_b)
            self.texture_coors.append(txs_x_e); self.texture_coors.append(txs_y_b)
            self.texture_coors.append(txs_x_b); self.texture_coors.append(txs_y_e)

            self.texture_coors.append(txs_x_b); self.texture_coors.append(txs_y_e)
            self.texture_coors.append(txs_x_e); self.texture_coors.append(txs_y_b)
            self.texture_coors.append(txs_x_e); self.texture_coors.append(txs_y_e)

            i += 1

        self.texture_coors = np.asarray(self.texture_coors, dtype=numpy.float32)

        for i in range(int(vertices.__len__()/3)):
            vertices[i*3] *= size; vertices[i*3+1] *= size
            colors.append(0); colors.append(0); colors.append(0)

        self.texture_id = loadTexture(texture_directory)
        self.texture_coordinates_VBO = GL.glGenBuffers(1)

        print(self.texture_coors)

        vertices = np.asarray(vertices, dtype=np.float32)
        colors = np.asarray(colors, dtype=np.float32)

        vsh = "main_window/field_graphics/assets/shaders/TextVertexShader.vsh"
        vsh = open(vsh).read()
        fsh = "main_window/field_graphics/assets/shaders/TextFragmentShader.fsh"
        fsh = open(fsh).read()
        shader = compileShaderProgram(vsh, fsh)
        super().__init__(vertices, colors, shader)

    def draw(self, tx, ty, scale, rotation, aspect_ratio, sim_time):

        if self.tracking is None:
            self.x = self.anchor[0]; self.y = self.anchor[1]
        else:
            self.x = self.anchor[0] + self.tracking.x; self.y = self.anchor[1] + self.tracking.y

        self.shaderProgram.bind()
        GL.glEnable(GL.GL_TEXTURE_2D)
        GL.glEnableVertexAttribArray(2)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture_id)
        GL.glActiveTexture(GL.GL_TEXTURE0)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.texture_coordinates_VBO)
        self.shaderProgram.setAttributeBuffer(2, GL.GL_FLOAT, 0, 2)
        # GL.glVertexAttribPointer(2, 2, GL.GL_FLOAT, False, 0, 0)
        super().draw(tx, ty, scale, rotation, aspect_ratio, sim_time)
        GL.glDisableVertexAttribArray(2)
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
        GL.glDisable(GL.GL_TEXTURE_2D)

    def update_vertex_attributes(self):
        super().update_vertex_attributes()
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.texture_coordinates_VBO)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.texture_coors, GL.GL_STATIC_DRAW)
