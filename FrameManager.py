from Frame import Frame

class FrameManager:
    __instance = None

    def __new__(cls):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.GF = Frame();
        self.TF = None;
        self.LF = [];

    def pushframe(self):
        if self.TF == None:
            exit(55) # error - frame does not exist

        self.LF.append(self.TF)
        self.TF = None

    def popframe(self):
        if self.LF == []:
            exit(55) # error - frame stack is empty

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
            exit(57) # wrong operand value
        frame, name = var.split("@")
        if frame not in frame_mapping.keys():
            exit(57) # frame of this type does not exist - wrong operand value

        # get frame
        frame = frame_mapping[frame]

        # check frame
        if frame == None:
            exit(55) # frame does not exist

        return frame, name

    @property
    def currentLF(self):
        if self.LF == []:
            return None

        return self.LF[-1]