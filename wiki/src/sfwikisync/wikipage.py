import dataclasses


@dataclasses.dataclass
class WikiPage:
    title: str
    text: str

    def filename(self) -> str:
        return f"{self.title}.md"
