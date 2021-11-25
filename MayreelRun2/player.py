from pico2d import *

import collision
import game_framework
import server

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


class IdleState:
    def enter(player, event):
        if event == JUMP:
            player.y += 50
        pass

    def exit(player, event):
        player.frame = 0  # 프레임 초기화
        pass

    def do(player):
        for block in server.block:
            if collision.collide(player.get_col_feet(), block.get_col()):
                break
            if block==server.block[len(server.block)-1]:
                player.add_event(JUMPING)
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 14

        pass

    def draw(player):
        if player.dir > 0:
            player.image_idle.clip_composite_draw(int(player.frame) * 256, 0, 256, 256, 0, '', player.x, player.y, 256,
                                                  256)
        else:
            player.image_idle.clip_composite_draw(int(player.frame) * 256, 0, 256, 256, 0, 'h', player.x + 10, player.y,
                                                  256, 256)

        pass


class LeftRunState:
    def enter(player, event):
        player.velocity -= RUN_SPEED_PPS
        player.dir = clamp(-1, player.velocity, 1)
        pass

    def exit(player, event):
        player.velocity += RUN_SPEED_PPS
        player.frame = 0  # 프레임 초기화
        pass

    def do(player):
        for block in server.block:
            if collision.collide(player.get_col_feet(), block.get_col()):
                break
            if block == server.block[len(server.block) - 1]:
                player.add_event(JUMPING)
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 11
        player.x += player.velocity * game_framework.frame_time
        player.x = clamp(25, player.x, 1600 - 25)


        pass

    def draw(player):
        player.image_walk.clip_composite_draw(int(player.frame) * 256, 0, 256, 256, 0, 'h', player.x + 10, player.y,
                                              256, 256)


class RightRunState:
    def enter(player, event):
        player.velocity += RUN_SPEED_PPS
        player.dir = clamp(-1, player.velocity, 1)
        pass

    def exit(player, event):
        player.velocity -= RUN_SPEED_PPS
        player.frame = 0  # 프레임 초기화
        pass

    def do(player):
        for block in server.block:
            if collision.collide(player.get_col_feet(), block.get_col()):
                break
            if block==server.block[len(server.block)-1]:
                player.add_event(JUMPING)
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 11
        player.x += player.velocity * game_framework.frame_time
        player.x = clamp(25, player.x, 1600 - 25)

        pass

    def draw(player):
        player.image_walk.clip_composite_draw(int(player.frame) * 256, 0, 256, 256, 0, '', player.x, player.y, 256,
                                              256)
        pass


class JumpState:
    def enter(player, event):
        if event == JUMP:
            player.jump_power = player.jump_power_max
            player.gravity = 0
        pass

    def exit(player, event):
        pass

    def do(player):
        if player.gravity < player.gravity_max:
            player.gravity += 100 * game_framework.frame_time
        if player.jump_power > 0:
            player.jump_power -= 100 * game_framework.frame_time
        player.x += player.velocity * game_framework.frame_time
        player.y -= player.gravity * game_framework.frame_time
        player.y += player.jump_power * game_framework.frame_time
        player.x = clamp(25, player.x, 1600 - 25)

        for block in server.block:
            if collision.collide(player.get_col_feet(), block.get_col()) and (player.jump_power - player.gravity) <= 0:
                player.y = 40 + block.col_top
                player.add_event(LANDING)
                break

    def draw(player):
        if player.dir > 0:
            player.image_jump_up.clip_composite_draw(0, 0, player.image_jump_up.w, player.image_jump_up.h, 0, '',
                                                     player.x, player.y)
        else:
            player.image_jump_up.clip_composite_draw(0, 0, player.image_jump_up.w, player.image_jump_up.h, 0, 'h',
                                                     player.x + 10, player.y)
        pass


class LeftJumpState:
    def enter(player, event):
        player.velocity -= RUN_SPEED_PPS
        if event == JUMP:
            player.jump_power = player.jump_power_max
            player.gravity = 0
        player.dir = clamp(-1, player.velocity, 1)

        pass

    def exit(player, event):
        player.velocity += RUN_SPEED_PPS
        pass

    def do(player):
        if player.gravity < player.gravity_max:
            player.gravity += 100 * game_framework.frame_time
        if player.jump_power > 0:
            player.jump_power -= 100 * game_framework.frame_time
        player.x += player.velocity * game_framework.frame_time
        player.y += player.jump_power * game_framework.frame_time
        player.y -= player.gravity * game_framework.frame_time

        player.x = clamp(25, player.x, 1600 - 25)

        for block in server.block:
            if collision.collide(player.get_col_feet(), block.get_col()) and (player.jump_power - player.gravity) <= 0:
                player.y = 40 + block.col_top
                player.add_event(LANDING)
                break

    def draw(player):
        player.image_jump_up.clip_composite_draw(0, 0, player.image_jump_up.w, player.image_jump_up.h, 0, 'h',
                                                 player.x + 10,
                                                 player.y)
        pass


