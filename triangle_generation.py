"""If this method of generation doesn't work, we can use pregenerated triangles."""

import itertools
from typing import Generator


def generate_triangles(teams: int):
    """Generates a series of triangles.

    We try to give each team an equal number of games while avoiding repeated matches.
    The method of generation is currently very poor.
    """
    for i in itertools.count():
        revolutions = (3 * i) // teams
        team1 = i * 3
        team2 = i * 3 + 1 + revolutions
        team3 = i * 3 + 2 + 2 * revolutions
        team1 = team1 % teams + 1
        team2 = team2 % teams + 1
        team3 = team3 % teams + 1
        # if team1 != team2 and team1 != team3 and team2 != team3:
        yield (team1, team2, team3)


def score_triangles(triangles, teams):
    """This prints a table that allows the quality of the triangle generation to be
    seen."""
    result = "\t" + "\t".join(str(team) for team in range(1, 1 + teams)) + "\n"
    for team1 in range(1, 1 + teams):
        result += str(team1) + "\t"
        for team2 in range(1, 1 + teams):
            if team1 == team2:
                match_count = len([triangle for triangle in triangles if triangle.count(team1) == 2])
            else:
                match_count = len([triangle for triangle in triangles if team1 in triangle and team2 in triangle])
            result += str(match_count) + "\t"
        result += "\n"

    print(result)


def main():
    triangles = []
    league_size = 6
    triangle_count = 50
    generator: Generator[tuple[int, int, int], None, None] = generate_triangles(league_size)
    for _ in range(triangle_count):
        triangle = generator.__next__()
        print(triangle)
        triangles.append(triangle)
    score_triangles(triangles, league_size)


if __name__ == "__main__":
    main()
