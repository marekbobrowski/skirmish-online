from .base import BaseUpdater
from protocol.messages import PosHPRRequest
import time


class PositionUpdater(BaseUpdater):
    """
    Position HPR updater
    """
    MESSAGE_CLS = PosHPRRequest
    INTERVAL = 0.001

    def handle(self, node, ref_node):
        """
        Handle new position
        """
        position = (
            node.get_x(ref_node),
            node.get_y(ref_node),
            node.get_z(ref_node),
            node.get_h(ref_node),
            node.get_p(ref_node),
            node.get_r(ref_node),
        )
        if self.last_state is None or position != self.last_state:
            self.send(
                PosHPRRequest.build(
                    *position
                )
            )
            self.last_state = position
            time.sleep(self.INTERVAL)
        return self._continue
