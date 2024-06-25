#!/usr/bin/env python3
"""This is an attempt at the volleyball scheduling problem by David Howlett after
previous attempts by Robert Howlett and Micheal Howlett."""
import collections
from typing import List

# type aliases that make sense for this program
Team = str
Venue = str
Week = int


def parse_leagues(leagues_str: str):
    leagues_str = leagues_str.strip().replace("\t", " ")
    leagues = {}
    for line in leagues_str.split("\n"):
        parts = line.split(" ")
        leagues[parts[0]] = parts[1:]
    return leagues


def parse_teams(teams_str: str):
    teams_str = teams_str.strip()
    teams = {}
    for line in teams_str.split("\n"):
        code, name, league, club = line.split("\t")
        teams[code] = {"name": name, "league": league, "club": club}
    return teams


def parse_team_unavailability(teams, unavailability_str: str):
    for team in teams.values():
        team["unavailability"] = set()
    unavailability_str = unavailability_str.strip()
    for line in unavailability_str.split("\n"):
        code, date = line.split("\t")
        teams[code]["unavailability"].add(int(date))
    return teams


def parse_venues(venues_str: str):
    venues_str = venues_str.strip()
    venues = collections.defaultdict(set)
    for line in venues_str.split("\n"):
        venue, club = line.split("\t")
        venues[club].add(venue.strip())
    return venues


# def parse_venues_unavailability(teams_str: str):
#    pass


def parse_dates_no_one_can_play(dates: str) -> List[int]:
    return [int(date.strip()) for date in dates.split()]


# def parse_week_to_date(dates: str):
#    pass


# def get_team_availability(
#    total_weeks: int, team_unavailability, weeks_no_one_can_play: List[int]
# ) -> Dict[Team, List[Week]]:
#    pass


# def get_venue_availability(
#    total_weeks: int, venue_unavailability, weeks_no_one_can_play: List[int]
# ) -> Dict[Venue, List[Week]]:
#    pass


def get_empty_solution():
    pass


# def greedy_solve1(solution):
#    best_solution = None
#    best_score = 999_999_999
#    for position in solution:
#        for triangle in triangles:
#            tmp_solution = solution.add_triangle(triangle, position)
#            score = score_solution(tmp_solution)
#            if score < best_score:
#                best_solution = tmp_solution
#        solution = best_solution


def main():
    # league_exclusions = parse_leagues(user_input.league_exclusions)
    # teams = parse_teams(user_input.teams)
    # team_unavilability = parse_team_unavailability(user_input.team_unavailability)
    # venues = parse_venues(user_input.venues)
    # venues_unavailability = parse_venues_unavailability(user_input.venue_not_available)
    # weeks_no_one_can_play = parse_dates_no_one_can_play(user_input.weeks_no_one_can_play)
    # week_to_date = parse_week_to_date(user_input.week_to_date)
    # total_weeks = len(week_to_date)
    # team_availability = get_team_availability(total_weeks, team_unavilability, weeks_no_one_can_play)
    # venues_availability = get_venue_availability(total_weeks, venues_unavailability, weeks_no_one_can_play)
    # empty_solution = get_empty_solution()
    pass


if __name__ == "__main__":
    main()
