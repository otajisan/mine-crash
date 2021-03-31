def make_mines():
    global mines
    mines = []
    mine_count = calc_mine_count()
    for index in range(mine_count):
        m = make_random_mine()
        for n in mines:
            # avoid duplicate mine
            if n[0] == m[0] and n[1] == m[1]:
                continue
        flash_mine(m)
        mines.append(m)
        print(m)

def calc_mine_count():
    if stage <= 3:
        return 3
    elif stage <= 5:
        return stage
    return 5

def flash_mine(mine):
    music.play_tone(523, music.beat(BeatFraction.EIGHTH))
    for i in range(3):
        led.plot(mine[0], mine[1])
        basic.pause(100)
    basic.pause(500)

def make_random_mine():
    mine_x = 0
    mine_y = 0
    # if mine position is right
    while (mine_x == 0 and mine_y == 0) or (mine_x == 4 and mine_y == 4):
        mine_x = randint(0, 4)
        mine_y = randint(0, 4)
    return [mine_x, mine_y]

def judge_mine():
    for mine in mines:
        if eddie.get(LedSpriteProperty.X) == mine[0] and eddie.get(LedSpriteProperty.Y) == mine[1]:
            damage()

def on_button_pressed_a():
    music.play_tone(330, music.beat(BeatFraction.EIGHTH))
    eddie.turn(Direction.RIGHT, 90)
    show_direction()
input.on_button_pressed(Button.A, on_button_pressed_a)

def show_bomb():
    basic.show_animation("""
        . . # # .
        . . # . .
        . # # # .
        # # # # #
        . # # # .
    """)

def goal():
    music.start_melody(music.built_in_melody(Melodies.POWER_UP), MelodyOptions.ONCE)
    global stage
    music.play_tone(147, music.beat(BeatFraction.EIGHTH))
    stage += 1
    basic.pause(2000)

def on_button_pressed_b():
    music.play_tone(262, music.beat(BeatFraction.EIGHTH))
    eddie.move(1)
    judge_mine()
    if eddie.get(LedSpriteProperty.X) == 4 and eddie.get(LedSpriteProperty.Y) == 4:
        goal()
        reset()
input.on_button_pressed(Button.B, on_button_pressed_b)

def show_direction():
    current_direction = eddie.direction()
    if current_direction == 90:
        arrow = ArrowNames.EAST
    elif current_direction == 180:
        arrow = ArrowNames.SOUTH
    elif current_direction == -90:
        arrow = ArrowNames.WEST
    elif current_direction == 0:
        arrow = ArrowNames.NORTH
    basic.show_arrow(arrow)

def show_current_life():
    basic.show_string("" + str(life))

def damage():
    global life
    if life > 0:
        music.start_melody(music.built_in_melody(Melodies.POWER_DOWN), MelodyOptions.ONCE)
        show_bomb()
        life += -1
        show_current_life()
        basic.pause(2000)
        initialize_eddie()
        music.start_melody(music.built_in_melody(Melodies.NYAN), MelodyOptions.ONCE)

def reset():
    initialize_eddie()
    make_mines()
    music.start_melody(music.built_in_melody(Melodies.NYAN), MelodyOptions.ONCE)

def initialize_eddie():
    eddie.set_direction(90)
    eddie.set(LedSpriteProperty.X, 0)
    eddie.set(LedSpriteProperty.Y, 0)

def clear_all():    
    global stage, life, mines
    mines = []
    stage = 0
    life = 3
    reset()
    eddie.on()

stage = 0
life = 3
eddie: game.LedSprite = game.create_sprite(0, 0)
mines: List[List[number]] = []

clear_all()

def on_forever():
    if life == 0:
        music.start_melody(music.built_in_melody(Melodies.WAWAWAWAA), MelodyOptions.ONCE)
        eddie.off()
        game.set_score(stage)
        basic.show_string("GAMEOVER")
        game.show_score()
        clear_all()

basic.forever(on_forever)