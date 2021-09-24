from protocol.domain.base import BaseModel


class Section:
    """
    Sections are different parts of applications having different views (scene, GUI) and state.
    """

    def enter(self) -> None:
        pass

    def leave(self) -> None:
        pass

    def load_state(self, state: BaseModel) -> None:
        pass
