n_spells = 10
n_spell_slots = 5

spell_names = [
    "SPELL A",
    "SPELL B",
    "SPELL C",
    "SPELL D",
    "SPELL E",
    "SPELL F",
    "SPELL G",
    "SPELL H",
    "SPELL I",
    "SPELL J"
]


spell_cooldowns = [
    1,
    1,
    3,
    3,
    5,
    5,
    10,
    10,
    15,
    15
]

welcome_msg = "Welcome to Skirmish Online!\n"

help = (
    "Available commands:\n "
    "/setname <name>\n"
    "/setspell <slot_number> <spell_id>\n"
    f"   - slot numbers are 0-{n_spell_slots-1}\n"
    f"   - spell ids are 0-{n_spells-1}\n"
    f"      - 0 lorem ipsum (1 sec cd)\n"
    f"      - 1 lorem ipsum (2 sec cd)\n"
    f"      - 2 lorem ipsum (3 sec cd)\n"
    f"      - 3 lorem ipsum (4 sec cd)\n"
    f"      - 4 lorem ipsum (5 sec cd)\n"
    f"      - 5 lorem ipsum (6 sec cd)\n"
    f"      - 6 lorem ipsum (7 sec cd)\n"
    f"      - 7 lorem ipsum (8 sec cd)\n"
    f"      - 8 lorem ipsum (9 sec cd)\n"
    f"      - 9 lorem ipsum (10 sec cd)\n"
    "Ability usage: \n"
    "q - use slot 0 \n"
    "e - use slot 1 \n"
    "r - use slot 2 \n"
    "f - use slot 3 \n"
    "c - use slot 4 \n"

)


welcome_msg += help

