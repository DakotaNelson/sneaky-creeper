class ExfilError(Exception):
    pass


class ExfilChannel(ExfilError):
    def __init__(self, val):
        self.value = val

    def __str__(self):
        return repr(self.value)


class ExfilEncoder(ExfilError):
    def __init__(self, val):
        self.value = val

    def __str__(self):
        return repr(self.value)

