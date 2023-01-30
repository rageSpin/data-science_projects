from PyQt6 import QtCore, QtWidgets


class jumpSlider(QtWidgets.QSlider):

    def __init__(self, parent=None):
        super(jumpSlider, self).__init__(parent)

    def mousePressEvent(self, event):
        print(event.pos())
        self.setValue(
            QtWidgets.QStyle.sliderValueFromPosition(
                self.minimum(), 
                self.maximum(), 
                event.pos().x(), 
                self.width()
            )
        )