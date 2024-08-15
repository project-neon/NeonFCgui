

class Match:

    def __init__(self, context):
        # FIXME context DEVE ser um objeto FieldView
        #  todavia infelizmente a 'língua do mercado' não aguenta
        #  duas classes usando dependências uma da outra.
        self.context = context

    def setup(self):
        pass

    def update(self, time: float):
        pass

    def get_field_dimention(self) -> tuple[float, float]:
        pass

    def clear(self):
        pass