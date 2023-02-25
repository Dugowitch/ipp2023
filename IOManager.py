import sys

class IOManager:
    def __init__(self, ARGS):
        self.INPUT = []
        if ARGS.input:
            with open(ARGS.input) as f:
                raw = f.read()
                self.INPUT = raw.split("\n")
        else:
            self.INPUT = self.read().split("\n")
            self.INPUT.reverse()

    def readOne(self):
        return self.INPUT.pop()

    def read(self):
        return sys.stdin.read()
    
    def write(self, message, isError = 0):
        if isError:
            print(message, file=sys.stderr, end="")
        else:
            # print(message, end="") # TODO: replace the line below by this
            print(message)