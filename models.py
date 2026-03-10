# This file defines the data used by the game

from dataclasses import dataclass
from typing import List, Tuple

# A position on the grid will be stored as (x, y)
Position = Tuple[int, int]


@dataclass
class PlayerGroup:
    """
    Represents a single player or a group of players
    """

    members: List[int]   # player IDs in this group
    position: Position   # location on the grid
    steps: int = 0       # number of moves made


@dataclass
class GameState:
    """
    Stores the entire game state
    """

    width: int
    height: int
    groups: List[PlayerGroup]
    time_steps: int = 0
    finished: bool = False