#!/usr/bin/python3

import random 

from collections import defaultdict
from enum import Enum


class RollStrategy(Enum):
    FORTY = 1
    HUNDO = 2
    FORTY_IF_PREVIOUS_HUNDO = 3
    FIFTY = 4

# Frame Strategies
UP_THE_MIDDLE = [RollStrategy.FORTY] * 9
UP_THE_MIDDLE_LAST_HUNDO = [RollStrategy.FORTY] * 8 + [RollStrategy.HUNDO]
UP_THE_MIDDLE_WITH_FIFTY = [RollStrategy.FORTY] * 3 + [RollStrategy.FIFTY] * 3 + [RollStrategy.FORTY] * 3
REVERSE_HYBRID_ADAPTIVE = [RollStrategy.FORTY] * 6 + [RollStrategy.FORTY_IF_PREVIOUS_HUNDO] * 3
REVERSE_HYBRID = [RollStrategy.FORTY] * 6 + [RollStrategy.HUNDO] * 3

STRATEGY_ODDS = {
  RollStrategy.FORTY: 0.80,
  RollStrategy.HUNDO: 0.2,
  RollStrategy.FORTY_IF_PREVIOUS_HUNDO: 0.2,
  RollStrategy.FIFTY: 0.7
}

VERBOSE = False

class SkeeSim:
  '''
  TODO
  '''

  def __init__(self):
    self.current_frame = []
    self.current_match = []
    self.all_scores = []


  def roll_successful(self, strategy: RollStrategy) -> bool:
    if random.random() <= STRATEGY_ODDS[strategy]:
      return True
    return False

  def roll(self, strategy: RollStrategy) -> int:
    if strategy == RollStrategy.FORTY:
      return 40 if self.roll_successful(strategy) else 10
    elif strategy == RollStrategy.FIFTY:
      return 50 if self.roll_successful(strategy) else 10
    elif strategy == RollStrategy.HUNDO:
      return 100 if self.roll_successful(strategy) else 10
    elif strategy == RollStrategy.FORTY_IF_PREVIOUS_HUNDO:
      if 100 in self.current_frame:
        return 40 if self.roll_successful(strategy) else 10
      else:
        return 100 if self.roll_successful(strategy) else 10


  def roll_frame(self, frame_strategy: list[RollStrategy]):
    self.current_frame = []
    for roll_strategy in frame_strategy:
      self.current_frame.append(self.roll(roll_strategy))
    score = int(sum(self.current_frame) / 10)
    if VERBOSE: print(f'Player just rolled: {score}')
    self.current_match.append(score)

  def roll_match(self, frame_strategy: list[RollStrategy]) -> int:
    self.current_match = []
    for i in range(10):
      frame_score = self.roll_frame(frame_strategy)
    match_score = sum(self.current_match)
    if VERBOSE: print(f'Player\'s match score: {match_score}')
    return match_score

  def simulate(self, frame_strategy: list[RollStrategy], sims: int):
    self.all_scores = []
    for i in range(sims):
      match_score = self.roll_match(frame_strategy)
      self.all_scores.append(match_score)
    average_match = sum(self.all_scores) / len(self.all_scores)
    print(f'After {sims} simulations, player\'s average match score was: {average_match}')


if __name__ == '__main__':
  s = SkeeSim()
  print('Rolling strategy: Up the middle')
  s.simulate(UP_THE_MIDDLE, 100_000)
  print('Rolling strategy: Up the middle; last hundo')
  s.simulate(UP_THE_MIDDLE_LAST_HUNDO, 100_000)
  print('Rolling strategy: Up the middle with fifties')
  s.simulate(UP_THE_MIDDLE_WITH_FIFTY, 100_000)
  print('Rolling strategy: Reverse hybrid adaptive')
  s.simulate(REVERSE_HYBRID_ADAPTIVE, 100_000)
  print('Rolling strategy: Reverse hybrid')
  s.simulate(REVERSE_HYBRID, 100_000)