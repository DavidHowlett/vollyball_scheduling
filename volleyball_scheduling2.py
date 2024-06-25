#!/usr/bin/env python3
"""This is an attempt at the volleyball scheduling problem by David Howlett after
previous attempts by Robert Howlett and Micheal Howlett."""
import collections
from typing import Dict, Set

import user_input

# type aliases that make sense for this program
Team = str
Venue = str
Week = int


def main():
    teams, venues, league_exclusions = setup()
    print(teams)
    print(venues)
    print(league_exclusions)


def setup():
    """This parses and checks the input data for the solve from user_input.py."""
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
    return teams, venues, league_exclusions


def parse_week_to_date(week_to_date_str: str):
    week_to_date_str = week_to_date_str.strip()
    week_to_date = {}
    for line in week_to_date_str.split("\n"):
        week, date = line.split("\t")
        week_to_date[int(week)] = date
    return week_to_date


def parse_weeks_no_one_can_play(dates: str) -> Set[int]:
    return {int(week.strip()) for week in dates.split()}


def parse_leagues(leagues_str: str):
    leagues_str = leagues_str.strip()
    leagues = {}
    for line in leagues_str.split("\n"):
        league, _, bad_matchups = line.partition("\t")
        leagues[league.strip()] = bad_matchups.split(" ") if bad_matchups else []
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


if __name__ == "__main__":
    main()
