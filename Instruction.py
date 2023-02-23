from abc import ABC, abstractmethod

class Instruction(ABC):
    def __init__(self, ins):
        self.opcode = ins.get("opcode")
        self.args = []
        for arg in ins:
            self.args.append(arg)

    def _getOps(FRAME, *args):
        frame, name = FRAME.getFrame(args[0].text)
        n1 = n2 = None

        if (args[1].type == "var"):
            _, n1_name = FRAME.getFrame(args[1].text)
            n1 = FRAME.getVal(n1_name)
        else:
            n1 = int(args[1].text)

        if args[2]:
            if (args[2].type == "var"):
                _, n2_name = FRAME.getFrame(args[2].text)
                n2 = FRAME.getVal(n2_name)
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
            newVal = None
            if src.type == "var":
                newVal = FRAME.getVal(src.text)
            else:
                newVal = src.text
            FRAME.save(dst, newVal)
        else:
            print("> exitting in Move.execute() - incorrect number of arguments") # TODO: remove
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
        FLOW.call(self.args[0])

class Return(Instruction):
    def execute(self, FLOW):
        FLOW.ret()

class Pushs(Instruction):
    def execute(self, FRAME, STACK):
        toPush = None
        if self.args[0].type == "var":
            toPush = FRAME.getVal(self.args[0].text)
        else:
            toPush = self.args[0].text
        STACK.push(toPush)

class Pops(Instruction):
    def execute(self, FRAME, STACK):
        if self.args[0]:
            frame, name = FRAME.getFrame(self.args[0].text)
            frame.save(name, STACK.pop())
        else:
            print("> exitting in Pops.execute() - incorrect number of arguments") # TODO: remove
            exit(52) # error - incorrect number of args

class Add(Instruction):
    def execute(self, FRAME):
        frame, name, n1, n2 = self._getOps(FRAME, self.args)
        frame.save(name, n1 + n2)

class Sub(Instruction):
    def execute(self, FRAME):
        frame, name, n1, n2 = self._getOps(FRAME, self.args)
        frame.save(name, n1 - n2)

class Mul(Instruction):
    def execute(self, FRAME):
        frame, name, n1, n2 = self._getOps(FRAME, self.args)
        frame.save(name, n1 * n2)

class Idiv(Instruction):
    def execute(self, FRAME):
        frame, name, n1, n2 = self._getOps(FRAME, self.args)
        if n2 == 0:
            exit(57) # error - attempting to devide by 0
        else:
            frame.save(name, n1 // n2)

class Lt(Instruction):
    def execute(self, FRAME):
        frame, name, n1, n2 = self._getOps(FRAME, self.args)
        frame.save(name, n1 < n2)

class Gt(Instruction):
    def execute(self, FRAME):
        frame, name, n1, n2 = self._getOps(FRAME, self.args)
        frame.save(name, n1 > n2)

class Eq(Instruction):
    def execute(self, FRAME):
        frame, name, n1, n2 = self._getOps(FRAME, self.args)
        frame.save(name, n1 == n2)

class And(Instruction):
    def execute(self, FRAME):
        frame, name, n1, n2 = self._getOps(FRAME, self.args)
        frame.save(name, n1 and n2)

class Or(Instruction):
    def execute(self, FRAME):
        frame, name, n1, n2 = self._getOps(FRAME, self.args)
        frame.save(name, n1 or n2)

class Not(Instruction):
    def execute(self, FRAME):
        frame, name, n1, _ = self._getOps(FRAME, self.args)
        frame.save(name, not n1)

class Int2char(Instruction):
    def execute(self, FRAME):
        frame, name, n1, _ = self._getOps(FRAME, self.args)
        frame.save(name, f"{n1}")

class Stri2int(Instruction):
    def execute(self, FRAME):
        frame, name, n1, n2 = self._getOps(FRAME, self.args)
        frame.save(name, ord(n1[n2]))

class Read(Instruction):
    def execute(self, FRAME, IO):
        frame, name = FRAME.getFrame(self.args[0].text)
        frame.save(name, IO.readOne())

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
        frame, name, n1, n2 = self._getOps(FRAME, self.args)
        frame.save(name, f"{n1}{n2}")

class Strlen(Instruction):
    def execute(self, FRAME):
        frame, name, n1, _ = self._getOps(FRAME, self.args)
        frame.save(name, len(n1))

class Getchar(Instruction):
    def execute(self, FRAME):
        frame, name, n1, n2 = self._getOps(FRAME, self.args)
        frame.save(name, n1[n2])

class Setchar(Instruction):
    def execute(self, FRAME):
        frame, name, n1, n2 = self._getOps(FRAME, self.args)
        orig = FRAME.getVal(name)
        newVal = orig
        newVal[n1] = n2[0]
        frame.save(name, newVal)

class Type(Instruction):
    def execute(self, FRAME):
        frame, name, _, _ = self._getOps(FRAME, self.args)
        frame.save(name, self.args[1].type)

class Label(Instruction):
    pass # its parsed in FrameManager constructor 

class Jump(Instruction):
    def execute(self, FLOW):
        FLOW.jump(self.args[0])

class Jumpifeq(Instruction):
    def execute(self, FRAME, FLOW):
        label, _, n1, n2 = self._getOps(FRAME, self.args)
        if (n1 == n2 and self.args[1].type == self.args[2].type):
            FLOW.jump(label)

class Jumpifneq(Instruction):
    def execute(self, FRAME, FLOW):
        label, _, n1, n2 = self._getOps(FRAME, self.args)
        if (n1 != n2 or self.args[1].type != self.args[2].type):
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
        _, _, n1, _ = self._getOps(FRAME, self.args[0])
        IO.write(n1)

class Break(Instruction):
    pass # TODO
    # na standardní chybový výstup (stderr) vypíše stav interpretu (např. pozice
    # v kódu, obsah rámců, počet vykonaných instrukcí) v danou chvíli 
