class StackManager:
    stack = []

    def __init__(self):
        pass

    @staticmethod
    def push(symb):
        __class__.stack.append(symb)

    @staticmethod
    def pop():
        return __class__.stack.pop()