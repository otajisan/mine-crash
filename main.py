def make_mines():
    global mines, mine_count
    mines = []
    mine_count = calc_mine_count()
    for index in range(mine_count):
        m = make_random_mine()
        # avoid duplicate mine
        for n in mines:
            if n[0] == m[0] and n[1] == m[1]:
                continue
        #print(m)
        flash_mine(m)
        mines.append(m)
def make_random_mine():
    global mine_x, mine_y
    mine_x = 0
    mine_y = 0
    # if mine position is right
    while mine_x == 0 and mine_y == 0 or mine_x == 4 and mine_y == 4:
        mine_x = randint(0, 4)
        mine_y = randint(0, 4)
    return [mine_x, mine_y]
def goal():
    global is_ready, stage
    is_ready = False
    music.start_melody(music.built_in_melody(Melodies.POWER_UP), MelodyOptions.ONCE)
    music.play_tone(147, music.beat(BeatFraction.EIGHTH))
    stage += 1
    basic.pause(2000)
    reset()
def judge_mine():
    for mine in mines:
        if eddie.get(LedSpriteProperty.X) == mine[0] and eddie.get(LedSpriteProperty.Y) == mine[1]:
            damage()
def initialize_eddie():
    eddie.set_direction(90)
    eddie.set(LedSpriteProperty.X, 0)
    eddie.set(LedSpriteProperty.Y, 0)

def on_button_pressed_a():
    if is_ready:
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
def calc_mine_count():
    if stage <= 3:
        return 3
    elif stage <= 5:
        return stage
    return 5
def clear_all():
    global mines, stage, life
    mines = []
    stage = 0
    life = 3
    reset()
    eddie.on()
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

def on_button_pressed_b():
    if is_ready:
        music.play_tone(262, music.beat(BeatFraction.EIGHTH))
        eddie.move(1)
        judge_mine()
        if eddie.get(LedSpriteProperty.X) == 4 and eddie.get(LedSpriteProperty.Y) == 4:
            goal()
input.on_button_pressed(Button.B, on_button_pressed_b)

def show_current_life():
    basic.show_string("" + str(life))
def reset():
    initialize_eddie()
    make_mines()
    play_game_music()
def damage():
    global is_ready, life
    if life > 0:
        is_ready = False
        music.start_melody(music.built_in_melody(Melodies.POWER_DOWN),
            MelodyOptions.ONCE)
        show_bomb()
        life += -1
        show_current_life()
        basic.pause(2000)
        initialize_eddie()
        play_game_music()
def play_game_music():
    global is_ready
    if life > 0:
        music.start_melody(music.built_in_melody(Melodies.NYAN), MelodyOptions.ONCE)
        is_ready = True
stage = 0
is_ready = False
mine_y = 0
mine_x = 0
mine_count = 0
mines: List[List[number]] = []
life = 0
eddie: game.LedSprite = None
def flash_mine(mine: List[number]):
    music.play_tone(523, music.beat(BeatFraction.EIGHTH))
    for i in range(3):
        led.plot(mine[0], mine[1])
        basic.pause(100)
    basic.pause(500)
life = 3
eddie = game.create_sprite(0, 0)
clear_all()

def on_forever():
    if life == 0:
        music.start_melody(music.built_in_melody(Melodies.WAWAWAWAA),
            MelodyOptions.ONCE)
        eddie.off()
        game.set_score(stage)
        basic.show_string("GAMEOVER")
        game.show_score()
        clear_all()
basic.forever(on_forever)
