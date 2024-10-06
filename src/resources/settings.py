### #### REMOVER #### ###
tile_size = 60
screen_width = 780
screen_height = 650

domino_pieces = [
    [0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6],
    [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6],
    [2, 2], [2, 3], [2, 4], [2, 5], [2, 6],
    [3, 3], [3, 4], [3, 5], [3, 6],
    [4, 4], [4, 5], [4, 6],
    [5, 5], [5, 6],
    [6, 6]
]
### #### REMOVER #### ###

TILE_SIZE = 60
SCREEN_WIDTH = 780
SCREEN_HEIGHT = 650

# Quantidade de jogadores
MINIMUN_QUANTITY_PLAYER = 2
MAXIMUM_QUANTITY_PLAYER = 4

all_pieces = [
    [0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6],
    [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6],
    [2, 2], [2, 3], [2, 4], [2, 5], [2, 6],
    [3, 3], [3, 4], [3, 5], [3, 6],
    [4, 4], [4, 5], [4, 6],
    [5, 5], [5, 6],
    [6, 6]
]

# direções em que as peças podem ser desenhadas
PIECE_DIRECTION_CENTER = 'center'
PIECE_DIRECTION_DOWN = 'down'
PIECE_DIRECTION_LEFT = 'left'
PIECE_DIRECTION_RIGHT = 'right'
PIECE_DIRECTION_UP = 'up'

# posições das peças no mapa
pieces_pos = {
    'right': [
        [6, 4], [7, 4], [8, 4], [9, 4], [10, 4], [11, 4], [12, 4], [12, 3], [12, 2], [12, 1], [12, 0],
        [11, 0], [10, 0], [9, 0], [8, 0], [7, 0], [6, 0], [5, 0], [4, 0], [3, 0], [2, 0], [1, 0],
        [0, 0], [0, 1], [0, 2], [1, 2], [2, 2], [3, 2]
    ],

    'left': [
        [6, 4], [5, 4], [4, 4], [3, 4], [2, 4], [1, 4], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8],
        [1, 8], [2, 8], [3, 8], [4, 8], [5, 8], [6, 8], [7, 8], [8, 8], [9, 8], [10, 8], [11, 8],
        [12, 8], [12, 7], [12, 6], [11, 6], [10, 6], [9, 6]
    ]
}

# formas de draw em cada posição no mapa
pieces_orientation = {
    'right': [
        PIECE_DIRECTION_CENTER, PIECE_DIRECTION_RIGHT, PIECE_DIRECTION_RIGHT, PIECE_DIRECTION_RIGHT, PIECE_DIRECTION_RIGHT, 
        PIECE_DIRECTION_RIGHT, PIECE_DIRECTION_RIGHT, PIECE_DIRECTION_UP, PIECE_DIRECTION_UP, PIECE_DIRECTION_UP, PIECE_DIRECTION_UP, 
        PIECE_DIRECTION_LEFT, PIECE_DIRECTION_LEFT, PIECE_DIRECTION_LEFT, PIECE_DIRECTION_LEFT, PIECE_DIRECTION_LEFT, 
        PIECE_DIRECTION_LEFT, PIECE_DIRECTION_LEFT, PIECE_DIRECTION_LEFT, PIECE_DIRECTION_LEFT, PIECE_DIRECTION_LEFT, 
        PIECE_DIRECTION_LEFT, PIECE_DIRECTION_LEFT, PIECE_DIRECTION_DOWN, PIECE_DIRECTION_DOWN, PIECE_DIRECTION_RIGHT, 
        PIECE_DIRECTION_RIGHT, PIECE_DIRECTION_RIGHT
    ],

    'left': [
        PIECE_DIRECTION_CENTER, PIECE_DIRECTION_LEFT, PIECE_DIRECTION_LEFT, PIECE_DIRECTION_LEFT, PIECE_DIRECTION_LEFT, 
        PIECE_DIRECTION_LEFT, PIECE_DIRECTION_LEFT, PIECE_DIRECTION_DOWN, PIECE_DIRECTION_DOWN, PIECE_DIRECTION_DOWN, 
        PIECE_DIRECTION_DOWN, PIECE_DIRECTION_RIGHT, PIECE_DIRECTION_RIGHT, PIECE_DIRECTION_RIGHT, PIECE_DIRECTION_RIGHT, 
        PIECE_DIRECTION_RIGHT, PIECE_DIRECTION_RIGHT, PIECE_DIRECTION_RIGHT, PIECE_DIRECTION_RIGHT, PIECE_DIRECTION_RIGHT, 
        PIECE_DIRECTION_RIGHT, PIECE_DIRECTION_RIGHT, PIECE_DIRECTION_RIGHT, PIECE_DIRECTION_UP, PIECE_DIRECTION_UP, 
        PIECE_DIRECTION_LEFT, PIECE_DIRECTION_LEFT, PIECE_DIRECTION_LEFT
    ]
}

### #### REMOVER #### ###

# positivo
domino_pieces_posR = [[[6, 4], 'mid'], [[7, 4], 'right'], [[8, 4], 'right'], [[9, 4], 'right'], 
                      [[10, 4], 'right'], [[11, 4], 'right'], [[12, 4], 'right'], [[12, 3], 'up'], 
                      [[12, 2], 'up'], [[12, 1], 'up'], [[12, 0], 'up'], [[11, 0], 'left'], [[10, 0], 'left'], 
                      [[9, 0], 'left'], [[8, 0], 'left'], [[7, 0], 'left'], [[6, 0], 'left'], [[5, 0], 'left'], 
                      [[4, 0], 'left'], [[3, 0], 'left'], [[2, 0], 'left'], [[1, 0], 'left'], [[0, 0], 'left'], 
                      [[0, 1], 'down'], [[0, 2], 'down'], [[1, 2], 'right'], [[2, 2], 'right'], [[3, 2], 'right']]

# negativo
domino_pieces_posL = [[[6, 4], 'mid'], [[5, 4], 'left'], [[4, 4], 'left'], [[3, 4], 'left'], [[2, 4], 'left'], 
                      [[1, 4], 'left'], [[0, 4], 'left'], [[0, 5], 'down'], [[0, 6], 'down'], [[0, 7], 'down'], 
                      [[0, 8], 'down'] , [[1, 8], 'right'], [[2, 8], 'right'], [[3, 8], 'right'], [[4, 8], 'right'], 
                      [[5, 8], 'right'], [[6, 8], 'right'], [[7, 8], 'right'], [[8, 8], 'right'], [[9, 8], 'right'], 
                      [[10, 8], 'right'], [[11, 8], 'right'], [[12, 8], 'right'], [[12, 7], 'up'], [[12, 6], 'up'], 
                      [[11, 6], 'left'], [[10, 6], 'left'], [[9, 6], 'left']]

