from models.TokenType import TokenType

class Token:
    """
    Identify a part of the requisite
    """

    def __init__(self, text: str, type: TokenType) -> None:
        self.text = text
        self.type = type
    
    def __eq__(self, value: object) -> bool:
        if isinstance(self, value.__class__):
            return self.text == value.text and self.type == value.type
        return False