from pico2d import *

import game_framework

PIXEL_PER_METER = (10.0 / 0.1)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, JUMP, JUMPING, LANDING = range(7)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_x): JUMP
}


class JumpState:
    def enter(player, event):
        if event == JUMP:
            player.y+=200
        if event == RIGHT_DOWN:
            player.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            player.velocity -= RUN_SPEED_PPS
        player.dir = clamp(-1, player.velocity, 1)
        pass

    def exit(player, event):
        if event == RIGHT_UP:
            player.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            player.velocity += RUN_SPEED_PPS
        player.dir = clamp(-1, player.velocity, 1)
        pass

    def do(player):
        if player.col_bottom <= 0:
            player.y = 40
            player.add_event(LANDING)

        if player.gravity < 500:
            player.gravity += 1
        player.x += player.velocity * game_framework.frame_time
        player.y -= player.gravity * game_framework.frame_time
        player.x = clamp(25, player.x, 1600 - 25)
        pass

    def draw(player):
        player.image_jump_up.clip_composite_draw(0, 0, player.image_jump_up.w,
                                                 player.image_jump_up.h, 0, '', player.x, player.y)
        pass


class IdleState:
    def enter(player, event):
        if event == JUMP:
            player.y+=50
        pass

    def exit(player, event):
        player.frame = 0  # 프레임 초기화
        pass

    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 14
        if player.col_bottom > 0:
            player.add_event(JUMPING)

        pass

    def draw(player):
        if player.dir > 0:
            player.image_idle.clip_composite_draw(int(player.frame) * 256, 0, 256, 256, 0, '', player.x, player.y, 256,
                                                  256)
        else:
            player.image_idle.clip_composite_draw(int(player.frame) * 256, 0, 256, 256, 0, 'h', player.x + 10, player.y,
                                                  256, 256)

        pass


class RunState:
    def enter(player, event):
        if event == RIGHT_DOWN:
            player.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            player.velocity -= RUN_SPEED_PPS
        player.dir = clamp(-1, player.velocity, 1)
        pass

    def exit(player, event):
        if event == RIGHT_UP:
            player.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            player.velocity += RUN_SPEED_PPS
        player.dir = clamp(-1, player.velocity, 1)
        player.frame = 0  # 프레임 초기화
        pass

    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 11
        player.x += player.velocity * game_framework.frame_time
        player.x = clamp(25, player.x, 1600 - 25)
        if player.col_bottom > 0:
            player.add_event(JUMPING)

        pass

    def draw(player):
        if player.dir > 0:
            player.image_walk.clip_composite_draw(int(player.frame) * 256, 0, 256, 256, 0, '', player.x, player.y, 256,
                                                  256)
        else:
            player.image_walk.clip_composite_draw(int(player.frame) * 256, 0, 256, 256, 0, 'h', player.x + 10, player.y,
                                                  256, 256)


next_state_table = {
    IdleState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState, JUMPING: JumpState,JUMP:JumpState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
               JUMPING: JumpState,JUMP:JumpState},
    JumpState: {RIGHT_UP: JumpState, LEFT_UP: JumpState, LEFT_DOWN: JumpState, RIGHT_DOWN: JumpState,
                LANDING: IdleState,JUMP:JumpState},
}


class Player:
    def __init__(self):
        self.x, self.y = 900, 900
        self.col_left = self.x - 30
        self.col_bottom = self.y - 40
        self.col_right = self.x + 40
        self.col_top = self.y + 40
        self.dir = 1
        self.velocity = 0
        self.gravity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.image_idle = load_image('Mayreel/idle.png')
        self.image_walk = load_image('Mayreel/walk.png')
        self.image_jump_up = load_image('Mayreel/jump_up/jump_up.png')
        self.image_jump_down = load_image('Mayreel/jump_down/jump_down.png')

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)
        # ---------------------------- 플레이어 콜라이더 위치 변경
        self.col_left = self.x - 30
        self.col_bottom = self.y - 40
        self.col_right = self.x + 40
        self.col_top = self.y + 40
        # ----------------------------

        pass

    def draw(self):
        draw_rectangle(self.col_left, self.col_bottom, self.col_right, self.col_top)
        self.cur_state.draw(self)
        pass

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
        pass
