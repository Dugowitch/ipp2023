class Frame:
    def __init__(self):
        self.vars = {} # dictionary as hashtable to store variables

    def defvar(self, name):
        if name in self.vars:
            print("> exitting in Frame.defvar() - var redefinition") # REMOVE
            exit(52) # error - var redefinition
        else:
            self.vars[name] = None;

    def save(self, name, value):
        if name not in self.vars:
            exit(54) # error - assignment to undefined variable
        else:
            self.vars[name] = value

    def getVal(self, name):
        if name in self.vars:
            return self.vars[name]
        else:
            exit(54) # error - accessing undefined variable