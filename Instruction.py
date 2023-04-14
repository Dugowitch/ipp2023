from abc import ABC, abstractmethod
from FrameManager import FrameManager
from FlowManager import FlowManager
from IOManager import IOManager
from StackManager import StackManager

import re


class Instruction(ABC):
    def __init__(self, ins):
        self.opcode = ins.get("opcode")
        self.args = [None, None, None]
        for arg in ins:
            try:
                order = int(arg.tag[-1]) - 1
            except ValueError:
                exit(52)
            self.args[order] = arg
        if self.args[2] == None:
            self.args.remove(self.args[2])
            if self.args[1] == None:
                self.args.remove(self.args[1])
                if self.args[0] == None:
                    self.args.remove(self.args[0])
        if len(self.args) > 1:
            if self.args[0] == None:
                exit(52)

    def _getOps(self, FRAME, *args):
        frame, name = FRAME.getFrame(args[0].text)

        n1 = n2 = None

        if (args[1].get("type") == "var"):
            n1 = FRAME.getVal(args[1].text)
        else:
            try:
                n1 = int(args[1].text)
            except ValueError:
                exit(53) # wrong operand type

        if len(args) >= 3:
            if (args[2].get("type") == "var"):
                n2 = FRAME.getVal(args[2].text)
            else:
                try:
                    n2 = int(args[2].text)
                except ValueError:
                    exit(53) # wrong operand type

        return frame, name, n1, n2
    
    @abstractmethod
    def execute(self, **params):
        pass

class Move(Instruction):
    def execute(self, FRAME):
        if len(self.args) != 2:
            exit(52)

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
            elif t == "nil":
                newVal = None
            else:
                newVal = src.text
        frame.save(name, newVal)

class Createframe(Instruction):
    def execute(self, FRAME):
        if len(self.args) != 0:
            exit(52)
            
        FRAME.createframe()

class Pushframe(Instruction):
    def execute(self, FRAME):
        if len(self.args) != 0:
            exit(52)
            
        FRAME.pushframe()

class Popframe(Instruction):
    def execute(self, FRAME):
        if len(self.args) != 0:
            exit(52)
            
        FRAME.popframe()

class Defvar(Instruction):
    def execute(self, FRAME):
        if len(self.args) != 1:
            exit(52)
            
        frame, name = FRAME.getFrame(self.args[0].text)
        frame.defvar(name)

class Call(Instruction):
    def execute(self, FLOW):
        if len(self.args) != 1:
            exit(52)
            
        FLOW.call(self.args[0].text)

class Return(Instruction):
    def execute(self, FLOW):
        if len(self.args) != 0:
            exit(52)
            
        FLOW.ret()

class Pushs(Instruction):
    def execute(self, FRAME, STACK):
        if len(self.args) != 1:
            exit(52)
            
        toPush = None
        if self.args[0].get("type") == "var":
            toPush = FRAME.getVal(self.args[0].text)
        else:
            toPush = self.args[0].text
        STACK.push(toPush)

class Pops(Instruction):
    def execute(self, FRAME, STACK):
        if len(self.args) != 1:
            exit(52)
            
        if len(self.args) == 1:
            frame, name = FRAME.getFrame(self.args[0].text)
            frame.save(name, STACK.pop())
        else:
            # print("> exitting in Pops.execute() - incorrect number of arguments") # REMOVE
            exit(52) # error - incorrect number of args

class Add(Instruction):
    def execute(self, FRAME):
        if len(self.args) != 3:
            exit(52)
            
        frame, name = FRAME.getFrame(self.args[0].text)
        n1 = n2 = None

        if (self.args[1].get("type") == "var"):
            n1 = FRAME.getVal(self.args[1].text)
        else:
            try:
                n1 = int(self.args[1].text)
            except ValueError:
                exit(53)

        if (self.args[2].get("type") == "var"):
            n2 = FRAME.getVal(self.args[2].text)
        else:
            try:
                n2 = int(self.args[2].text)
            except ValueError:
                exit(53)

        frame.save(name, n1 + n2)

class Sub(Instruction):
    def execute(self, FRAME):
        if len(self.args) != 3:
            exit(52)
            
        frame, name, n1, n2 = self._getOps(FRAME, *self.args)
        frame.save(name, n1 - n2)

class Mul(Instruction):
    def execute(self, FRAME):
        if len(self.args) != 3:
            exit(52)
            
        frame, name, n1, n2 = self._getOps(FRAME, *self.args)
        frame.save(name, n1 * n2)

