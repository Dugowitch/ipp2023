from abc import ABC, abstractmethod
import re

class Instruction(ABC):
    def __init__(self, ins):
        self.opcode = ins.get("opcode")
        self.args = []
        for arg in ins:
            self.args.append(arg)

    def _getOps(self, FRAME, *args):
        frame, name = FRAME.getFrame(args[0].text)
        n1 = n2 = None

        if (args[1].get("type") == "var"):
            n1 = FRAME.getVal(args[1].text)
        else:
            n1 = int(args[1].text)

        if len(args) >= 3:
            if (args[2].get("type") == "var"):
                n2 = FRAME.getVal(args[2].text)
            else:
                n2 = int(args[2].text)

        return frame, name, n1, n2
    
    @abstractmethod
    def execute(self, **params):
        pass

class Move(Instruction):
    def execute(self, FRAME):
        if len(self.args) == 2:
            dst = self.args[0]
            src = self.args[1]
            frame, name = FRAME.getFrame(dst.text)
            newVal = None
            if src.get("type") == "var":
                newVal = FRAME.getVal(src.text)
            else:
                t = src.get("type")
                if t == "int":
                    newVal = int(src.text)
                elif t == "bool":
                    newVal = True if src.text.lower() == "true" else False
                else:
                    newVal = src.text
            frame.save(name, newVal)
        else:
            print("> exitting in Move.execute() - incorrect number of arguments") # REMOVE
            exit(52) # error - incorrect number of args

class Createframe(Instruction):
    def execute(self, FRAME):
        FRAME.createframe()

class Pushframe(Instruction):
    def execute(self, FRAME):
        FRAME.pushframe()

class Popframe(Instruction):
    def execute(self, FRAME):
        FRAME.popframe()

class Defvar(Instruction):
    def execute(self, FRAME):
        frame, name = FRAME.getFrame(self.args[0].text)
        frame.defvar(name)

class Call(Instruction):
    def execute(self, FLOW):
        FLOW.call(self.args[0].text)

class Return(Instruction):
    def execute(self, FLOW):
        FLOW.ret()

class Pushs(Instruction):
    def execute(self, FRAME, STACK):
        toPush = None
        if self.args[0].get("type") == "var":
            toPush = FRAME.getVal(self.args[0].text)
        else:
            toPush = self.args[0].text
        STACK.push(toPush)

class Pops(Instruction):
    def execute(self, FRAME, STACK):
        if len(self.args) == 1:
            frame, name = FRAME.getFrame(self.args[0].text)
            frame.save(name, STACK.pop())
        else:
            print("> exitting in Pops.execute() - incorrect number of arguments") # REMOVE
            exit(52) # error - incorrect number of args

class Add(Instruction):
    def execute(self, FRAME):
        frame, name = FRAME.getFrame(self.args[0].text)
        n1 = n2 = None

        if (self.args[1].get("type") == "var"):
            n1 = FRAME.getVal(self.args[1].text)
        else:
            n1 = int(self.args[1].text)

        if (self.args[2].get("type") == "var"):
            n2 = FRAME.getVal(self.args[2].text)
        else:
            n2 = int(self.args[2].text)

        frame.save(name, n1 + n2)

class Sub(Instruction):
    def execute(self, FRAME):
        frame, name, n1, n2 = self._getOps(FRAME, *self.args)
        frame.save(name, n1 - n2)

class Mul(Instruction):
    def execute(self, FRAME):
        frame, name, n1, n2 = self._getOps(FRAME, *self.args)
        frame.save(name, n1 * n2)

