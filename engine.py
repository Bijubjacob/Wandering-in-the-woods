# This file contains the main game logic

import random
from .models import PlayerGroup, GameState


def create_game(width, height, start_positions):
    """
    Creates a new game with players placed on the grid
    """

    groups = []

    # create one group per player
    for i, pos in enumerate(start_positions):

        group = PlayerGroup(
            members=[i],      # this group has player i
            position=pos      # starting position
        )

        groups.append(group)

    state = GameState(
        width=width,
        height=height,
        groups=groups
    )

    return state


def get_valid_moves(position, width, height):
    """
    Returns all valid moves (up, down, left, right)
    that stay inside the grid
    """

    x, y = position
    moves = []

    # move right
    if x + 1 < width:
        moves.append((x + 1, y))

    # move left
    if x - 1 >= 0:
        moves.append((x - 1, y))

    # move down
    if y + 1 < height:
        moves.append((x, y + 1))

    # move up
    if y - 1 >= 0:
        moves.append((x, y - 1))

    return moves


def step(state):
    """
    Performs one movement step in the simulation
    """

    # if the game already finished do nothing
    if state.finished:
        return state

    # move every group
    for group in state.groups:

        # get all possible moves for this group
        moves = get_valid_moves(
            group.position,
            state.width,
            state.height
        )

        # choose one move randomly
        group.position = random.choice(moves)

        # add one step to this group
        group.steps += 1

    # increase total game time
    state.time_steps += 1

    # check if any groups landed on the same cell
    merge_groups(state)

    return state


def merge_groups(state):
    """
    If groups land on the same position,
    they merge into one group
    """

    position_map = {}

    # go through each group
    for group in state.groups:
        pos = group.position

        # if this position is not in the dictionary yet, add it
        if pos not in position_map:
            position_map[pos] = []

        # add the group to that position
        position_map[pos].append(group)

    new_groups = []

    # now check each position
    for pos, groups_here in position_map.items():

        # if only one group is here, keep it the same
        if len(groups_here) == 1:
            new_groups.append(groups_here[0])

        else:
            # if multiple groups are here, merge them
            merged_members = []
            merged_steps = 0

            for g in groups_here:
                # combine all player IDs into one list
                merged_members.extend(g.members)

                # add their step counts together
                merged_steps += g.steps

            # create one new merged group
            merged_group = PlayerGroup(
                members=merged_members,
                position=pos,
                steps=merged_steps
            )

            new_groups.append(merged_group)

    # replace the old groups with the new updated groups
    state.groups = new_groups

    # if only one group remains, everyone has met
    if len(state.groups) == 1:
        state.finished = True
    state.groups = new_groups

    if len(state.groups) == 1:

        state.finished = True
