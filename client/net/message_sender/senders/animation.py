from .base import BaseSender
from client.local.client_event import ClientEvent
from protocol.messages import AnimationRequest


class AnimationSender(BaseSender):
    """
    Sends animation updates
    """

    MANAGED_EVENT = ClientEvent.ANIMATION_CHANGE
    MESSAGE_CLS = AnimationRequest

    def handle(self, animation: str, loop: int) -> None:
        """
        Sends the animation update
        """
        self.send(AnimationRequest.build(animation_name=animation, loop=loop))
