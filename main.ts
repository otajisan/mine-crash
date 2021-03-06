function make_mines() {
    let m: number[];
    
    mines = []
    mine_count = calc_mine_count()
    for (let index = 0; index < mine_count; index++) {
        m = make_random_mine()
        //  avoid duplicate mine
        for (let n of mines) {
            if (n[0] == m[0] && n[1] == m[1]) {
                continue
            }
            
        }
        flash_mine(m)
        mines.push(m)
    }
}

function make_random_mine(): number[] {
    
    mine_x = 0
    mine_y = 0
    //  if mine position is right
    while (mine_x == 0 && mine_y == 0 || mine_x == 4 && mine_y == 4) {
        mine_x = randint(0, 4)
        mine_y = randint(0, 4)
    }
    return [mine_x, mine_y]
}

function goal() {
    
    is_ready = false
    music.startMelody(music.builtInMelody(Melodies.PowerUp), MelodyOptions.Once)
    music.playTone(147, music.beat(BeatFraction.Eighth))
    stage += 1
    basic.pause(2000)
    reset()
}

function judge_mine() {
    for (let mine of mines) {
        if (eddie.get(LedSpriteProperty.X) == mine[0] && eddie.get(LedSpriteProperty.Y) == mine[1]) {
            damage()
        }
        
    }
}

function initialize_eddie() {
    eddie.setDirection(90)
    eddie.set(LedSpriteProperty.X, 0)
    eddie.set(LedSpriteProperty.Y, 0)
}

input.onButtonPressed(Button.A, function on_button_pressed_a() {
    
    if (is_ready) {
        is_ready = false
        music.playTone(330, music.beat(BeatFraction.Eighth))
        eddie.turn(Direction.Right, 90)
        show_direction()
        basic.pause(100)
        is_ready = true
    }
    
})
function show_bomb() {
    basic.showAnimation(`
        . . # # .
        . . # . .
        . # # # .
        # # # # #
        . # # # .
    `)
}

function calc_mine_count(): number {
    if (stage <= 3) {
        return 3
    } else if (stage <= 5) {
        return stage
    }
    
    return 5
}

function clear_all() {
    
    mines = []
    stage = 0
    life = 3
    reset()
    eddie.on()
}

function show_direction() {
    let arrow: number;
    let current_direction = eddie.direction()
    if (current_direction == 90) {
        arrow = ArrowNames.East
    } else if (current_direction == 180) {
        arrow = ArrowNames.South
    } else if (current_direction == -90) {
        arrow = ArrowNames.West
    } else if (current_direction == 0) {
        arrow = ArrowNames.North
    }
    
    basic.showArrow(arrow)
}

input.onButtonPressed(Button.B, function on_button_pressed_b() {
    
    if (is_ready) {
        is_ready = false
        music.playTone(262, music.beat(BeatFraction.Eighth))
        eddie.move(1)
        judge_mine()
        basic.pause(100)
        is_ready = true
        if (eddie.get(LedSpriteProperty.X) == 4 && eddie.get(LedSpriteProperty.Y) == 4) {
            goal()
        }
        
    }
    
})
function show_current_life() {
    basic.showString("" + ("" + life))
}

function reset() {
    initialize_eddie()
    make_mines()
    play_game_music()
}

function damage() {
    
    if (life > 0) {
        is_ready = false
        music.startMelody(music.builtInMelody(Melodies.PowerDown), MelodyOptions.Once)
        show_bomb()
        life += -1
        show_current_life()
        basic.pause(2000)
        initialize_eddie()
        play_game_music()
    }
    
}

function play_game_music() {
    
    if (life > 0) {
        music.startMelody(music.builtInMelody(Melodies.Nyan), MelodyOptions.Once)
        is_ready = true
    }
    
}

let stage = 0
let is_ready = false
let mine_y = 0
let mine_x = 0
let mine_count = 0
let mines : number[][] = []
let life = 0
let eddie : game.LedSprite = null
function flash_mine(mine: number[]) {
    music.playTone(523, music.beat(BeatFraction.Eighth))
    for (let i = 0; i < 3; i++) {
        led.plot(mine[0], mine[1])
        basic.pause(100)
    }
    basic.pause(500)
}

life = 3
eddie = game.createSprite(0, 0)
clear_all()
basic.forever(function on_forever() {
    if (life == 0) {
        music.startMelody(music.builtInMelody(Melodies.Wawawawaa), MelodyOptions.Once)
        eddie.off()
        game.setScore(stage)
        basic.showString("GAMEOVER")
        game.showScore()
        clear_all()
    }
    
})
