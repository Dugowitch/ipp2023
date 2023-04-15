from Frame import Frame
from sys import stderr

class FrameManager:
    __instance = None

    def __new__(cls):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        # TODO if __instance != None and __new__ returns an instance, that does not mean __init__ does not get called
        self.GF = Frame();
        self.TF = None;
        self.LF = [];
    
    @staticmethod
    def getInstance():
        return __class__.__instance

    def pushframe(self):
        if self.TF == None:
            stderr.write("> FrameManager: frame does not exist\n")
            exit(55) # frame does not exist

        self.LF.append(self.TF)
        self.TF = None

    def popframe(self):
        if self.LF == []:
            stderr.write("> FrameManager: frame stack is empty\n")
            exit(55) # frame stack is empty

        self.TF = self.LF.pop()

    def createframe(self):
        self.TF = Frame()

    def getVal(self, var):
        frame, name = self.getFrame(var)
        return frame.getVal(name)

    def getFrame(self, var):
        frame_mapping = {
            "LF": self.currentLF,
            "TF": self.TF,
            "GF": self.GF
        }

        # check var value, split into parts
        if "@" not in var:
            stderr.write("> FrameManager: missing '@' in variable\n")
            exit(57) # wrong operand value
        frame, name = var.split("@")
        if frame not in frame_mapping.keys():
            stderr.write("> FrameManager: frame of this type does not exist\n")
            exit(57) # frame of this type does not exist - wrong operand value

        # get frame
        frame = frame_mapping[frame]

        # check frame
        if frame == None:
            stderr.write("> FrameManager: frame does not exist\n")
            exit(55) # frame does not exist

        return frame, name

    @property
    def currentLF(self):
        if self.LF == []:
            return None

        return self.LF[-1]
