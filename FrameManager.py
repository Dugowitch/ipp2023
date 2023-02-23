from Frame import Frame

class FrameManager:
    def __init__(self):
        self.GF = Frame();
        self.TF = None;
        self.LF = [];

    def pushframe(self):
        if self.TF != None:
            self.LF.append(self.TF)
            self.TF = None
        else:
            exit(55) # error - frame does not exist

    def popframe(self):
        if self.LF != []:
            self.TF = self.LF.pop()
        else:
            exit(55) # error - frame stack is empty

    def createframe(self):
        self.TF = Frame()

    def getVal(self, var):
        frame, name = self.getFrame(var)
        return frame.getVal(name)

    def getFrame(self, var):
        frame, name = var.split("@")
        # Set frame
        if frame == "LF":
            frame = self.currentLF
        elif frame == "TF":
            frame = self.TF
        elif frame == "GF":
            frame = self.GF
        return frame, name

    @property
    def currentLF(self):
        if self.LF != []:
            return self.LF[0]
        else:
            exit(55) # error - frame does not exist