class AssignmentCommand(object):
    def __init__(self, target: str, source: str):
        self.target = target
        self.source = source

    @classmethod
    def create(cls, target: str, source: str):
        command = cls(target=target, source=source)
        commands.append(command)

    def __str__(self):
        return f'{self.target} = {self.source}'


class ConditionCommand(object):
    def __init__(self, cond: str, goto_command_ind: int = None):
        self.cond = cond
        self.goto_command_ind = goto_command_ind

    @classmethod
    def create(cls, cond: str, goto_command_ind: int = None):
        command = cls(cond, goto_command_ind)
        commands.append(command)

    def __str__(self):
        return f'if {self.cond} goto {self.goto_command_ind}'


class GotoCommand(object):
    def __init__(self, next_command_ind: int):
        self.next_command_ind = next_command_ind

    @classmethod
    def create(cls, next_command_ind: int = None):
        command = cls(next_command_ind)
        commands.append(command)

    def __str__(self):
        return f'goto {self.next_command_ind}'


commands = []
