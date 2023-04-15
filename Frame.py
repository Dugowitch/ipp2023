from sys import stderr

class Frame:
    def __init__(self):
        self.vars = {} # dictionary as hashtable to store variables

    def defvar(self, name):
        if name in self.vars:
            stderr.write("> Frame: variable redefinition\n")
            exit(52) # variable redefinition

        # stderr.write(f"> Frame.defvar(): saving {self}@{name}\n") # REMOVE
        self.vars[name] = None;

    def save(self, name, value):
        if name not in self.vars:
            stderr.write("> Frame: assignment to undefined variable\n")
            exit(54) # assignment to undefined variable
            
        self.vars[name] = value

    def getVal(self, name):
        if name not in self.vars:
            stderr.write("> Frame: accessing undefined variable\n")
            exit(54) # accessing undefined variable

        return self.vars[name]
