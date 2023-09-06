import dataclasses
from typing import List


@dataclasses.dataclass
class WikiPage:
    title: str
    text: str
    labels: List[str]

    def filename(self) -> str:
        return f"{self.title}.md"

    def label_string(self) -> str:
        return ','.join(self.labels)
