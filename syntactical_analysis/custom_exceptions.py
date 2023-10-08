class BaseAnalyzerException(Exception):
    msg = ''

    def __init__(self):
        super().__init__(self.msg)


class WrongTokenError(Exception):
    msg = 'Неверный токен'


class AnalysisException(BaseAnalyzerException):
    msg = 'Произошла ошибка'


class IdentifierRedeclarationException(BaseAnalyzerException):
    msg = 'Повторное объявление идентификатора'


class FieldRedeclarationError(BaseAnalyzerException):
    msg = 'Повторное объявление поля класса'


class TabExpectedException(BaseAnalyzerException):
    msg = 'Ожидалась табуляция'


class NewLineExpectedException(BaseAnalyzerException):
    msg = 'Ожидался перевод строки'


class TypeNameExpectedException(BaseAnalyzerException):
    msg = 'Ожидалось имя типа'


class VarNameExpectedError(BaseAnalyzerException):
    msg = 'Ожидалось имя переменной'


class StartProgExpectedError(BaseAnalyzerException):
    msg = 'Программа должна начинаться со start_prog'


class EndProgExpectedError(BaseAnalyzerException):
    msg = 'Программа должна заканчиваться end_prog'


class BlockVarDefExpectedError(BaseAnalyzerException):
    msg = 'Ожидалось начало блока объявления идентификаторов'


class EndBlockVarDefExpectedError(BaseAnalyzerException):
    msg = 'Ожидалось окончание блока объявление идентификаторов'
