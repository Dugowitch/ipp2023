import FrameManager
import IOManager
import StackManager
import FlowManager
from Instruction import *

class InstructionFactory:
    __instance = None

    def __new__(cls):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    # def getReq(ins):
    #     FRAME = FrameManager()
    #     FLOW = FlowManager()
    #     IO = IOManager()
    #     STACK = StackManager()
    #     opcode = ins.get("opcode").upper()
    #     req_mapping = {
    #         "FRAME": ["MOVE", "CREATEFRAME", "PUSHFRAME", "POPFRAME", "DEFVAR", "PUSHS", "POPS", "ADD", "SUB", "MUL", "IDIV", "LT", "GT", "EQ", "AND", "OR", "NOT", "INT2CHAR", "STRI2INT", "READ", "WRITE", "CONCAT", "STRLEN", "GETCHAR", "SETCHAR", "TYPE", "DPRINT", "BREAK", "JUMPIFEQ", "JUMPIFNEQ"],
    #         "FLOW": ["CALL", "RETURN", "JUMP", "JUMPIFEQ", "JUMPIFNEQ", "BREAK"],
    #         "IO": ["READ", "WRITE", "DPRINT", "BREAK"],
    #         "STACK": ["PUSHS", "POPS"]
    #     }
    #     req = []

    #     if (opcode in req_mapping["FRAME"]):
    #         req.append(FRAME);
    #     if (opcode in req_mapping["FLOW"]):
    #         req.append(FLOW);
    #     if (opcode in req_mapping["IO"]):
    #         req.append(IO);
    #     if (opcode in req_mapping["STACK"]):
    #         req.append(STACK);

    #     return req

    def gen(self, ins):
        opcode = ins.get("opcode").upper()
        
        if (opcode == "MOVE"):
            return Move(ins)

        elif (opcode == "CREATEFRAME"):
            return Createframe(ins)

        elif (opcode == "PUSHFRAME"):
            return Pushframe(ins)

        elif (opcode == "POPFRAME"):
            return Popframe(ins)

        elif (opcode == "DEFVAR"):
            return Defvar(ins)

        elif (opcode == "CALL"):
            return Call(ins)

        elif (opcode == "RETURN"):
            return Return(ins)

        elif (opcode == "PUSHS"):
            return Pushs(ins)

        elif (opcode == "POPS"):
            return Pops(ins)

        elif (opcode == "ADD"):
            return Add(ins)

        elif (opcode == "SUB"):
            return Sub(ins)

        elif (opcode == "MUL"):
            return Mul(ins)

        elif (opcode == "IDIV"):
            return Idiv(ins)

        elif (opcode == "LT"):
            return Lt(ins)

        elif (opcode == "GT"):
            return Gt(ins)

        elif (opcode == "EQ"):
            return Eq(ins)

        elif (opcode == "AND"):
            return And(ins)

        elif (opcode == "OR"):
            return Or(ins)

        elif (opcode == "NOT"):
            return Not(ins)

        elif (opcode == "INT2CHAR"):
            return Int2char(ins)

        elif (opcode == "STRI2INT"):
            return Stri2int(ins)

        elif (opcode == "READ"):
            return Read(ins)

        elif (opcode == "WRITE"):
            return Write(ins)

        elif (opcode == "CONCAT"):
            return Concat(ins)

        elif (opcode == "STRLEN"):
            return Strlen(ins)

        elif (opcode == "GETCHAR"):
            return Getchar(ins)

        elif (opcode == "SETCHAR"):
            return Setchar(ins)

        elif (opcode == "TYPE"):
            return Type(ins)

        elif (opcode == "LABEL"):
            return Label(ins)

        elif (opcode == "JUMP"):
            return Jump(ins)

        elif (opcode == "JUMPIFEQ"):
            return Jumpifeq(ins)

        elif (opcode == "JUMPIFNEQ"):
            return Jumpifneq(ins)

        elif (opcode == "EXIT"):
            return Exit(ins)

        elif (opcode == "DPRINT"):
            return Dprint(ins)

        elif (opcode == "BREAK"):
            return Break(ins)

        else:
            # print("> exitting in InstructionFactory.gen() - unknown instruction") # REMOVE
            exit(32) # error - unknown instruction