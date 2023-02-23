from sys import argv
from re import sub
class ArgParser:
    def __init__(self):
        self.source = None
        self.input = None
        if (len(argv) < 2):
            exit(10) # missing arg - error 10
        for arg in argv:
            parts = arg.split("=")
            if (parts[0] in ["--help", "-h"]):
                if (len(argv) > 2):
                    exit(10) # invalid arg combination - error 10
                    pass
                else:
                    print("Usage: python3.10 interpret.py [--source=SOURCE_FILE] [--input=INPUT_FILE]")
                    print("    -h, --help\tprints this help message")
                    print("    --source=SOURCE_FILE\tspecifies source file")
                    print("    --input=INPUT_FILE\tspecifies input file")
                    print("At least SOURCE_FILE or INPUT_FILE has to be given, the other is loaded from STDIN if not specified.")
            elif (parts[0] == "--source"):
                self.source = sub("\"", "", parts[1])
            elif (parts[0] == "--input"):
                self.input = sub("\"", "", parts[1])