from lexical_analysis.const import BOOL
from .commands import (
    AssignmentCommand, ConditionCommand, GotoCommand, commands
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
        ConditionCommand.create(cond=identifier_name, goto_command_ind=len(commands) + 2)
        AssignmentCommand.create(temp_var_name, 'False')


class AndOperationHandler(object):
    @classmethod
    def handle(cls, left_identifier_name: str, right_identifier_name: str):
        temp_var = TempVar(type_=BOOL)
        cls.__generate_commands(temp_var.name, left_identifier_name, right_identifier_name)
        return temp_var

    @classmethod
    def __generate_commands(cls, temp_var_name: str, left_identifier_name: str, right_identifier_name: str):
        commands_len = len(commands)

        AssignmentCommand.create(temp_var_name, 'True')
        ConditionCommand.create(cond=left_identifier_name, goto_command_ind=commands_len + 4)
        AssignmentCommand.create(temp_var_name, 'False')
        GotoCommand.create(next_command_ind=commands_len + 6)
        ConditionCommand.create(cond=right_identifier_name, goto_command_ind=commands_len + 6)
        AssignmentCommand.create(temp_var_name, 'False')


class OrOperationHandler(object):
    @classmethod
    def handle(cls, left_identifier_name: str, right_identifier_name: str):
        temp_var = TempVar(type_=BOOL)
        cls.__generate_commands(temp_var.name, left_identifier_name, right_identifier_name)
        return temp_var

    @classmethod
    def __generate_commands(cls, temp_var_name: str, left_identifier_name: str, right_identifier_name: str):
        commands_len = len(commands)

        AssignmentCommand.create(temp_var_name, 'True')
        ConditionCommand.create(cond=left_identifier_name, goto_command_ind=commands_len + 4)
        ConditionCommand.create(cond=right_identifier_name, goto_command_ind=commands_len + 4)
        AssignmentCommand.create(temp_var_name, 'False')


class ArithmeticOperationHandler(object):
    @classmethod
    def handle(cls, left_identifier_name: str, right_identifier_name: str, operation: str, type_: str):
        temp_var = TempVar(type_=type_)
        cls.__generate_commands(temp_var.name, left_identifier_name, right_identifier_name, operation)
        return temp_var

    @classmethod
    def __generate_commands(
            cls, temp_var_name: str, left_identifier_name: str, right_identifier_name: str, operation: str
    ):
        source = f'{left_identifier_name} {operation} {right_identifier_name}'
        AssignmentCommand.create(temp_var_name, source)


class RelationOperationHandler(object):
    @classmethod
    def handle(cls, left_identifier_name: str, right_identifier_name: str, operation: str, type_: str):
        temp_var = TempVar(type_=BOOL)
        cls.__generate_commands(temp_var.name, left_identifier_name, right_identifier_name, operation)
        return temp_var

    @classmethod
    def __generate_commands(
            cls, temp_var_name: str, left_identifier_name: str, right_identifier_name: str, operation: str
    ):
        commands_len = len(commands)

        AssignmentCommand.create(temp_var_name, 'True')
        ConditionCommand.create(
            cond=f'{left_identifier_name}{operation}{right_identifier_name}', goto_command_ind=commands_len + 3
        )
        AssignmentCommand.create(temp_var_name, 'False')


class AssignmentHandler(object):
    @classmethod
    def handle(cls, left_identifier_name: str, right_identifier_name: str):
        AssignmentCommand.create(left_identifier_name, right_identifier_name)
