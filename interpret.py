from ArgParser import ArgParser
from FlowManager import FlowManager
from FrameManager import FrameManager
from IOManager import IOManager
from InstructionFactory import InstructionFactory
from StackManager import StackManager
from XMLManager import XMLManager

class Interpreter:
    __instance = None

    def __new__(cls):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        # initialize all
        ArgParser()
        IOManager()
        XMLManager()
        FlowManager()
        FrameManager()
        StackManager()
        InstructionFactory()

    @staticmethod
    def getInstance():
        return __class__.__instance

    def interpret(self):
        FLOW = FlowManager.getInstance()
        IF = InstructionFactory.getInstance()

        # program loop
        while (True):
            curr = FLOW.getNextIns()

            # end condition
            if curr == None:
                break
            
            ins = IF.gen(curr)
            ins.execute()

my_interpreter = Interpreter()
my_interpreter.interpret()
