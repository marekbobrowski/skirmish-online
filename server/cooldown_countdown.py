import time


def cooldown_countdown(player, ability_id, cd_time):
    start = time.time()
    elapsed = time.time() - start
    while elapsed < cd_time:
        player.cooldowns[ability_id] = cd_time - elapsed
        time.sleep(0.01)
        elapsed = time.time() - start
    player.cooldowns[ability_id] = 0
