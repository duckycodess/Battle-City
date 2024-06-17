class Stage:
    player_spawn_col = 0 # Must be a valid column
    player_spawn_row = 0 # Must be a valid row
    enemy_spawn_col = 15 # Must be a valid column
    enemy_spawn_row = 15 # Must be a valid row
    '''
    Each level is specified by its key and its layout by its value.
    All cells within a 16x16 range should contain a number from 0-8
    Values are as follows:
    EMPTY = 0
    STONE = 1
    BRICK = 2
    MIRROR_NE = 3
    MIRROR_SE = 4
    WATER = 5
    CRACKED_BRICK = 6
    FOREST = 7
    HOME = 8
    '''
    levels: dict[int, list[str]] = {
        1: ['0000000000000000',
            '0222220000002220',
            '0222220000002220',
            '0233330000002330',
            '0244440000002440',
            '0255550000002550',
            '0000000000000000',
            '0000001111110000',
            '0000001222210000',
            '0000001333310000',
            '0000001444410000',
            '0000001555510000',
            '0000000000000000',
            '0222220000001110',
            '0122220000001220',
            '0000000000000000',],

        2: ['0222000000002222',
            '0000000000002000',
            '2000000000002000',
            '2000000000002000',
            '2000000000002000',
            '2000000000002000',
            '2222220000002222',
            '0000000000000000',
            '0000000000000000',
            '2222000022222222',
            '2000000020000000',
            '2000000020000000',
            '2000000020000000',
            '2000000020000000',
            '2000000020000000',
            '2222222222222222',]
    }