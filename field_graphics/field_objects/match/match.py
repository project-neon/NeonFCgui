from main_window.widgets.field_view import FieldView


class Match:

    def __init__(self, context: FieldView):
        self.context = context

    def setup(self):
        pass

    def update(self, time: float):
        pass

    def get_field_dimention(self) -> tuple[float, float]:
        pass

    def clear(self):
        pass