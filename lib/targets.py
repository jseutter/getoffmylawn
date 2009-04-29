"""Example implementation.

Testing ground for graphics:
- pick a bad guy
- pick a starting place
- pick a path

"""

import random
import characters

def get_random_target_class(targets=characters.enemies.ENEMIES):
    return targets[int(random.random() * len(targets))]

def get_random_target(targets=characters.enemies.ENEMIES):
    return get_random_target_class(targets)()
