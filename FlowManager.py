import ArgParser
import XMLManager

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

        AP = ArgParser()

        # loop over all instructions, save labels, and map order 
        for i, ins in enumerate(AP.root):
            order = int(ins.get("order")) # this should never raise an exception since it's checked in XMLManager
            opcode = ins.get("opcode")

            # more instructions with the same order or an instruction with not positive order
            if order in self._orderMapping or order <= 0:
                exit(32)

            self._orderMapping[order] = i

            if opcode == "LABEL":
                for arg in ins:
                    if arg.text in self._labels:
                        exit(52) # label redefinition

                    # self._labels[arg.text] = int(ins.get("order")) # REMOVE
                    self._labels[arg.text] = i

            # print(self._orderMapping) # REMOVE
            # print(self._orderMapping.keys()) # REMOVE

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
        XML = XMLManager()
        return XML.getIns(xml_index)

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