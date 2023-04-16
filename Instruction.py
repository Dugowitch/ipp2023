from abc import ABC, abstractmethod
from sys import stderr

from FrameManager import FrameManager
from FlowManager import FlowManager
from IOManager import IOManager
from StackManager import StackManager

class Instruction(ABC):
    def __init__(self, ins):
        self.opcode = ins.get("opcode").upper()
        self.args = {}

        for arg in ins:
            if arg.tag in self.args:
                exit(32) # duplicit arg order

            self.args[arg.tag] = arg
        
    def _checkSymb(self, symb):
        if symb.get("type") not in ["var", "int", "bool", "string", "nil"]:
            stderr.write("> Instruction: wrong symb type\n")
            exit(53) # wrong operand type

    def _checkArgsTypes(self, type_lists):
        if len(self.args) != len(type_lists):
            stderr.write("> Instruction: expected args length mismatch\n")
            exit(32) # unexpected XML structure
        
        for arg in self.args:
            arg = self.args[arg]
            result = False
            if arg.get("type") in type_lists[arg.tag]:
                result = True
            if not result:
                stderr.write("> Instruction: wrong type in type attribute\n")
                exit(53) # wrong operand type

    def _cast(self, arg):
        arg_text = arg.text
        arg_type = arg.get("type")
        FRAME = FrameManager.getInstance()
        n = None

        # cast and assign based on type
        if arg_type == "int":
            try:
                n = int(arg_text)
            except (TypeError, ValueError):
                stderr.write("> Instruction: operand value cannot get cast into int\n")
                exit(57) # wrong operand value
        elif arg_type == "bool":
            n = True if arg_text.lower() == "true" else False
        elif arg_type in ["string", "label", "type"]:
            n = arg_text
        elif arg_type == "var":
            n = FRAME.getVal(arg_text)
        # nX is None by default, no need to check and assign for arg_type == "nil"

        return n
    
    def _getAndCheckOps(self, options, param_count = 2, instance_class = int, check_class = True):
        FRAME = FrameManager.getInstance()
        n1 = n2 = None

        # arg1 is the var for the result of an instruction
        frame, name = FRAME.getFrame(self.args["arg1"].text)

        self._checkArgsTypes(options)
        # self._checkArgsText(options)
        for arg in self.args: # warning: arguments can come in any order
            arg = self.args[arg]
            if arg.tag == "arg1": continue # arg1 is not an operand

            n = self._cast(arg)

            if arg.tag == "arg2":
                n1 = n
            elif arg.tag == "arg3":
                n2 = n

        if check_class:
            # var might have gotten casted into something else than int
            if (not isinstance(n1, instance_class)) or (instance_class == int and isinstance(n1, bool)):
                stderr.write("> Instruction: operand1 value is of wrong type\n")
                exit(53) # wrong operand type
            if param_count == 2:
                if (not isinstance(n2, instance_class)) or (instance_class == int and isinstance(n2, bool)):
                    stderr.write("> Instruction: operand2 value is of wrong type\n")
                    exit(53) # wrong operand type

        return frame, name, n1, n2
    
    @abstractmethod
    def execute(self):
        pass

class Move(Instruction):
    def execute(self):
        FRAME = FrameManager.getInstance()
        newVal = None
        dst = self.args["arg1"]
        src = self.args["arg2"]
        frame, name = FRAME.getFrame(dst.text)

        self._checkSymb(src)
        # self._checkArgsText({"arg1": ["var"], "arg2": ["int", "bool", "string", "nil", "var"]})
        newVal = self._cast(src)

        frame.save(name, newVal)

class Createframe(Instruction):
    def execute(self):
        FRAME = FrameManager.getInstance()
        FRAME.createframe()

class Pushframe(Instruction):
    def execute(self):
        FRAME = FrameManager.getInstance()
        FRAME.pushframe()

class Popframe(Instruction):
    def execute(self):
        FRAME = FrameManager.getInstance()
        FRAME.popframe()

class Defvar(Instruction):
    def execute(self):
        FRAME = FrameManager.getInstance()
        # self._checkArgsText({"arg1": ["var"]})
        # stderr.write(f"> Defvar: GF: {FRAME.GF}\n") # REMOVE
        # stderr.write(f"> Defvar: creating {self.args['arg1'].text}\n") # REMOVE
        frame, name = FRAME.getFrame(self.args["arg1"].text)
        frame.defvar(name)

class Call(Instruction):
    def execute(self):
        FLOW = FlowManager.getInstance()
        # self._checkArgsText({"arg1": ["label"]})
        FLOW.call(self.args["arg1"].text)

class Return(Instruction):
    def execute(self):
        FLOW = FlowManager.getInstance()
        FLOW.ret()

