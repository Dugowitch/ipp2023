from sys import stderr

class StackManager:
    __instance = None

    def __new__(cls):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.stack = []

    @staticmethod
    def getInstance():
        return __class__.__instance

    def push(self, symb):
        self.stack.append(symb)

    def pop(self):
        if self.stack == []:
            stderr.write("> StackManager: missing stack item\n")
            exit(56) # missing stack item

        return self.stack.pop()
