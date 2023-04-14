import FlowManager
import InstructionFactory

def interpret():
    FLOW = FlowManager()
    IF = InstructionFactory()

    while (True):
        curr = FLOW.getNextIns()

        if curr == None:
            break
        
        # req = IF.getReq(curr)
        ins = IF.gen(curr)
        # ins.execute(*req)
        ins.execute()
        
interpret()
