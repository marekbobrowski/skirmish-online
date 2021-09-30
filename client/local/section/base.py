from protocol.domain.base import BaseModel


class Section:
    """
    Sections are different parts of applications having different views (scene, GUI) and model.
    """

    def show(self) -> None:
        pass

    def hide(self) -> None:
        pass

    def load_state(self, state: BaseModel) -> None:
        pass

    def post_state_setup(self) -> None:
        """
        Called after loading the model.
        """
        pass