class RightJumpState:
    def enter(player, event):
        player.velocity += RUN_SPEED_PPS
        if event == JUMP:
            player.jump_power = player.jump_power_max
            player.gravity = 0
        player.dir = clamp(-1, player.velocity, 1)
        pass

    def exit(player, event):
        player.velocity -= RUN_SPEED_PPS
        pass

    def do(player):
        if player.gravity < player.gravity_max:
            player.gravity += 100 * game_framework.frame_time
        if player.jump_power > 0:
            player.jump_power -= 100 * game_framework.frame_time
        player.x += player.velocity * game_framework.frame_time
        player.y += player.jump_power * game_framework.frame_time
        player.y -= player.gravity * game_framework.frame_time
        player.x = clamp(25, player.x, 1600 - 25)

        for block in server.block:
            if collision.collide(player.get_col_feet(), block.get_col()) and (player.jump_power - player.gravity) <= 0:
                player.y = 40 + block.col_top
                player.add_event(LANDING)
                break

    def draw(player):
        player.image_jump_up.clip_composite_draw(0, 0, player.image_jump_up.w, player.image_jump_up.h, 0, '', player.x,
                                                 player.y)
        pass


next_state_table = {
    IdleState: {RIGHT_UP: IdleState, LEFT_UP: IdleState,
                RIGHT_DOWN: RightRunState, LEFT_DOWN: LeftRunState,
                JUMPING: JumpState, JUMP: JumpState, LANDING: IdleState},
    LeftRunState: {RIGHT_UP: LeftRunState, LEFT_UP: IdleState,
                   LEFT_DOWN: LeftRunState, RIGHT_DOWN: RightRunState,
                   JUMPING: LeftJumpState, JUMP: LeftJumpState, LANDING: LeftRunState},
    RightRunState: {RIGHT_UP: IdleState, LEFT_UP: RightRunState,
                    LEFT_DOWN: LeftRunState, RIGHT_DOWN: RightRunState,
                    JUMPING: RightJumpState, JUMP: RightJumpState, LANDING: RightRunState},

    JumpState: {RIGHT_UP: JumpState, LEFT_UP: JumpState,
                LEFT_DOWN: LeftJumpState, RIGHT_DOWN: RightJumpState,
                LANDING: IdleState, JUMP: JumpState, JUMPING: JumpState},
    LeftJumpState: {RIGHT_UP: LeftJumpState, LEFT_UP: JumpState,
                    LEFT_DOWN: LeftJumpState, RIGHT_DOWN: RightJumpState,
                    LANDING: LeftRunState, JUMP: LeftJumpState,JUMPING: LeftJumpState},
    RightJumpState: {RIGHT_UP: JumpState, LEFT_UP: RightJumpState,
                     LEFT_DOWN: LeftJumpState, RIGHT_DOWN: RightJumpState,
                     LANDING: RightRunState, JUMP: RightJumpState,JUMPING: RightJumpState}
}


class Player:
    def __init__(self):
        self.x, self.y = 900, 900
        self.col_left = self.x - 30
        self.col_bottom = self.y - 40
        self.col_right = self.x + 40
        self.col_top = self.y + 40
        self.col_left_feet = self.x - 20
        self.col_bottom_feet = self.y - 40
        self.col_right_feet = self.x + 30
        self.col_top_feet = self.y - 20
        self.dir = 1
        self.velocity = 0
        self.gravity = 0
        self.gravity_max = 200
        self.jump_power = 0
        self.jump_power_max = 200
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.font = load_font('ENCR10B.TTF', 16)
        self.image_idle = load_image('Mayreel/idle.png')
        self.image_walk = load_image('Mayreel/walk.png')
        self.image_jump_up = load_image('Mayreel/jump_up/jump_up.png')
        self.image_jump_down = load_image('Mayreel/jump_down/jump_down.png')

    def get_col(self):
        return self.x - 30, self.y - 40, self.x + 40, self.y + 40

    def get_col_feet(self):
        return self.x - 20, self.y - 40, self.x + 30, self.y - 20

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
        self.col_left_feet = self.x - 20
        self.col_bottom_feet = self.y - 40
        self.col_right_feet = self.x + 30
        self.col_top_feet = self.y - 20
        # ----------------------------

        pass

    def draw(self):
        self.cur_state.draw(self)
        draw_rectangle(*self.get_col())
        draw_rectangle(*self.get_col_feet())
        self.font.draw(self.x - 60, self.y + 50, '(Time: %3.2f)' % get_time(), (255, 255, 0))
        self.font.draw(self.x - 60, self.y + 70, '%s' % self.cur_state, (255, 255, 0))
        pass

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
        pass
