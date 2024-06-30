from models.Serializable import Serializable
from models.Tag import Tag

class Requisite(Serializable):
    """
    Identify a requisite by its operation and tags
    """

    def __init__(self, operation: str) -> None:
        self.tags: list[Tag] = []
        self.operation: str = operation
    
    def get_tags(self) -> list[Tag]:
        """
        Get the tags in the requisite
        :rtype: list
        """
        
        return self.tags

    def add_tag(self, tag: Tag):
        """
        Add a tag to the requisite
        :param tag: Tag to add to the requisite
        :type tag: Tag
        """

        self.tags.append(tag)