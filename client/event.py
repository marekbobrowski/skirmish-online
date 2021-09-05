class Event:
    # caused by event from the server
    MAIN_PLAYER_JOINED = 'main-played-joined'
    PLAYER_JOINED = 'played-joined'
    HEALTH_CHANGED = 'health-changed'
    NAME_CHANGED = 'name-changed'
    MSG_FROM_SERVER_RECEIVED = 'msg-from-server-received'

    # caused by event from the client
    COMMAND_TYPED = 'message-typed'
    MSG_TO_SERVER_TYPED = 'msg-to-server-typed'
    CLIENT_SPELL_ATTEMPT = 'client-ability-attempt'
    CLIENT_SEND_ANIMATION_ATTEMPT = 'client-send-animation-attempt'
