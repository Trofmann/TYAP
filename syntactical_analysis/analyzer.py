from copy import deepcopy
from typing import List

from tokens import (
    Token, IdentifierToken, DigitalConstToken,
    CLASS_TOKEN, COLON_TOKEN, NL_TOKEN, TAB_TOKEN, START_PROG_TOKEN, END_PROG_TOKEN,
    BLOCK_VAR_DEF_TOKEN, ENDBLOCK_VAR_DEF_TOKEN, MATCH_TOKEN, CASE_TOKEN, POINT_TOKEN,
    INT_TOKEN, FLOAT_TOKEN, BOOL_TOKEN, UNDERSCORE_TOKEN,
    PLUS_TOKEN, MINUS_TOKEN, DIV_TOKEN, MULT_TOKEN, AND_TOKEN, OR_TOKEN, NOT_TOKEN,
    EQUAL_TOKEN, NOT_EQUAL_TOKEN, LESS_TOKEN, MORE_TOKEN, LESS_EQUAL_TOKEN, MORE_EQUAL_TOKEN,
    ASSIGNMENT_TOKEN,
    TRUE_TOKEN, FALSE_TOKEN,
)
from .custom_exceptions import (
    IdentifierRedeclarationException, TabExpectedException, NewLineExpectedException, TypeNameExpectedException,
    StartProgExpectedError, EndProgExpectedError, BlockVarDefExpectedError, EndBlockVarDefExpectedError,
    VarNameExpectedError, AnalysisException, FieldRedeclarationError, WrongTokenError, IdentifierExpectedError,
    CaseExpectedError, DigitalConstExpectedError, ColonExpectedError
)
from .expression_analyzer import ExpressionAnalyzer
from .commands import commands, fix_commands
from .match_case_data import MatchCaseData, CaseData


