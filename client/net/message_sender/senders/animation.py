from .base import BaseSender, Event
from protocol.messages import AnimationRequest


class AnimationSender(BaseSender):
    """
    Sends animation updates
    """
    MANAGED_EVENT = Event.CLIENT_STARTED_ANIMATION
    MESSAGE_CLS = AnimationRequest

    def handle(self, animation: str, loop: int) -> None:
        """
        Sends the animation update
        """
        self.send(AnimationRequest.build(animation_name=animation, loop=loop))

