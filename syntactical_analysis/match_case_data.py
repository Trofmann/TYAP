from typing import List


class MatchCaseData(object):
    def __init__(self):
        self.target_tokens = []
        self.cases = []  # type: List[CaseData]


class CaseData(object):
    def __init__(self):
        self.const_token = None
        self.expression_tokens = []
