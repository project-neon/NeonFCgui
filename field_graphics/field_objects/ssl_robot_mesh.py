from field_graphics.rendering.objects.renderable_mesh import RenderableMesh


class SSLRobotMesh(RenderableMesh):
    def __init__(self):

        template: RenderableMesh = modelFromJSON(open("field_graphics/assets/models/robot_vsss.json").read())[0]
        colors = gen_color_array(robot_color,back_tag_color,left_tag_color,right_tag_color)
        super().__init__(template.vertices, colors, template.shaderProgram)
