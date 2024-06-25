#!/usr/bin/env python3
"""This file is the user input for David's code.

I have formatted all the variables as tab separated values to make it easy to paste from
Excel.
"""


# This is a dictionary of the leagues.
# It maps the leagues to the other leagues that can't be scheduled at the same time.
league_exclusions = """
mens1	mixed
mens2	mixed
womens1	mixed
womens2	mixed
mixed	mens1 mens2 womens1 womans2
juniors
"""

# first column is the team code
# second column is the team name
# third column is the league
teams = """
BSJ1	Basingstoke Lynx	J1
BSJ2	Basingstoke Hornets	J1
BSL1	Basingstoke Lionesses	L1
BSM1	Basingstoke Lions	M1
BSM2	Basingstoke Jaguars	M2
BSX1	Basingstoke Tigers	X1
FBJ1	Farnborough Wolves	J1
FBL1	Farnborough Pheonix	L1
FBM1	Farnborough Vipers	M1
FBM2	Farnborough Hawks	M2
FBX1	Farnborough Panthers	X1
MHL1	Maidenhead Braywick	L1
MHM1	Maidenhead Braywick	M1
MHM2	Maidenhead Magnet	M2
MHX1	Maidenhead Braywick	X1
MHX2	Maidenhead Magnet	X1
MVJ1	Maverick Juniors	J1
MVX	Maverick Mixed	X2
NBJ1	Newbury Juniors	J1
NBL1	Newbury Ladies	L1
NBM1	Newbury Mens	M2
NBM2	Newbury Juniors	M2
NBX1	Newbury Mixed	X2
OUL1	Oxford Uni Ladies	L1
OUM1	Oxford Uni Men	M2
OXL1	Oxford Falcons	L1
OXL2	Oxford Flamingoes	L1
OXM1	Oxford Vollox	M1
OXM2	Oxford Bulls	M1
OXM3	Oxford Bullox	M1
OXX1	Oxford Globetrotters	X1
RAJ1	Reading Aces Juniors A	J1
RAJ2	Reading Aces Juniors B	J1
RAL1	Reading Aces Ladies	L1
RAM1	Reading Aces Mens 1	M1
RAM2	Reading Aces Mens 2	M2
RAM3	Reading Aces Mens 3	M2
RAX1	Reading Aces Mixed 1	X1
RAX2	Reading Aces Mixed 2	X2
SBJ1	South Bucks Juniors	J1
SBL1	South Bucks Ladies	L1
SPL1	Spikeopaths Ladies	L1
SPM1	Spikeopaths Mens 1	M1
SPM2	Spikeopaths Mens 2	M1
SPX1	Spikeopaths Mixed 1	X1
SPX2	Spikeopaths Mixed 2	X2
SPX3	Spikeopaths Mixed 3	X2
WEM1	Wycombe Eagles	M2
WEX1	Wycombe Eagles	X2
"""

team_unavailability = """
BSM1	2
BSM1	3
BSM1	6
BSM1	10
FBJ1	10
BSL1	2
BSL1	10
MHL1	24
OUL1	9
OUL1	10
OUL1	11
OUL1	14
OUL1	23
OUL1	24
OUL1	25
OUL1	26
OUL1	28
FBL1	1
FBL1	11
SBL1	6
SBL1	8
SBL1	10
SBL1	11
SBL1	15
SBL1	18
SBL1	20
SBL1	28
SBL1	29
SBL1	30
BSM2	8
BSM2	28
OUM1	1
OUM1	9
OUM1	10
OUM1	11
OUM1	14
OUM1	23
OUM1	24
OUM1	25
OUM1	26
OUM1	28
WEM1	3
WEM1	6
WEM1	7
WEM1	10
WEM1	18
WEM1	19
WEX1	3
WEX1	6
WEX1	7
WEX1	10
WEX1	18
WEX1	19
MHX1	24
MHX2	24
"""

venues = """
BS1	Basingstoke
FB1	Farnborough
MH1	Maidenhead
MV1	Mavericks
NB1	Newbury
OU1	Oxford Uni
OX1	Oxford
RA1	Reading Aces
SB1	South Bucks
SP1	Spikeopaths
SP2	Spikeopaths
"""

venue_unavailability = """
BS1	10
FB1	11
MV1	15
MV1	16
MV1	17
MV1	18
MV1	19
MV1	20
MV1	21
MV1	22
MV1	23
MV1	25
MV1	28
MV1	29
MV1	30
"""

weeks_no_one_can_play = """
12
13
27
"""

week_to_date = """
1	Sun 09-Oct-22
2	Sun 16-Oct-22
3	Sun 23-Oct-22
4	Sun 30-Oct-22
5	Sun 06-Nov-22
6	Sun 13-Nov-22
7	Sun 20-Nov-22
8	Sun 27-Nov-22
9	Sun 04-Dec-22
10	Sun 11-Dec-22
11	Sun 18-Dec-22
12	Sun 25-Dec-22
13	Sun 01-Jan-23
14	Sun 08-Jan-23
15	Sun 15-Jan-23
16	Sun 22-Jan-23
17	Sun 29-Jan-23
18	Sun 05-Feb-23
19	Sun 12-Feb-23
20	Sun 19-Feb-23
21	Sun 26-Feb-23
22	Sun 05-Mar-23
23	Sun 12-Mar-23
24	Sun 19-Mar-23
25	Sun 26-Mar-23
26	Sun 02-Apr-23
27	Sun 09-Apr-23
28	Sun 16-Apr-23
29	Sun 23-Apr-23
30	Sun 30-Apr-23
"""

