import xml.etree.ElementTree as ET
class FlowManager:
    __instance = None

    def __new__(cls, source):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, root):
        self.ip = 0
        self._labels = {}
        self._callstack = []
        self._orderMapping = {}
        # loop over all instructions and save labels
        for i, ins in enumerate(root):
            try:
                order = int(ins.get("order"))
            except ValueError:
                exit(32)
            except TypeError:
                exit(32)

            if order in self._orderMapping:
                exit(32)
            elif order <= 0:
                exit(32)
            self._orderMapping[int(ins.get("order"))] = i

            if (ins.get("opcode") == "LABEL"):
                for arg in ins:
                    if arg.text not in self._labels:
                        # self._labels[arg.text] = int(ins.get("order"))
                        self._labels[arg.text] = i
                    else:
                        exit(52)
            # print(self._orderMapping) # REMOVE
            # print(self._orderMapping.keys()) # REMOVE

    def getIp(self):
        self.ip += 1
        index = list(self._orderMapping.keys())
        index.sort()
        # print(f"> idx: {index}") # REMOVE
        # print(f"> ip: {self.ip - 1}") # REMOVE
        # print(f"> ord: {index[self.ip - 1]}") # REMOVE
        return self._orderMapping[index[self.ip - 1]]

    def jump(self, label):
        if label in self._labels:
            self.ip = self._labels[label]
        else:
            # print(f"> trying to jump to {label}") # REMOVE
            # print("> exitting in FlowManager.jump() - accessing undefined label") # REMOVE
            exit(52) # error - trying to use undefined label

    def call(self, label):
        self._callstack.append(self.ip)
        self.jump(label)

    def ret(self):
        if self._callstack != []:
            self.ip = self._callstack.pop()
        else:
            exit(56) # error - missing callstack value