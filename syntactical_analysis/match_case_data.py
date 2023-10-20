from typing import List

from syntactical_analysis.custom_exceptions import TooManyDefaultCases
from syntactical_analysis.expression_analyzer import ExpressionAnalyzer


class MatchCaseData(object):
    def __init__(self):
        self.target_tokens = []
        self.cases = []  # type: List[CaseData]

    def check_cases(self):
        if len(list(filter(lambda c: c.const_token is None, self.cases))) > 1:
            raise TooManyDefaultCases()

    def analyze(self):
        self.check_cases()
        pass


class CaseData(object):
    def __init__(self):
        self.const_token = None
        self.expression_tokens = []
