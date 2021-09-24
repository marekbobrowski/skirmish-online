from .base import BaseModel, String, DateTime


class TextMessage(BaseModel):
    player_name = String.customize(required=False)
    send_dtime = DateTime.customize(required=False)
    message = String
