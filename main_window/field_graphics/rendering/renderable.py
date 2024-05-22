class Renderable:
    """
    The renderable class is an abstract class that serves as template for any object which may use the OpenGL pipeline.
    """

    def draw(self, tx: float, ty: float, scale: float, rotation: float, aspect_ratio: float, sim_time: float):
        """
        Draws the object at the currently bound OpenGL Framebuffer object.
        Note that all transformations are meant to be GLOBAL transformations,
        local object transformations may be handled internally.
        """
        pass
