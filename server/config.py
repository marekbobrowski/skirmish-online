spell_names = [
    "SPELL A",
    "SPELL B",
    "SPELL C"
]


spell_cooldowns = [
    1,
    2,
    3
]

n_spells = len(spell_names)
n_spell_slots = 5
n_models = 5
n_weapons = 4

welcome_msg = "Welcome to Skirmish Online!\n"

help = (
    "Available commands:\n "
    "/setname <name>\n"
    f"/setmodel 0-{n_models-1}\n"
    "/setspell <slot_number> <spell_id>\n"
    f"   - slot numbers are 0-{n_spell_slots-1}\n"
    f"   - spell ids are 0-{n_spells-1}\n"
    "/setweapon <weapon_id>\n"
    f"   - weapon ids are 0-{n_weapons-1}\n"
    "Ability usage: \n"
    "q - use slot 0 \n"
    "e - use slot 1 \n"
    "r - use slot 2 \n"
    "f - use slot 3 \n"
    "c - use slot 4 \n"

)


welcome_msg += help

