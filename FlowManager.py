import xml.etree.ElementTree as ET
class FlowManager:
    def __init__(self, root):
        self.ip = 1
        self._labels = {}
        self._callstack = []
        # loop over all instructions and save labels
        for ins in root:
            if (ins.get("opcode") == "LABEL"):
                for arg in ins:
                    self._labels[arg.text] = int(ins.get("order"))

    def jump(self, label):
        if label in self._labels:
            self.ip = self._labels[label]
        else:
            print(f"> trying to jump to {label}")
            print("> exitting in FlowManager.jump() - accessing undefined label") # REMOVE
            exit(52) # error - trying to use undefined label

    def call(self, label):
        self._callstack.append(self.ip)
        self.jump(label)

    def ret(self):
        if self._callstack != []:
            self.ip = self._callstack.pop()
        else:
            exit(56) # error - missing callstack value