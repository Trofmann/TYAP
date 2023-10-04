__all__ = [
    'WrongSymbolException',
]


class WrongSymbolException(Exception):
    def __init__(self, symbol):
        super().__init__(f'Неожиданный символ {symbol}')
