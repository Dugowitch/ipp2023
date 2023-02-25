from FrameManager import FrameManager
from StackManager import StackManager
from IOManager import IOManager
from ArgParser import ArgParser
from FlowManager import FlowManager
from InstructionFactory import InstructionFactory
import xml.etree.ElementTree as ET

class Interpreter:
    def __init__(self):
        self.ARGS = ArgParser()
        self.IO = IOManager(self.ARGS)
        self._loadXML()
        self.FLOW = FlowManager(self.SOURCE)
        self.FRAME = FrameManager()
        self.STACK = StackManager()
        self.IF = InstructionFactory()

    def interpret(self):
        while (self.FLOW.ip <= len(self.SOURCE)):
            # get requirements
            req = []
            req_print = "" # TODO: remove
            curr = self.SOURCE[self.FLOW.ip - 1]
            if (curr.get("opcode") in self.IF.requirements["FRAME"]):
                req.append(self.FRAME);
                req_print += "FRAME " # TODO: remove
            if (curr.get("opcode") in self.IF.requirements["FLOW"]):
                req.append(self.FLOW);
                req_print += "FLOW " # TODO: remove
            if (curr.get("opcode") in self.IF.requirements["IO"]):
                req.append(self.IO);
                req_print += "IO " # TODO: remove
            if (curr.get("opcode") in self.IF.requirements["STACK"]):
                req.append(self.STACK);
                req_print += "STACK " # TODO: remove
            
            # execute instruction
            ins = self.IF.gen(curr)
            print(f"> {ins} with {req_print}") # TODO: remove
            ins.execute(*req)

            # increment
            self.FLOW.ip += 1

    def _loadXML(self):
        if self.ARGS.source:
            XML = ET.parse(self.ARGS.source)
            self.SOURCE = XML.getroot()

        else:
            rawXML = self.IO.read()
            self.SOURCE = ET.fromstring(rawXML) # returns root

interpreter = Interpreter()
interpreter.interpret()