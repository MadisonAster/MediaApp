from PySide import QtGui, QtCore

class FloatKnob(object):
    def __init__(self, a):
        self.setValue(a)
    def setValue(self, a):
        if type(a) != float:
            raise TypeError
        else:
            self.knobValue = a
    def value(self):
        return self.knobValue