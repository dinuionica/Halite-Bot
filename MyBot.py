# SBI Team
from BotHelpers import *

# The main point of the game
while True:
    # get the current frame
    game_map.get_frame()

    # reset the map with movements
    moves_map.clear()

    # update the moves for square with max strength
    moves_for_max_strength = [get_move_max(square) for square in game_map
                             if square.owner == myID
                             and square.strength == MAX_STRENGTH]

    # update the moves for square with strength less than 255
    moves = [get_move(square) for square in game_map if square.owner == myID
            and square.strength != MAX_STRENGTH]

    # create the final list of moves and send them to the game
    moves = moves + moves_for_max_strength
    hlt.send_frame(moves)