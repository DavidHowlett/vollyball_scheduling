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



Solution Scoring
----------------

- More games are good.
- all teams (across leagues) should have a similar number of games.
- Friendlies are bad (but not very bad).
- Each team in a league should 'host' a similar amount of times.
- It is better to have games happen earlier in the season than later.


Allowed Simplifications
-----------------------

- It is permissible to not find the optimal solution. There are many solutions that are good enough in practice.
- It is permissible to accept as input a list of triangles to be scheduled


Other Goals
-----------

- The data input format and data output format should be copy paste-able from and to google sheets. This probably means
tab separated lines.

Outstanding questions
---------------------

- When does the next season start? I wonder when the deadline is for the program working well.
- Can we score each team on it's average score against each other team?
  - This would mean that are no more friendlies.
  - We could efficiently pack in more games per season without imbalances caused by who got scheduled with who.
- Are the team codes (like OXM2) customer facing? I don't want to change things that would annoy teams.
- How many triangles can be scheduled at one venue in one weekend?
