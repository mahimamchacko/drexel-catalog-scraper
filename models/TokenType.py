from enum import Enum

class TokenType(Enum):
    """
    Define the types of tokens
    """

    Course = 1
    OpenParenthesis = 2
    CloseParenthesis = 3
    OrOperation = 4
    AndOperation = 5