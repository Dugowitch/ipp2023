from sys import stderr

import xml.etree.ElementTree as ET
from ArgParser import ArgParser
from IOManager import IOManager

class XMLManager():
    __instance = None

    def __new__(cls):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.__getXMLRoot()
        self.__checkXML()

    @staticmethod
    def getInstance():
        return __class__.__instance

    def __getXMLRoot(self):
        AP = ArgParser.getInstance()
        IO = IOManager.getInstance()
    
        try:
            if AP.source:
                XML = ET.parse(AP.source)
                self.root = XML.getroot()
            else:
                rawXML = IO.read()
                self.root = ET.fromstring(rawXML) # returns root
        except ET.ParseError:
            stderr.write("> XMLManager: source XML is not well-formated\n")
            exit(31) # source XML is not well-formated

    def __checkXML(self):
        OPCODES = ["MOVE", "CREATEFRAME", "PUSHFRAME", "POPFRAME", "DEFVAR", "CALL", "RETURN", "PUSHS", "POPS", "ADD", "SUB", "MUL", "IDIV", "LT", "GT", "EQ", "AND", "OR", "NOT", "INT2CHAR", "STRI2INT", "READ", "WRITE", "CONCAT", "STRLEN", "GETCHAR", "SETCHAR", "TYPE", "LABEL", "JUMP", "JUMPIFEQ", "JUMPIFNEQ", "EXIT", "DPRINT", "BREAK"]
        TYPES = ["int", "bool", "string", "nil", "label", "type", "var"]
        ALLOWED_ATTRIBUTES = ["program", "language", "description", "name"]

        # check <program>
        if self.root.tag != "program" or self.root.get("language") != "IPPcode23":
            stderr.write("> XMLManager: wrong program tag\n")
            exit(32) # unexpected XML structure

        program_tag_attributes = self.root.attrib.keys()
        for attr in program_tag_attributes:
            if attr not in ALLOWED_ATTRIBUTES:
                stderr.write("> XMLManager: root unallowd attribute\n")
                exit(32) # unexpected XML structure

        # check instrucitons
        for ins in self.root:
            if ins.tag != "instruction" or not ins.get("opcode") or not ins.get("order") or ins.get("opcode").upper() not in OPCODES:
                stderr.write("> XMLManager: wrong instruction tag\n")
                exit(32) # unexpected XML structure

            try:
                int(ins.get("order"))
            except (ValueError, TypeError):
                stderr.write("> XMLManager: wrong order value\n")
                exit(32) # unexpected XML structure

            # check arguments
            for arg in ins:
                # check arg tag and arguments
                if arg.tag[:3] != "arg" or arg.get("type") not in TYPES:
                    stderr.write("> XMLManager: wrong arg tag\n")
                    exit(32) # error - unexpected XML structure

                # check arg order
                try:
                    order = int(arg.tag[-1])
                    if order > 3 or order <= 0:
                        raise ValueError("Max number of arg is 3")
                except (ValueError, IndexError, TypeError):
                    stderr.write("> XMLManager: argN, N not in {1, 2, 3}\n")
                    exit(32)

    def getIns(self, index):
        return self.root[index]
