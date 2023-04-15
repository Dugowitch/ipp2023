from ArgParser import ArgParser
from FlowManager import FlowManager
from FrameManager import FrameManager
from IOManager import IOManager
from InstructionFactory import InstructionFactory
from StackManager import StackManager
from XMLManager import XMLManager

from sys import stderr


def interpret():
    ArgParser()
    IOManager()
    XMLManager()
    FlowManager()
    FrameManager()
    StackManager()
    InstructionFactory()
    
    FLOW = FlowManager.getInstance()
    IF = InstructionFactory.getInstance()

    while (True):
        curr = FLOW.getNextIns()

        if curr == None:
            break
        
        ins = IF.gen(curr)
        # stderr.write(f"> interpret(): {ins}\n") # REMOVE
        ins.execute()
        
interpret()
