from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color
from kivy.graphics import Line, Ellipse, Bezier


class Draw(Widget):
    def __init__(self, **kwargs):
        super(Draw, self).__init__(**kwargs)
        self.bind(pos=self.update_canvas)
        self.bind(size=self.update_canvas)
        self.update_canvas()

    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(0.0, 1., 0.0, .5, mode='rgba')
            # self.line1 = Line(points=[200, 100, 100, 200, 350, 250], width=3)
            #Color(0.0, 0.0, 1., .5, mode='rgba')
            #Ellipse(pos=self.pos, size=(20,20))
            Line(points=(10,10), bezier=[0, 0, 100, 150, 30, 50, 200, 220], width=3)


class MyApp(App):
    def build(self):
        return Draw()


if __name__ == "__main__":
    MyApp().run()