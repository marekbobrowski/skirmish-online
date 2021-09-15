import time


def cooldown_countdown(player, slot_number, cd_time):
    start = time.time()
    elapsed = time.time() - start
    while elapsed < cd_time:
        player.cooldowns[slot_number] = cd_time - elapsed
        time.sleep(0.01)
        elapsed = time.time() - start
    player.cooldowns[slot_number] = 0
