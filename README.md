-------------------------------------------------------------------------------
## Halite Bot Project 2022
## The SBI team

-------------------------------------------------------------------------------
Members:<br>
    - Dinu Ion-Irinel - ion_irinel.dinu@stud.acs.upb.ro<br>
    - Pana Sergiu-Laurentiu - sergiu.pana@stud.acs.upb.ro<br>
    - Serban Bianca-Sanziana - bianca.serban2506@stud.acs.upb.ro<br>

-------------------------------------------------------------------------------
# Running instructions:
    - run source: python3 MyBot.py
    - running script against PA team bots:
        python3 ./run.py --cmd "python3 MyBot.py"
    - running in a custom scenario:
        - the parameters in the "run_game.sh" script change, depending
        preferences (bots against which the match is played, map size)
        ./run_game.sh

-------------------------------------------------------------------------------
# Details about the project structure:
    - "MyBot.py" - the entry-point of the bot, contains the assignment of movements
    - "BotHelpers.py" - contains the implementation help functions
    bot logic<
    - "hlt.py" - contains the functions that describe the state of the game
    - Makefile - contains the run rule
    - README - contains details about implementation and structure

-------------------------------------------------- ----------------------------
# Responsibility of each team member:<br>
In the first phase, each member came up with ideas that we put together,<br>
and then I optimized / modified / gave up / added ideas, as<br>
we ran into other problems / bugs and had to find new ways
through which our bot can perform<br>
We all worked together most of the time, sitting on calls on
disagreement, each member having an equal contribution on the project.

    -------------------------------------------------- ----------------------------
Ideas that stood out:
    - Determining the ideal direction depending on strength and production.
    - If two allied squares are in danger of attacking each other
    when the sum of their strengths exceeds the maximum, they should go
    in the same direction.
    - Treatment with priority of squares that have the maximum strength.
    - Guide squares with a strength of less than 255 depending on
    those with a strength equal to 255.

-------------------------------------------------- ----------------------------
Move execution logic:
    - The moves that the squares will make are determined first
    with maximum strength, thus
        -> if he has another neighbor with maximum strength, they will both move
        in the same direction.
        -> if not, try to check the optimal move of a function
        of heuristics (ratio between production and strength)
        -> if the optimal move was found (the current square is on
        edge), that move will be made
        -> if the move was not found, we go to the nearest square
        unoccupied by us

    - It is then determined the moves that the squares that do not have will make
    maximum strength, thus
        -> if their strength is equal to 0 or 5 times less than
        the production of that square stands still to accumulate strength
        -> we check if there is an ally among the neighbors of this square
        whose strength is maximum, in which case we want to avoid them
        intersect.
        -> either the two squares swap (if the little one can't
        to attack), or the little one moves in the previously calculated direction of the one
        big.
        -> if the small square does not have a neighbor with maximum strength, it will
        calculate the optimal direction and will check if he can conquer it or not.
        -> if he can't, he will stand still to accumulate strength.
        -> if he can, he will conquer it.

-------------------------------------------------- ----------------------------
Implemented functions:
    - get_move - assigns the move to the current square (only for
    squares with strenght other than 255)
    - get_move_max - assigns the move to the current square (only for
    squares with strength equal to 255)
    - check_neighbor_diagonal - check if a square is given as a parameter
    is a neighbor on the diagonal of the square on which the function is called
    - find_nearest_enemy_direction - find the nearest enemy square or
    neutral, in one of the four cardinal directions
    - heuristic - calculates the efficiency of the square, determining the ratio
    production / strength, if this ratio is possible
                - if not possible, the maximum potential damage is calculated
                taking into account the overkill feature of the game
    - find_allied_neighbours - returns a list of all your allied neighbors
    the given square, including the neighbors on the diagonal.
    - find_all_neighbours - returns a list of all neighbors of a square,
    including those on the diagonal, regardless of owner
    - find_neighbour_list_enemy - build the list of enemy neighbors on
    the cardinal directions of the given square as a parameter
    - get_direction_to_square - returns the direction it should follow
    the given square as a parameter to reach the given given square as
    parameter
-------------------------------------------------------------------------------
# Sources of inspiration:
 The official forum (http://2016.forums.halite.io/) represented the point of
 start for the project.

# Useful Links:
https://2016.halite.io/rules_game.html<br>
http://2016.forums.halite.io/t/so-youve-improved-the-random-bot-now-what/482.html<br>
https://2016.halite.io/basics_improve_random.html<br>
