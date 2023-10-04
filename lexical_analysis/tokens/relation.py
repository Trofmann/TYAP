from lexical_analysis.tokens.token import Token


__all__ = [
    'EQUAL_TOKEN',
    'NOT_EQUAL_TOKEN',
    'MORE_TOKEN',
    'MORE_EQUAL_TOKEN',
    'LESS_TOKEN',
    'LESS_EQUAL_TOKEN',
]


EQUAL_TOKEN = Token(name='rel', code=23, value=0)
NOT_EQUAL_TOKEN = Token(name='rel', code=23, value=1)
MORE_TOKEN = Token(name='rel', code=23, value=2)
MORE_EQUAL_TOKEN = Token(name='rel', code=23, value=3)
LESS_TOKEN = Token(name='rel', code=23, value=4)
LESS_EQUAL_TOKEN = Token(name='rel', code=23, value=5)
