from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color
from kivy.graphics import Line


class Draw(Widget):
    def __init__(self, **kwargs):
        super(Draw, self).__init__(**kwargs)
        self.bind(pos=self.update_canvas)
        self.bind(size=self.update_canvas)
        self.update_canvas()

    def update_canvas(self, *args):
        # Widget has a property called canvas
        with self.canvas:
            Color(0, 1, 0, .5, mode='rgba')
            Line(points=(350, 400, 500, 800, 650, 400, 300, 650, 700, 650, 350, 400), width=3)

            Color(0, 0, 1, .5, mode='rgba')
            Line(bezier=(200, 100, 250, 150, 300, 50, 350, 100), width=3)


class MyApp(App):
    def build(self):
        return Draw()


if __name__ == "__main__":
    MyApp().run()