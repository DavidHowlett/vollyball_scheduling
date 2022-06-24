"""
Andrew Tatarek asked me to help organize a volleyball tournament. Given a set of groups of teams called ORIGINAL_GROUPS
I need to assign which 3 teams will play each other for each court for each round.

The code in this file was written Michael Howlett building on code written by Michael, Robert, and David Howlett.
To enable easy deployment, we put all the logic in a single file so that it can be pasted into
https://www.w3schools.com/python/trypython.asp?filename=demo_ref_min
so that users don't need to install python and deal with the issues associated with that.

TODO: make there a preference for a team to play on home turf
      output friendlies in a better format
"""

import copy
import random
from typing import List

# groups = [
#     ["teamA1", "teamA2", "teamA3", "teamA4", "teamA5"],
#     ["teamB1", "teamB2", "teamB3", "teamB4", "teamB5", "teamB6", "teamB7"],
#     ["teamC1", "teamC2", "teamC3", "teamC4", "teamC5", "teamC6", "teamC7", "teamC8"],
# ]
# ORIGINAL_GROUPS = [
#     ["Team1-01", "Team1-02", "Team1-03", "Team1-04", "Team1-05"],
#     ["Team2-01", "Team2-02", "Team2-03", "Team2-04", "Team2-05"],
#     ["Team3-01", "Team3-02", "Team3-03", "Team3-04"],
#     ["Team4-01", "Team4-02", "Team4-03", "Team4-04", "Team4-05", "Team4-06"],
# ]
ORIGINAL_GROUPS = [
    ["OXM1", "SPM1", "BSM1", "MHM1", "OXM2", "FBM1", "OUM1"],
    ["RAM1", "SPM2", "OXM3", "NBM1", "FBM2", "MHM2", "BSM2"],
    ["OXL1", "FBL1", "BSL1", "MHL1", "SPL1", "NBL1", "OXL2", "SBL1", "OUL1", "RAL1", "MHL2"],
    ["BSX1", "FBX1", "MHX1", "SPX1", "MHX2", "RAX1", "OXX1", "NBX1", "SPX2"],
    ["RAJ1", "SPJ1", "BSJ1", "NBJ1", "RAJ2", "BHJ1"]]
