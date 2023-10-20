from typing import List

from syntactical_analysis.custom_exceptions import TooManyDefaultCasesError, DefaultCaseWrongLocationError
from syntactical_analysis.expression_analyzer import ExpressionAnalyzer
from syntactical_analysis.utils import parse_identifiers


class MatchCaseData(object):
    def __init__(self):
        self.target_tokens = []
        self.cases = []  # type: List[CaseData]

    def check_cases(self):
        found = False
        cases_count = len(self.cases)
        for ind, case in enumerate(self.cases):
            if case.const_token is None:
                if found:
                    raise TooManyDefaultCasesError()
                if ind == cases_count - 1:
                    raise DefaultCaseWrongLocationError()
                found = True

    def analyze(self):
        self.check_cases()
        target = parse_identifiers(self.target_tokens)

        for case in self.cases:
            pass


class CaseData(object):
    def __init__(self):
        self.const_token = None
        self.expression_tokens = []
