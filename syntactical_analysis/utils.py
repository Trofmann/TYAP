from syntactical_analysis.custom_exceptions import UnknownVarError, VarNameExpectedError, UnknownFieldError, \
    AnalysisException, WrongTokenError
from syntactical_analysis.identifier_info import IdentifierInfo
from tokens import IdentifierToken, POINT_TOKEN


def parse_identifiers(tokens):
    result = []
    identifier = None
    full_name = ''
    for ind in range(len(tokens)):
        token = tokens[ind]
        if isinstance(token, IdentifierToken):
            # Встретили идентификатор
            if identifier is None:
                if not token.category:
                    raise UnknownVarError()
                if token.category == IdentifierToken.CATEGORY_TYPE:
                    raise VarNameExpectedError()
                identifier = token
                full_name += identifier.attr_name
            else:
                prev_token = tokens[ind - 1]
                if prev_token == POINT_TOKEN:
                    # Предыдущая точка, всё хорошо
                    found = False
                    for field in identifier.fields:
                        if field.attr_name == token.attr_name:
                            identifier = field
                            full_name = full_name + '.' + token.attr_name
                            found = True
                    if not found:
                        raise UnknownFieldError()
                else:
                    raise AnalysisException()
        elif token == POINT_TOKEN:
            # Встретили точку
            # А значит предыдущий только идентификатор, и следующий идентификатор
            if ind == len(tokens):
                raise AnalysisException()
            next_token = tokens[ind + 1]
            prev_token = tokens[ind - 1]
            if isinstance(next_token, IdentifierToken) and (prev_token, IdentifierToken):
                # Всё хорошо
                pass
            else:
                raise WrongTokenError()
        else:
            # Встретили другой токен.
            if identifier:
                # Если есть идентификатор, сбросим его в result
                identifier_info = IdentifierInfo(full_name=full_name, type=identifier.type)
                result.append(identifier_info)
                identifier = None
                full_name = ''
            result.append(token)
    if identifier:
        identifier_info = IdentifierInfo(full_name=full_name, type=identifier.type)
        result.append(identifier_info)
    return result