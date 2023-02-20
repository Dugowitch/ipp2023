import Frame

class FrameMaganer:
    GF = Frame();
    TF = None;
    LF = [];

    def pushframe(self):
        if __class__.TF != None:
            __class__.LF.append(__class__.TF)
            __class__.TF = None
        else:
            # TODO: error, there is not frame to push
            pass

    def popframe(self):
        if __class__.LF != []:
            __class__.TF = __class__.LF.pop()
        else:
            # TODO: error, there is not frame to pop
            pass

    def createframe(self):
        __class__.TF = Frame()

    @property
    def currentLF(self):
        if __class__.LF != []:
            return __class__.LF[0]
        else:
            # TODO: error, accessing LF before CREATEFRAME and PUSHFRAME
            return None