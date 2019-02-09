class AnyString:
    def __eq__(self, other):
        return True if type(other) is str else False

    def __repr__(self):
        return "Any str"


class AnyStringWith:
    def __init__(self, *args):
        self.sub_strings = args

    def __eq__(self, other):
        for sub_string in self.sub_strings:
            if sub_string not in other:
                return False
        return True

    def __repr__(self):
        return "Any str with " + str(self.sub_strings)
