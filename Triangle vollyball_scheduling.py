"""
Andrew Tatarek asked me to help organize a volleyball tournament. Given a set of groups of teams called ORIGINAL_GROUPS
I need to assign which 3 teams will play each other for each court for each round.

The code in this file was written Michael Howlett building on code written by Michael, Robert, and David Howlett.
To enable easy deployment, we put all the logic in a single file so that it can be pasted into
https://www.w3schools.com/python/trypython.asp?filename=demo_ref_min
so that users don't need to install python and deal with the issues associated with that.

TODO: make there a preference for a team to play on home turf
      implement a "team cant play" defined by user to account for a team having a birthday and not wanting to play
"""

import copy
import random
from typing import List

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
NUM_OF_COURTS = len(BASES)
WEEKS_NOT_PLAYABLE = [11, 12, 13]
total = 0
for group in ORIGINAL_GROUPS:
    total += int(len(group) / 3)
COURTS_TO_USE = min(NUM_OF_COURTS, total)

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
        print(team.id, " doesn't follow correct formatting and is of unknown type")
        print("The type read is currently: ", team_type,
              "  but needs to be one of M (mens), L (ladies), J (juniors), X (mixed), S (single)")
        exit()
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
    best_groups_info = []
    average_match_up_score = 0
    best_friendly_count = 0
    for _ in range(NUM_OF_SIMULATION):  # run the setup "NUM_OF_SIMULATION" times and picks best
        # Michael found another bug which crashes the code once every few hundred games.
        # where if for all teams the [teams they can play against] are already playing someone else, no game gets
        # added causing an empty court and a crash. Due to rarity, we just catch the error and continue.
        match_up_score, output_matrix, result_groups, groups_info = run_sim(copy.deepcopy(groups))
        friendlies, friendly_count = find_friendlies(result_groups)
        match_up_score = get_score(result_groups, match_up_score, friendly_count)
        if match_up_score < best_match_up_score:
            best_match_up_score = match_up_score
            best_output_matrix = output_matrix
            best_friendlies = friendlies
            best_friendly_count = friendly_count
            best_groups_info = groups_info
        average_match_up_score += match_up_score / NUM_OF_SIMULATION
    return best_output_matrix, average_match_up_score, best_match_up_score, \
        best_friendlies, best_friendly_count, best_groups_info


def run_sim(groups):
    """
    generate a single solution and partially scores it
    """
    output_matrix = []
    # at this point in the calculation the number format of groups is changed
    groups = reformat_teams(groups)
    groups_info = []  # list where each item is for a group. group is a dict containing {number of games: [pairs]}
    for group in groups:
        pairings = []
        for i, team1 in enumerate(group):
            for j, team2 in enumerate(group):
                if j == i:  # don't include teams facing themselves and have only one of a vs b, and b vs a
                    break
                pairings.append([team1.id, team2.id])
        groups_info.append({0: pairings, 1: []})  # each pairing has been played 0 times.
    match_up_score = 0
    for x in range(ROUNDS):
        occupied = []  # TODO: fill in occupied based on which teams can't play
        courts = []
        for _ in range(COURTS_TO_USE):
            courts.append([])
        if x + 1 not in WEEKS_NOT_PLAYABLE:
            fill_in_courts(courts, groups, occupied, groups_info)
        for group_id, group in enumerate(groups):
            for team in group:
                if len(team.history) <= x:
                    team.history += 'f'
            for pairs_list in groups_info[group_id]:
                if groups_info[group_id][pairs_list]:
                    random.shuffle(groups_info[group_id][pairs_list])
            if groups_info[group_id][len(groups_info[group_id]) - 1]:
                # groups_info[group_id][2] = []
                groups_info[group_id][len(groups_info[group_id])] = []
        to_output = []
        for court in courts:
            to_output.extend(court)
        output_matrix.append(to_output)
    # print(groups_info)
    return match_up_score, output_matrix, groups, groups_info


