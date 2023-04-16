from Instruction import *
from sys import stderr

class InstructionFactory:
    __instance = None

    def __new__(cls):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @staticmethod
    def getInstance():
        return __class__.__instance
    
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
            stderr.write("> InstructionFactory: unknown opcode\n")
            exit(32) # error - unknown instruction
