from field_graphics.rendering.renderable import Renderable


class RenderingContext:
    # TODO: VAO IMPLEMENTATION
    objects: list[Renderable] = []
    x: float = 0
    y: float = 0
    aspect_ratio: float = 0
    scale: float = .15
    rotation: float = 0

    def __init__(self):
        pass

    def set_transformations(self, x=0, y=0, scale=1, rotation=0):
        self.x = x
        self.y = y
        self.scale = scale
        self.rotation = rotation

    def draw_obj(self,obj: list | Renderable, sim_time):
        if isinstance(obj, list):
            for i in obj: self.draw_obj(i, sim_time)
        elif isinstance(obj, Renderable):
            obj.draw(self.x, self.y, self.scale,
                     self.rotation, self.aspect_ratio, sim_time)
        else:
            print("WARNING: INVALID OBJECT QUEUED FOR RENDER: " + str(obj))
            

    def set_aspect_ratio(self, aspect_ratio):
        self.aspect_ratio = aspect_ratio

    def draw(self, sim_time: float):
        for obj in self.objects:
            self.draw_obj(obj, sim_time)