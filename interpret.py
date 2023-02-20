import FrameManager
from sys import argv

for arg in argv:
    parts = arg.split("=")
    if (parts[0] == "--help"):
        # TODO: print help
        # TODO: check arg combination
        pass
    elif (parts[0] == "--source"):
        # TODO
        pass
    elif (parts[0] == "--input"):
        # TODO
        pass

FrameManager()
# TODO parse XML
