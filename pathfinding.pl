adjacent(X, Y, X, Y1) :- Y1 is Y + 1.
adjacent(X, Y, X, Y1) :- Y1 is Y - 1.
adjacent((X, Y), (X1, Y)) :- X1 is X + 1.
adjacent((X, Y), (X1, Y)) :- X1 is X - 1.
adjacent((X, Y), (X, Y1)) :- Y1 is Y + 1.
adjacent((X, Y), (X, Y1)) :- Y1 is Y - 1.

valid_cell((X, Y), Width, Height) :-
    X >= 0, X < Width,
    Y >= 0, Y < Height.

walkable((X, Y), Maze) :-
    nth0(Y, Maze, Row),
    nth0(X, Row, Cell),
    Cell =:= 0.

find_path(Start, Goal, Maze, Width, Height, Path) :-
    bfs([(Start, [Start])], Goal, Maze, Width, Height, Path).

bfs([(Goal, RevPath)|_], Goal, _, _, _, Path) :-
    reverse(RevPath, Path).
bfs([((X, Y), P)|Queue], Goal, Maze, Width, Height, Path) :-
    findall(
        (Next, [Next|(X, Y)|P]),
        (
            adjacent((X, Y), Next),
            valid_cell(Next, Width, Height),
            walkable(Next, Maze),
            \+ memberchk((Next, _), Queue),
            \+ memberchk(Next, P)
        ),
        NeighPairs
    ),
    append(Queue, NeighPairs, NewQueue),
    bfs(NewQueue, Goal, Maze, Width, Height, Path).

solve_maze(StartX, StartY, GoalX, GoalY, Maze, Width, Height, Path) :-
    find_path((StartX, StartY), (GoalX, GoalY), Maze, Width, Height, Path).