# Using pre-made triangles simplifies some of the work of deciding who to schedule when
pre_made_triangles = {
    5: [[1, 2, 3], [3, 4, 5], [4, 2, 1], [5, 3, 1], [4, 5, 2], [1, 3, 4], [2, 5, 3], [5, 1, 4], [2, 1, 5], [3, 4, 2]],
    6: [
        [1, 2, 3],
        [4, 5, 6],
        [1, 2, 4],
        [3, 5, 6],
        [1, 5, 2],
        [3, 4, 6],
        [6, 4, 1],
        [5, 3, 2],
        [5, 3, 1],
        [2, 6, 4],
        [3, 4, 5],
        [6, 2, 1],
        [6, 1, 3],
        [2, 3, 4],
        [4, 1, 5],
        [2, 6, 5],
    ],
    7: [
        [1, 3, 2],
        [7, 6, 4],
        [4, 1, 5],
        [6, 3, 2],
        [1, 7, 2],
        [3, 5, 6],
        [2, 6, 4],
        [3, 7, 5],
        [5, 2, 7],
        [4, 1, 6],
        [7, 4, 3],
        [1, 2, 5],
        [6, 7, 1],
        [3, 5, 4],
        [2, 5, 6],
        [7, 1, 3],
        [4, 2, 3],
        [5, 6, 7],
        [2, 4, 7],
        [6, 3, 1],
        [5, 4, 1],
    ],
    8: [
        [3, 8, 2],
        [7, 4, 1],
        [2, 5, 7],
        [8, 1, 4],
        [7, 3, 1],
        [4, 2, 6],
        [5, 7, 8],
        [1, 3, 2],
        [3, 4, 5],
        [1, 2, 8],
        [5, 1, 6],
        [4, 8, 7],
        [6, 7, 3],
        [2, 4, 5],
        [3, 5, 4],
        [2, 7, 6],
        [8, 6, 3],
        [6, 5, 1],
        [4, 6, 8],
        [8, 6, 5],
    ],
    9: [
        [1, 2, 3],
        [9, 8, 4],
        [5, 6, 7],
        [1, 4, 6],
        [7, 8, 2],
        [5, 9, 3],
        [5, 1, 8],
        [3, 4, 7],
        [6, 2, 9],
        [9, 7, 1],
        [2, 4, 5],
        [8, 6, 3],
        [2, 3, 4],
        [6, 7, 8],
        [9, 5, 1],
        [7, 5, 2],
        [4, 1, 6],
        [3, 8, 9],
        [2, 9, 6],
        [1, 3, 7],
        [4, 5, 8],
        [8, 2, 1],
        [3, 6, 5],
        [4, 7, 9],
    ],
    10: [
        [6, 1, 4],
        [10, 5, 2],
        [9, 7, 3],
        [1, 9, 5],
        [6, 2, 7],
        [3, 8, 10],
        [10, 7, 1],
        [9, 4, 3],
        [5, 6, 8],
        [5, 3, 6],
        [8, 7, 4],
        [2, 10, 9],
        [1, 8, 5],
        [4, 10, 6],
        [3, 1, 8],
        [2, 4, 5],
        [7, 6, 9],
        [8, 6, 2],
        [5, 3, 7],
        [10, 4, 1],
        [7, 5, 10],
        [4, 9, 8],
        [1, 2, 3],
        [5, 6, 9],
        [7, 8, 2],
        [9, 2, 1],
        [3, 10, 6],
        [4, 5, 7],
        [8, 9, 10],
        [2, 3, 4],
        [6, 1, 7],
    ],
    11: [
        [1, 2, 3],
        [7, 5, 6],
        [10, 11, 9],
        [3, 7, 11],
        [8, 4, 6],
        [2, 1, 10],
        [4, 5, 3],
        [2, 6, 10],
        [1, 8, 11],
        [7, 8, 9],
        [1, 4, 6],
        [10, 11, 3],
        [10, 1, 7],
        [9, 3, 6],
        [8, 2, 5],
        [8, 10, 3],
        [5, 9, 1],
        [4, 7, 2],
        [5, 10, 4],
        [3, 9, 2],
        [11, 6, 7],
        [9, 10, 4],
        [6, 1, 3],
        [2, 5, 11],
        [2, 6, 8],
        [4, 1, 11],
        [3, 5, 7],
        [9, 1, 7],
        [8, 3, 4],
        [6, 5, 10],
        [9, 8, 5],
        [4, 7, 2],
        [5, 8, 1],
        [6, 4, 9],
        [5, 6, 11],
        [7, 8, 10],
        [9, 11, 2],
        [8, 4, 11],
    ],
    12: [
        [1, 3, 10],
        [2, 11, 12],
        [7, 9, 4],
        [8, 5, 6],
        [4, 5, 1],
        [10, 6, 2],
        [11, 3, 7],
        [8, 9, 12],
        [6, 1, 4],
        [3, 2, 5],
        [9, 10, 7],
        [11, 8, 12],
        [7, 11, 1],
        [6, 2, 8],
        [3, 12, 5],
        [4, 9, 10],
        [8, 1, 11],
        [2, 5, 7],
        [6, 9, 3],
        [10, 4, 12],
        [1, 10, 12],
        [2, 7, 3],
        [11, 4, 6],
        [9, 8, 5],
        [2, 1, 9],
        [4, 3, 8],
        [5, 10, 11],
        [7, 6, 12],
        [1, 3, 12],
        [10, 2, 8],
        [5, 7, 4],
        [11, 9, 6],
        [8, 7, 1],
        [4, 11, 2],
        [10, 6, 3],
        [5, 9, 12],
        [1, 6, 5],
        [2, 12, 4],
        [3, 11, 9],
        [7, 8, 10],
        [9, 1, 2],
        [8, 3, 4],
        [10, 11, 5],
        [12, 6, 7],
    ],
}