class SyntacticalAnalyzer(object):
    """Синтаксический анализатор"""

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens

    def write(self, filename='syntactical_analysis_result.txt'):
        with open(filename, 'w') as f:
            f.write('\n'.join(map(str, commands)))

    @staticmethod
    def _add_identifier_category(token: IdentifierToken, category, type_token=None):
        """Установка категории идентификатора"""
        if token.category is not None:
            raise IdentifierRedeclarationException()
        token.category = category
        if type_token:
            token.type = type_token.attr_name

        if category == IdentifierToken.CATEGORY_VAR:
            # Объявляем переменную
            if type_token not in [INT_TOKEN, FLOAT_TOKEN, BOOL_TOKEN]:
                # Значит имеем дело с классом.
                # Скопируем поля
                token.fields = deepcopy(type_token.fields)
                print()

    def _clean_nl_tokens(self):
        """Очистка перевода строк"""
        while len(self.tokens) and self.tokens[0] == NL_TOKEN:
            self.tokens.pop(0)

    def analyze(self):
        if self.tokens[0] != START_PROG_TOKEN:
            # Программа должна начинаться с start_prog
            raise StartProgExpectedError()
        if self.tokens[-1] != END_PROG_TOKEN:
            # И заканчиваться на end_prog
            raise EndProgExpectedError()

        # Удалим start_prog и end_prog. Они нам больше не нужны
        self.tokens.pop(0)  # Удаляем start_prog
        self.tokens.pop(-1)  # Удаляем end_prog

        # Если дошли сюда, значит ожидаем встретить перевод строки и блок объявления переменных
        self._clean_nl_tokens()  # Очистим от перевода строк

        # region Объявление переменных
        # Ожидаем начало блока объявления переменных
        if self.tokens[0] != BLOCK_VAR_DEF_TOKEN:
            raise BlockVarDefExpectedError()

        # Ожидаем, что в программе есть окончание блока объявления переменных
        if ENDBLOCK_VAR_DEF_TOKEN not in self.tokens:
            raise EndBlockVarDefExpectedError()

        # Дошли до сюда, значит есть блок описания идентификаторов
        self.tokens.pop(0)  # Удалим block_var_def
        self._clean_nl_tokens()
        self.tokens.insert(0, NL_TOKEN)  # Хак для удобства
        endblock_var_def_index = self._var_definition()
        self.tokens = self.tokens[endblock_var_def_index + 1::]

        # Очистим таблицу идентификатором от идентификаторов без категории.
        # Такие могли появиться из-за того, что поля класса вносились в таблицу идентификаторов
        # global identifiers_table
        # identifiers_table = list(filter(lambda x: x.category is not None, identifiers_table))
        # endregion

        self._clean_nl_tokens()

        current_token_index = 0
        tokens_count = len(self.tokens)  # Количество оставшихся токенов
        while True:
            if current_token_index == len(self.tokens):
                # Дошли до конца
                break
            # Пока оставим while True, надо что-то придумать
            token = self.tokens[current_token_index]
            if token == NL_TOKEN:
                # Перевод строки. Пропустим
                current_token_index += 1
            elif isinstance(token, IdentifierToken):
                # Встретили идентификатор, а значит дальше будет выражение
                # current_token_index += 1
                expression_tokens = [token]
                while True:
                    # Начнём собирать токены для выражения до переноса строки
                    # Нам могут встретиться: идентификаторы, числовые константы, операторы,
                    # ключевые слова True Или False, знак присвоения
                    current_token_index += 1

                    if current_token_index == tokens_count:
                        # Дошли до конца файла. Выйдем
                        break
                    token = self.tokens[current_token_index]

                    if token == NL_TOKEN:
                        # Дошли до конца строки. Выйдем
                        break

                    identifier_cond = isinstance(token, IdentifierToken)
                    digital_const_cond = isinstance(token, DigitalConstToken)
                    operator_cond = token in [
                        PLUS_TOKEN, MINUS_TOKEN, DIV_TOKEN, MULT_TOKEN, AND_TOKEN, OR_TOKEN, NOT_TOKEN,
                        EQUAL_TOKEN, NOT_EQUAL_TOKEN, LESS_TOKEN, MORE_TOKEN, LESS_EQUAL_TOKEN, MORE_EQUAL_TOKEN
                    ]
                    true_false_cond = token in [TRUE_TOKEN, FALSE_TOKEN]
                    assignment_token = (token == ASSIGNMENT_TOKEN)
                    point_cond = (token == POINT_TOKEN)
                    cond = any([
                        identifier_cond, digital_const_cond, operator_cond, true_false_cond,
                        assignment_token, point_cond
                    ])

                    # Пока просто проверим, что нам придут правильные токены. Все остальные проверки позже
                    if cond:
                        # Удовлетворяет хотя бы одному условию, добавим
                        expression_tokens.append(token)
                    else:
                        raise WrongTokenError()

                # Собрали токены выражения. Надо обработать
                expression_analyzer = ExpressionAnalyzer(tokens=expression_tokens)
            elif token == MATCH_TOKEN:
                match_case_data = MatchCaseData()
                next_token = self.tokens[current_token_index + 1]
                if not isinstance(next_token, IdentifierToken):
                    # После match может идти только идентификатор
                    raise IdentifierExpectedError()
                target_identifier_tokens = []
                while True:
                    # Ищем новую строку
                    current_token_index += 1
                    current_token = self.tokens[current_token_index]
                    if current_token == NL_TOKEN:
                        prev_token = self.tokens[current_token_index - 1]
                        if prev_token != COLON_TOKEN:
                            raise WrongTokenError()
                        # Нашли, завершим
                        break
                    if current_token == COLON_TOKEN:
                        prev_token = self.tokens[current_token_index - 1]
                        if not isinstance(prev_token, IdentifierToken):
                            raise IdentifierExpectedError()

                    if isinstance(current_token, IdentifierToken):
                        # Текущий токен идентификатор. А значит предыдущий либо точка, либо match
                        prev_token = self.tokens[current_token_index - 1]
                        if prev_token not in [MATCH_TOKEN, POINT_TOKEN]:
                            raise WrongTokenError()
                        # А следующий - либо двоеточие, либо точка
                        next_token = self.tokens[current_token_index + 1]
                        if next_token not in [COLON_TOKEN, POINT_TOKEN]:
                            raise WrongTokenError()
                        target_identifier_tokens.append(current_token)
                    elif current_token == POINT_TOKEN:
                        # Текущий токен точка, а значит и следующий, предыдущий - идентификаторы
                        prev_token = self.tokens[current_token_index - 1]
                        next_token = self.tokens[current_token_index + 1]
                        if not (isinstance(prev_token, IdentifierToken) and isinstance(next_token, IdentifierToken)):
                            raise IdentifierExpectedError()
                        target_identifier_tokens.append(current_token)

                if not target_identifier_tokens:
                    raise WrongTokenError()
                match_case_data.target_tokens = target_identifier_tokens

                case_data = None

                while True:
                    case_data = CaseData() if case_data is None else case_data
                    current_token_index += 1
                    if current_token_index == len(self.tokens):
                        break
                    token = self.tokens[current_token_index]

                    prev_token = self.tokens[current_token_index - 1]
                    next_token = self.tokens[current_token_index + 1]

                    if token == TAB_TOKEN:
                        # Встретили таблуляцию
                        if prev_token == TAB_TOKEN:
                            # Это второй таб
                            if not isinstance(next_token, IdentifierToken):
                                raise WrongTokenError()
                            current_token_index += 1
                            token = self.tokens[current_token_index]

                            expression_tokens = [token]
                            while True:
                                # Надо проанализировать выражение
                                current_token_index += 1
                                if current_token_index == tokens_count:
                                    # Дошли до конца файла. Выйдем
                                    break
                                token = self.tokens[current_token_index]

                                if token == NL_TOKEN:
                                    # Дошли до конца строки. Выйдем
                                    break

                                identifier_cond = isinstance(token, IdentifierToken)
                                digital_const_cond = isinstance(token, DigitalConstToken)
                                operator_cond = token in [
                                    PLUS_TOKEN, MINUS_TOKEN, DIV_TOKEN, MULT_TOKEN, AND_TOKEN, OR_TOKEN, NOT_TOKEN,
                                    EQUAL_TOKEN, NOT_EQUAL_TOKEN, LESS_TOKEN, MORE_TOKEN, LESS_EQUAL_TOKEN,
                                    MORE_EQUAL_TOKEN
                                ]
                                true_false_cond = token in [TRUE_TOKEN, FALSE_TOKEN]
                                assignment_token = (token == ASSIGNMENT_TOKEN)
                                point_cond = (token == POINT_TOKEN)
                                cond = any([
                                    identifier_cond, digital_const_cond, operator_cond, true_false_cond,
                                    assignment_token, point_cond
                                ])

                                # Пока просто проверим, что нам придут правильные токены. Все остальные проверки позже
                                if cond:
                                    # Удовлетворяет хотя бы одному условию, добавим
                                    expression_tokens.append(token)
                                else:
                                    raise WrongTokenError()
                            case_data.expression_tokens = expression_tokens
                            # Добавим в список кейсов
                            match_case_data.cases.append(case_data)
                            # Можно сбросить
                            case_data = None
                        elif prev_token == NL_TOKEN:
                            # Это первый таб
                            if next_token not in [CASE_TOKEN, TAB_TOKEN]:
                                raise WrongTokenError()
                        else:
                            raise WrongTokenError()

                    elif token == CASE_TOKEN:
                        # Встретили case
                        if not (isinstance(next_token, DigitalConstToken) or next_token == UNDERSCORE_TOKEN):
                            raise WrongTokenError()
                    elif isinstance(token, DigitalConstToken) or token == UNDERSCORE_TOKEN:
                        if prev_token != CASE_TOKEN:
                            raise CaseExpectedError()
                        if next_token != COLON_TOKEN:
                            raise ColonExpectedError()
                        if token != UNDERSCORE_TOKEN:
                            case_data.const_token = token
                    elif token == COLON_TOKEN:
                        if not (isinstance(prev_token, DigitalConstToken) or prev_token == UNDERSCORE_TOKEN):
                            raise WrongTokenError()
                        if next_token != NL_TOKEN:
                            raise TabExpectedException()
                    elif token == NL_TOKEN:
                        if next_token != TAB_TOKEN or current_token_index == len(self.tokens):
                            # Конец match case
                            break
                    else:
                        raise AnalysisException()
                match_case_data.analyze()
            else:
                raise AnalysisException()
        fix_commands()

    def _var_definition(self):
        """Разбор блока описания переменных"""
        endblock_var_def_index = None  # Индекс токена окончания блока описания переменных (endblock_var_def)

        # Флаг, показывающий, что находимся в состоянии объявления класса
        in_class_declaration_state = False
        # Токен, являющийся новым классом
        new_class_token = None
        for index, token in enumerate(self.tokens):
            if not in_class_declaration_state:
                # НЕ Находимся объявления класса. Значит ожидаем увидеть или перевод строки, или идентификатор,
                # или endblock_var_def, или class
                if token == NL_TOKEN:
                    # Пусть вначале идёт перевод строки
                    if index:
                        # Пришёл перевод строки, а значит перед этим должна быть переменная
                        # Перевод строки после имени типа недопустим
                        prev_token = self.tokens[index - 1]
                        if (not isinstance(prev_token, IdentifierToken) or
                                prev_token.category == IdentifierToken.CATEGORY_TYPE):
                            raise VarNameExpectedError()
                        else:
                            # В противном случае всё хорошо. Продолжаем.
                            pass
                elif token == ENDBLOCK_VAR_DEF_TOKEN:
                    prev_token = self.tokens[index - 1]
                    if prev_token != NL_TOKEN:
                        # Перед endblock_var_def должен быть перевод строки
                        raise AnalysisException()
                    else:
                        # Всё хорошо. Вернём индекс
                        return index
                elif token == CLASS_TOKEN:
                    prev_token = self.tokens[index - 1]
                    if prev_token != NL_TOKEN:
                        # Перед class должен быть перевод строки
                        raise AnalysisException()
                    else:
                        # Всё хорошо. Продолжаем
                        pass
                elif isinstance(token, IdentifierToken):
                    # Пришёл идентификатор
                    prev_token = self.tokens[index - 1]
                    if prev_token == NL_TOKEN:
                        # После перевода строки, а значит текущий токен обязательно должен быть именем типа
                        if token.category != IdentifierToken.CATEGORY_TYPE:
                            raise TypeNameExpectedException()
                    elif prev_token == CLASS_TOKEN:
                        # Предыдущий токен - ключевое слово class. Значит здесь объявление типа
                        self._add_identifier_category(token, category=IdentifierToken.CATEGORY_TYPE)
                        # Начинается объявление класса
                        in_class_declaration_state = True
                        new_class_token = token
                    elif isinstance(prev_token,
                                    IdentifierToken) and prev_token.category == IdentifierToken.CATEGORY_TYPE:
                        # Предыдущий токен - тип. Значит здесь объявление переменной типа
                        self._add_identifier_category(
                            token, category=IdentifierToken.CATEGORY_VAR, type_token=prev_token
                        )
                    else:
                        raise AnalysisException()
            elif in_class_declaration_state:
                # Находимся в состоянии объявления класса
                prev_token = self.tokens[index - 1]
                if token == COLON_TOKEN and prev_token == new_class_token:
                    # Двоеточие после имени класса. Всё хорошо
                    pass
                elif token == NL_TOKEN:
                    # Перевод на новую строку.
                    next_token = self.tokens[index + 1]
                    # Если предыдущий токен - двоеточие, то следующий обязательно таб
                    if prev_token == COLON_TOKEN:
                        if next_token != TAB_TOKEN:
                            # Пришёл не таб. Ошибка
                            raise TabExpectedException()
                        else:
                            # Пришёл таб, всё хорошо
                            pass
                    elif next_token == TAB_TOKEN:
                        # Всё хорошо, ничего не делаем
                        pass
                    # Если следующий токен не таб, то выходим из состояния объявления класс
                    elif next_token != TAB_TOKEN:
                        in_class_declaration_state = False
                elif token == TAB_TOKEN:
                    # Табуляция. Должна быть только после перевода на новую строку
                    if prev_token != NL_TOKEN:
                        raise NewLineExpectedException()
                elif isinstance(token, IdentifierToken):
                    # Встретили идентификатор
                    prev_token = self.tokens[index - 1]
                    # Предыдущий токен - таб
                    if prev_token == TAB_TOKEN:
                        next_token = self.tokens[index + 1]
                        # А значит текущий может быть только типом
                        if token.category != IdentifierToken.CATEGORY_TYPE:
                            raise TypeNameExpectedException()
                        # А следующий - переводом идентифкатором
                        if not isinstance(next_token, IdentifierToken):
                            raise VarNameExpectedError()
                    # Предыдущий токен - идентификатор
                    elif isinstance(prev_token, IdentifierToken):
                        # Предыдущее условие гарантирует, предыдущий токен именно имя типа
                        # А значит текущий должен быть переменной, т.е НЕ именем типа
                        if token.category == IdentifierToken.CATEGORY_TYPE:
                            raise VarNameExpectedError()
                        # Попробуем найти в полях типа объявляемого типа
                        found = list(filter(lambda x: x.attr_name == token.attr_name, new_class_token.fields))
                        if found:
                            # Поле повторно объявлять нельзя
                            raise FieldRedeclarationError()
                        else:
                            # Не нашли. Значит можем добавить в поля.
                            # Создадим новый. Этот менять нельзя, чтобы не было пересечений
                            identifier = IdentifierToken(
                                value=len(new_class_token.fields),
                                attr_name=token.attr_name,
                                attr_value=None,
                                type=prev_token.attr_name,
                                category=IdentifierToken.CATEGORY_VAR,
                            )
                            new_class_token.fields.append(identifier)
                        pass
                    else:
                        raise AnalysisException()
                else:
                    raise AnalysisException()
