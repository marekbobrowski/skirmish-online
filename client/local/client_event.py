class ClientEvent:
    """
    This class represents an event that occurred within client, locally.
    For example, user has typed a command.

    However, this event can be indirectly caused by server.
    For example, the game server sends only ID of a player whose state has changed.
    The client translates such event by finding the exact unit that is represented by the ID. The client
    sends then a new event with reference to the unit, so it's state can be easily manipulated.

    Event is actually a string because panda3d framework represents events as strings.
    """

    NEW_UNIT = "client-event-new-unit"
    UNIT_HP = "client-event-unit-hp"
    UNIT_NAME = "client-event-unit-name"
    UNIT_POS_ROT = "client-event-unit-pos-rot"
    UNIT_ANIMATION = "client-event-unit-animation"
    COMMAND = "client-event-command"
    COMMAND_TO_SERVER = "client-event-command-to-server"
    SPELL_ATTEMPT = "client-event-spell-attempt"
    ANIMATION_CHANGE = "client-event-animation-change"
