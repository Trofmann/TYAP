from typing import List
from tokens import Token, ASSIGNMENT_TOKEN, IdentifierToken, POINT_TOKEN
from .custom_exceptions import WrongTokenError, AssignmentExpectedError, UnknownFieldError, WrongExpressionError

__all__ = [
    'ExpressionAnalyzer',
]


class ExpressionAnalyzer(object):
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.analyze()

    def analyze(self):
        if self.tokens.count(ASSIGNMENT_TOKEN) != 1:
            # Значительно упростит дальнейший анализ
            raise AssignmentExpectedError()
        if self.tokens[-1] == ASSIGNMENT_TOKEN:
            # Гарантируем наличие правой части выражения
            raise WrongExpressionError()
        identifier_type, identifier_full_name = self.analyze_left_part()

    def analyze_left_part(self):
        """Анализ левой части выражения"""
        # Индекс присвоения. Всё, что слева - или идентификаторы, или точка
        assignment_index = self.tokens.index(ASSIGNMENT_TOKEN)
        # Конечный идентификатор
        identifier = None
        full_name = ''
        for ind in range(assignment_index):
            token = self.tokens[ind]
            if isinstance(token, IdentifierToken):
                # Встретили идентификатор
                # Следующий токен или присвоение, или точка
                next_token = self.tokens[ind + 1]
                if next_token in [POINT_TOKEN, ASSIGNMENT_TOKEN]:
                    # Всё хорошо
                    if identifier is None:
                        # Ещё не было идентификатора. Значит запомним этот
                        identifier = token
                        full_name += identifier.attr_name
                    else:
                        # Уже был. Значит в его полях ищем идентификатор с там же именем
                        found = False
                        for field in identifier.fields:
                            if field.attr_name == token.attr_name:
                                identifier = field
                                full_name = full_name + '.' + token.attr_name
                                found = True
                        if not found:
                            # Не нашли, а должны были
                            raise UnknownFieldError()

                else:
                    raise WrongTokenError()
            elif token == POINT_TOKEN:
                # Встретили точку, а значит следующий - только идентификатор
                next_token = self.tokens[ind + 1]
                if isinstance(next_token, IdentifierToken):
                    # Всё хорошо
                    pass
                else:
                    raise WrongTokenError()
        # Вернём тип идентификатора и его полное имя
        return identifier.type, full_name
