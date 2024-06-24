Problem statement
=================

Situation
---------

- Each year there is one volleyball season in southern England.
- Andrew Tatarek schedules all competitive volleyball matches for a season at the start of the season.
- Volleyball matches happen at weekends.
- Each weekend in a year is numbered sequentially starting from 1.
    - This may not line up with the beginning of the year but this doesn't matter for solving the problem.

- There are one or more leagues
- There are one or more clubs
- Each club has one or more teams
- Each team is connected with one club
- Each club has 0 or more home locations. Most clubs have 1 home location.
- Each team is a member of 1 league
- Each league has 3 or more teams.
- A match consists of an unordered set of 2 teams and a team that works as the referee
- To save on traveling it is common practice to schedule three matches between three teams on one weekend at one location. This is referred to as a triangle.
- For each match in a triangle, the team that is not playing is the ref
- Each triangle must be scheduled on one weekend at one location
- Each triangle must be scheduled at one of the home locations of one of it's members
- A triangle consists of an unordered set of 3 teams from the same league.
- A season has many triangles (about 70)
- A season can contain duplicate triangles with the same teams in.

- Team names have the following format: XXYZ where XX is club, Y is type (M= Mens, X=miXed, L=Ladies, J=Juniors), Z is for when there is multiple of the same type at the same club.

- A team is forbidden to play twice in one weekend
- Clubs can have a few types of second venue
  - Physical second venue
  - Two matches on one day
  - One match Saturday one match Sunday
  - I should not care what the second venue type is


Program inputs
--------------

- The length of the season is expressed as an integer number of weeks
- Lookup table between week number and date
- List of leagues
  - For each league a list of other leagues it can't play at the same time as
- List of clubs
  - For each club a list of teams
  - For each club a list of venues
    - For each venue there is a list of weeks they can't do
- List of teams
  - For each team there is a list of dates they can't do
- For each number of teams in a league, there will be a lookup table for the triangles.


Program output
--------------

- Main output will be a team focused table:
  - Teams on the left
  - Dates at the top
  - Total number of games per team on the right
  - The bulk of the table will be a venue if there is a game and "." if there is no game
- Second output will be a match focused table. Each triangle will be three grouped rows.
  - The second two rows should be the matches played by the home team
  - The columns in order are:
    - League
    - Unique match code (This will be of the format: M101A)
    - Venue
    - Team 1
    - Team 2
- Third output is a list of the triangles that were not scheduled


Solution Scoring
----------------

- More games played is better
- All teams (across leagues) should have a similar number of games.
- Friendlies are bad (but not very bad).
- Each club should have a number of home games roughly proportional to the number of teams it has (more important)
- Each team in a league should 'host' a similar amount of times (less important)
- It is better to have games happen earlier in the season than later.


Allowed Simplifications
-----------------------

- It is permissible to not find the optimal solution. There are many solutions that are good enough in practice.
- It is permissible to accept as input a list of triangles to be scheduled


Other Goals
-----------

- The data input format and data output format should be copy-paste-able from and to google sheets. This probably means
tab separated lines.

Outstanding questions
---------------------

- When does the next season start? I wonder when the deadline is for the program working well.
  - Volleyball season is October - April
  - Answer: Teams are picked in August
- Can we score each team on it's average score against each other team?
  - This would mean that are no more friendlies.
  - We could efficiently pack in more games per season without imbalances caused by who got scheduled with who.
  - Answer: It is preferable to have a preset number of games as the input (e.g. each team plays 2 games)
- Are the team codes (like OXM2) customer facing? I don't want to change things that would annoy teams.
- How many triangles can be scheduled at one venue in one weekend?