from models.Serializable import Serializable

class Tag(Serializable):
    """
    Identify a course by its tag
    """
    
    def __init__(self, subject: str, number: str) -> None:
        self.subject: str = subject
        self.number: str = number
    
    def get_subject(self) -> str:
        """
        Get the subject of the tag
        :rtype: str
        """

        return self.subject
    
    def get_number(self) -> str:
        """
        Get the number of the tag
        :rtype: str
        """

        return self.number

    def __hash__(self) -> int:
        return hash((self.subject, self.number))

    def __eq__(self, value: object) -> bool:
        if isinstance(self, value.__class__):
            return self.subject == value.subject and self.number == value.number
        return False