class NameGenerator:

    def __init__(self, prefix, start_index = 1, separator = '-'):
        self.prefix = prefix
        self.index = start_index
        self.separator = separator

    def next_name(self):
        index = self.index
        self.index += 1
        return self.prefix + self.separator + str(index)
