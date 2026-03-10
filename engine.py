# This file contains the main game logic

import random
from .models import PlayerGroup, GameState


def create_game(width, height, start_positions):
    groups = []

    # create one group per player
    for i, pos in enumerate(start_positions):

        group = PlayerGroup(
            members=[i],
            position=pos
        )

        groups.append(group)

    state = GameState(
        width=width,
        height=height,
        groups=groups
    )

    return state


def get_valid_moves(position, width, height):

    x, y = position
    moves = []

    if x + 1 < width:
        moves.append((x + 1, y))

    if x - 1 >= 0:
        moves.append((x - 1, y))

    if y + 1 < height:
        moves.append((x, y + 1))

    if y - 1 >= 0:
        moves.append((x, y - 1))

    return moves


def step(state):

    if state.finished:
        return state

    for group in state.groups:

        moves = get_valid_moves(
            group.position,
            state.width,
            state.height
        )

        group.position = random.choice(moves)

        group.steps += 1

    state.time_steps += 1

    merge_groups(state)

    return state


def merge_groups(state):

    position_map = {}

    for group in state.groups:

        pos = group.position

        if pos not in position_map:
            position_map[pos] = []

        position_map[pos].append(group)

    new_groups = []

    for pos, groups_here in position_map.items():

        if len(groups_here) == 1:

            new_groups.append(groups_here[0])

        else:

            members = []

            for g in groups_here:
                members.extend(g.members)

            merged = PlayerGroup(
                members=members,
                position=pos
            )

            new_groups.append(merged)

    state.groups = new_groups

    if len(state.groups) == 1:
        state.finished = True