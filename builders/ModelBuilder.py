from models.Course import Course
from models.Requisite import Requisite
from models.Tag import Tag
from models.Token import Token
from models.TokenType import TokenType

def build_tag(subject: str, number: str) -> Tag:
    """
    Build a tag
    :param subject: Subject
    :type subject: str
    :param number: Number
    :type number: str
    :rtype: Tag
    """
    
    return Tag(subject, number)

def build_requisite(operation: str) -> Requisite:
    """
    Build a requisite
    :param operation: Operation
    :type operation: str
    :rtype: Requisite
    """

    return Requisite(operation)
    

def build_course(subject: str, number: str, title: str, credits: str, description: str, prerequisites: Requisite, corequisites: Requisite) -> Course:
    """
    Build a course
    :param subject: Subject
    :type subject: str
    :param number: Number
    :type number: str
    :param title: Title
    :type title: str
    :param credits: Credits
    :type credits: str
    :param description: Description
    :type description: str
    :param prerequisites: Prerequisites
    :type prerequisites: Requisite
    :param corequisites: Corequisites
    :type corequisites: Requisite
    :rtype: Course
    """

    return Course(build_tag(subject, number), title, credits, description, prerequisites, corequisites)

def build_token(text: str, type: TokenType):
    """
    Build a token
    :param text: Text
    :type text: str
    :param type: Type of token
    :type type: TokenType
    """
    
    return Token(text, type)