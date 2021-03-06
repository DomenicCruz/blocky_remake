"""Configuration file with global variables shared between this project files"""


# Global constants

#Color
SKY_BLUE = "#37b7da"

#Player
PLAYER_STEP_HEIGHT = 2
PLAYER_HEIGHT = 1.86
#Physics
GRAVITY_FORCE = 9.8

#Player block Highlight
HIGHLIGHT_RANGE=14

SIX_AXIS = [
(1,0,0),
(-1,0,0),
(0,1,0),
(0,-1,0),
(0,0,1),
(0,0,-1)
]

class BlockTypeNames:
    def __init__(self):
        self.grass = "grass"
        self.soil = "soil"
        self.stone = "stone"
        self.ice = "ice"
        self.snow= "snow"
block_names = BlockTypeNames()


