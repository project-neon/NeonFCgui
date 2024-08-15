import math

from field_graphics.field_objects.match.field_match import Match
from field_graphics.field_objects.text import Text
from field_graphics.field_objects.vsss_robot_mesh import VSSSRobotMesh
from field_graphics.rendering.render_manager import modelFromJSON
from main_window.widgets.field_view import FieldView


class VSSSMatch(Match):

    hasInfo: bool = False
    robots: dict[str,VSSSRobotMesh] | None = None

    def __init__(self, context: FieldView):
        super().__init__(context)
        self.field_dimentions = [150.0,130.0]
        self.setup()

    def setup(self):

        field = modelFromJSON(open("field_graphics/assets/models/field_vsss.json").read())
        for obj in field:
            # obj.x = 75; obj.y = 65
            self.context.rendering_context.objects.append(obj)


        self.robots = {}

        # Sets the robot models
        for r in self.context.match_api.robots:
            r_m = VSSSRobotMesh([.1, .1, .1], [0, 1, 0], [1, 0, 0], [0, 0, 1])
            r_id = r.robot_id
            r_m.color_accordingly_to_id(r_id, self.context.match_api.team_color == 'yellow')
            self.context.rendering_context.objects.append(r_m)
            self.robots.update({str(r_id):r_m})
        # Sets the 'opposite' models
        for r in self.context.match_api.opposites:
            r_m = VSSSRobotMesh([.1, .1, .1], [0, 1, 0], [1, 0, 0], [0, 0, 1])
            r_id = r.robot_id
            r_m.color_accordingly_to_id(r_id, self.context.match_api.team_color != 'yellow')
            self.context.rendering_context.objects.append(r_m)
            self.robots.update({str(r_id):r_m})

        for r in self.robots:
            robot_text = Text(  # TODO: Config file with standard depths
                "#{:02d}".format(int(r)),
                "field_graphics/assets/bitmaps/Arial Bold_1024.bmp",
                size=6,
                tracking=self.robots[r], anchor=(10, 0))
            self.context.rendering_context.objects.append(robot_text)

    def update(self, time: float):
        if self.context.no_info:
            self.playStartAnimation(time)
        else:
            if not self.hasInfo:
                self.hasInfo = True
                self.context.reset()
                self.setup()  # Redoes the setup to get the IDs in place
            for r in self.robots:
                self.update_robot_coord(r,self.robots[r])

    def playStartAnimation(self, time: float):
        self.robots['5'].x = math.sin(time/100) * 20
        self.robots['5'].y = math.cos(time/100) * 20

        self.robots['7'].x = math.sin(time/100 + math.pi * 4/3) * 20
        self.robots['7'].y = math.cos(time/100 + math.pi * 4/3) * 20

        self.robots['8'].x = math.sin(time/100 + math.pi * 2/3) * 20
        self.robots['8'].y = math.cos(time/100 + math.pi * 2/3) * 20

        self.robots['5'].rotation = self.context.sim_time * (1/100) + math.pi/2
        self.robots['7'].rotation = self.context.sim_time * (1/100) - math.pi/6
        self.robots['8'].rotation = self.context.sim_time * (1/100) + math.pi * (9.5/3)

    def update_robot_coord(self, robot_id: int, model: VSSSRobotMesh):
        r = self.context.match_api.fetch_robot_by_id(robot_id)
        model.x = r.robot_pos[0] * 100 - self.field_dimentions[0]*0.5
        model.y = r.robot_pos[1] * 100 - self.field_dimentions[1]*0.5
        model.rotation = -r.robot_pos[2] + math.pi/2

    def get_field_dimention(self) -> tuple[float, float]:
        return self.field_dimentions[0], self.field_dimentions[1]

    def clear(self):
        self.robots.clear()