class Idiv(Instruction):
    def execute(self, FRAME):
        frame, name, n1, n2 = self._getOps(FRAME, *self.args)
        if n2 == 0:
            exit(57) # error - attempting to devide by 0
        else:
            frame.save(name, n1 // n2)

class Lt(Instruction):
    def execute(self, FRAME):
        frame, name, n1, n2 = self._getOps(FRAME, *self.args)
        frame.save(name, n1 < n2)

class Gt(Instruction):
    def execute(self, FRAME):
        frame, name, n1, n2 = self._getOps(FRAME, *self.args)
        frame.save(name, n1 > n2)

class Eq(Instruction):
    def execute(self, FRAME):
        frame, name, n1, n2 = self._getOps(FRAME, *self.args)
        frame.save(name, n1 == n2)

class And(Instruction):
    def execute(self, FRAME):
        frame, name, n1, n2 = self._getOps(FRAME, *self.args)
        frame.save(name, n1 and n2)

class Or(Instruction):
    def execute(self, FRAME):
        frame, name, n1, n2 = self._getOps(FRAME, *self.args)
        frame.save(name, n1 or n2)

class Not(Instruction):
    def execute(self, FRAME):
        frame, name, n1, _ = self._getOps(FRAME, *self.args)
        frame.save(name, not n1)

class Int2char(Instruction):
    def execute(self, FRAME):
        frame, name, n1, _ = self._getOps(FRAME, *self.args)
        frame.save(name, f"{n1}")

class Stri2int(Instruction):
    def execute(self, FRAME):
        frame, name, n1, n2 = self._getOps(FRAME, *self.args)
        frame.save(name, ord(n1[n2]))

class Read(Instruction):
    def execute(self, FRAME, IO):
        frame, name = FRAME.getFrame(self.args[0].text)
        t = self.args[1].text
        val = IO.readOne()
        if val:
            if t == "int":
                val = int(val)
            elif t == "bool":
                val = True if val.lower() == "true" else False
        frame.save(name, val)

class Write(Instruction):
    def execute(self, FRAME, IO):
        message = ""
        if self.args[0].get("type") == "var":
            message = FRAME.getVal(self.args[0].text)
        else:
            message = self.args[0].text
        IO.write(message)

class Concat(Instruction):
    def execute(self, FRAME):
        frame, name, n1, n2 = self._getOps(FRAME, *self.args)
        frame.save(name, f"{n1}{n2}")

class Strlen(Instruction):
    def execute(self, FRAME):
        frame, name, n1, _ = self._getOps(FRAME, *self.args)
        frame.save(name, len(n1))

class Getchar(Instruction):
    def execute(self, FRAME):
        frame, name, n1, n2 = self._getOps(FRAME, *self.args)
        frame.save(name, n1[n2])

class Setchar(Instruction):
    def execute(self, FRAME):
        frame, name, n1, n2 = self._getOps(FRAME, *self.args)
        orig = FRAME.getVal(name)
        newVal = orig
        newVal[n1] = n2[0]
        frame.save(name, newVal)

class Type(Instruction):
    def execute(self, FRAME):
        frame, name = FRAME.getFrame(self.args[0].text)
        t = self.args[1].get("type")
        if (t == "var"):
            t = str(type(FRAME.getVal(self.args[1].text)))
            if re.search(r"int", t):
                t = "int"
            elif re.search(r"str", t):
                t = "string"
            elif re.search(r"bool", t):
                t = "bool"
            elif re.search(r"NoneType", t):
                t = "nil"
        frame.save(name, t)

class Label(Instruction):
    pass # it's parsed in FrameManager constructor

class Jump(Instruction):
    def execute(self, FLOW):
        FLOW.jump(self.args[0].text)

class Jumpifeq(Instruction):
    def execute(self, FRAME, FLOW):
        label, _, n1, n2 = self._getOps(FRAME, *self.args)
        if (n1 == n2 and self.args[1].get("type") == self.args[2].get("type")):
            FLOW.jump(label)

class Jumpifneq(Instruction):
    def execute(self, FRAME, FLOW):
        label, _, n1, n2 = self._getOps(FRAME, *self.args)
        if (n1 != n2 or self.args[1].get("type") != self.args[2].get("type")):
            FLOW.jump(label)

class Exit(Instruction):
    def execute(self):
        errCode = int(self.args[0].text)
        if 0 <= errCode <= 49:
            exit(errCode)
        else:
            exit(57) # error -ivalid exit code

class Dprint(Instruction):
    def execute(self, FRAME, IO):
        _, _, n1, _ = self._getOps(FRAME, *self.args[0])
        IO.write(n1)

class Break(Instruction):
    def execute(self, FRAME, FLOW, IO):
        IO.write(f"BREAK: instruction #{FLOW.ip} - {self.opcode}\n", 1);
        self.__printFrames(FRAME, IO)

    def __printFrames(self, FRAME, IO):
        if FRAME.GF != None:
            self.__printFrame(FRAME.GF.vars, IO, "GF")
        else:
            self.__printFrame({}, IO, "GF")

        if FRAME.TF != None:
            self.__printFrame(FRAME.TF.vars, IO, "TF")
        else:
            self.__printFrame({}, IO, "TF")
        
        if FRAME.LF != []:
            self.__printFrame(FRAME.LF[0].vars, IO, "LF")
        else:
            self.__printFrame({}, IO, "LF")


    def __printFrame(self, frame, IO, name):
        IO.write(f"{name} = ", 1);
        IO.write("{ ", 1)
        isfirst = 1
        for key, val in frame.items():
            if isfirst:
                isfirst = 0
            else:
                IO.write(", ", 1)
            if isinstance(val, str):
                val = f"\"{val}\""
            if val == None:
                val = "nil"
            IO.write(f"\"{key}\" = {val}", 1);
        IO.write(" }\n", 1)
