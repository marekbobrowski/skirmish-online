from direct.task.Task import Task
import config


class Abilities:
    def __init__(self, skirmish):
        self.skirmish = skirmish
        self.core = skirmish.core
        # (time left to cool down, cooldown time)
        self.icons = [config.artwork_dir + 'warrior_ability_1.png',
                      config.artwork_dir + 'warrior_ability_2.png',
                      config.artwork_dir + 'warrior_ability_3.png',
                      config.artwork_dir + 'warrior_ability_4.png']
        self.names = ['ability_1', 'ability_2', 'ability_3', 'ability_4']
        self.cooldowns = [
            [0, 2],
            [0, 4],
            [0, 5],
            [0, 10]
        ]

    def trigger_cooldown(self, ability):
        task = Task(self.count_down_cooldown)
        self.core.task_mgr.add(task, 'cooldown countdown', extraArgs=[ability, task])

    def count_down_cooldown(self, ability, task):
        diff = self.cooldowns[ability][1] - task.time
        if diff > 0:
            self.cooldowns[ability][0] = diff
            return Task.cont
        else:
            self.cooldowns[ability][0] = 0
            return Task.done


