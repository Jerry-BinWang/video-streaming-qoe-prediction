import random
import yaml

DELAY_LOWER_BOUND = 30
DELAY_UPPER_BOUND = 1000

class Comcast:
    def __init__(self):
        self._rng = random.Random()
        self.delay = 0
        self.jitter = 0

    def coin_toss(self, true_prob = 0.5):
        if self._rng.uniform(0, 1) <= true_prob:
            return True
        else:
            return False

    def generate_random_network_condition(self):
        if self.coin_toss():
            self.delay = DELAY_LOWER_BOUND + self._rng.betavariate(alpha=1, beta=3) * (DELAY_UPPER_BOUND - DELAY_LOWER_BOUND)
        else:
            self.delay = 0
            self.jitter = 0

    def apply(self):
        pass

    def reset(self):
        pass


if __name__ == "__main__":
    comcast = Comcast()
    comcast.generate_random_network_condition()
    print(yaml.dump(comcast))
