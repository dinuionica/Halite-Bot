# SBI Team
import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square, \
    opposite_cardinal

(myID, game_map) = hlt.get_init()
hlt.send_init('SBI_Bot')

# the map using for assigning moves to squares of maximum strength
moves_map = {}

# the factor of minumum necessary production for a square to be useful
PRODUCTION_FACTOR = 5

# the list with cardinal directions
CARDINALS = [NORTH, EAST, SOUTH, WEST]

# maximum strength of a square
MAX_STRENGTH = 255


# The function that checks if a given neighbour of a square on a diagonal
def check_neighbour_diagonal(square, neighbour):
    # south east check
    if neighbour.x == square.x + 1 and neighbour.y == square.y + 1:
        return True
    
    # north west check
    elif neighbour.x == square.x - 1 and neighbour.y == square.y - 1:
        return True

    # north east check
    elif neighbour.x == square.x - 1 and neighbour.y == square.y + 1:
        return True

    # south west check
    elif neighbour.x == square.x + 1 and neighbour.y == square.y - 1:
        return True
    return False


# The function that return the direction to the nearest enemy
# or neutral square
def find_nearest_unowned_direction(square):
    direction = NORTH
    max_distance = min(game_map.width, game_map.height) / 2
    for direction_cardinal in CARDINALS:
        distance = 0
        current = square

        # keep going until we find an unowned square
        while current.owner == myID and distance < max_distance:
            distance += 1
            current = game_map.get_target(current, direction_cardinal)

        # update the max distance if we found a better one
        if distance < max_distance:
            direction = direction_cardinal
            max_distance = distance
    return direction


# The function that calculates the heuristic value for a given square
def heuristic(square):
    # calculate the efficiecy of a square by calculating
    # the ratio of strength to production
    if square.owner == 0 and square.strength > 0:
        return square.production / square.strength
    else:

        # calculate the total potential damage caused by overkill when
        # attacking this square
        return sum(neighbor.strength for neighbor in
                   game_map.neighbors(square) if neighbor.owner
                   not in (0, myID))


# The function that returns a list of all allied neighbours of a square,
# including diagonals
def find_allied_neighbours(square):
    neighbours = []
    for direction in CARDINALS:
        # get neighbour in from given direction
        neighbour = game_map.get_target(square, direction)
        if neighbour.owner == myID:
            # if the neighbour is an ally, add it to the list
            neighbours.append(neighbour)
        if direction == NORTH or direction == SOUTH:
            # check the north-east or south-east direction
            diagonal_neighbour = game_map.get_target(neighbour, EAST)
            if diagonal_neighbour.owner == myID:
                # if the neighbour is an ally, add it to the list
                neighbours.append(diagonal_neighbour)
            
            # check the north-west or south-west direction
            diagonal_neighbour = game_map.get_target(neighbour, WEST)
            if diagonal_neighbour.owner == myID:
                # if the neighbour is an ally, add it to the list
                neighbours.append(diagonal_neighbour)
    return neighbours


# The function that returns a list of all neighbours of a square,
# including diagonals
def find_all_neighbours(square):
    neighbours = []
    for direction in CARDINALS:
        # get neighbour in from given direction
        neighbour = game_map.get_target(square, direction)
        # make sure there are no duplicates in the list
        if neighbour not in neighbours:
            neighbours.append(neighbour)
        if direction == NORTH or direction == SOUTH:
            # get neighbour in the north-east or south-east direction
            diagonal_neighbour = game_map.get_target(neighbour, EAST)

            # make sure there are no duplicates in the list
            if diagonal_neighbour not in neighbours:
                neighbours.append(diagonal_neighbour)

            # get neighbour in the north-east or south-east direction
            diagonal_neighbour = game_map.get_target(neighbour, WEST)
            
            # make sure there are no duplicates in the list
            if diagonal_neighbour not in neighbours:
                neighbours.append(diagonal_neighbour)
    return neighbours


# The function that returns a list of enemy or neutral neighbours
# on cardinal directions
def find_neighbour_list_enemy(square):
    neighbours = []
    for direction in CARDINALS:
        neighbour = game_map.get_target(square, direction)

        # find the enemy neighbour or neutral neighbour
        if neighbour.owner != myID:

            # add the desired neighbour to the list
            neighbours.append(neighbour)
    return neighbours


