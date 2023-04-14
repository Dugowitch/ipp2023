from FrameManager import FrameManager
from StackManager import StackManager
from IOManager import IOManager
from ArgParser import ArgParser
from FlowManager import FlowManager
from InstructionFactory import InstructionFactory
import xml.etree.ElementTree as ET

class Interpreter:
    __instance = None

    def __new__(cls):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.ARGS = ArgParser()
        self.IO = IOManager(self.ARGS)
        try:
            self.__loadXML()
        except ET.ParseError:
            exit(31)
        self.__checkXML()
        self.FLOW = FlowManager(self.SOURCE)
        self.FRAME = FrameManager()
        self.STACK = StackManager()
        self.IF = InstructionFactory()

    def interpret(self):
        # while (self.FLOW.ip < len(self.SOURCE)):
        for _ in self.SOURCE:
            # get requirements
            req = []
            curr = self.SOURCE[self.FLOW.getIp()]
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
            for ins in root:
                if ins.tag == "instruction" and ins.get("opcode") and ins.get("opcode").upper() in OPCODES:
                    # check arguments 
                    for arg in ins:
                        if arg.tag[:3] != "arg" or arg.get("type") not in TYPES:
                            exit(32) # error - unexpected XML structure
                else:
                    exit(32) # error - unexpected XML structure
        else:
            exit(32) # error - unexpected XML structure
            

interpreter = Interpreter()
interpreter.interpret()
