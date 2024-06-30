from bs4 import BeautifulSoup
from requests import Session, Response

class RequestHelper():
    """
    Help make requests
    """
    
    def __init__(self) -> None:
        self.session = Session()
    
    def get_soup(self, link: str) -> BeautifulSoup:
        """
        Send a GET request and retrieve the BeautifulSoup
        :param link: Link for the new request
        :type link: str
        :rtype: bs4.BeautifulSoup
        """
        
        page = self.__get(link)
        return BeautifulSoup(page.content, "html.parser", from_encoding="utf-8")
    
    def __get(self, link: str) -> Response:
        """
        Send a GET request
        :param link: Link for the new request
        :type link: str
        :rtype: requests.Response
        """
        
        return self.session.get(link)

    def __del__(self):
        self.session.close()