class Idiv(Instruction):
    def execute(self, FRAME):
        if len(self.args) != 3:
            exit(52)
            
        frame, name, n1, n2 = self._getOps(FRAME, *self.args)
        if n2 == 0:
            exit(57) # error - attempting to devide by 0
        else:
            frame.save(name, n1 // n2)

class Lt(Instruction):
    def execute(self, FRAME):
        if len(self.args) != 3:
            exit(52)
            
        frame, name, n1, n2 = self._getOps(FRAME, *self.args)
        frame.save(name, n1 < n2)

class Gt(Instruction):
    def execute(self, FRAME):
        if len(self.args) != 3:
            exit(52)
            
        frame, name, n1, n2 = self._getOps(FRAME, *self.args)
        frame.save(name, n1 > n2)

class Eq(Instruction):
    def execute(self, FRAME):
        if len(self.args) != 3:
            exit(52)
            
        frame, name, n1, n2 = self._getOps(FRAME, *self.args)
        frame.save(name, n1 == n2)

class And(Instruction):
    def execute(self, FRAME):
        if len(self.args) != 3:
            exit(52)
            
        frame, name, n1, n2 = self._getOps(FRAME, *self.args)
        frame.save(name, n1 and n2)

class Or(Instruction):
    def execute(self, FRAME):
        if len(self.args) != 3:
            exit(52)
            
        frame, name, n1, n2 = self._getOps(FRAME, *self.args)
        frame.save(name, n1 or n2)

class Not(Instruction):
    def execute(self, FRAME):
        if len(self.args) != 3:
            exit(52)
            
        frame, name, n1, _ = self._getOps(FRAME, *self.args)
        frame.save(name, not n1)

class Int2char(Instruction):
    def execute(self, FRAME):
        if len(self.args) != 2:
            exit(52)
            
        frame, name, n1, _ = self._getOps(FRAME, *self.args)
        frame.save(name, f"{n1}")

class Stri2int(Instruction):
    def execute(self, FRAME):
        if len(self.args) != 3:
            exit(52)
            
        frame, name, n1, n2 = self._getOps(FRAME, *self.args)
        frame.save(name, ord(n1[n2]))

class Read(Instruction):
    def execute(self, FRAME, IO):
        if len(self.args) != 2:
            exit(52)
            
        frame, name = FRAME.getFrame(self.args[0].text)
        t = self.args[1].text
        val = IO.readOne()
        if val:
            if t == "int":
                try:
                    val = int(val)
                except ValueError:
                    val = None
            elif t == "bool":
                if val.lower() == "true":
                    val = True
                elif val.lower() == "false":
                    val = False
                else:
                    val = None
        frame.save(name, val)

class Write(Instruction):
    def execute(self, FRAME, IO):
        if len(self.args) != 1:
            exit(52)
            
        message = ""
        if self.args[0].get("type") == "var":
            message = FRAME.getVal(self.args[0].text)
        else:
            message = self.args[0].text
        IO.write(message)

class Concat(Instruction):
    def execute(self, FRAME):
        if len(self.args) != 3:
            exit(52)
            
        frame, name, n1, n2 = self._getOps(FRAME, *self.args)
        frame.save(name, f"{n1}{n2}")

class Strlen(Instruction):
    def execute(self, FRAME):
        if len(self.args) != 2:
            exit(52)
            
        frame, name, n1, _ = self._getOps(FRAME, *self.args)
        frame.save(name, len(n1))

class Getchar(Instruction):
    def execute(self, FRAME):
        if len(self.args) != 3:
            exit(52)
            
        frame, name, n1, n2 = self._getOps(FRAME, *self.args)
        frame.save(name, n1[n2])

class Setchar(Instruction):
    def execute(self, FRAME):
        if len(self.args) != 3:
            exit(52)
            
        frame, name, n1, n2 = self._getOps(FRAME, *self.args)
        orig = FRAME.getVal(name)
        newVal = orig
        newVal[n1] = n2[0]
        frame.save(name, newVal)

class Type(Instruction):
    def execute(self, FRAME):
        if len(self.args) != 2:
            exit(52)
            
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
    def execute(self):
        if len(self.args) != 1:
            exit(52)
            
        pass # it's parsed in FrameManager constructor

class Jump(Instruction):
    def execute(self, FLOW):
        if len(self.args) != 1:
            exit(52)
            
        FLOW.jump(self.args[0].text)

class Jumpifeq(Instruction):
    def execute(self, FRAME, FLOW):
        if len(self.args) != 3:
                exit(52)

        label = self.args[0].text
        n1 = n2 = None
        n1_t = n2_t = None

        if (self.args[1].get("type") == "var"):
            n1 = FRAME.getVal(self.args[1].text)
        else:
            n1 = self.args[1].text
            n1_t = self.args[1].get("type")

        if (self.args[2].get("type") == "var"):
            n2 = FRAME.getVal(self.args[2].text)
        else:
            n2 = self.args[2].text
            n2_t = self.args[2].get("type")
                
        if (n1 == n2 and n1_t == n2_t):
            FLOW.jump(label)

class Jumpifneq(Instruction):
    def execute(self, FRAME, FLOW):
        if len(self.args) != 3:
                exit(52)
                
        label = self.args[0].text
        n1 = n2 = None
        n1_t = n2_t = None

        if (self.args[1].get("type") == "var"):
            n1 = FRAME.getVal(self.args[1].text)
        else:
            n1 = self.args[1].text
            n1_t = self.args[1].get("type")

        if (self.args[2].get("type") == "var"):
            n2 = FRAME.getVal(self.args[2].text)
        else:
            n2 = self.args[2].text
            n2_t = self.args[2].get("type")

        if (n1 != n2 or n1_t != n2_t):
            FLOW.jump(label)

class Exit(Instruction):
    def execute(self):
        if len(self.args) != 1:
            exit(52)
            
        try:
            errCode = int(self.args[0].text)
        except ValueError:
            exit(53)
        
        if 0 <= errCode <= 49:
            exit(errCode)
        else:
            exit(57) # error -ivalid exit code

class Dprint(Instruction):
    def execute(self, FRAME, IO):
        if len(self.args) != 1:
            exit(52)
            
        # _, _, n1, _ = self._getOps(FRAME, *self.args[0])
        n1 = ""
        if self.args[0].get("type") == "var":   
            n1 = FRAME.getVal(self.args[0].text)
        else:
            n1 = self.args[0].get("type")
        IO.write(n1, True)

class Break(Instruction):
    def execute(self, FRAME, FLOW, IO):
        if len(self.args) != 0:
            exit(52)
            
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
