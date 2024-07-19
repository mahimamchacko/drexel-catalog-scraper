import re
from models.Course import Course
from models.NestType import NestType
from models.Requisite import Requisite
from models.Tag import Tag

SPACE: str =  " "
EMPTY: str = ""
OPERATIONS: list = [" and ", " or "]

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

def build_requisite(requisite: str) -> Requisite:
    """
    Build a requisite
    :param requisite: Requisite
    :type requisite: str
    :rtype: Requisite
    """
    
    tree = None
    
    # clean data
    requisite = re.sub(" \[Min Grade: .{0,2}\]", "", requisite)
    requisite = requisite.replace(" (Can be taken Concurrently)", "")

    # get positions
    positions = []
    stack = []
    for index in range(len(requisite)):
        if requisite[index] == "(":
            if len(stack) > 0 and stack[-1][1] == NestType.Open:
                positions.append((stack.pop()[0], index))
            stack.append((index + 1, NestType.Close))
        elif requisite[index] == ")":
            if len(stack) == 1:
                positions.append((stack.pop()[0], index))
            else:
                stack.pop()
        elif len(stack) == 0:
            stack.append((index, NestType.Open))
    if len(stack) > 0 and stack[-1][1] == NestType.Open:
        positions.append((stack.pop()[0], len(requisite)))
    
    # build tree
    if len(positions) == 1: # no nesting
        operation = list(filter(lambda operation: operation in requisite, OPERATIONS))
        if len(operation) > 0: # multiple courses
            if len(operation) == 2: # two operations
                if requisite.startswith(operation[0]) and requisite.endswith(operation[1]) or requisite.startswith(operation[1]) and requisite.endswith(operation[0]):
                    operation = operation[1]
                elif requisite.startswith(SPACE):
                    operation = operation[0] if requisite.find(operation[0]) < requisite.find(operation[1]) else operation[1]
                else:
                    operation = operation[0] if requisite.rfind(operation[0]) > requisite.rfind(operation[1]) else operation[1]
                tree = Requisite(__remove_fixes(operation, SPACE, SPACE))

                # build tree
                tags = requisite.split(operation)
                for tag in filter(lambda tag: tag is not EMPTY, tags):
                    tag = build_requisite(tag)
                    tree.add_tag(tag)
            else: # one operation
                operation = operation[0]
                tree = Requisite(__remove_fixes(operation, SPACE, SPACE))
                
                # build tree
                tags = requisite.split(operation)
                for tag in filter(lambda tag: tag is not EMPTY, tags):
                    tag = tag.split()
                    tree.add_tag(build_tag(tag[0], tag[1]))
                
            # clean tree
            if len(tree.get_tags()) == 1:
                tree = tree.get_tags()[0]

            # create tuple with tree and operation if requisite is asymmetrical
            if EMPTY in tags:
                tree = (tree, operation)
        else: # one course
            tags = requisite.split()
            tree = build_tag(tags[0], tags[1])
    else: # yes nesting
        # build sub-requisites
        subrequisites = []
        for position in positions:
            subrequisites.append(requisite[position[0]:position[1]])
        
        operation = list(filter(lambda operation: operation in subrequisites, OPERATIONS))
        if len(operation) > 0: # even nesting
            operation = operation[0]
            tree = Requisite(__remove_fixes(operation, SPACE, SPACE))
            subrequisites = filter(lambda subrequisite: subrequisite != operation, subrequisites)
        
        # get subtrees
        subtrees = []
        for subrequisite in subrequisites:
            subtree = build_requisite(subrequisite)
            if type(subtree) is tuple:
                tree = Requisite(__remove_fixes(subtree[1], SPACE, SPACE))
                subtree = subtree[0]
                if type(subtree) is tuple:
                    if subrequisite.startswith(subtree[1]):
                        tag = subtree[0]
                        subtree = Requisite(__remove_fixes(subtree[1], SPACE, SPACE))
                        subtree.add_tag(subtrees.pop())
                        subtree.add_tag(tag)
            if len(subtrees) > 0 and type(subtrees[-1]) is tuple:
                tag1, operation = subtrees.pop()
                tag2 = subtree
                subtree = Requisite(__remove_fixes(operation, SPACE, SPACE))
                subtree.add_tag(tag1)
                subtree.add_tag(tag2)  
            subtrees.append(subtree)
            
        # build tree
        for subtree in subtrees:
            if type(subtree) is Requisite and subtree.get_operation() == tree.get_operation():
                for tag in subtree.get_tags():
                    tree.add_tag(tag)
            else:
                tree.add_tag(subtree)
                
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