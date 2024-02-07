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
    texture_coordinates_array = []

    def __init__(self, display: str, texture_directory: str, color=None, size=1, fixed_rotation=False,
                 tracking: Renderable | None = None):

        if color is None:
            color = [1, 1, 1, 1]
        self.display = display
        self.texture_directory = texture_directory
        self.color = color

        vertices = []
        colors = []

        i = 0.0
        for act in display:
            pos: int = ord(act) - 32
            bmp_x: int = pos % 16;
            bmp_y: int = math.floor(pos / 16)

            wspc_c = (i / 2 - display.__len__() / 4)

            vertices.append(wspc_c);      vertices.append(-.5); vertices.append(-.8)  # --
            vertices.append(wspc_c + .5); vertices.append(-.5); vertices.append(-.8)  # +-
            vertices.append(wspc_c);      vertices.append(.5);  vertices.append(-.8)  # -+

            vertices.append(wspc_c);      vertices.append(.5);  vertices.append(-.8)  # -+
            vertices.append(wspc_c + .5); vertices.append(-.5); vertices.append(-.8)  # +-
            vertices.append(wspc_c + .5); vertices.append(.5);  vertices.append(-.8)  # ++

            txs_x = bmp_x / 16; txs_y = bmp_y / 16

            self.texture_coordinates_array.append(txs_x)
            self.texture_coordinates_array.append(txs_y)

            self.texture_coordinates_array.append(txs_x + 1 / 32)
            self.texture_coordinates_array.append(txs_y + 1 / 16)

            i += 1

        self.texture_coordinates_array = np.asarray(self.texture_coordinates_array, dtype=numpy.float32)

        for _ in vertices:
            colors.append(0)

        self.texture_id = loadTexture("main_window/field_graphics/assets/bitmaps/teste.png")
        self.texture_coordinates_VBO = GL.glGenBuffers(1)

        print(self.texture_coordinates_array)

        vertices = np.asarray(vertices, dtype=np.float32)
        colors = np.asarray(colors, dtype=np.float32)

        vsh = "main_window/field_graphics/assets/shaders/TextVertexShader.vsh"
        vsh = open(vsh).read()
        fsh = "main_window/field_graphics/assets/shaders/TextFragmentShader.fsh"
        fsh = open(fsh).read()
        shader = compileShaderProgram(vsh, fsh)
        super().__init__(vertices, colors, shader)

    def draw(self, tx, ty, scale, rotation, aspect_ratio, sim_time):
        self.shaderProgram.bind()
        GL.glEnable(GL.GL_TEXTURE_2D)
        GL.glEnableVertexAttribArray(2)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture_id)
        GL.glActiveTexture(GL.GL_TEXTURE0)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.texture_coordinates_VBO)
        self.shaderProgram.setAttributeBuffer(2, GL.GL_FLOAT, 0, 3)
        # GL.glVertexAttribPointer(2, 2, GL.GL_FLOAT, False, 0, 0)
        super().draw(tx, ty, scale, rotation, aspect_ratio, sim_time)
        GL.glDisableVertexAttribArray(2)
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)

    def update_vertex_attributes(self):
        super().update_vertex_attributes()
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.texture_coordinates_VBO)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.texture_coordinates_array, GL.GL_STATIC_DRAW)
