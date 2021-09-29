class ServerEvent:
    """
    This class represents an event that was sent by the server.
    It's actually a string because panda3d framework represents events as strings.
    """

    # caused by event from the server
    PLAYER_JOINED = "player-joined"
    PLAYER_CHANGED_ANIMATION = "played-changed-animation"
    HEALTH_CHANGED = "health-changed"
    NAME_CHANGED = "name-changed"
    TXT_MSG_FROM_SERVER_RECEIVED = "msg-from-server-received"
    PLAYER_CHANGED_POS_HPR = "player-changed-pos"
    RECEIVED_COMBAT_DATA = "received-combat-data"
    TRIGGER_COOLDOWN = "trigger-cooldown"
    SET_SPELL = "set-spell"
    MODEL_CHANGED = "set-model"
    WEAPON_CHANGED = "weapon-changed"
    POSITION_CHANGED = "position-changed"
