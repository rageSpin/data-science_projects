from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, ClearColor
from kivy.graphics import Line, Ellipse, Bezier


class Draw(Widget):
    def __init__(self, loop=False,**kwargs):
        super(Draw, self).__init__(**kwargs)
        self.loop = loop
        self.bind(pos=self.update_canvas)
        self.bind(size=self.update_canvas)
        self.update_canvas()

    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas.before:
            Color(0.0, 1., 0.0, 0.5)
            self.line1 = Line(points=[200, 100, 100, 200, 350, 250], width=3)
            # ClearColor(1,1,1,1)
            c=Color(b=1, a=0.4, r=0, g=0)
            # Line(circle=(150, 150, 50, 90, 180, 20), width=4)
            #Ellipse(pos=self.pos, size=(20,20))
            Line(bezier=(200, 100, 250, 150, 300, 50, 350, 100), width=5, dash_length=100, dash_offset=10, bezier_precision=100)
            # Bezier(points=[0, 0, 100, 150, 30, 50, 200, 220], width=5, dash_length=100, dash_offset=10)


class MyApp(App):
    def build(self):
        return Draw()


if __name__ == "__main__":
    MyApp().run()