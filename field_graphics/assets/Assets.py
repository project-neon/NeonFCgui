from field_graphics.rendering.objects.renderable_mesh import RenderableMesh    
from PyQt6.QtOpenGL import QOpenGLShaderProgram

from field_graphics.rendering.render_manager import compileShaderProgram

import numpy as np

def shaderProgram() -> QOpenGLShaderProgram:
    vsh = open("field_graphics/assets/shaders/VertexShader.vsh").read()
    fsh = open("field_graphics/assets/shaders/FragmentShader.fsh").read()
    return compileShaderProgram(vsh, fsh)

def gen_custom_field(width, height, line_len, goal_depth, goal_height, penalty_area_width, penalty_area_height) -> list[RenderableMesh]:
    origin = (-width/2.0,-height/2.0)
    vertices = [
        origin[0] - line_len/2.0, origin[1] - line_len/2.0, -0.9,
        origin[0] + line_len/2.0, origin[1] - line_len/2.0, -0.9,
        origin[0] + line_len/2.0, origin[1] - line_len/2.0 + height, -0.9,

        origin[0] - line_len/2.0, origin[1] - line_len/2.0 + height, -0.9,
        origin[0] + line_len/2.0, origin[1] - line_len/2.0 + height, -0.9,
        origin[0] - line_len/2.0, origin[1] - line_len/2.0, -0.9,

        origin[0] + width - line_len/2.0, origin[1] - line_len/2.0, -0.9,
        origin[0] + width + line_len/2.0, origin[1] - line_len/2.0, -0.9,
        origin[0] + width + line_len/2.0, origin[1] - line_len/2.0 + height, -0.9,

        origin[0] + width - line_len/2.0, origin[1] - line_len/2.0 + height, -0.9,
        origin[0] + width + line_len/2.0, origin[1] - line_len/2.0 + height, -0.9,
        origin[0] + width - line_len/2.0, origin[1] - line_len/2.0, -0.9,
        
        origin[0] - line_len/2.0, origin[1] - line_len/2.0, -0.9,
        origin[0] - line_len/2.0, origin[1] + line_len/2.0, -0.9,
        origin[0] + width + line_len/2.0, origin[1] + line_len/2.0, -0.9,

        origin[0] + width + line_len/2.0, origin[1] + line_len/2.0, -0.9,
        origin[0] - line_len/2.0, origin[1] - line_len/2.0, -0.9,
        origin[0] + width + line_len/2.0, origin[1] - line_len/2.0, -0.9,

        origin[0] - line_len/2.0,height +  origin[1] - line_len/2.0, -0.9,
        origin[0] - line_len/2.0,height +  origin[1] + line_len/2.0, -0.9,
        origin[0] + width + line_len/2.0,height +  origin[1] + line_len/2.0, -0.9,

        origin[0] + width + line_len/2.0, height + origin[1] + line_len/2.0, -0.9,
        origin[0] - line_len/2.0, height + origin[1] - line_len/2.0, -0.9,
        origin[0] + width + line_len/2.0, height + origin[1] - line_len/2.0, -0.9,



        origin[0] + width + line_len/2.0, -line_len/2.0 - penalty_area_height/2.0, -0.9,
        origin[0] + width - penalty_area_width, line_len/2.0 - penalty_area_height/2.0, -0.9,
        origin[0] + width + line_len/2.0, line_len/2.0 - penalty_area_height/2.0, -0.9,

        origin[0] + width + line_len/2.0,       -line_len/2.0 - penalty_area_height/2.0, -0.9,
        origin[0] + width - penalty_area_width, line_len/2.0 - penalty_area_height/2.0, -0.9,
        origin[0] + width - penalty_area_width, -line_len/2.0 - penalty_area_height/2.0, -0.9,

        origin[0] + width + line_len/2.0, -line_len/2.0 + penalty_area_height/2.0, -0.9,
        origin[0] + width - penalty_area_width, line_len/2.0 + penalty_area_height/2.0, -0.9,
        origin[0] + width + line_len/2.0, line_len/2.0 + penalty_area_height/2.0, -0.9,

        origin[0] + width + line_len/2.0,       -line_len/2.0 + penalty_area_height/2.0, -0.9,
        origin[0] + width - penalty_area_width, line_len/2.0 + penalty_area_height/2.0, -0.9,
        origin[0] + width - penalty_area_width, -line_len/2.0 + penalty_area_height/2.0, -0.9,

        origin[0] + width - penalty_area_width + line_len/2.0, line_len/2.0 + penalty_area_height/2.0, -0.9,
        origin[0] + width - penalty_area_width - line_len/2.0, line_len/2.0 + penalty_area_height/2.0, -0.9,
        origin[0] + width - penalty_area_width - line_len/2.0, line_len/2.0 - penalty_area_height/2.0, -0.9,
        
        origin[0] + width - penalty_area_width + line_len/2.0, - line_len/2.0 + penalty_area_height/2.0, -0.9,
        origin[0] + width - penalty_area_width - line_len/2.0, - line_len/2.0 - penalty_area_height/2.0, -0.9,
        origin[0] + width - penalty_area_width + line_len/2.0, - line_len/2.0 - penalty_area_height/2.0, -0.9,



        origin[0] - line_len/2.0 + line_len/2.0, -line_len/2.0 - penalty_area_height/2.0, -0.9,
        origin[0] - line_len/2.0 + penalty_area_width, line_len/2.0 - penalty_area_height/2.0, -0.9,
        origin[0] - line_len/2.0 + line_len/2.0, line_len/2.0 - penalty_area_height/2.0, -0.9,

        origin[0] - line_len/2.0 + line_len/2.0,       -line_len/2.0 - penalty_area_height/2.0, -0.9,
        origin[0] - line_len/2.0 + penalty_area_width, line_len/2.0 - penalty_area_height/2.0, -0.9,
        origin[0] - line_len/2.0 + penalty_area_width, -line_len/2.0 - penalty_area_height/2.0, -0.9,

        origin[0] - line_len/2.0 + line_len/2.0, -line_len/2.0 + penalty_area_height/2.0, -0.9,
        origin[0] - line_len/2.0 + penalty_area_width, line_len/2.0 + penalty_area_height/2.0, -0.9,
        origin[0] - line_len/2.0 + line_len/2.0, line_len/2.0 + penalty_area_height/2.0, -0.9,

        origin[0] - line_len/2.0 + line_len/2.0,       -line_len/2.0 + penalty_area_height/2.0, -0.9,
        origin[0] - line_len/2.0 + penalty_area_width, line_len/2.0 + penalty_area_height/2.0, -0.9,
        origin[0] - line_len/2.0 + penalty_area_width, -line_len/2.0 + penalty_area_height/2.0, -0.9,

        origin[0] - line_len/2.0 + penalty_area_width + line_len/2.0, line_len/2.0 + penalty_area_height/2.0, -0.9,
        origin[0] - line_len/2.0 + penalty_area_width - line_len/2.0, line_len/2.0 + penalty_area_height/2.0, -0.9,
        origin[0] - line_len/2.0 + penalty_area_width - line_len/2.0, line_len/2.0 - penalty_area_height/2.0, -0.9,
        
        origin[0] - line_len/2.0 + penalty_area_width + line_len/2.0, - line_len/2.0 + penalty_area_height/2.0, -0.9,
        origin[0] - line_len/2.0 + penalty_area_width - line_len/2.0, - line_len/2.0 - penalty_area_height/2.0, -0.9,
        origin[0] - line_len/2.0 + penalty_area_width + line_len/2.0, - line_len/2.0 - penalty_area_height/2.0, -0.9,



    
        origin[0] - line_len/2.0 + line_len/2.0, -line_len/2.0 - goal_height/2.0, -0.9,
        origin[0] - line_len/2.0 - goal_depth, line_len/2.0 - goal_height/2.0, -0.9,
        origin[0] - line_len/2.0 + line_len/2.0, line_len/2.0 - goal_height/2.0, -0.9,

        origin[0] - line_len/2.0 + line_len/2.0,       -line_len/2.0 - goal_height/2.0, -0.9,
        origin[0] - line_len/2.0 - goal_depth, line_len/2.0 - goal_height/2.0, -0.9,
        origin[0] - line_len/2.0 - goal_depth, -line_len/2.0 - goal_height/2.0, -0.9,

        origin[0] - line_len/2.0 + line_len/2.0, -line_len/2.0 + goal_height/2.0, -0.9,
        origin[0] - line_len/2.0 - goal_depth, line_len/2.0 + goal_height/2.0, -0.9,
        origin[0] - line_len/2.0 + line_len/2.0, line_len/2.0 + goal_height/2.0, -0.9,

        origin[0] - line_len/2.0 + line_len/2.0, -line_len/2.0 + goal_height/2.0, -0.9,
        origin[0] - line_len/2.0 - goal_depth, line_len/2.0 + goal_height/2.0, -0.9,
        origin[0] - line_len/2.0 - goal_depth, -line_len/2.0 + goal_height/2.0, -0.9,

        origin[0] - line_len/2.0 - goal_depth + line_len/2.0, line_len/2.0 + goal_height/2.0, -0.9,
        origin[0] - line_len/2.0 - goal_depth - line_len/2.0, line_len/2.0 + goal_height/2.0, -0.9,
        origin[0] - line_len/2.0 - goal_depth - line_len/2.0, -line_len/2.0 - goal_height/2.0, -0.9,
        
        origin[0] - line_len/2.0 - goal_depth + line_len/2.0, line_len/2.0 + goal_height/2.0, -0.9,
        origin[0] - line_len/2.0 - goal_depth - line_len/2.0, -line_len/2.0 - goal_height/2.0, -0.9,
        origin[0] - line_len/2.0 - goal_depth + line_len/2.0, -line_len/2.0 - goal_height/2.0, -0.9,



        origin[0] + width - line_len/2.0 + line_len/2.0, -line_len/2.0 - goal_height/2.0, -0.9,
        origin[0] + width - line_len/2.0 + goal_depth, line_len/2.0 - goal_height/2.0, -0.9,
        origin[0] + width - line_len/2.0 + line_len/2.0, line_len/2.0 - goal_height/2.0, -0.9,

        origin[0] + width - line_len/2.0 + line_len/2.0,       -line_len/2.0 - goal_height/2.0, -0.9,
        origin[0] + width - line_len/2.0 + goal_depth, line_len/2.0 - goal_height/2.0, -0.9,
        origin[0] + width - line_len/2.0 + goal_depth, -line_len/2.0 - goal_height/2.0, -0.9,

        origin[0] + width - line_len/2.0 + line_len/2.0, -line_len/2.0 + goal_height/2.0, -0.9,
        origin[0] + width - line_len/2.0 + goal_depth, line_len/2.0 + goal_height/2.0, -0.9,
        origin[0] + width - line_len/2.0 + line_len/2.0, line_len/2.0 + goal_height/2.0, -0.9,

        origin[0] + width - line_len/2.0 + line_len/2.0, -line_len/2.0 + goal_height/2.0, -0.9,
        origin[0] + width - line_len/2.0 + goal_depth, line_len/2.0 + goal_height/2.0, -0.9,
        origin[0] + width - line_len/2.0 + goal_depth, -line_len/2.0 + goal_height/2.0, -0.9,

        origin[0] + width - line_len/2.0 + goal_depth + line_len/2.0, line_len/2.0 + goal_height/2.0, -0.9,
        origin[0] + width - line_len/2.0 + goal_depth - line_len/2.0, line_len/2.0 + goal_height/2.0, -0.9,
        origin[0] + width - line_len/2.0 + goal_depth - line_len/2.0, -line_len/2.0 - goal_height/2.0, -0.9,
        
        origin[0] + width- line_len/2.0 + goal_depth + line_len/2.0, line_len/2.0 + goal_height/2.0, -0.9,
        origin[0] + width - line_len/2.0 + goal_depth - line_len/2.0, -line_len/2.0 - goal_height/2.0, -0.9,
        origin[0] + width - line_len/2.0 + goal_depth + line_len/2.0, -line_len/2.0 - goal_height/2.0, -0.9,


        origin[0], line_len/2.0, 0.9, origin[0], -line_len/2.0, 0.9, origin[0]+width, line_len/2.0, 0.9,
        origin[0], -line_len/2.0, 0.9, origin[0]+width, -line_len/2.0, 0.9, origin[0]+width, line_len/2.0, 0.9, 
    
        -line_len/2.0, -origin[1], 0.9, line_len/2.0, -origin[1], 0.9, line_len/2.0, origin[1], 0.9, 
        -line_len/2.0,  origin[1], 0.9, -line_len/2.0, -origin[1], 0.9, line_len/2.0, origin[1], 0.9 


    ]
    
    colors = [1] * len(vertices)
    field = RenderableMesh(np.asarray(vertices,dtype=np.float32), np.asarray(colors,dtype=np.float32), shaderProgram())
    # field.draw = print
    # print(vertices)
    # print(colors)
    return [field]