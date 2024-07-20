import config
from helpers.CollectionHelper import CollectionHelper
from helpers.RequestHelper import RequestHelper
from Scraper import get_levels, get_subjects, get_courses

if __name__ == "__main__":
    request_helper = RequestHelper()
    collection_helper = CollectionHelper(config.MONGODB_DATABASE_NAME, config.MONGODB_COLLECTION_NAME)

    courses = []
    for subject in get_subjects(request_helper, config.QUARTER_UNDERGRAD_EXTENSION):
        courses.extend(get_courses(request_helper, subject))

    collection_helper.publish(courses)