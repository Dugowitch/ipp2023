class Frame:
    # všetky premenné tu sú static
    # TODO use dictionary as hashtable to store variables
 
    def __init__(self):
        self.vars = {}

    def save(self, name, value):
        self.vars[name] = value

    @staticmethod
    def has(self, key):
        if key in self.vars:
            return self.vars[key]
        else:
            # TODO: check collision with bool@false
            return False 