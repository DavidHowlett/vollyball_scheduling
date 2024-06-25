#!/usr/bin/env python3
"""This is an attempt at the volleyball scheduling problem by David Howlett after
previous attempts by Robert Howlett and Micheal Howlett."""
import collections
from typing import Dict, FrozenSet, List, Set, Tuple

import user_input

# type aliases that make sense for this program
Team = str
Venue = str
League = str
Week = int
Spot = Tuple[Venue, Week]
Triangle = FrozenSet[Team]
Solution = Dict[Spot, Triangle]


def main():
    teams, venues, league_exclusions, season_length = setup()
    print(f"teams: {teams})")
    print(f"venues: {venues}")
    print(f"leagues that can't play at the same time: {league_exclusions}")
    solution = solve(teams, venues, league_exclusions)
    display_solution(solution, teams, venues, season_length)


def setup():
    """This parses and checks the data from user_input.py.

    It returns easier to use datastructures
    """
    week_to_date = parse_week_to_date(user_input.week_to_date)
    weeks_no_one_can_play = parse_weeks_no_one_can_play(user_input.weeks_no_one_can_play)
    season_length = len(week_to_date)

    league_exclusions = parse_leagues(user_input.league_exclusions)
    teams, clubs = parse_teams(user_input.teams)
    team_unavailability = parse_team_unavailability(user_input.team_unavailability)
    teams = get_team_availability(teams, team_unavailability, season_length, weeks_no_one_can_play)
    venues = parse_venues(user_input.venues)
    venue_unavailability = parse_venues_unavailability(user_input.venues_unavailability)
    venues = get_venue_availability(venues, venue_unavailability, season_length, weeks_no_one_can_play)
    for venue in venues.values():
        if venue["club"] not in clubs:
            raise ValueError(f"{venue['club']} not in clubs")
    return teams, venues, league_exclusions, season_length


def parse_week_to_date(week_to_date_str: str):
    week_to_date_str = week_to_date_str.strip()
    week_to_date = {}
    for line in week_to_date_str.split("\n"):
        week, date = line.split("\t")
        week_to_date[int(week)] = date
    return week_to_date


def parse_weeks_no_one_can_play(dates: str) -> Set[int]:
    return {int(week.strip()) for week in dates.split()}


def parse_leagues(leagues_str: str) -> Dict[League, Set[League]]:
    leagues_str = leagues_str.strip()
    leagues = {}
    for line in leagues_str.split("\n"):
        league, _, bad_matchups = line.partition("\t")
        leagues[league.strip()] = set(bad_matchups.split(" ")) if bad_matchups else set()
    return leagues


def parse_teams(teams_str: str):
    teams_str = teams_str.strip()
    teams = {}
    clubs: Dict[str, Dict] = {}
    for line in teams_str.split("\n"):
        code, name, league, club = line.split("\t")
        teams[code.strip()] = {"name": name, "league": league, "club": club}
        clubs[club] = {}
    return teams, clubs


def parse_team_unavailability(unavailability_str: str):
    unavailability_str = unavailability_str.strip()
    team_unavailability = collections.defaultdict(set)
    for line in unavailability_str.split("\n"):
        team, date = line.split("\t")
        team_unavailability[team.strip()].add(int(date))
    return dict(team_unavailability)


def get_team_availability(
    teams, team_unavailability, total_weeks: int, weeks_no_one_can_play: Set[int]
) -> Dict[Team, Dict]:
    """The program inputs are specified in terms of the weeks that can't be played, but
    it is easier to work with sets of weeks that can be played."""
    all_weeks = set(range(1, total_weeks + 1))
    playable_weeks = all_weeks - weeks_no_one_can_play
    for team in teams.values():
        team["availability"] = playable_weeks.copy()
    for team_code, unavailable_dates in team_unavailability.items():
        assert all(1 <= date <= total_weeks for date in unavailable_dates)
        teams[team_code]["availability"].difference_update(unavailable_dates)
    return teams


def parse_venues(venues_str: str):
    venues_str = venues_str.strip()
    venues = {}
    for line in venues_str.split("\n"):
        venue, club = line.split("\t")
        venues[venue.strip()] = {"club": club}
    return venues


