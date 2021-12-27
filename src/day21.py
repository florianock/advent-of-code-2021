#!/usr/bin/env python3
import copy
import itertools
import re
from collections import Counter
from dataclasses import dataclass

from aocd import data, submit

# --- Day 21: Dirac Dice ---

@dataclass
class Player:
    id: int
    position: int
    score: int

    def walk(self, num: int):
        self.position += num
        self.position = ((self.position - 1) % 10) + 1
        self.score += self.position


@dataclass
class Die:
    def roll(self):
        pass


@dataclass
class OneHunderdSidedDie(Die):
    current: int

    def roll(self):
        self.current += 1
        if self.current > 100:
            self.current = 1
        return self.current


@dataclass
class DiracDie(Die):
    def roll(self):
        return [1, 2, 3]


@dataclass
class Dicegame:
    score_limit: int
    players: list[Player]
    die: Die
    finished: bool


def main():
    ex1 = solve(example, OneHunderdSidedDie(0))
    assert ex1 == 739785, f"expected 739785, but got {ex1}"
    answer1 = solve(data, OneHunderdSidedDie(0))
    assert answer1 == 675024, f"expected 675024, but got {answer1}"
    ex2 = solve(example, DiracDie())
    assert ex2 == 444356092776315, f"expected 444356092776315, but got {ex2}"


def solve(inputs: str, die) -> int:
    """
    What do you get if you multiply the score of the losing player by the number of times the die was rolled during the game?
    :param inputs: Input string containing the player starting positions
    :param die: The die to roll
    :return: losing_score * num_die_rolls
    """
    starting_positions = [re.findall(r'\d+', player) for player in inputs.split('\n')]
    players = list(map(lambda x: Player(int(x[0]), int(x[1]), 0), starting_positions))
    if type(die) is OneHunderdSidedDie:
        result = play(Dicegame(1000, players, die, False))
        return result[0] * min([p.score for p in result[1].players])
    if type(die) is DiracDie:
        universes = play_dirac(Dicegame(21, players, die, False), 1)
        return max(universes.values())


def play_dirac(game: Dicegame, universe_count: int) -> Counter:
    print(str(universe_count))
    universes = Counter({p.id: 0 for p in game.players})
    for player in game.players:
        if player.score >= game.score_limit:
            print(f"finished universe {universe_count}")
            universes[player.id] += 1
            game.finished = True
            break
        points = game.die.roll()
        for point in points:
            other_universe_players = [Player(p.id, p.position, p.score) for p in game.players]
            other_player = [p for p in other_universe_players if p.id == player.id]
            other_player[0].walk(point)
            split_game = Dicegame(21, other_universe_players, game.die, False)
            universes.update(play_dirac(split_game, universe_count + 1))
    return universes


def play(game: Dicegame) -> (int, Dicegame):
    roll_count = 0
    turn = 0
    while True:
        turn += 1
        for p in game.players:
            points = game.die.roll() + game.die.roll() + game.die.roll()
            p.walk(points)
            roll_count += 3
            if p.score >= game.score_limit:
                game.finished = True
                break
        if game.finished:
            break
    return roll_count, game


example = """
Player 1 starting position: 4
Player 2 starting position: 8
""".strip()

if __name__ == "__main__":
    main()
