class Event:
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

    # caused by event from the client
    COMMAND_TYPED = "message-typed"
    TXT_MSG_TO_SERVER_TYPED = "msg-to-server-typed"
    CLIENT_SPELL_ATTEMPT = "client-ability-attempt"
    CLIENT_STARTED_ANIMATION = "client-send-animation-attempt"
    CLIENT_STARTED_CHANGING_POS_HPR = "client-started-changing-pos-hpr"
    CLIENT_STOPPED_CHANGING_POS_HPR = "client-stopped-changing-pos-hpr"

    LOCAL_NEW_UNIT = "local-new-unit"
    LOCAL_UNIT_HP_CHANGED = "local-unit-hp-changed"
    LOCAL_UNIT_NAME_CHANGED = "local-unit-name-changed"
