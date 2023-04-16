from sys import argv, stderr
from re import sub

class ArgParser:
    __instance = None

    def __new__(cls):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.source = None
        self.input = None

        if (len(argv) < 2):
            stderr.write("> Argparser: missing parameter\n")
            exit(10) # missing parameter or forbidden combination

        for i, arg in enumerate(argv):
            ALLOWED_ARGS = ["--help", "-h", "--source", "--input"]

            if i == 0: # skip first argument (interpret.py)
                continue

            if "=" not in arg:
                # there is no error for incorrect parameter format so the closest one is used
                stderr.write("> Argparser: missing '=' in parameter\n")
                exit(10) # missing parameter or forbidden combination

            name, value = arg.split("=")

            if (name not in ALLOWED_ARGS) or (name in ALLOWED_ARGS[:2] and len(argv) > 2):
                stderr.write("> Argparser: forbidden parameter combination\n")
                exit(10) # missing parameter or forbidden combination

            if (name in ALLOWED_ARGS[:2]):
                print("Usage: python3.10 interpret.py [--source=SOURCE_FILE] [--input=INPUT_FILE]")
                print("    -h, --help\tprints this help message")
                print("    --source=SOURCE_FILE\tspecifies source file")
                print("    --input=INPUT_FILE\tspecifies input file")
                print("At least SOURCE_FILE or INPUT_FILE has to be given, the other is loaded from STDIN if not specified.")
            elif (name == "--source"):
                self.source = sub("\"", "", value)
            elif (name == "--input"):
                self.input = sub("\"", "", value)

    @staticmethod
    def getInstance():
        return __class__.__instance