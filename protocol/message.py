class Message:
    # INITIAL TYPES #
    ASK_FOR_PASS = 1
    ASK_FOR_INITIAL_DATA = 2

    # SENT BY CLIENT AND SERVER #
    POS_HPR = 3
    IS_MOVING = 4
    ACTION = 5
    DISCONNECTION = 6
    CHAT_MSG = 7

    # SENT ONLY BY SERVER
    CHARACTER_REACTION = 8  # reaction to hit, or spell-casting animation'
    TELEPORT = 9
    NEW_PLAYER = 10
    HEALTH = 11

    # SENT ONLY BY CLIENT
    READY_FOR_UPDATES = 12
