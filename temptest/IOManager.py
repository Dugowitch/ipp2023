import sys
import re

class IOManager:
    __instance = None

    def __new__(cls, ARGS):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, ARGS):
        self.INPUT = None
        if ARGS.input:
            self.INPUT = open(ARGS.input, "r")

    def __del__(self):
        if self.INPUT:
            self.INPUT.close()

    def readOne(self):
        text = None
        try:
            if self.INPUT:
                text = self.INPUT.readline().strip()
            else:
                text = input()
        except EOFError:
            pass
        if (text == ""):
            text = None
        return text

    def read(self):
        return sys.stdin.read()
    
    def write(self, message, isError = False):
        if isError:
            print(message, file=sys.stderr, end="")
        else:
            if isinstance(message, str):
                matches = re.findall(r"\\[0-9]{3}", message)
                for match in matches:
                    code = re.sub(r"\\0*", "", match)
                    char = chr(int(code))
                    # print(f"> \'{match}\' {type(match)} -> \'{char}\' {type(char)}") # REMOVE
                    message = message.replace(match, char)
            elif message == None:
                message = ""
            elif message == True:
                message = "true"
            elif message == False:
                message = "false"
            # print(message)
            print(message, end="")