"""This tests the code in volleyball_scheduling2.py."""

import volleyball_scheduling2


def test_main():
    """This test just checks that main does not crash."""
    volleyball_scheduling2.main()


def test_parse_week_to_date():
    week_to_date_str = """
    1	Sun 09-Oct-22
    2	Sun 16-Oct-22
    3	Sun 23-Oct-22
    """
    week_to_date = volleyball_scheduling2.parse_week_to_date(week_to_date_str)
    assert week_to_date == {
        1: "Sun 09-Oct-22",
        2: "Sun 16-Oct-22",
        3: "Sun 23-Oct-22",
    }


def test_parse_weeks_no_one_can_play():
    weeks_no_one_can_play_str = """
    12
    13
    27
    """
    weeks_no_one_can_play = volleyball_scheduling2.parse_weeks_no_one_can_play(weeks_no_one_can_play_str)
    assert weeks_no_one_can_play == {12, 13, 27}


def test_parse_leagues():
    leagues_str = """
    mens1	mixed
    mens2	mixed
    womens1	mixed
    womens2	mixed
    mixed	mens1 mens2 womens1 womans2
    juniors
    """
    leagues = volleyball_scheduling2.parse_leagues(leagues_str)
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
    BSJ1	Basingstoke Lynx	J1	Basingstoke
    BSJ2	Basingstoke Hornets	J1	Basingstoke
    BSL1	Basingstoke Lionesses	L1	Basingstoke
    BSM1	Basingstoke Lions	M1	Basingstoke
    BSM2	Basingstoke Jaguars	M2	Basingstoke
    RAX1	Reading Aces Mixed 1	X1	Reading Aces
    RAX2	Reading Aces Mixed 2	X2	Reading Aces
    SPX3	Spikeopaths Mixed 3	X2	Spikeopaths
    WEM1	Wycombe Eagles	M2	Wycombe
    WEX1	Wycombe Eagles	X2	Wycombe
    """
    teams, clubs = volleyball_scheduling2.parse_teams(teams_str)
    assert teams == {
        "BSJ1": {"name": "Basingstoke Lynx", "league": "J1", "club": "Basingstoke"},
        "BSJ2": {"name": "Basingstoke Hornets", "league": "J1", "club": "Basingstoke"},
        "BSL1": {"name": "Basingstoke Lionesses", "league": "L1", "club": "Basingstoke"},
        "BSM1": {"name": "Basingstoke Lions", "league": "M1", "club": "Basingstoke"},
        "BSM2": {"name": "Basingstoke Jaguars", "league": "M2", "club": "Basingstoke"},
        "RAX1": {"name": "Reading Aces Mixed 1", "league": "X1", "club": "Reading Aces"},
        "RAX2": {"name": "Reading Aces Mixed 2", "league": "X2", "club": "Reading Aces"},
        "SPX3": {"name": "Spikeopaths Mixed 3", "league": "X2", "club": "Spikeopaths"},
        "WEM1": {"name": "Wycombe Eagles", "league": "M2", "club": "Wycombe"},
        "WEX1": {"name": "Wycombe Eagles", "league": "X2", "club": "Wycombe"},
    }
    assert clubs == {"Basingstoke": {}, "Reading Aces": {}, "Spikeopaths": {}, "Wycombe": {}}


def test_parse_team_unavailability():
    team_unavailability_str = """
    BSM1	2
    BSM1	3
    BSM1	6
    BSM1	10
    FBJ1	10
    """
    team_unavailability = volleyball_scheduling2.parse_team_unavailability(team_unavailability_str)
    assert team_unavailability == {
        "BSM1": {2, 3, 6, 10},
        "FBJ1": {10},
    }


def test_get_team_availability():
    teams = {"BSM1": {}, "FBJ1": {}, "fake": {}}
    team_unavailability = {
        "BSM1": {2, 3, 6, 10},
        "FBJ1": {10},
    }
    team_availabilty = volleyball_scheduling2.get_team_availability(teams, team_unavailability, 10, {4, 5})
    assert team_availabilty == {
        "BSM1": {"availability": {1, 7, 8, 9}},
        "FBJ1": {"availability": {1, 2, 3, 6, 7, 8, 9}},
        "fake": {"availability": {1, 2, 3, 6, 7, 8, 9, 10}},
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
        "BS1": {"club": "Basingstoke"},
        "FB1": {"club": "Farnborough"},
        "OU1": {"club": "Oxford Uni"},
        "OX1": {"club": "Oxford"},
        "SP1": {"club": "Spikeopaths"},
        "SP2": {"club": "Spikeopaths"},
    }


def test_parse_venues_unavailability():
    venues_unavailability_str = """
    BS1	10
    FB1	11
    MV1	15
    MV1	29
    MV1	30
    """
    venue_unavailability = volleyball_scheduling2.parse_venues_unavailability(venues_unavailability_str)
    assert venue_unavailability == {"BS1": {10}, "FB1": {11}, "MV1": {15, 29, 30}}


def test_get_venue_availability():
    venues = {"BS1": {}, "FB1": {}, "MV1": {}, "fake": {}}
    venue_unavailability = {"BS1": {10}, "FB1": {1}, "MV1": {9, 3}}
    venues = volleyball_scheduling2.get_venue_availability(venues, venue_unavailability, 10, {4, 5})
    assert venues == {
        "BS1": {"availability": {1, 2, 3, 6, 7, 8, 9}},
        "FB1": {"availability": {2, 3, 6, 7, 8, 9, 10}},
        "MV1": {"availability": {1, 2, 6, 7, 8, 10}},
        "fake": {"availability": {1, 2, 3, 6, 7, 8, 9, 10}},
    }
