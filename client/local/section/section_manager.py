from .base import Section
from typing import Type


class SectionManager:
    """
    Responsible for switching sections, for example
    login screen, character creation or main gameplay section.
    """
    def __init__(self):
        self.active_section = None

    def switch_to_section(self, cls: Type[Section]) -> None:
        if self.active_section is not None:
            self.active_section.leave()
        self.active_section = cls()
        self.active_section.enter()
