from typing import List
from tokens import Token

__all__ = [
    'ExpressionAnalyzer',
]


class ExpressionAnalyzer(object):
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.check()

    def check(self):
        """Проверка правильности выражения"""
        pass
