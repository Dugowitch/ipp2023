from XMLManager import XMLManager
from sys import stderr

class FlowManager:
    __instance = None

    def __new__(cls):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.ip = 0 # instruction pointer
        self._labels = {}
        self._callstack = []
        self._orderMapping = {}

        XML = XMLManager.getInstance()

        # loop over all instructions, save labels, and map order
        for i, ins in enumerate(XML.root):
            order = int(ins.get("order")) # this should never raise an exception since it's checked in XMLManager
            opcode = ins.get("opcode")

            # more instructions with the same order or an instruction with not positive order
            if order in self._orderMapping or order <= 0:
                stderr.write("> FlowManager: instructions with the same order\n")
                exit(32)

            self._orderMapping[order] = i

            if opcode == "LABEL":
                for arg in ins:
                    if arg.text in self._labels:
                        stderr.write("> FlowManager: label redefinition\n")
                        exit(52) # label redefinition

                    # self._labels[arg.text] = int(ins.get("order")) # REMOVE
                    self._labels[arg.text] = i

            # print(self._orderMapping) # REMOVE
            # print(self._orderMapping.keys()) # REMOVE
        
    @staticmethod
    def getInstance():
        return __class__.__instance

    def getNextIns(self):
        self.ip += 1

        # check end conditions
        if self._orderMapping == {} or self.ip > len(self._orderMapping):
            return None

        # determine index in XML
        index = list(self._orderMapping.keys())
        index.sort()
        xml_index = self._orderMapping[index[self.ip - 1]]

        # return <instruction> element
        XML = XMLManager.getInstance()
        return XML.getIns(xml_index)

    def jump(self, label):
        if label not in self._labels:
            stderr.write("> FlowManager: trying to use undefined label\n")
            exit(52) # trying to use undefined label

        self.ip = self._labels[label]

    def call(self, label):
        self._callstack.append(self.ip)
        self.jump(label)

    def ret(self):
        if self._callstack == []:
            stderr.write("> FlowManager: missing callstack value\n")
            exit(56) # missing callstack value

        self.ip = self._callstack.pop()
