from models.Course import Course
from models.Requisite import Requisite
from models.RequisiteType import RequisiteType
from models.Tag import Tag

SPACE: str =  " "
OPERATIONS: list = ["and", "or"]

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

def build_requisite(type: RequisiteType, requisites: str) -> Requisite:
    """
    Build a requisite
    :param type: Type of requisite
    :type type: RequisiteType
    :param requisites: Requisites
    :type requisites: str
    :rtype: Requisite
    """
    
    tree = None
    
    operations = list(filter(lambda operation: __add_fixes(operation, SPACE, SPACE) in requisites, OPERATIONS))
    if len(operations) > 0:
        operation = operations[0]
        tree = Requisite(operation)
        
        requisites = __remove_fixes(requisites, "(", ")")
        for requisite in requisites.split(__add_fixes(operation, SPACE, SPACE)):
            value = build_requisite(type, requisite)
            if value:
                tree.add_tag(value)
        
        if len(tree.get_tags()) == 1:
            tree = tree.get_tags()[0]
    else:
        items = requisites.split(" ", 2)
        if (type == RequisiteType.Prerequisite and len(items) == 3) or (type == RequisiteType.Corequisite):
            tree = build_tag(items[0], items[1])
    
    return tree

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

def __add_fixes(string: str, prefix: str, suffix: str) -> str:
    """
    Add prefix and suffix to a string
    :param string: String to change
    :type string: str
    :param prefix: Prefix to add
    :type prefix: str
    :param suffix: Suffix to add
    :type suffix: str
    :return: String with prefix and suffix
    :rtype: str
    """

    return prefix + string + suffix

def __remove_fixes(string: str, prefix: str, suffix: str) -> str:
    """
    Remove prefix and suffix from a string
    :param string: String to change
    :type string: str
    :param prefix: Prefix to remove
    :type prefix: str
    :param suffix: Suffix to remove
    :type suffix: str
    :return: String without prefix and suffix
    :rtype: str
    """

    return string.removeprefix(prefix).removesuffix(suffix)