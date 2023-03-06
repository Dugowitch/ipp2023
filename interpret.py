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
        self.__loadXML()
        self.__checkXML()
        self.FLOW = FlowManager(self.SOURCE)
        self.FRAME = FrameManager()
        self.STACK = StackManager()
        self.IF = InstructionFactory()

    def interpret(self):
        while (self.FLOW.ip <= len(self.SOURCE)):
            # get requirements
            req = []
            # req_print = "" # REMOVE
            curr = self.SOURCE[self.FLOW.ip - 1]
            if (curr.get("opcode") in self.IF.requirements["FRAME"]):
                req.append(self.FRAME);
                # req_print += "FRAME " # REMOVE
            if (curr.get("opcode") in self.IF.requirements["FLOW"]):
                req.append(self.FLOW);
                # req_print += "FLOW " # REMOVE
            if (curr.get("opcode") in self.IF.requirements["IO"]):
                req.append(self.IO);
                # req_print += "IO " # REMOVE
            if (curr.get("opcode") in self.IF.requirements["STACK"]):
                req.append(self.STACK);
                # req_print += "STACK " # REMOVE
            
            # execute instruction
            ins = self.IF.gen(curr)
            # print(f"> {ins} with {req_print}") # REMOVE
            ins.execute(*req)

            # increment
            self.FLOW.ip += 1

    def __loadXML(self):
        if self.ARGS.source:
            XML = ET.parse(self.ARGS.source)
            self.SOURCE = XML.getroot()

        else:
            rawXML = self.IO.read()
            self.SOURCE = ET.fromstring(rawXML) # returns root

    def __checkXML(self):
        OPCODES = ["MOVE", "CREATEFRAME", "PUSHFRAME", "POPFRAME", "DEFVAR", "CALL", "RETURN", "PUSHS", "POPS", "ADD", "SUB", "MUL", "IDIV", "LT", "GT", "EQ", "AND", "OR", "NOT", "INT2CHAR", "STRI2INT", "READ", "WRITE", "CONCAT", "STRLEN", "GETCHAR", "SETCHAR", "TYPE", "LABEL", "JUMP", "JUMPIFEQ", "JUMPIFNEQ", "EXIT", "DPRINT", "BREAK"]
        TYPES = ["int", "bool", "string", "nil", "label", "type", "var"]
        root = self.SOURCE
        if root.tag == "program" and root.get("language") == "IPPcode23":
            # check instrucitons 
            for i, ins in enumerate(root):
                if ins.tag == "instruction" and ins.get("order") == f"{i+1}" and ins.get("opcode") in OPCODES:
                    # check arguments 
                    for j, arg in enumerate(ins):
                        if arg.tag != f"arg{j+1}" or arg.get("type") not in TYPES:
                            exit(32) # error - unexpected XML structure
                else:
                    exit(32) # error - unexpected XML structure
        else:
            exit(32) # error - unexpected XML structure
            

interpreter = Interpreter()
interpreter.interpret()