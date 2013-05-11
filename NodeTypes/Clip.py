from NodeConstructor import *

from KnobTypes import *

class Clip(NodeConstructor):
    def __init__(self, CorePointer):
        global Core
        Core = CorePointer
        self['ClassName'] = StrKnob('Clip')
        self['nodeName'] = StrKnob(Core.getIncrementedName('Clip'))
        super(Clip, self).__init__(CorePointer)
        ################################
    
        
        
    #def node(self):
    #    return self.NodeType
    #def setNodeType(self, shape):
    #    self.nodeType = shape
    #def setRandomNodeType(self):
    #    self.setNodeType(random.randint(1, 7))
        
        