temp_vars_count = 0


class TempVar(object):
    def __init__(self, type_):
        global temp_vars_count
        self.type = type_
        self.code = temp_vars_count + 1
        temp_vars_count += 1

    def __str__(self):
        return self.name

    @property
    def name(self):
        return f'${self.code}'
