from lexical_analysis.const import BOOL
from .commands import (
    AssignmentCommand, ConditionCommand, commands
)
from .temp_var import TempVar


class NotOperationHandler(object):
    @classmethod
    def handle(cls, identifier_name: str):
        temp_var = TempVar(type_=BOOL)
        cls.__generate_commands(temp_var.name, identifier_name)
        return temp_var

    @classmethod
    def __generate_commands(cls, temp_var_name, identifier_name):
        AssignmentCommand.create(temp_var_name, 'True')
        cond_command = ConditionCommand.create(cond=identifier_name, goto_command_ind=len(commands) + 2)
        AssignmentCommand.create(temp_var_name, 'False')
