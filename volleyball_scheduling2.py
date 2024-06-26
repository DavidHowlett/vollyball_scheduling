#!/usr/bin/env python3
"""This is an attempt at the volleyball scheduling problem by David Howlett after
previous attempts by Robert Howlett and Micheal Howlett."""
import collections
from typing import Any, Dict, FrozenSet, List, Set, Tuple

import user_input

# type aliases that make sense for this program
TeamCode = str
VenueCode = str
LeagueCode = str
Teams = Dict[TeamCode, Dict[str, Any]]  # it would be better to not use Any here
Venues = Dict[VenueCode, Dict[str, Any]]
Leagues = Dict[LeagueCode, Dict[str, Any]]
Week = int
Spot = Tuple[VenueCode, Week]
Triangle = FrozenSet[TeamCode]
Solution = Dict[Spot, Triangle]


def main():
    teams, venues, leagues, triangles, season_length = setup()
    print(f"teams: {teams})")
    print(f"venues: {venues}")
    print(f"leagues: {leagues}")
    print(f"triangles: {triangles}")
    solution = solve(teams, venues, leagues, triangles)
    display_solution(solution, teams, venues, season_length)


def setup():
    """This parses and checks the data from user_input.py.

    It returns easier to use datastructures
    """
    week_to_date = parse_week_to_date(user_input.week_to_date)
    weeks_no_one_can_play = parse_weeks_no_one_can_play(user_input.weeks_no_one_can_play)
    season_length = len(week_to_date)

    leagues = parse_leagues(user_input.league_exclusions)
    teams, clubs = parse_teams(user_input.teams)
    for team in teams.values():
        assert team["league"] in leagues  # catches some typos
        assert team["club"] in clubs  # catches some typos
    team_unavailability = parse_team_unavailability(user_input.team_unavailability)
    teams = get_team_availability(teams, team_unavailability, season_length, weeks_no_one_can_play)
    leagues = add_teams_to_leagues(teams, leagues)
    venues = parse_venues(user_input.venues)
    venue_unavailability = parse_venues_unavailability(user_input.venues_unavailability)
    venues = get_venue_availability(venues, venue_unavailability, season_length, weeks_no_one_can_play)
    for venue in venues.values():
        if venue["club"] not in clubs:
            raise ValueError(f"{venue['club']} not in clubs")
    triangles = get_triangles(leagues)
    return teams, venues, leagues, triangles, season_length


def parse_week_to_date(week_to_date_str: str):
    week_to_date_str = week_to_date_str.strip()
    week_to_date = {}
    for line in week_to_date_str.split("\n"):
        week, date = line.split("\t")
        week_to_date[int(week)] = date
    return week_to_date


def parse_weeks_no_one_can_play(dates: str) -> Set[int]:
    return {int(week.strip()) for week in dates.split()}


def parse_leagues(leagues_str: str) -> Leagues:
    leagues_str = leagues_str.strip()
    leagues = {}
    for line in leagues_str.split("\n"):
        league, _, bad_matchups = line.partition("\t")
        leagues[league.strip()] = {"bad matchups": set(bad_matchups.split(" ")) if bad_matchups else set()}
    return leagues


def parse_teams(teams_str: str):
    teams_str = teams_str.strip()
    teams = {}
    clubs: Dict[str, Dict[str, Any]] = {}
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
    teams: Teams, team_unavailability, total_weeks: int, weeks_no_one_can_play: Set[Week]
) -> Teams:
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


def add_teams_to_leagues(teams: Teams, leagues: Leagues):
    for team_code, team in teams.items():
        league = team["league"]
        if "teams" not in leagues[league]:
            leagues[league]["teams"] = []
        leagues[league]["teams"].append(team_code)
    return leagues


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
    venues: Venues, venue_unavailability, total_weeks: int, weeks_no_one_can_play: Set[Week]
) -> Venues:
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


def get_triangles(leagues: Leagues):
    triangles = []
    for league in leagues.values():
        team_count = len(league["teams"])
        triangles_with_numbers = user_input.pre_made_triangles[team_count]
        # replace the digits in the triangles with actual teams
        for triangle_with_numbers in triangles_with_numbers:
            triangle = frozenset(league["teams"][team_number - 1] for team_number in triangle_with_numbers)
            triangles.append(triangle)
    return triangles


def solve(teams: Teams, venues: Venues, leagues: Leagues, triangles) -> Solution:
    """This function converts the user inputs and does the scheduling.

    This function is the core of the program.
    """
    #    solution: Solution = {}
    #    for spot, triangle in all_legal_next_spots(solution, venues, triangles):
    #        print(spot,triangle)  # todo
    assert leagues  # to make pylint happy
    assert triangles  # to make pylint happy
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
    return {(next(iter(venues)), 1): frozenset(list(teams)[:3])}


# def all_legal_next_spots(solution, venues, triangles):
#    pass


def score_solution(solution: Solution, teams, season_length: int) -> int:
    """Calculates a score for the solution. More is better.

    If you feel that the solver is consistently valuing things wrong, you need to adjust
    this function.
    """
    # It is good to schedule more games
    score = 50 * len(solution)

    # It is good to schedule games earlier in the season
    score += sum(season_length - week for _, week in solution)

    # It is good for teams to play a similar number of games
    add_games_to_teams(solution, teams)
    games_played_by_teams = [len(team["spots played"]) for team in teams.values()]
    minimum_games_played_by_team = min(games_played_by_teams)
    maximum_games_played_by_team = max(games_played_by_teams)
    score -= 100 * (maximum_games_played_by_team - minimum_games_played_by_team)

    # It is good for clubs to play a similar number of games weighted by number of teams
    # some of this logic could be moved to the setup stage to speed things up
    clubs = {}
    for team in teams.values():
        club_code = team["club"]
        if club_code not in clubs:
            clubs[club_code] = {"team count": 0, "spots played": 0}
        clubs[club_code]["team count"] += 1
        clubs[club_code]["spots played"] += len(team["spots played"])
    games_played_by_clubs = [len(team["spots played"]) for team in teams.values()]
    minimum_games_played_by_club = min(games_played_by_clubs)
    maximum_games_played_by_team = max(games_played_by_clubs)
    score -= 200 * (maximum_games_played_by_team - minimum_games_played_by_club)

    # todo minor incentive for keeping the number of placement options high.
    #  This might keep options open during tree search.
    # todo strongly penalise triangles that can't be scheduled anywhere.
    #  This is an early signal of trouble in the tree search.

    return score


def display_solution(solution: Solution, teams, venues, season_length: int) -> None:
    """The user has requested that the solution be displayed in a tabular format."""
    teams_table = make_teams_table(solution, teams, season_length)
    print(teams_table)
    venues_table = make_venues_table(solution, venues, season_length)
    print(venues_table)
    print(f"solution found: {solution}")
    unused_triangles = "todo"
    print(f"unused triangles: {unused_triangles}")
    score = score_solution(solution, teams, season_length)
    print(f"solution score: {score}")


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
    # Every value in the solution should appear 3 times in the teams
    assert sum(len(team["spots played"]) for team in teams.values()) == 3 * len(solution)
    return teams


def make_venues_table(solution: Solution, venues, season_length: int) -> str:
    header = "Venues Table:\n"
    columns = "Venues\t" + "   \t".join(str(week) for week in range(1, season_length + 1)) + "  \tTriangles Played\n"
    body = ""
    add_games_to_venues(solution, venues)
    for venue_code, venue in venues.items():
        body += venue_code + " \t"
        follow_up_lines: List[List[TeamCode]] = [[], []]
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
