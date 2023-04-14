class StackManager:
    __instance = None

    def __init__(self):
        self.stack = []

    def __new__(cls):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def push(self, symb):
        self.stack.append(symb)

    def pop(self):
        return self.stack.pop()