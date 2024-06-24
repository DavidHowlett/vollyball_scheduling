#!/usr/bin/env python3
"""This was written by David Howlett."""
from typing import Dict, List

import user_input

# type aliases that make sense for this program
Team = str
Venue = str
Week = int


def parse_leagues(leagues: str):
    leagues = leagues.strip()


def parse_teams(teams: str):
    pass


def parse_team_unavailability(teams_str: str):
    pass


def parse_venues(teams_str: str):
    pass


def parse_venuess_unavailability(teams_str: str):
    pass


def parse_dates_no_one_can_play(dates: str) -> List[int]:
    return [int(date.strip()) for date in dates.split()]


def parse_week_to_date(dates: str):
    pass


def get_team_availability(
    total_weeks: int, team_unavilability, weeks_no_one_can_play: List[int]
) -> Dict[Team, List[Week]]:
    pass


def get_venue_availability(
    total_weeks: int, venue_unavilability, weeks_no_one_can_play: List[int]
) -> Dict[Venue, List[Week]]:
    pass


def get_empty_solution():
    pass


def main():
    league_exclusions = parse_leagues(user_input.league_exclusions)
    teams = parse_teams(user_input.teams)
    team_unavilability = parse_team_unavailability(user_input.team_unavailability)
    venues = parse_venues(user_input.venues)
    venues_unavailability = parse_venuess_unavailability(user_input.venue_not_available)
    weeks_no_one_can_play = parse_dates_no_one_can_play(user_input.weeks_no_one_can_play)
    week_to_date = parse_week_to_date(user_input.week_to_date)
    total_weeks = len(week_to_date)
    team_availability = get_team_availability(total_weeks, team_unavilability, weeks_no_one_can_play)
    venues_availability = get_venue_availability(total_weeks, venues_unavailability, weeks_no_one_can_play)
    empty_solution = get_empty_solution()


if __name__ == "__main__":
    main()
