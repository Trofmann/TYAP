from typing import List

from .custom_exceptions import TooManyDefaultCasesError, DefaultCaseWrongLocationError
from .expression_analyzer import ExpressionAnalyzer
from .utils import parse_identifiers
from .commands import ConditionCommand, GotoCommand, commands
from .custom_exceptions import TypeIncompatibilityError


class MatchCaseData(object):
    def __init__(self):
        self.target_tokens = []
        self.cases = []  # type: List[CaseData]
        self.has_default = False

    def check_cases(self):
        cases_count = len(self.cases)
        for ind, case in enumerate(self.cases):
            if case.const_token is None:
                if self.has_default:
                    raise TooManyDefaultCasesError()
                if ind != cases_count - 1:
                    raise DefaultCaseWrongLocationError()
                self.has_default = True

    def analyze(self):
        self.check_cases()
        target = parse_identifiers(self.target_tokens)[0]

        cond_commands = []
        goto_commands = []

        for case in self.cases:
            if case.const_token:
                if case.const_token.type != target.type:
                    raise TypeIncompatibilityError()
                # Метку следующей команды поставим позже
                cond_command = ConditionCommand.create(f'{target.name} != {case.const_token.attr}')
                cond_commands.append(cond_command)

            ExpressionAnalyzer(tokens=case.expression_tokens)
            if case.const_token:
                goto_command = GotoCommand.create()
                goto_commands.append(goto_command)

        commands_count = len(commands)
        for cond_command in cond_commands:
            cond_command.goto_command_ind = commands_count

        for goto_command in goto_commands:
            goto_command.next_command_ind = commands_count


class CaseData(object):
    def __init__(self):
        self.const_token = None
        self.expression_tokens = []
