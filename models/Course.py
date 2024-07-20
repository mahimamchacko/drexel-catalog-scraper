from models.Requisite import Requisite
from models.Serializable import Serializable
from models.Tag import Tag

class Course(Serializable):
    """
    Identify a course
    """

    def __init__(self, tag: Tag, title: str, credits: str, description: str, prerequisites: Requisite, corequisites: Requisite) -> None:
        self.tag: Tag = tag
        self.title: str = title
        self.credits: str = credits
        self.description: str = description
        self.prerequisites: Requisite = prerequisites
        self.corequisites: Requisite = corequisites
    
    def get_key(self) -> str:
        """
        Get the key of the course
        :rtype: str
        """

        return f"{self.tag.get_subject()},{self.tag.get_number()}"

    @staticmethod
    def get_json_key(json) -> str:
        """
        Get the key of the JSON format of the course
        :param json: JSON
        :rtype: str
        """
        
        return f"{json['tag']['subject']},{json['tag']['number']}"

    @staticmethod
    def get_dict_key(dictionary: dict) -> str:
        """
        Get the key of dictionary format of the course
        :param dictionary: Dictionary
        :type dictionary: dict
        :rtype: str
        """

        return { "tag" : dictionary["tag"] }

    @staticmethod
    def equals(dict1: dict, dict2: dict) -> bool:
        """
        Get the equality of two dictionaries with contents relationg to courses
        :param dict1: Dictionary
        :type dict1: dict
        :param dict2: Dictionary
        :type dict2: dict
        :rtype: bool
        """
        
        return dict1["tag"] == dict2["tag"] and dict1["title"] == dict2["title"] and dict1["credits"] == dict2["credits"] and dict1["description"] == dict2["description"] and dict1["prerequisites"] == dict2["prerequisites"] and dict1["corequisites"] == dict2["corequisites"]