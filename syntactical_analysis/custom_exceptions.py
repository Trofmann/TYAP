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


class AssignmentExpectedError(BaseAnalyzerException):
    msg = 'Ожидался ровно 1 знак присвоения'


class UnknownFieldError(BaseAnalyzerException):
    msg = 'Неизвестное поле'


class UnknownVarError(BaseAnalyzerException):
    msg = 'Неизвестная переменная'


class WrongExpressionError(BaseAnalyzerException):
    msg = 'Неверное выражение'


class TypeIncompatibilityError(BaseAnalyzerException):
    msg = 'Типы не совместимы'


class WrongTypeForOperator(BaseAnalyzerException):
    msg = 'Неверный тип для операции'


class RelationCountError(BaseAnalyzerException):
    msg = 'Допустимо не более 1 операции сравнения'


class IdentifierExpectedError(BaseAnalyzerException):
    msg = 'Ожидался идентификатор'


class CaseExpectedError(BaseAnalyzerException):
    msg = 'Ожидался case'


class DigitalConstExpectedError(BaseAnalyzerException):
    msg = 'Ожидалась числовая константа'


class ColonExpectedError(BaseAnalyzerException):
    msg = 'Ожидалось двоеточие'


class TooManyDefaultCasesError(BaseAnalyzerException):
    msg = 'Превышено количество операторов по умолчанию'


class DefaultCaseWrongLocationError(BaseAnalyzerException):
    msg = 'Оператор по умолчанию должен быть последним'
