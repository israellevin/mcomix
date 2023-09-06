from typing import List

import requests

from .bearerauth import BearerAuth
from .wikipage import WikiPage

SOURCEFORGE_API_BASE_URL = "https://sourceforge.net/rest/p"


class WikiClient:
    def __init__(self, projectname: str, wikiname: str, bearertoken: str) -> None:
        self.projectname = projectname
        self.wikiname = wikiname
        self.bearertoken = bearertoken

    def pagenames(self) -> List[str]:
        response = requests.get(self._generate_url(""))
        pagenames: List[str] = response.json()["pages"]
        return pagenames

    def page(self, pagename: str) -> WikiPage:
        response = requests.get(self._generate_url(pagename))
        json = response.json()
        return WikiPage(title=json["title"], text=json["text"])

    def _generate_url(self, path: str) -> str:
        """Generate a REST API url from the base path determined by script arguments,
        and the given relative path."""
        if path and not path.startswith("/"):
            path = f"/{path}"
        return f"{SOURCEFORGE_API_BASE_URL}/{self.projectname}/{self.wikiname}{path}"
