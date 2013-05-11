from PySide import QtGui, QtCore

class StrKnob(object):
    def __init__(self, a):
        self.setValue(a)
    def setValue(self, a):
        if type(a) != str:
            raise TypeError
        else:
            self.knobValue = a
    def value(self):
        return self.knobValue
       