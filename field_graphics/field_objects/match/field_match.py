class Match:

    isInit = False

    def __init__(self, context):
        # FIXME context DEVE ser um objeto FieldView
        #  todavia o python não aguenta
        #  duas classes usando dependências uma da outra.
        self.context = context

    def setup(self):
        self.isInit = True

    def update(self, time: float) -> bool:
        """Checks if this object is properly initialized, if it is not then checks if OpenGL is initialized and tries to init itself.
        \nReturns false if and only if object fails to properly initialize itself."""
        if (not self.isInit) and self.context.isOpenGLInit:
            self.setup()
        return self.isInit


    def get_field_dimention(self) -> tuple[float, float]:
        pass

    def clear(self):
        pass