import os
import random
import global_variables
import strategies

import cherrypy

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""


class Battlesnake(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        # This function is called when you register your Battlesnake on play.battlesnake.com
        # It controls your Battlesnake appearance and author permissions.
        # TIP: If you open your Battlesnake URL in browser you should see this data
        return {
            "apiversion": "1",
            "author": "rebeckky&ladyelle",  # TODO: Your Battlesnake Username
            "color": "#3f0654",
            "head": "silly",  # TODO: Personalize
            "tail": "hook",  # TODO: Personalize
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        data = cherrypy.request.json
        print(data)
        global_variables.BOARD_MAXIMUM_X = data["board"]["width"] - 1
        global_variables.BOARD_MAXIMUM_Y = data["board"]["height"] - 1
        print("START")
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It's how your snake decides where to move.
        # Valid moves are "up", "down", "left", or "right".
        # TODO: Use the information in cherrypy.request.json to decide your next move.
        data = cherrypy.request.json
        #startdir = calculateStartingDirection(data)
        current_head = data["you"]["head"]
        # Choose a random direction to move in
        possible_moves = ["up", "down", "left", "right"]
        move = random.choice(possible_moves)
        #move = startdir
        
        while strategies.avoid_walls(current_head, move) is not True:
            move = random.choice(possible_moves)

        print(f"MOVE: {move}")
        return {"move": move}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json

        print("END")
        return "ok"

'''
    def calculateClosestFood(self, data):
        gameId = data["game"]["id]"
        food = data["board"]["food"]
        myhead = data["board"]["you"]["head"]
        mytail = data["board"]["you"]["body"][-1]
'''

    def calculateStartingDirection(self, data):
        head = data["board"]["you"]["head"]
        tail = data["board"]["you"]["body"][-1]
        xdiff = head["x"] - tail["x"]
        if xdiff > 0:
            return "right"
        elif xdiff < 0:
            return "left"
        elif xdiff == 0:
            ydiff = head["y"] - tail["y"]
            if ydiff > 0:
                return "up"
            else:
                return "down"


        
        

if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
