#===============================================================================
# @Author: Thomas McVay
# @ModuleDescription: 
# @License:
#    On Loan from Lit
#===============================================================================

from collections import deque

class RingCache(deque):
    def __init__(self, *args, **kwargs):
        super(RingCache, self).__init__(*args)
        
        self.zeroFrame = 0
        if 'zero' in kwargs:
            self.zeroFrame = kwargs['zero']
        self.rotateCounter = 0
    def __contains__(self, frame):
        if frame >= self.zeroFrame and frame < self.zeroFrame+len(self):
            return True
        else:
            return False

    def goto(self, frameNumber, end = False):
        rotationAmount = frameNumber - self.zeroFrame + self.rotateCounter
        self.rotate(-rotationAmount-end)

    #overrides
    def pop(self, *args):
        returnList = []
        if len(args) is 1:
            frames = args[0]
        else:
            frames = 1
        for i in range(frames):
            returnList.append(super(RingCache, self).pop())
            if self.rotateCounter < 0:
                self.rotateCounter += 1
        return returnList
    def rotate(self, value):
        super(RingCache, self).rotate(value)
        self.rotateCounter += value
    def reset(self):
        self.rotate(-self.rotateCounter)
    

