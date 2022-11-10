import gym
from gym import spaces
from gym.utils import seeding

def cmp(a, b):
    """
    Descripción
    """
    return int((a > b)) - int((a < b))

# 1 = Ace, 2-10 = Number cards, Jack/Queen/King = 10
deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]


def draw_card(np_random):
    """
    Descripción
    """
    return np_random.choice(deck)


def draw_hand(np_random):
    """
    Descripción
    """
    return [draw_card(np_random), draw_card(np_random)]


def usable_ace(hand):
    """
    Descripción
    """   
    return 1 in hand and sum(hand) + 10 <= 21


def sum_hand(hand):
    """
    Descripción
    """
    if usable_ace(hand):
            return sum(hand) + 10
    return sum(hand)


def is_bust(hand):
    """
    Descripción
    """
    return sum_hand(hand) > 21


def score(hand): 
    """
    Descripción
    """
    return 0 if is_bust(hand) else sum_hand(hand)


class BlackjackEnv(gym.Env):
    """
    Descripción
    """
    def __init__(self):
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Tuple((
            spaces.Discrete(32),
            spaces.Discrete(11),
            spaces.Discrete(2)))
        self._seed()
        self._reset()

    def reset(self):
        return self._reset()

    def step(self, action):
        return self._step(action)

    def _seed(self, seed=None):
        """
        Descripción
        """
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _step(self, action):
        """
        Descripción
        """
        assert self.action_space.contains(action), "Fallo, Action = {}".format(action)
        if action:  # Descripción
            self.player.append(draw_card(self.np_random))
            if is_bust(self.player):
                done = True
                reward = -1
            else:
                done = False
                reward = 0
        else:  # Descripción
            done = True
            while sum_hand(self.dealer) < 17:
                self.dealer.append(draw_card(self.np_random))
            reward = cmp(score(self.player), score(self.dealer))
        return self._get_obs(), reward, done, {}

    def _get_obs(self):
        """
        Descripción
        """
        return (sum_hand(self.player), self.dealer[0], usable_ace(self.player))

    def _reset(self):
        """
        Descripción
        """
        self.dealer = draw_hand(self.np_random)
        self.player = draw_hand(self.np_random)
        
        while sum_hand(self.player) < 12:
            self.player.append(draw_card(self.np_random))

        return self._get_obs()