BASES = ["BS1", "FB1", "MH1", "NB1", "OX1", "OU1", "RA1", "SB1", "SP1"]
ALL_TEAMS = [team for group in ORIGINAL_GROUPS for team in group]
NUM_OF_SIMULATION: int = 100  # number of times it tries to produce a setup, higher improves matching but slows program
ROUNDS = 26
NUM_OF_COURTS = 7
WEEKS_NOT_PLAYABLE = [11, 12, 13]
COURTS_TO_USE = min(NUM_OF_COURTS, len(ALL_TEAMS) // 3)

assert len(ALL_TEAMS) == len(set(ALL_TEAMS)), "Duplicate team, or team in >1 group!"
# debugging is easier if the randomness is not really random.
random.seed(10)


class TeamStats:
    def __init__(self, name: str, group: List[str], qty: int):
        self.id = name
        playable = []
        for _ in range(qty):
            playable += group.copy()
            playable.remove(name)
        random.shuffle(playable)
        self.eligible_opponents = playable
        self.games_played = 0
        self.opponents_played = []
        self._backup_opponents = playable.copy()
        self.history = ''  # g = Game, r = Referee, f = Free. example: 'ggrgfg'

    def play(self, other: str, other2: str):
        if other not in self.eligible_opponents:
            self.refresh_eligible()
        self.eligible_opponents.remove(other)
        self.opponents_played += [other]
        if other2 not in self.eligible_opponents:
            self.refresh_eligible()
        self.eligible_opponents.remove(other2)
        self.opponents_played += [other2]
        self.games_played += 1
        self.history += 'g'

    def refresh_eligible(self):
        self.eligible_opponents.extend(self._backup_opponents)


def reformat_teams(given_groups):
    """
    replace team with TeamStats object
    """
    new_groups = []
    i = 0
    for group in given_groups:
        new_group = [TeamStats(name=team, group=group, qty=1) for team in group]
        new_groups.append(new_group)
        i += 1
    return new_groups


def print_table(output_matrix):
    """
    This prints the transpose of the table in the code
    """
    for i in range(COURTS_TO_USE * 3):
        to_output = ""
        for j in range(len(output_matrix)):
            try:
                to_output = to_output + "\t" + output_matrix[j][i]
            except IndexError:
                to_output = to_output + "\t" + "free"
        print(to_output[1:])


def extra_occupied(groups, team):
    """
    finds all the other teams that cant play as a result of team being occupied.
    This is to prevent clashes caused by a player being in both men/women and mixed/juniors
    """
    exclude = ''
    occupied_teams = [team.id]
    team_type = team.id[2]
    #  including both upper and lower case as I don't trust end users.
    #  if statements can be more compact using a dict, but this is easier if non-programmer needs to change it
    if team_type == 'M' or team_type == 'm':  # Mens
        exclude = 'JjXx'  # juniors and mixed
    if team_type == 'L' or team_type == 'l':  # ladies
        exclude = 'JjXx'  # juniors and mixed
    if team_type == 'J' or team_type == 'j':  # juniors
        exclude = 'MmLl'  # Mens and Ladies
    if team_type == 'X' or team_type == 'x':  # miXed
        exclude = 'MmLl'  # Mens and Ladies
    if team_type == 'S' or team_type == 's':  # Single, don't exclude anyone
        exclude = ' '  # empty
    if exclude == '':
        print(team, " doesn't follow correct formatting and is of unknown type")
        print("currently it's:  ", team_type,
              "   but needs to be one of M (mens), L (ladies), J (juniors), X (mixed), S (single)")
        assert 0 == 0, "program stop."
    team_loc = team.id[0:1]  # where the team is based
    for group in groups:
        for team2 in group:
            if team2.id[0:1] == team_loc and team2.id[2] in exclude:
                occupied_teams.append(team2.id)
    return occupied_teams


def print_friendlies(friendlies):
    for group in friendlies:
        for pair in group:
            print(pair[0], "\t", pair[1])


def run_sims(groups):
    """
    generate a collection of solutions with a bit of randomness and return the best one,
    the best score and the average score
    """
    best_output_matrix = []
    best_match_up_score = 999999  # This will be overridden later
    best_friendlies = []
    average_match_up_score = 0
    friendly_count = 0
    for _ in range(NUM_OF_SIMULATION):  # run the setup "NUM_OF_SIMULATION" times and picks best
        # Michael found another bug which crashes the code once every few hundred games.
        # where if for all teams the [teams they can play against] are already playing someone else, no game gets
        # added causing an empty court and a crash. Due to rarity, we just catch the error and continue.
        try:
            match_up_score, output_matrix, result_groups = run_sim(copy.deepcopy(groups))
        except EmptyCourtException:
            continue
        friendlies, friendly_count = find_friendlies(result_groups)
        match_up_score = get_score(result_groups, match_up_score, friendly_count)
        if match_up_score < best_match_up_score:
            best_match_up_score = match_up_score
            best_output_matrix = output_matrix
            best_friendlies = friendlies
        average_match_up_score += match_up_score / NUM_OF_SIMULATION
    return best_output_matrix, average_match_up_score, best_match_up_score, best_friendlies, friendly_count


def run_sim(groups):
    """
    generate a single solution and partially scores it
    """
    output_matrix = []
    # at this point in the calculation the number format of groups is changed
    groups = reformat_teams(groups)
    match_up_score = 0
    for x in range(ROUNDS):
        occupied = []  # TODO: fill in occupied based on which teams can't play
        courts = []
        for _ in range(COURTS_TO_USE):
            courts.append([])
        if x+1 not in WEEKS_NOT_PLAYABLE:
            fill_in_courts(courts, groups, occupied)
        for group in groups:
            for team in group:
                if len(team.history) <= x:
                    team.history += 'f'
        to_output = []
        for court in courts:
            to_output.extend(court)
        output_matrix.append(to_output)
    return match_up_score, output_matrix, groups


def fill_in_courts(courts, groups, occupied):
    """
    fills in players for all courts with some randomness
    """
    for court_id, court in enumerate(courts):
        if court:
            # Court already filled
            continue
        # find team with the least games
        least = min(team.games_played for group in groups for team in group)
        escape = False
        for i in range(20):  # pick a group at random up to 20 times to find an available team.
            if escape:  # need to break out of 3 while loops, so "escape" variable needed.
                break
            if i % 5 == 0:  # if 5 random groups don't work, be less picky (lower numbers increase randomness)
                least += 1
            group_no = random.randint(0, len(groups) - 1)
            group = groups[group_no]
            escape = False
            for team1 in group:
                if escape:
                    break
                if team1.id in occupied:  # the team is already playing
                    continue
                if team1.games_played <= least:  # if no team has played less than this one
                    if not team1.eligible_opponents:
                        team1.refresh_eligible()
                    for team2 in group:
                        if team2.id not in team1.eligible_opponents:
                            continue
                        if team2.id in occupied:
                            continue
                        if team2.games_played > least + 1:
                            continue
                        # a game shall be played between team and team2 (unless team3 can't be found)
                        opponents = [value for value in team1.eligible_opponents if value in team2.eligible_opponents]
                        #  list of possible opponents that the 2 teams can face
                        to_remove = []
                        for team in opponents:
                            if team in occupied:
                                to_remove += [team]
                            elif team == team1.id:
                                to_remove += [team]
                            elif team == team2.id:
                                to_remove += [team]
                        for team in to_remove:
                            opponents.remove(team)
                        if not opponents:
                            opponents = team1.eligible_opponents + team2.eligible_opponents
                            to_remove = []
                            for team in opponents:
                                if team in occupied:
                                    to_remove += [team]
                                elif team == team1.id:
                                    to_remove += [team]
                                elif team == team2.id:
                                    to_remove += [team]
                            for team in to_remove:
                                opponents.remove(team)
                            if not opponents:
                                break  # nobody suitable to play if team 2 chosen, try again
                        min_games = 99999
                        best_team = "error"
                        for team3 in group:
                            if team3.games_played < min_games and team3.id in opponents:
                                min_games = team3.games_played
                                best_team = team3
                        team3 = best_team
                        courts[court_id] = [
                            team1.id,
                            team2.id,
                            team3.id,
                        ]
                        occupied += extra_occupied(groups, team1)
                        occupied += extra_occupied(groups, team2)
                        occupied += extra_occupied(groups, team3)
                        team1.play(team2.id, team3.id)
                        team2.play(team1.id, team3.id)
                        team3.play(team1.id, team2.id)
                        escape = True
                        break


def find_friendlies(groups):
    """
    :return: list of matches that are friendly and not ranked along with the count
    """
    friendlies = []
    friendly_count = 0
    for group in groups:
        friendlies_in_group = []
        formal_rounds = 999999
        for team in group:
            for team2 in group:
                if team != team2:
                    formal_rounds = min(formal_rounds, team.opponents_played.count(team2.id))
        for team in group:
            for team2 in group:
                if team != team2:
                    for _ in range(team.opponents_played.count(team2.id) - formal_rounds):
                        friendlies_in_group += [[team.id, team2.id]]
                        friendly_count += 1
        friendlies += [friendlies_in_group]
    return friendlies, friendly_count/2


def get_score(groups, match_up_score, friendly_count):
    """
    given a partially calculated score, and the data structure describing the solution,
    calculate the final score
    """
    match_up_score += friendly_count/2
    min_games = min(team.games_played for group in groups for team in group)
    max_games = max(team.games_played for group in groups for team in group)
    for group in groups:
        min_g = min(team.games_played for team in group)
        max_g = max(team.games_played for team in group)
        match_up_score += (max_g - min_g) * 2
        for team in group:
            match_up_score += score_history(team.history)
            match_up_score -= team.games_played
    match_up_score += (max_games - min_games) * 5
    return match_up_score


def score_history(history):
    """
    looks at the history of a team and says how badly it does in terms of doing things back to back
    Used to minimise people playing lots of games back to back without a break and preventing long breaks for bordem
    :param history: For a team what order were the games and referees. example: 'rgfgggrfrgg'
    :return: score of how bad it is
    """
    weights = {'g': 3, 'f': 2}
    last = ''
    total_score = 0
    repetitions = 0
    for x in history:
        if x == last:
            repetitions += 1
            total_score += repetitions * weights[x]
        else:
            repetitions = 0
        last = x
    return total_score*0.05


def main():
    """
    Run the simulation and print the results
    """
    output_matrix, average_match_up_score, match_up_score, friendlies, friendly_count = run_sims(ORIGINAL_GROUPS)
    print_table(output_matrix)
    print_friendlies(friendlies)
    print(
        str(round(-match_up_score, 2)),
        "best score compared to average of :",
        str(round(-average_match_up_score, 2)),
    )
    print("There are a total of:", int(friendly_count), "friendly matches")


if __name__ == "__main__":
    main()
