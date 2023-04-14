from sys import stdin, stdout, stderr
import re
import ArgParser

class IOManager:
    __instance = None

    def __new__(cls):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.INPUT = None
        AP = ArgParser()
        if AP.input:
            self.INPUT = open(AP.input, "r")

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
        return stdin.read()
    
    def write(self, message, isError = False):
        out_file = stdout
        
        if isError:
            out_file = stderr
        else:
            if isinstance(message, str): # parse escape sequences
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

        print(message, file=out_file, end="")
