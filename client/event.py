class Event:
    # caused by event from the server
    PLAYER_JOINED = 'player-joined'
    HEALTH_CHANGED = 'health-changed'
    NAME_CHANGED = 'name-changed'
    TXT_MSG_FROM_SERVER_RECEIVED = 'msg-from-server-received'
    PLAYER_CHANGED_POS_HPR = 'player-changed-pos'

    # caused by event from the client
    COMMAND_TYPED = 'message-typed'
    TXT_MSG_TO_SERVER_TYPED = 'msg-to-server-typed'
    CLIENT_SPELL_ATTEMPT = 'client-ability-attempt'
    CLIENT_SEND_ANIMATION_ATTEMPT = 'client-send-animation-attempt'
    CLIENT_MAIN_PLAYER_CHANGED_POS_HPR = 'client-main-player-changed-pos-hpr'
