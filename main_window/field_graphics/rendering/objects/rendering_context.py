from main_window.field_graphics.rendering.objects.renderable import RenderableMesh


class RenderingContext:
    objects: list[RenderableMesh] = []
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

    def set_aspect_ratio(self, aspect_ratio):
        self.aspect_ratio = aspect_ratio

    def draw(self, sim_time):
        for obj in self.objects:
            obj.draw(self.x, self.y,
                     self.scale,
                     self.rotation, self.aspect_ratio, sim_time)
