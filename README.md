-------------------------------------------------------------------------------
# Halite Bot Project 2022
# The SBI team

![Screenshot from 2022-06-28 22-29-31](https://user-images.githubusercontent.com/51510817/176270236-5e8fb08f-cde9-4149-82dc-5df039878410.png)

-------------------------------------------------------------------------------
Members:<br>
    - Dinu Ion-Irinel - ion_irinel.dinu@stud.acs.upb.ro<br>
    - Pana Sergiu-Laurentiu - sergiu.pana@stud.acs.upb.ro<br>
    - Serban Bianca-Sanziana - bianca.serban2506@stud.acs.upb.ro<br>

-------------------------------------------------------------------------------
## Running instructions:
    - run source: python3 MyBot.py
    - running script against PA team bots:
        python3 ./run.py --cmd "python3 MyBot.py"
    - running in a custom scenario:
        - the parameters in the "run_game.sh" script change, depending
        preferences (bots against which the match is played, map size)
        ./run_game.sh

-------------------------------------------------------------------------------
## Details about the project structure:
    - "MyBot.py" - the entry-point of the bot, contains the assignment of movements
    - "BotHelpers.py" - contains the implementation help functions
    bot logic<
    - "hlt.py" - contains the functions that describe the state of the game
    - Makefile - contains the run rule
    - README - contains details about implementation and structure

-------------------------------------------------------------------------------
## Responsibility of each team member:<br>
In the first phase, each member came up with ideas that we put together,
and then I optimized / modified / gave up / added ideas, as
we ran into other problems / bugs and had to find new ways
through which our bot can perform
We all worked together most of the time, sitting on calls on
different platforms, each member having an equal contribution on the project.

-------------------------------------------------------------------------------
## Ideas that stood out:<br>
- Determining the ideal direction depending on strength and production.<br>
- If two allied squares are in danger of attacking each other
when the sum of their strengths exceeds the maximum, they should go
in the same direction.<br>
- Treatment with priority of squares that have the maximum strength.<br>
- Guide squares with a strength of less than 255 depending on
those with a strength equal to 255.<br>

-------------------------------------------------------------------------------
## Move execution logic:<br>
- The moves that the squares will make are determined first
with maximum strength, thus<br>
    -> if he has another neighbor with maximum strength, they will both move
    in the same direction.<br>
    -> if not, try to check the optimal move of a function
    of heuristics (ratio between production and strength)<br>
    -> if the optimal move was found (the current square is on
    edge), that move will be made<br>
    -> if the move was not found, we go to the nearest square
    unoccupied by us<br>

- It is then determined the moves that the squares that do not have will make
maximum strength, thus<br>
    -> if their strength is equal to 0 or 5 times less than
    the production of that square stands still to accumulate strength<br>
    -> we check if there is an ally among the neighbors of this square
    whose strength is maximum, in which case we want to avoid them
    intersect.<br>
    -> either the two squares swap (if the little one can't
    to attack), or the little one moves in the previously calculated direction of the one
    big.<br>
    -> if the small square does not have a neighbor with maximum strength, it will
    calculate the optimal direction and will check if he can conquer it or not.<br>
    -> if he can't, he will stand still to accumulate strength.<br>
    -> if he can, he will conquer it.<br>

-------------------------------------------------------------------------------
## Implemented functions:
- get_move - assigns the move to the current square (only for
squares with strenght other than 255)<br>
- get_move_max - assigns the move to the current square (only for
squares with strength equal to 255)<br>
- check_neighbor_diagonal - check if a square is given as a parameter
is a neighbor on the diagonal of the square on which the function is called<br>
- find_nearest_enemy_direction - find the nearest enemy square or
neutral, in one of the four cardinal directions<br>
- heuristic - calculates the efficiency of the square, determining the ratio
production / strength, if this ratio is possible<br>
            - if not possible, the maximum potential damage is calculated
            taking into account the overkill feature of the game<br>
- find_allied_neighbours - returns a list of all your allied neighbors
the given square, including the neighbors on the diagonal.<br>
- find_all_neighbours - returns a list of all neighbors of a square,
including those on the diagonal, regardless of owner<br>
- find_neighbour_list_enemy - build the list of enemy neighbors on
the cardinal directions of the given square as a parameter<br>
- get_direction_to_square - returns the direction it should follow
the given square as a parameter to reach the given given square as
parameter<br>
-------------------------------------------------------------------------------
## Sources of inspiration:
 The official forum (http://2016.forums.halite.io/) represented the point of
 start for the project.

## Useful Links:
https://2016.halite.io/rules_game.html<br>
http://2016.forums.halite.io/t/so-youve-improved-the-random-bot-now-what/482.html<br>
https://2016.halite.io/basics_improve_random.html<br>