# The function that returns the direction to a given square destination
# from source square
def get_direction_to_square(source, destination):
    # calculate difference on x axis
    dx = destination.x - source.x

    # calculate difference on y axis
    dy = destination.y - source.y

    # return the WEST direction
    if dx > 0:
        return WEST
    elif dx < 0:

    # return the EAST direction
        return EAST
    elif dy > 0:

    # return the NORTH direction
        return NORTH
    elif dy < 0:

    # return the SOUTH direction
        return SOUTH
    return STILL


# The function that determines the move for a given square with max strength
def get_move_max(square):
    # determine if current square is on border
    border = any(neighbor.owner != myID for neighbor in
                 game_map.neighbors(square))

    # check if the current square has an allied neighbour with strength 255
    # around it and and if so, update the movement as well
    for neighbour in find_allied_neighbours(square):
        if neighbour.strength == MAX_STRENGTH and neighbour in moves_map:

            # check if the neighbour is on a diagonal
            if check_neighbour_diagonal(square, neighbour):

                # move the square in the same direction as the neighbour
                return Move(square, moves_map[neighbour])

    # find the target enemy or neutral square and direction by the heuristic
    (target, direction) = max(((neighbor, direction) for (direction,
                              neighbor) in
                              enumerate(game_map.neighbors(square))
                              if neighbor.owner != myID),
                              default=(None, None), key=lambda t: \
                              heuristic(t[0]))

    # if the target is found and the strengths allows the attack,
    # move to desired direction
    if target is not None and target.strength < square.strength:
        # assign the direction to the square in the map
        moves_map[square] = direction

        # move the square in the desired direction
        return Move(square, direction)

    # if the square is not on the border, move to the nearest enemy or
    # neutral square
    if not border:
        # assign the direction to the square in the map
        moves_map[square] = find_nearest_unowned_direction(square)

        # move the square in the desired direction
        return Move(square, find_nearest_unowned_direction(square))
    else:
        # if the square is on the border, move to the nearest enemy
        for neighbour in find_all_neighbours(square):
            if neighbour.owner != myID and neighbour.owner != 0:
                if neighbour.strength > square.strength:
                    # assign the direction to the square in the map
                    moves_map[square] = moves_map[neighbour]

                    # move the square in the desired direction
                    return Move(square, moves_map[neighbour])

    # wait until we have enough strength to attack
    return Move(square, STILL)


# The function that determines the move for a given square with
# strength less than 255
def get_move(square):
    # determine if current square is on border
    border = any(neighbor.owner != myID for neighbor in
                 game_map.neighbors(square))

    # check if the current square has an allied neighbour with strength 255
    # around it and and if so, update the movement as well
    for neighbour in find_allied_neighbours(square):
        if neighbour.strength == MAX_STRENGTH and neighbour in moves_map:
            if square.strength > 0:
                # check if the neighbour is on a diagonal
                if check_neighbour_diagonal(square, neighbour):

                    # move the square in the same direction as the neighbour
                    return Move(square, moves_map[neighbour])

                # check if list enemy of the square is empty
                if len(find_neighbour_list_enemy(neighbour)) == 0:

                    # move the square in the same direction as the neighbour
                    return Move(square, moves_map[neighbour])
                else:
                    for enemy in find_neighbour_list_enemy(square):

                        # check if the square can attack the enemy
                        if enemy.strength < square.strength:
                            # move the square in the the desired direction
                            return Move(square,
                                    get_direction_to_square(square,
                                    enemy))
                        else:
                            # swap the direction with ally
                            return Move(square,
                                    opposite_cardinal(moves_map[neighbour]))

    # find the target enemy or neutral square and direction by the heuristic
    (target, direction) = max(((neighbor, direction) for (direction,
                              neighbor) in
                              enumerate(game_map.neighbors(square))
                              if neighbor.owner != myID),
                              default=(None, None), key=lambda t: \
                              heuristic(t[0]))

    # if the square has strength 0, it cannot move
    if square.strength == 0:
        return Move(square, STILL)

    # if the target is found and the strengths allows the attack,
    # move to desired direction
    if target is not None and target.strength < square.strength:
        return Move(square, direction)

    # if the square has not enough strength to attack, stay still
    if square.strength < PRODUCTION_FACTOR * square.production:
        return Move(square, STILL)

    # if the square is not on the border, move to the nearest 
    # enemy or neutral square
    if not border:
        return Move(square, find_nearest_unowned_direction(square))
    else:
        # if the square is on the border, move to the nearest enemy
        for neighbour in find_all_neighbours(square):
            if neighbour.owner != myID and neighbour.owner != 0:
                if neighbour.strength < square.strength:
                    return Move(square, get_direction_to_square(square,
                                neighbour))

    # wait until we have enough strength to attack
    return Move(square, STILL)