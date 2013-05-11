from PySide import QtGui, QtCore

class IntKnob(object):
    def __init__(self, a):
        self.setValue(a)
    def setValue(self, a):
        if type(a) != int:
            raise TypeError
        else:
            self.knobValue = a
    def value(self):
        return self.knobValue