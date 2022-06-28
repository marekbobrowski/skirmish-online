from direct.actor.Actor import Actor
from client.local.animation.base import AnimationBase
from abc import abstractmethod
import warnings


class ConfiguredActor(Actor):
    """
    Enhanced Panda3D Actor with additional configuration for specific animated models.
    """
    MODEL_PATH: str = None
    ANIMATION_MAPPING: dict = {}
    """
    Connects animation names in universal format with their embedded names (for this specified model).
    """

    def __init__(self):
        super().__init__(self.MODEL_PATH)
        self.REVERSE_ANIMATION_MAPPING = {v: k for k, v in self.ANIMATION_MAPPING.items()}
        """
        Connects embedded names with their universal names.
        """
        self.configure()

    def play_anim_uf(self, animation: AnimationBase) -> None:
        """
        Play animation specified in universal format.
        """
        embedded = self.ANIMATION_MAPPING.get(animation)
        if embedded is None:
            warnings.warn(f"Actor {type(self).__name__} doesn't support animation {animation}.")
        if animation.LOOP:
            self.loop(embedded)
        else:
            self.play(embedded)

    def get_current_anim_uf(self) -> AnimationBase:
        """
        Get current animation string in universal format.
        """
        current_embedded = self.get_current_anim()
        return self.REVERSE_ANIMATION_MAPPING.get(current_embedded)


    @abstractmethod
    def configure(self) -> None:
        pass
