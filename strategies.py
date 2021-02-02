import global_variables
import copy


def convert_coords_to_direction(current_head, x, y):

    if x - current_head["x"] > 0:
        result = "right"
    elif x - current_head["x"] < 0:
        result = "down" # TODO: check logic
    else:
        if y - current_head["y"] > 0:
            result = "up"
        else:
            result = "down"
    
    return result

def convert_direction_to_coords(current_head, next_move):

    future_head = copy.deepcopy(current_head)

    if next_move == "right":
        future_head["x"] = current_head["x"] + 1
    elif next_move == "left":
        future_head["x"] = current_head["x"] - 1
    elif next_move == "up":
        future_head["y"] = current_head["y"] + 1
    elif next_move == "down":
        future_head["y"] = current_head["y"] - 1

    return future_head


def avoid_walls(move_coords):
    ''' Return true if the move coords will avoid hitting
        a wall, false if it will cause the snake to hit the wall
    '''

    if move_coords["x"] < 0 or move_coords["y"] < 0:
        result = False
    elif move_coords["x"] > global_variables.BOARD_MAXIMUM_X or move_coords["y"] > global_variables.BOARD_MAXIMUM_Y:
        result = False
    else:
        result = True
    
    return result


def avoid_snake(move_coords, body_coords):
    
    """ return true if the move will avoid colliding with
        myself or other snakes
    """
    if type(body_coords[0]) == dict:
        for coord in body_coords:
            if move_coords == coord:
                return False
            else:
                result = True
    else: 
        for body in body_coords:
            if move_coords in body:
                return False
            else:
                result = True
    
    return result

def safe_move(move_coords, body_coords):
    """ return true if the grid coords are
        safe to move to, ie avoid walls and 
        myself/other snakes
    """
    if avoid_walls(move_coords) and avoid_snake(move_coords, body_coords) and avoid_head_to_head_collision(move_coords, body_coords):
        result = True
    else:
        result = False

    return result

def update_snake_loc_data(data):
    current_snakes = data["board"]["snakes"]
    all_snake_bodies = []
    for snake in current_snakes:
        all_snake_bodies.append(snake["body"])

    return all_snake_bodies


def avoid_head_to_head_collision(next_move, current_snakes):
    snakes = copy.deepcopy(current_snakes)
    snakes.pop(0)
    for snake in snakes:
        if (next_move["x"] + 1) == (snake["body"][0]["x"] + 1):
            return False
        elif (next_move["x"] - 1) == (snake["body"][0]["x"] - 1):
            return False
        elif (next_move["y"] + 1) == (snake["body"][0]["y"] + 1):
            return False
        elif (next_move["y"] - 1) == (snake["body"][0]["y"] - 1):
            return False
        else:
            result = True
    
    return result