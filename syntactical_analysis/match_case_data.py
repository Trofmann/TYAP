from typing import List

from syntactical_analysis.expression_analyzer import ExpressionAnalyzer


class MatchCaseData(object):
    def __init__(self):
        self.target_tokens = []
        self.cases = []  # type: List[CaseData]

    def analyze(self):
        pass


class CaseData(object):
    def __init__(self):
        self.const_token = None
        self.expression_tokens = []
