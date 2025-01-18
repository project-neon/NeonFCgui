import math

from field_graphics.field_objects.ssl_robot_mesh import SSLRobotMesh
from field_graphics.field_objects.text import Text
from field_graphics.rendering.render_manager import modelFromJSON
from field_graphics.field_objects.match.field_match import Match as FieldMatch
from field_graphics.rendering.objects.renderable_mesh import RenderableMesh
#TODO concerta esse zoom inicial do SSL

class SSLMatch(FieldMatch):
    hasInfo: bool = False
    robots: dict[str, SSLRobotMesh] | None = None
    ball: RenderableMesh

    def __init__(self, context):
        super().__init__(context)
        self.field_dimentions = [520.0*2, 300.0*2]


    def update(self, time: float) -> bool:
        if not super().update(time): return False
        if self.context.no_info:
            pass  # self.playStartAnimation(time)
        else:
            if not self.hasInfo:  # First time since recognising field info
                self.hasInfo = True
                self.context.reset()
                self.setup()  # Redoes the setup to get the IDs in place
            self.ball.x = self.context.match_api.ball.ball_pos[0] * 100 - self.field_dimentions[0] * 0.5
            self.ball.y = self.context.match_api.ball.ball_pos[1] * 100 - self.field_dimentions[1] * 0.5
            for r in self.robots:
                self.update_robot_coord(r[0] != '-', int(r), self.robots[r])




    def setup(self):
        self.context.rendering_context.objects.clear()
        field = modelFromJSON(open("field_graphics/assets/models/field_ssl.json").read())
        for obj in field: self.context.rendering_context.objects.append(obj)
        self.robots = {}
        self.ball = modelFromJSON(open("field_graphics/assets/models/ball.json").read())[0]
        # Sets the robot models
        for r in self.context.match_api.robots:
            r_id = r.robot_id
            r_m = SSLRobotMesh(r_id)
            self.context.rendering_context.objects.append(r_m)
            self.robots.update({str(r_id): r_m})
        # Sets the 'opposite' models
        for r in self.context.match_api.opposites:
            r_id = r.robot_id
            r_m = SSLRobotMesh(r_id)
            r_m.set_id(r_id,False)
            self.context.rendering_context.objects.append(r_m)
            self.robots.update({'-'+str(r_id): r_m})
        self.context.displaySSLModels()
        
        for r in self.robots:
            #print(str(r) + ": " + r)
            robot_text = Text(  # TODO: Config file with standard depths
                "#{:02d}".format(abs(int(r))),
                "field_graphics/assets/bitmaps/Arial Bold_1024.bmp",
                size=12,
                tracking=self.robots[r], anchor=(10, 0))
            self.context.rendering_context.objects.append(robot_text)

        self.context.rendering_context.objects.append(self.ball)
        super().setup()

    def update_robot_coord(self, team: bool, robot_id: int, model: SSLRobotMesh):
        if robot_id < 0 : robot_id = - robot_id
        r = self.context.match_api.fetch_robot_by_id(team, robot_id)
        model.x = r.robot_pos[0] * 100 - self.field_dimentions[0] * 0.5
        model.y = r.robot_pos[1] * 100 - self.field_dimentions[1] * 0.5
        model.rotation = -r.robot_pos[2] + math.pi / 2

    def get_field_dimention(self) -> tuple[float, float]:
        return self.field_dimentions[0], self.field_dimentions[1]

    def clear(self):
        self.robots.clear()
