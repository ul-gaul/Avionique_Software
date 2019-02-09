class AnyString:
    def __eq__(self, other):
        return True if type(other) is str else False

    def __repr__(self):
        return "Any str"
