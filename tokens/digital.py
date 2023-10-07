from lexical_analysis import const
from tokens.token import Token

__all__ = [
    'DigitalConstToken',
    'digital_consts_table',
]


class DigitalConstToken(Token):
    """Токен для числовых констант"""

    def __init__(self, value, attr, type):
        super().__init__(name='num', code=26, value=value)
        # Само числовое значение
        self.attr = attr
        self.type = type

    @classmethod
    def get_or_create(cls, lexeme, type):
        """Находим в таблице числовых констант токен с attr==attr или создаём его"""
        attr = float(lexeme)
        if type == const.INT:
            attr = int(attr)

        found = list(filter(lambda x: x.attr == attr and x.type == type, digital_consts_table))
        if found:
            return found[0]
        token_value = len(digital_consts_table)
        new_token = DigitalConstToken(value=token_value, attr=attr, type=type)
        digital_consts_table.append(new_token)
        return new_token


# Таблица числовых констант
digital_consts_table = []
