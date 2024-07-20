import re
from models.OperationType import OperationType
from models.Requisite import Requisite
from models.Token import Token
from models.TokenType import TokenType
from builders.ModelBuilder import build_token, build_tag, build_requisite

def build(requisite: str) -> Requisite:
    """
    Build requisite
    :param requisite: Requisite
    :type requisite: str
    :rtype: Requisite
    """

    return parse(tokenize(requisite))

def tokenize(requisite: str) -> list[Token]:
    """
    Convert requisite into tokens
    :param requisite: Requisite
    :type requisite: str
    :rtype: list[Token]
    """

    # clean data
    requisite = re.sub(" \[Min Grade: .{0,2}\]", "", requisite)
    requisite = requisite.replace(" (Can be taken Concurrently)", "")

    # build tokens
    tokens: list[Token] = []
    index = 0
    while index < len(requisite):
        token_text = requisite[index]
        token_type = None
        if token_text.isalnum():
            while True:
                index += 1
                if index >= len(requisite) or not(requisite[index].isalnum()):
                    break
                token_text += requisite[index]

            if token_text == "and":
                token_type = TokenType.AndOperation
            elif token_text == "or":
                token_type = TokenType.OrOperation
            else:
                token_type = TokenType.Course
                previous_token = tokens[-1] if len(tokens) > 0 else None
                if previous_token is not None and previous_token.type == TokenType.Course:
                    previous_token.text += " " + token_text
                    continue
        else:
            index += 1
            if token_text == "(":
                token_type = TokenType.OpenParenthesis
            elif token_text == ")":
                token_type = TokenType.CloseParenthesis
            else:
                continue
        tokens.append(build_token(token_text, token_type))    
    
    return tokens

def parse(tokens: list[Token]) -> Requisite:
    """
    Parse tokens into a requisite
    :param tokens: Tokens
    :type tokens: list[Token]
    :rtype: Requisite
    """
    
    requisites = []
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token.type == TokenType.Course:
            tag = token.text.split(" ")
            requisites.append(build_tag(tag[0], tag[1]))
        elif token.type == TokenType.AndOperation or token.type == TokenType.OrOperation:
            requisites.append(build_requisite(token.text))
        else:
            subtokens = []
            stack = 1
            while True:
                index += 1
                if index >= len(tokens):
                    break
                token = tokens[index]
                if token.type == TokenType.OpenParenthesis:
                    stack += 1
                elif token.type == TokenType.CloseParenthesis:
                    stack -= 1
                    if stack == 0:
                        break
                subtokens.append(token)
            requisite = parse(subtokens)
            if requisite is not None:
                requisites.append(requisite)
        index += 1
    
    requisites = __condense(requisites, OperationType.And)
    requisites = __condense(requisites, OperationType.Or)
    
    requisite = None
    if len(requisites) == 1:
        requisite = requisites[0]
    elif len(requisites) > 1:
        requisite = requisites[-1]
    return requisite

def __condense(requisites: list[Requisite], operation: OperationType) -> list[Requisite]:
    """
    Condense requisites into a tree
    :param requisites: Requisites
    :type requisites: list[Requisite]
    :param operation: Type of operation
    :type operation: OperationType
    :rtype: list[Requisite]
    """

    index = 1
    while index < len(requisites) - 1:
        requisite = requisites[index]
        if __check_operation(requisite, operation): # if the current object is a requisite of that operation
            previous_requisite = requisites[index - 1]
            if __check_operation(previous_requisite, operation): # if the previous object is a requisite of that operation
                next_requisite = requisites.pop(index + 1)
                if __check_operation(next_requisite, operation): # if the next object is a requisite of that operation
                    for tag in next_requisite.get_tags():
                        previous_requisite.add_tag(tag)
                else: # if the next object is not a requisite of that operation
                    previous_requisite.add_tag(next_requisite)
                
                if len(requisite.get_tags()) == 0: # if the current object is a requisite with no tags
                    requisites.pop(index)
            else: # if the previous object is not a requisite of that operation
                requisite.add_tag(requisites.pop(index + 1))
                requisite.add_tag(requisites.pop(index - 1))
        else: # if the object is not a requisite of that operation
            index += 1
    return requisites

def __check_operation(obj, operation: OperationType) -> bool:
    """
    Check if object is a requisite that matches the operation type
    :param obj: Object to check
    :param operation: Operation
    :type operation: OperationType
    :rtype: bool
    """

    return isinstance(obj, Requisite) and obj.get_operation() == operation.value