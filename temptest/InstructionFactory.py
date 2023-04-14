from Instruction import *

class InstructionFactory:
    __instance = None

    def __new__(cls):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.requirements = {
            "FRAME": ["MOVE", "CREATEFRAME", "PUSHFRAME", "POPFRAME", "DEFVAR", "PUSHS", "POPS", "ADD", "SUB", "MUL", "IDIV", "LT", "GT", "EQ", "AND", "OR", "NOT", "INT2CHAR", "STRI2INT", "READ", "WRITE", "CONCAT", "STRLEN", "GETCHAR", "SETCHAR", "TYPE", "DPRINT", "BREAK", "JUMPIFEQ", "JUMPIFNEQ"],
            "FLOW": ["CALL", "RETURN", "JUMP", "JUMPIFEQ", "JUMPIFNEQ", "BREAK"],
            "IO": ["READ", "WRITE", "DPRINT", "BREAK"],
            "STACK": ["PUSHS", "POPS"]
        }

    def gen(self, ins):
        if (ins.get("opcode") == "MOVE"):
            return Move(ins)

        elif (ins.get("opcode") == "CREATEFRAME"):
            return Createframe(ins)

        elif (ins.get("opcode") == "PUSHFRAME"):
            return Pushframe(ins)

        elif (ins.get("opcode") == "POPFRAME"):
            return Popframe(ins)

        elif (ins.get("opcode") == "DEFVAR"):
            return Defvar(ins)

        elif (ins.get("opcode") == "CALL"):
            return Call(ins)

        elif (ins.get("opcode") == "RETURN"):
            return Return(ins)

        elif (ins.get("opcode") == "PUSHS"):
            return Pushs(ins)

        elif (ins.get("opcode") == "POPS"):
            return Pops(ins)

        elif (ins.get("opcode") == "ADD"):
            return Add(ins)

        elif (ins.get("opcode") == "SUB"):
            return Sub(ins)

        elif (ins.get("opcode") == "MUL"):
            return Mul(ins)

        elif (ins.get("opcode") == "IDIV"):
            return Idiv(ins)

        elif (ins.get("opcode") == "LT"):
            return Lt(ins)

        elif (ins.get("opcode") == "GT"):
            return Gt(ins)

        elif (ins.get("opcode") == "EQ"):
            return Eq(ins)

        elif (ins.get("opcode") == "AND"):
            return And(ins)

        elif (ins.get("opcode") == "OR"):
            return Or(ins)

        elif (ins.get("opcode") == "NOT"):
            return Not(ins)

        elif (ins.get("opcode") == "INT2CHAR"):
            return Int2char(ins)

        elif (ins.get("opcode") == "STRI2INT"):
            return Stri2int(ins)

        elif (ins.get("opcode") == "READ"):
            return Read(ins)

        elif (ins.get("opcode") == "WRITE"):
            return Write(ins)

        elif (ins.get("opcode") == "CONCAT"):
            return Concat(ins)

        elif (ins.get("opcode") == "STRLEN"):
            return Strlen(ins)

        elif (ins.get("opcode") == "GETCHAR"):
            return Getchar(ins)

        elif (ins.get("opcode") == "SETCHAR"):
            return Setchar(ins)

        elif (ins.get("opcode") == "TYPE"):
            return Type(ins)

        elif (ins.get("opcode") == "LABEL"):
            return Label(ins)

        elif (ins.get("opcode") == "JUMP"):
            return Jump(ins)

        elif (ins.get("opcode") == "JUMPIFEQ"):
            return Jumpifeq(ins)

        elif (ins.get("opcode") == "JUMPIFNEQ"):
            return Jumpifneq(ins)

        elif (ins.get("opcode") == "EXIT"):
            return Exit(ins)

        elif (ins.get("opcode") == "DPRINT"):
            return Dprint(ins)

        elif (ins.get("opcode") == "BREAK"):
            return Break(ins)

        else:
            # print("> exitting in InstructionFactory.gen() - unknown instruction") # REMOVE
            exit(52) # error - unknown instruction