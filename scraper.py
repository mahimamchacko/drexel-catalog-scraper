import config
from builders import ModelBuilder
from helpers.RequestHelper import RequestHelper
from models.RequisiteType import RequisiteType

LEVEL = "grad"
PREREQUISITE = "Prerequisite"
COREQUISITE = "Corequisite"

def get_levels(request_helper: RequestHelper, extension: str) -> list:
    """
    Get the levels of subjects
    :param request_helper: Help make the request
    :type request_helper: RequestHelper
    :param extension: Extension to get the levels from
    :type extension: str
    :rtype: list
    """
    
    soup = request_helper.get_soup(config.CATALOG_LINK + extension)
    return list(filter(lambda extension: LEVEL in extension, [extension["href"] for extension in soup.find("div", { "class": "sitemap" }).find_all("a", { "class": "sitemaplink" })]))

def get_subjects(request_helper: RequestHelper, extension: str) -> set:
    """
    Get the subjects
    :param request_helper: Help make the request
    :type request_helper: RequestHelper
    :param extension: Extension to get the subjects from
    :type extension: str
    :rtype: list
    """
    
    soup = request_helper.get_soup(config.CATALOG_LINK + extension)
    return set([ext["href"] for ext in soup.find_all("a", href=lambda href: href and href.startswith(extension))])

def get_courses(request_helper: RequestHelper, extension: str) -> list:
    """
    Get the courses
    :param request_helper: Help make the request
    :type request_helper: RequestHelper
    :param extension: Extension to get the courses from
    :type extension: str
    :rtype: list
    """
    
    soup = request_helper.get_soup(config.CATALOG_LINK + extension)
    courses = []
    for course in soup.find_all("div", { "class": "courseblock" }):
        header = course.find("p", { "class": "courseblocktitle" }).contents[0].contents
        label = header[0].text.strip().split("\xa0")
        subject = label[0]
        number = label[1].removesuffix(" [WI]")
        title = header[1].text.strip()
        credits = header[2].strip()
        
        description = course.find("p", { "class": "courseblockdesc" }).text.strip()

        prereqs_parent = course.find("b", text=lambda text: text.startswith(PREREQUISITE))
        prerequisites = ModelBuilder.build_requisite(RequisiteType.Prerequisite, str(prereqs_parent.find_next_sibling(text=True)).strip()) if prereqs_parent is not None else None

        coreqs_parent = course.find("b", text=lambda text: text.startswith(COREQUISITE))
        corequisites = ModelBuilder.build_requisite(RequisiteType.Corequisite, str(coreqs_parent.find_next_sibling(text=True)).strip().removeprefix(": ")) if coreqs_parent is not None else None

        courses.append(ModelBuilder.build_course(subject, number, title, credits, description, prerequisites, corequisites))
    return courses