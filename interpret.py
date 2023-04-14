from FrameManager import FrameManager
from StackManager import StackManager
from IOManager import IOManager
from ArgParser import ArgParser
from FlowManager import FlowManager
from XMLManager import XMLManager
from InstructionFactory import InstructionFactory

class Interpreter:
    __instance = None

    def __new__(cls):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    # # this should not be needed 
    # def __init__(self):
    #     # initialize all here which ensures they get created in correct order
    #     ArgParser()
    #     IOManager()
    #     XMLManager()
    #     FlowManager()
    #     FrameManager()
    #     StackManager()
    #     InstructionFactory()

    def interpret():
        FLOW = FlowManager()
        IF = InstructionFactory()

        while (True):
            curr = FLOW.getNextIns()

            if curr == None:
                break
            
            req = IF.getReq(curr)
            ins = IF.gen(curr)
            ins.execute(*req)
            
interpreter = Interpreter()
interpreter.interpret()