def fill_in_courts(courts, groups, occupied, groups_info):
    """
    fills in players for all courts with some randomness
    """
    # find team with the least games
    least = min(team.games_played for group in groups for team in group)
    desperation = 0  # how desperate you are to find a match
    escape = True
    for court_id, court in enumerate(courts):
        # random.seed(10)  # RANDOM SEED RANDOM SEED RANDOM SEED RANDOM SEED RANDOM SEED RANDOM SEED RANDOM SEED
        if court:
            # Court already filled
            continue
        if not escape:  # if it couldn't find a successful match despite many attempts
            break
        escape = False
        failed_groups = []
        for i in range(200):  # pick a group at random up to 20 times to find an available team.
            if escape:  # need to break out of 3 while loops, so "escape" variable needed.
                break
            if (i + 1) % 10 == 0:  # if 5 random groups don't work, be less picky (lower numbers increase randomness)
                desperation += 1
                failed_groups = []
            group_no = random.randint(0, len(groups) - 1)
            if group_no in failed_groups:  # don't try a group again until desperation increases (as it will fail).
                continue
            failed_groups.append(group_no)  # assume group will fail, will be corrected if it doesn't
            group = groups[group_no]
            escape = False
            min_pairs = -(desperation + 1)  # pick on pairs with least games played
            for j in groups_info[group_no]:  # j = number of times each of the pairs have played each other.
                if escape:
                    break
                if groups_info[group_no][j]:
                    min_pairs += 1
                    if min_pairs > 0:
                        break
                    for pair in groups_info[group_no][j]:
                        if pair[0] in occupied or pair[1] in occupied:
                            continue
                        team1, team2 = 'error', 'error'  # stops pycharm whinging
                        for team1 in group:
                            if team1.id == pair[0]:
                                break
                        for team2 in group:
                            if team2.id == pair[1]:
                                break
                        if team1.games_played + team2.games_played >= (least * 2) + desperation:
                            continue  # look for teams who have played less games
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
                        opponents_dict = {}  # there must be a better way of picking the team with most copies
                        for team in opponents:
                            if team in opponents_dict:
                                opponents_dict[team] += 1
                            else:
                                opponents_dict[team] = 1
                        max = 0
                        best_team = "error"  # to be overwritten
                        for team in opponents_dict:
                            if opponents_dict[team] > max:
                                max = opponents_dict[team]
                                best_team = team
                        for team in group:
                            if team.id == best_team:
                                best_team = team
                                break
                        team3 = best_team  # we finally have decided on a match
                        courts[court_id] = [
                            team1.id,
                            team2.id,
                            team3.id,
                        ]
                        failed_groups.remove(group_no)
                        occupied += extra_occupied(groups, team1)  # as team is occupied, it can't play again this round
                        occupied += extra_occupied(groups, team2)  # preventing double booking.
                        occupied += extra_occupied(groups, team3)
                        team1.play(team2.id, team3.id)
                        team2.play(team1.id, team3.id)
                        team3.play(team1.id, team2.id)
                        group_matches = groups_info[group_no]
                        pairs = [[team1.id, team2.id],  # pairs which could be in groups_info
                                 [team2.id, team3.id], [team3.id, team2.id],
                                 [team1.id, team3.id], [team3.id, team1.id]]
                        for x in group_matches:
                            index = 0
                            while index < len(pairs):
                                if pairs[index] in group_matches[x]:
                                    # increase number of matches between that pair by 1
                                    group_matches[x].remove(pairs[index])
                                    group_matches[x + 1].append(pairs[index])
                                    pairs.remove(pairs[index])
                                    index += -1
                                index += 1
                        escape = True  # move on to next court
                        break


def find_friendlies(groups):
    """
    could be made more efficient by using groups_info, but I can't be bothered
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
    return friendlies, friendly_count / 2


def get_score(groups, match_up_score, friendly_count):
    """
    given a partially calculated score, and the data structure describing the solution,
    calculate the final score
    """
    match_up_score += friendly_count * 2
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
    return total_score * 0.05


def main():
    """
    Run the simulation and print the results
    """
    output_matrix, average_match_up_score, match_up_score, friendlies, friendly_count, info = run_sims(ORIGINAL_GROUPS)
    for group in info:
        print(group)
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
