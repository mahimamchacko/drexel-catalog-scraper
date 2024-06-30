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