class Pushs(Instruction):
    def execute(self):
        STACK = StackManager.getInstance()
        arg1 = self.args["arg1"]
        self._checkSymb(arg1)
        toPush = self._cast(arg1)
        STACK.push(toPush)

class Pops(Instruction):
    def execute(self):
        FRAME = FrameManager.getInstance()
        STACK = StackManager.getInstance()
        options = {"arg1": ["var"]}
        self._checkArgsTypes(options)
        # self._checkArgsText(options)
        frame, name = FRAME.getFrame(self.args["arg1"].text)
        frame.save(name, STACK.pop())

class Add(Instruction):
    def execute(self):
        options = {"arg1": ["var"], "arg2": ["var", "int"], "arg3": ["var", "int"]}
        frame, name, n1, n2 = self._getAndCheckOps(options)
        frame.save(name, n1 + n2)

class Sub(Instruction):
    def execute(self):
        options = {"arg1": ["var"], "arg2": ["var", "int"], "arg3": ["var", "int"]}
        frame, name, n1, n2 = self._getAndCheckOps(options)
        frame.save(name, n1 - n2)

class Mul(Instruction):
    def execute(self):
        options = {"arg1": ["var"], "arg2": ["var", "int"], "arg3": ["var", "int"]}
        frame, name, n1, n2 = self._getAndCheckOps(options)
        frame.save(name, n1 * n2)