def parse_venues_unavailability(venue_unavailability_str: str):
    venue_unavailability = collections.defaultdict(set)
    venue_unavailability_str = venue_unavailability_str.strip()
    for line in venue_unavailability_str.split("\n"):
        venue, date = line.split("\t")
        venue_unavailability[venue.strip()].add(int(date))
    return dict(venue_unavailability)


def get_venue_availability(
    venues, venue_unavailability, total_weeks: int, weeks_no_one_can_play: Set[int]
) -> Dict[Venue, Dict]:
    """The program inputs are specified in terms of the weeks that can't be played, but
    it is easier to work with sets of weeks that can be played."""
    all_weeks = set(range(1, total_weeks + 1))
    playable_weeks = all_weeks - weeks_no_one_can_play
    for venue in venues.values():
        venue["availability"] = playable_weeks.copy()
    for venue_code, unavailable_dates in venue_unavailability.items():
        assert all(1 <= date <= total_weeks for date in unavailable_dates)
        venues[venue_code]["availability"].difference_update(unavailable_dates)
    return venues


def solve(teams: Dict[Team, Dict], venues: Dict[Venue, Dict], leagues: Dict[League, Set[League]]) -> Solution:
    """This function converts the user inputs and does the scheduling.

    This function is the core of the program.
    """
    assert leagues  # to make pylint happy
    # def greedy_solve(solution):
    #    best_solution = None
    #    best_score = 999_999_999
    #    for position in solution:
    #        for triangle in triangles:
    #            tmp_solution = solution.add_triangle(triangle, position)
    #            score = score_solution(tmp_solution)
    #            if score < best_score:
    #                best_solution = tmp_solution
    #        solution = best_solution

    # This is not a real solution, but it has the right type signature
    solution = {(next(iter(venues)), 1): frozenset(list(teams)[:3])}
    return solution


def display_solution(solution: Solution, teams, venues, season_length: int) -> None:
    """The user has requested that the solution be displayed in a tabular format."""
    print(f"solution found: {solution}")
    teams_table = make_teams_table(solution, teams, season_length)
    print(teams_table)
    venues_table = make_venues_table(solution, venues, season_length)
    print(venues_table)


def make_teams_table(solution: Solution, teams, season_length: int) -> str:
    header = "Teams Table:\n"
    columns = "Teams\t" + "\t".join(str(week) for week in range(1, season_length + 1)) + "\tGames Played\n"
    body = ""
    add_games_to_teams(solution, teams)
    for team_code, team in teams.items():
        body += team_code + "\t"
        for week in range(1, season_length + 1):
            if week in team["spots played"]:
                assert week in team["availability"]
                body += team["spots played"][week]
            elif week in team["availability"]:
                body += "-"
            else:
                body += "x"
            body += "\t"
        body += str(len(team["spots played"])) + "\n"
    return header + columns + body


def add_games_to_teams(solution: Solution, teams):
    """The solution object is the wrong shape for some team focussed processes."""
    for team in teams.values():
        team["spots played"] = {}
    for (venue, week), triangle in solution.items():
        for team_code in triangle:
            teams[team_code]["spots played"][week] = venue
    return teams


def make_venues_table(solution: Solution, venues, season_length: int) -> str:
    header = "Venues Table:\n"
    columns = "Venues\t" + "   \t".join(str(week) for week in range(1, season_length + 1)) + "  \tTriangles Played\n"
    body = ""
    add_games_to_venues(solution, venues)
    for venue_code, venue in venues.items():
        body += venue_code + " \t"
        follow_up_lines: List[List[Team]] = [[], []]
        for week in range(1, season_length + 1):
            if week in venue["spots played"]:
                assert week in venue["availability"]
                triangle = list(venue["spots played"][week])
                body += triangle[0]
                follow_up_lines[0].append(triangle[1])
                follow_up_lines[1].append(triangle[2])
            elif week in venue["availability"]:
                body += "-   "
            else:
                body += "x   "
            body += "\t"
        body += str(len(venue["spots played"])) + "\n"
        for follow_up_line in follow_up_lines:
            body += "    \t" + "\t".join(follow_up_line) + "\n"

        body += "\n"
    return header + columns + body


def add_games_to_venues(solution, venues):
    """The solution object is the wrong shape for some venue focussed processes."""
    for venue in venues.values():
        venue["spots played"] = {}
    for (venue_code, week), triangle in solution.items():
        venues[venue_code]["spots played"][week] = triangle
    return venues


if __name__ == "__main__":
    main()
