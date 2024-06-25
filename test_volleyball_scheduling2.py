"""This tests the code in volleyball_scheduling2.py."""

import volleyball_scheduling2


def test_parse_leagues():
    leagues = volleyball_scheduling2.parse_leagues(
        """
mens1	mixed
mens2	mixed
womens1	mixed
womens2	mixed
mixed	mens1 mens2 womens1 womans2
juniors
"""
    )
    assert leagues == {
        "mens1": ["mixed"],
        "mens2": ["mixed"],
        "womens1": ["mixed"],
        "womens2": ["mixed"],
        "mixed": ["mens1", "mens2", "womens1", "womans2"],
        "juniors": [],
    }


def test_parse_teams():
    teams_str = """
BSJ1	Basingstoke Lynx	J1
BSJ2	Basingstoke Hornets	J1
BSL1	Basingstoke Lionesses	L1
BSM1	Basingstoke Lions	M1
BSM2	Basingstoke Jaguars	M2
"""
    teams = volleyball_scheduling2.parse_teams(teams_str)
    assert teams == {
        "BSJ1": {"name": "Basingstoke Lynx", "league": "J1"},
        "BSJ2": {"name": "Basingstoke Hornets", "league": "J1"},
        "BSL1": {"name": "Basingstoke Lionesses", "league": "L1"},
        "BSM1": {"name": "Basingstoke Lions", "league": "M1"},
        "BSM2": {"name": "Basingstoke Jaguars", "league": "M2"},
    }


def test_parse_team_unavailability():
    teams = {
        "BSJ2": {"name": "Basingstoke Lynx", "league": "J1"},
        "FBJ1": {"name": "Basingstoke Hornets", "league": "J1"},
        "BSM1": {"name": "Basingstoke Lionesses", "league": "L1"},
    }
    team_unavailability_str = """
BSM1	2
BSM1	3
BSM1	6
BSM1	10
FBJ1	10
"""
    teams = volleyball_scheduling2.parse_team_unavailability(teams, team_unavailability_str)
    assert teams == {
        "BSM1": {"name": "Basingstoke Lionesses", "league": "L1", "unavailability": {2, 3, 6, 10}},
        "FBJ1": {"name": "Basingstoke Hornets", "league": "J1", "unavailability": {10}},
        "BSJ2": {"name": "Basingstoke Lynx", "league": "J1", "unavailability": set()},
    }


def test_parse_venues():
    venues_str = """
    BS1	Basingstoke
    FB1	Farnborough
    OU1	Oxford Uni
    OX1	Oxford
    SP1	Spikeopaths
    SP2	Spikeopaths
    """
    venues = volleyball_scheduling2.parse_venues(venues_str)
    assert venues == {
        "Basingstoke": {"BS1"},
        "Farnborough": {"FB1"},
        "Oxford Uni": {"OU1"},
        "Oxford": {"OX1"},
        "Spikeopaths": {"SP1", "SP2"},
    }