class Idiv(Instruction):
    def execute(self):
        options = {"arg1": ["var"], "arg2": ["var", "int"], "arg3": ["var", "int"]}
        frame, name, n1, n2 = self._getAndCheckOps(options)
        if n2 == 0:
            stderr.write("> Idiv: attempting to devide by 0\n")
            exit(57) # attempting to devide by 0
        frame.save(name, n1 // n2)

class Lt(Instruction):
    def execute(self):
        options = {"arg1": ["var"], "arg2": ["var", "int", "bool", "string"], "arg3": ["var", "int", "bool", "string"]}
        frame, name, n1, n2 = self._getAndCheckOps(options, check_class=False)
        if not (((isinstance(n1, int) and not isinstance(n1, bool)) and (isinstance(n2, int) and not isinstance(n2, bool))) or (isinstance(n1, bool) and isinstance(n2, bool)) or (isinstance(n1, str) and isinstance(n2, str))):
            stderr.write("> Lt: wrong operand type combination\n")
            exit(53) # wrong operand type combination
        frame.save(name, n1 < n2)

class Gt(Instruction):
    def execute(self):
        options = {"arg1": ["var"], "arg2": ["var", "int", "bool", "string"], "arg3": ["var", "int", "bool", "string"]}
        frame, name, n1, n2 = self._getAndCheckOps(options, check_class=False)
        if not (((isinstance(n1, int) and not isinstance(n1, bool)) and (isinstance(n2, int) and not isinstance(n2, bool))) or (isinstance(n1, bool) and isinstance(n2, bool)) or (isinstance(n1, str) and isinstance(n2, str))):
            stderr.write("> Gt: wrong operand type combination\n")
            exit(53) # wrong operand type combination
        frame.save(name, n1 > n2)

class Eq(Instruction):
    def execute(self):
        options = {"arg1": ["var"], "arg2": ["var", "int", "bool", "string", "nil"], "arg3": ["var", "int", "bool", "string", "nil"]}
        frame, name, n1, n2 = self._getAndCheckOps(options, check_class=False)
        if not (((isinstance(n1, int) and not isinstance(n1, bool)) and (isinstance(n2, int) and not isinstance(n2, bool))) or (isinstance(n1, bool) and isinstance(n2, bool)) or (isinstance(n1, str) and isinstance(n2, str) or isinstance(n1, type(None)) or isinstance(n2, type(None)))):
            stderr.write("> Eq: wrong operand type combination\n")
            exit(53) # wrong operand type combination
        frame.save(name, n1 == n2)

class And(Instruction):
    def execute(self):
        options = {"arg1": ["var"], "arg2": ["var", "bool"], "arg3": ["var", "bool"]}
        frame, name, n1, n2 = self._getAndCheckOps(options, instance_class=bool)
        frame.save(name, n1 and n2)

class Or(Instruction):
    def execute(self):
        options = {"arg1": ["var"], "arg2": ["var", "bool"], "arg3": ["var", "bool"]}
        frame, name, n1, n2 = self._getAndCheckOps(options, instance_class=bool)
        frame.save(name, n1 or n2)

class Not(Instruction):
    def execute(self):
        options = {"arg1": ["var"], "arg2": ["var", "bool"]}
        frame, name, n1, _ = self._getAndCheckOps(options, param_count=1, instance_class=bool)
        frame.save(name, not n1)

class Int2char(Instruction):
    def execute(self):
        options = {"arg1": ["var"], "arg2": ["var", "int"]}
        frame, name, n1, _ = self._getAndCheckOps(options, param_count=1)
        try:
            char = chr(n1)
        except ValueError:
            stderr.write("> Int2char: int too large for chr()\n")
            exit(58) # wrong operand value # TODO I'd use 57, but tests expect 58
        frame.save(name, chr(n1))

class Stri2int(Instruction):
    def execute(self):
        options = {"arg1": ["var"], "arg2": ["var", "string"], "arg3": ["var", "int"]}
        frame, name, n1, n2 = self._getAndCheckOps(options, check_class=False)
        if not (isinstance(n1, str) and (isinstance(n2, int) and not isinstance(n2, bool))):
            stderr.write("> Stri2Int: wrong operand type\n")
            exit(53) # wrong operand type
        if n2 > len(n1) -1:
            stderr.write("> Stri2Int: string index out of range\n")
            exit(58) # string index out of range
        frame.save(name, ord(n1[n2]))

class Read(Instruction):
    def execute(self):
        FRAME = FrameManager.getInstance()
        IO = IOManager.getInstance()
        options = {"arg1": ["var"], "arg2": ["type"]}

        self._checkArgsTypes(options)
        # self._checkArgsText(options)
        frame, name = FRAME.getFrame(self.args["arg1"].text)
        t = self.args["arg2"].text

        val = IO.readOne()
        if t == "int":
            try:
                val = int(val)
            except (ValueError, TypeError):
                val = None
        elif t == "bool":
            if val == None:
                pass
            elif val.lower() == "true":
                val = True
            else:
                val = False

        frame.save(name, val)

class Write(Instruction):
    def execute(self):
        IO = IOManager.getInstance()
        message = ""
        options = {"arg1": ["int", "bool", "nil", "string", "var"]}

        self._checkArgsTypes(options)
        # self._checkArgsText(options)
        message = self._cast(self.args["arg1"])

        IO.write(message)

class Concat(Instruction):
    def execute(self):
        options = {"arg1": ["var"], "arg2": ["string", "var"], "arg3": ["string", "var"]}
        frame, name, n1, n2 = self._getAndCheckOps(options, instance_class=str)
        frame.save(name, f"{n1}{n2}")

class Strlen(Instruction):
    def execute(self):
        options = {"arg1": ["var"], "arg2": ["string", "var"]}
        frame, name, n1, _ = self._getAndCheckOps(options, param_count=1, instance_class=str)
        frame.save(name, len(n1))

class Getchar(Instruction):
    def execute(self):
        options = {"arg1": ["var"], "arg2": ["var", "string"], "arg3": ["var", "int"]}
        frame, name, n1, n2 = self._getAndCheckOps(options, check_class=False)

        if not (isinstance(n1, str) and (isinstance(n2, int) and not isinstance(n2, bool))):
            stderr.write("> GetChar: wrong operand type\n")
            exit(53) # wrong operand type
        if n2 < 0 or n2 > len(n1) -1:
            stderr.write("> GetChar: string index out of range\n")
            exit(58) # string index out of range
        frame.save(name, n1[n2])

class Setchar(Instruction):
    def execute(self):
        FRAME = FrameManager.getInstance()
        options = {"arg1": ["var"], "arg2": ["var", "int"], "arg3": ["var", "string"]}
        frame, name, n1, n2 = self._getAndCheckOps(options, check_class=False)
        val = FRAME.getVal(self.args["arg1"].text)

        if n2 == None:
            stderr.write("> Setchar: wrong arg3 value - empty\n")
            exit(58) # wrong arg3 value - empty
        if not (isinstance(val, str) and (isinstance(n1, int) and not isinstance(n1, bool)) and isinstance(n2, str)):
            stderr.write("> Setchar: wrong operand type\n")
            exit(53) # wrong operand type
        if n1 < 0 or n1 > len(val) -1:
            stderr.write("> Setchar: string index out of range\n")
            exit(58) # string index out of range

        newVal = val[:n1] + n2[0] + val[n1+1:]
        frame.save(name, newVal)

class Type(Instruction):
    def execute(self):
        FRAME = FrameManager.getInstance()
        options = {"arg1": ["var"], "arg2": ["int", "bool", "string", "nil", "var"]}

        self._checkArgsTypes(options)
        # self._checkArgsText(options)

        frame, name = FRAME.getFrame(self.args["arg1"].text)
        val = self._cast(self.args["arg2"])
        t = None

        # check bool first since bool is a subcalss of int
        if isinstance(val, bool):
            t = "bool"
        elif isinstance(val, int):
            t = "int"
        elif isinstance(val, str):
            t = "string"
        elif isinstance(val, type(None)):
            t = "nil"
        
        frame.save(name, t)

class Label(Instruction):
    def execute(self):
        pass # it's parsed in FrameManager constructor

class Jump(Instruction):
    def execute(self):
        FLOW = FlowManager.getInstance()
        options = {"arg1": ["label"]}
        self._checkArgsTypes(options)
        # self._checkArgsText(options)
        FLOW.jump(self.args["arg1"].text)

class Jumpifeq(Instruction):
    def execute(self):
        FLOW = FlowManager.getInstance()
        options = {"arg1": ["label"], "arg2": ["var", "int", "bool", "string", "nil"], "arg3": ["var", "int", "bool", "string", "nil"]}
        
        self._checkArgsTypes(options)
        # self._checkArgsText(options)
        
        n1 = n2 = None
        for arg in self.args: # warning: arguments can come in any order
            arg = self.args[arg]
            if arg.tag == "arg1": continue # arg1 is not an operand

            n = self._cast(arg)

            if arg.tag == "arg2":
                n1 = n
            elif arg.tag == "arg3":
                n2 = n
        
        if not (((isinstance(n1, int) and not isinstance(n1, bool)) and (isinstance(n2, int) and not isinstance(n2, bool))) or (isinstance(n1, bool) and isinstance(n2, bool)) or (isinstance(n1, str) and isinstance(n2, str) or isinstance(n1, type(None)) or isinstance(n2, type(None)))):
            stderr.write("> Jumpifeq: wrong operand type combination\n")
            exit(53) # wrong operand type combination

        label = self.args["arg1"].text
        if (n1 == n2):
            FLOW.jump(label)

class Jumpifneq(Instruction):
    def execute(self):
        FLOW = FlowManager.getInstance()
        options = {"arg1": ["label"], "arg2": ["var", "int", "bool", "string", "nil"], "arg3": ["var", "int", "bool", "string", "nil"]}
        
        self._checkArgsTypes(options)
        # self._checkArgsText(options)
        
        n1 = n2 = None
        for arg in self.args: # warning: arguments can come in any order
            arg = self.args[arg]
            if arg.tag == "arg1": continue # arg1 is not an operand

            n = self._cast(arg)

            if arg.tag == "arg2":
                n1 = n
            elif arg.tag == "arg3":
                n2 = n
        
        if not (((isinstance(n1, int) and not isinstance(n1, bool)) and (isinstance(n2, int) and not isinstance(n2, bool))) or (isinstance(n1, bool) and isinstance(n2, bool)) or (isinstance(n1, str) and isinstance(n2, str) or isinstance(n1, type(None)) or isinstance(n2, type(None)))):
            stderr.write("> Jumpifneq: wrong operand type combination\n")
            exit(53) # wrong operand type combination

        label = self.args["arg1"].text
        if (n1 != n2):
            FLOW.jump(label)

class Exit(Instruction):
    def execute(self):
        options = {"arg1": ["int", "var"]}

        self._checkArgsTypes(options)
        # self._checkArgsText(options)

        errCode = self._cast(self.args["arg1"])

        if not (isinstance(errCode, int) and not isinstance(errCode, bool)):
            stderr.write("> Exit: wrong operand type \n")
            exit(53) # wrong operand type        
        if errCode < 0 or errCode > 49:
            stderr.write("> Exit: ivalid exit code \n")
            exit(57) # ivalid exit code - wrong operand value

        exit(errCode)

class Dprint(Instruction):
    def execute(self):
        IO = IOManager.getInstance()
        message = ""
        options = {"arg1": ["int", "bool", "nil", "string", "var"]}

        self._checkArgsTypes(options)
        # self._checkArgsText(options)
        message = self._cast(self.args["arg1"])

        IO.write(message, True)

class Break(Instruction):
    def execute(self):
        IO = IOManager.getInstance()
        FLOW = FlowManager.getInstance()

        IO.write(f"BREAK: instruction #{FLOW.ip +1} - {self.opcode}\n", True);
        self.__printFrames()

    def __printFrames(self):
        FRAME = FrameManager.getInstance()

        if FRAME.GF != None:
            self.__printFrame(FRAME.GF.vars, "GF")
        else:
            self.__printFrame({}, "GF")

        if FRAME.TF != None:
            self.__printFrame(FRAME.TF.vars, "TF")
        else:
            self.__printFrame({}, "TF")
        
        if FRAME.LF != []:
            self.__printFrame(FRAME.LF[0].vars, "LF")
        else:
            self.__printFrame({}, "LF")

    def __printFrame(self, frame, name):
        IO = IOManager.getInstance()
        
        dict_name = f"{name} = "
        IO.write(dict_name, True);
        IO.write("{ ", True)
        isfirst = True
        for key, val in frame.items():
            if isfirst:
                isfirst = False
            else:
                IO.write(", ", True)
            if isinstance(val, str):
                val = f"\"{val}\""
            if val == None:
                val = "nil"
            key_value_pair = f"\"{key}\" = {val}"
            IO.write(key_value_pair, True);
        IO.write(" }\n", True)
