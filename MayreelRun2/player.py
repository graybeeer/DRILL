from pico2d import *

import collision
import game_framework
import game_world
import server
import start_state
from missile import Cushion
from missile import Missile
from stepsmoke import Stepsmoke

PIXEL_PER_METER = (10.0 / 0.1)  # 10 pixel 10 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 16
SHOT_FRAMES_PER_ACTION = 20

RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, UP_DOWN, UP_UP, RUN_DOWN, RUN_UP, \
JUMP, JUMPING, LANDING, SHOT, SHOT_END, HIT_BLOCK, HIT_MONSTER = range(15)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_UP): UP_DOWN,
    (SDL_KEYUP, SDLK_UP): UP_UP,
    (SDL_KEYDOWN, SDLK_z): RUN_DOWN,
    (SDL_KEYUP, SDLK_z): RUN_UP,
    (SDL_KEYDOWN, SDLK_x): JUMP,
    (SDL_KEYDOWN, SDLK_c): SHOT,

}


class IdleState:
    def enter(player, event):
        player.jump_count = player.jump_count_max
        pass

    def exit(player, event):
        if event is None:
            player.frame = 0  # 프레임 초기화
        pass

    def do(player):

        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 14
        player.jumping_check()
        pass

    def draw(player):
        if player.dir > 0:
            player.image_idle.clip_composite_draw(int(player.frame) * 256, 0, 256, 256, 0, '', player.cx, player.cy,
                                                  256, 256)
        else:
            player.image_idle.clip_composite_draw(int(player.frame) * 256, 0, 256, 256, 0, 'h', player.cx + 10,
                                                  player.cy,
                                                  256, 256)

        pass


class LeftWalkState:
    def enter(player, event):
        player.jump_count = player.jump_count_max
        player.velocity -= RUN_SPEED_PPS
        player.dir = clamp(-1, player.velocity, 1)
        pass

    def exit(player, event):
        player.velocity += RUN_SPEED_PPS
        player.frame = 0  # 프레임 초기화
        player.frame_step = 0  # 달리기 구름 초기
        pass

    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 11
        player.x += player.velocity * game_framework.frame_time
        player.jumping_check()
        player.block_collide_left()

        pass

    def draw(player):
        player.image_walk.clip_composite_draw(int(player.frame) * 256, 0, 256, 256, 0, 'h', player.cx + 10, player.cy,
                                              256, 256)


class RightWalkState:
    def enter(player, event):
        player.jump_count = player.jump_count_max
        player.velocity += RUN_SPEED_PPS
        player.dir = clamp(-1, player.velocity, 1)

        pass

    def exit(player, event):
        player.velocity -= RUN_SPEED_PPS
        player.frame = 0  # 프레임 초기화
        player.frame_step = 0  # 달리기 구름 초기화
        pass

    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 11
        player.x += player.velocity * game_framework.frame_time
        player.jumping_check()
        player.block_collide_right()

        pass

    def draw(player):
        player.image_walk.clip_composite_draw(int(player.frame) * 256, 0, 256, 256, 0, '', player.cx, player.cy, 256,
                                              256)
        pass


class LeftRunState:
    def enter(player, event):
        player.jump_count = player.jump_count_max
        player.velocity -= RUN_SPEED_PPS * 1.5
        player.dir = clamp(-1, player.velocity, 1)
        pass

    def exit(player, event):
        player.velocity += RUN_SPEED_PPS * 1.5
        player.frame = 0  # 프레임 초기화
        player.frame_step = 0  # 달리기 구름 초기화
        pass

    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time * 1.5) % 11
        player.x += player.velocity * game_framework.frame_time
        # 달리기 구름 생성 주기

        player.step(player.col_right, player.col_bottom, player.frame_step_max)
        player.jumping_check()
        player.block_collide_left()

        pass

    def draw(player):
        player.image_walk.clip_composite_draw(int(player.frame) * 256, 0, 256, 256, 0, 'h', player.cx + 10,
                                              player.cy,
                                              256, 256)


class RightRunState:
    def enter(player, event):
        player.jump_count = player.jump_count_max
        player.velocity += RUN_SPEED_PPS * 1.5
        player.dir = clamp(-1, player.velocity, 1)

        pass

    def exit(player, event):
        player.velocity -= RUN_SPEED_PPS * 1.5
        player.frame = 0  # 프레임 초기화
        player.frame_step = 0  # 달리기 구름 초기화
        pass

    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time * 1.5) % 11
        player.x += player.velocity * game_framework.frame_time
        # 달리기 구름 생성 주기
        player.step(player.col_left, player.col_bottom, player.frame_step_max)
        player.jumping_check()
        player.block_collide_right()

        pass

    def draw(player):
        player.image_walk.clip_composite_draw(int(player.frame) * 256, 0, 256, 256, 0, '', player.cx, player.cy, 256,
                                              256)
        pass


class JumpState:
    def enter(player, event):
        if event == JUMP and player.jump_count > 0:  # 키를 눌러서 점프 상태가 되면 위로 점프
            player.jump_power = player.jump_power_max
            player.gravity = 0
            player.jump_count -= 1
            player.sound_jump()
        elif event == JUMPING:  # 발판에서 떨어져서 점프 상태가 됨
            player.jump_power = 0
            player.gravity = 0
            player.jump_count -= 1
        pass

    def exit(player, event):
        pass

    def do(player):
        player.jump_gravity()
        player.x += player.velocity * game_framework.frame_time
        player.y -= player.gravity * game_framework.frame_time
        player.y += player.jump_power * game_framework.frame_time
        player.block_collide_left()
        player.block_collide_right()
        player.landing_feet_head()

    def draw(player):
        if player.dir > 0:
            if player.jump_power - player.gravity >= 0:
                player.image_jump_up.clip_composite_draw(0, 0, player.image_jump_up.w, player.image_jump_up.h, 0, '',
                                                         player.cx, player.cy)
            else:
                player.image_jump_down.clip_composite_draw(0, 0, player.image_jump_up.w, player.image_jump_up.h, 0, '',
                                                           player.cx, player.cy)
        else:
            if player.jump_power - player.gravity >= 0:
                player.image_jump_up.clip_composite_draw(0, 0, player.image_jump_up.w, player.image_jump_up.h, 0, 'h',
                                                         player.cx + 10, player.cy)
            else:
                player.image_jump_down.clip_composite_draw(0, 0, player.image_jump_up.w, player.image_jump_up.h, 0, 'h',
                                                           player.cx + 10, player.cy)
        pass


class LeftJumpState:
    def enter(player, event):
        player.velocity -= RUN_SPEED_PPS
        if event == JUMP and player.jump_count > 0:
            player.jump_power = player.jump_power_max
            player.gravity = 0
            player.jump_count -= 1
            player.sound_jump()
        elif event == JUMPING:
            player.gravity = 0
            player.jump_power = 0
            player.jump_count -= 1
        player.dir = clamp(-1, player.velocity, 1)

        pass

    def exit(player, event):
        player.velocity += RUN_SPEED_PPS
        if event == JUMP and player.climb is True:  # 벽차기
            smoke = Stepsmoke(player.col_left, player.col_top)
            game_world.add_object(smoke, 3)
            player.power = player.power_climb
            player.jump_power = player.jump_power_max
            player.gravity = player.gravity_max * 0.5
            player.climb = False
            player.sound_jump()
        pass

    def do(player):
        player.jump_gravity()
        player.x += player.velocity * game_framework.frame_time
        player.y += player.jump_power * game_framework.frame_time
        player.y -= player.gravity * game_framework.frame_time

        player.block_collide_left()
        player.block_collide_right()
        player.landing_feet_head()
        if player.climb is True:
            player.angle = math.pi * 1.5
            player.step(player.col_left, player.col_top, player.frame_step_max_climb)
        else:
            player.angle = 0

    def draw(player):
        if player.jump_power - player.gravity >= 0:
            player.image_jump_up.clip_composite_draw(0, 0, player.image_jump_up.w, player.image_jump_up.h, 0, 'h',
                                                     player.cx + 10, player.cy)
        else:
            player.image_jump_down.clip_composite_draw(0, 0, player.image_jump_up.w, player.image_jump_up.h,
                                                       player.angle, 'h',
                                                       player.cx + 10, player.cy)
        pass


class RightJumpState:
    def enter(player, event):
        player.velocity += RUN_SPEED_PPS
        if event == JUMP and player.jump_count > 0:
            player.jump_power = player.jump_power_max
            player.gravity = 0
            player.jump_count -= 1
            player.sound_jump()
        elif event == JUMPING:
            player.gravity = 0
            player.jump_power = 0
            player.jump_count -= 1
        player.dir = clamp(-1, player.velocity, 1)
        pass

    def exit(player, event):
        player.velocity -= RUN_SPEED_PPS
        if event == JUMP and player.climb is True:
            smoke = Stepsmoke(player.col_right, player.col_top)
            game_world.add_object(smoke, 3)
            player.power = -player.power_climb
            player.jump_power = player.jump_power_max
            player.gravity = player.gravity_max * 0.5
            player.climb = False
            player.sound_jump()
        pass

    def do(player):
        player.jump_gravity()
        player.x += player.velocity * game_framework.frame_time
        player.y += player.jump_power * game_framework.frame_time
        player.y -= player.gravity * game_framework.frame_time

        player.block_collide_left()
        player.block_collide_right()
        player.landing_feet_head()
        if player.climb is True:
            player.angle = math.pi * 0.5
            player.step(player.col_right, player.col_top, player.frame_step_max_climb)
        else:
            player.angle = 0

    def draw(player):
        if player.jump_power - player.gravity >= 0:
            player.image_jump_up.clip_composite_draw(0, 0, player.image_jump_up.w, player.image_jump_up.h, 0, '',
                                                     player.cx, player.cy)
        else:
            player.image_jump_down.clip_composite_draw(0, 0, player.image_jump_down.w, player.image_jump_down.h,
                                                       player.angle, '', player.cx, player.cy)
        pass


class LeftJumpRunState:
    def enter(player, event):
        player.velocity -= RUN_SPEED_PPS * 1.5
        if event == JUMP and player.jump_count > 0:
            player.jump_power = player.jump_power_max
            player.gravity = 0
            player.jump_count -= 1
            player.sound_jump()
        elif event == JUMPING:
            player.gravity = 0
            player.jump_power = 0
            player.jump_count -= 1
        player.dir = clamp(-1, player.velocity, 1)

        pass

    def exit(player, event):
        player.velocity += RUN_SPEED_PPS * 1.5
        if event == JUMP and player.climb is True:
            smoke = Stepsmoke(player.col_left, player.col_top)
            game_world.add_object(smoke, 3)
            player.power = player.power_climb
            player.jump_power = player.jump_power_max
            player.gravity = player.gravity_max * 0.5
            player.climb = False
            player.sound_jump()
        pass

    def do(player):
        player.jump_gravity()
        player.x += player.velocity * game_framework.frame_time
        player.y += player.jump_power * game_framework.frame_time
        player.y -= player.gravity * game_framework.frame_time

        player.block_collide_left()
        player.block_collide_right()
        player.landing_feet_head()
        if player.climb is True:
            player.angle = math.pi * 1.5
            player.step(player.col_left, player.col_top, player.frame_step_max_climb)
        else:
            player.angle = 0

    def draw(player):
        if player.jump_power - player.gravity >= 0:
            player.image_jump_up.clip_composite_draw(0, 0, player.image_jump_up.w, player.image_jump_up.h, 0, 'h',
                                                     player.cx + 10, player.cy)
        else:
            player.image_jump_down.clip_composite_draw(0, 0, player.image_jump_up.w, player.image_jump_up.h,
                                                       player.angle, 'h',
                                                       player.cx + 10, player.cy)
        pass


class RightJumpRunState:
    def enter(player, event):
        player.velocity += RUN_SPEED_PPS * 1.5
        if event == JUMP and player.jump_count > 0:
            player.jump_power = player.jump_power_max
            player.gravity = 0
            player.jump_count -= 1
            player.sound_jump()
        elif event == JUMPING:
            player.gravity = 0
            player.jump_power = 0
            player.jump_count -= 1
        player.dir = clamp(-1, player.velocity, 1)
        pass

    def exit(player, event):
        player.velocity -= RUN_SPEED_PPS * 1.5
        if event == JUMP and player.climb is True:
            smoke = Stepsmoke(player.col_right, player.col_top)
            game_world.add_object(smoke, 3)
            player.power = -player.power_climb
            player.jump_power = player.jump_power_max
            player.gravity = player.gravity_max * 0.5
            player.climb = False
            player.sound_jump()
        pass

    def do(player):
        player.jump_gravity()
        player.x += player.velocity * game_framework.frame_time
        player.y += player.jump_power * game_framework.frame_time
        player.y -= player.gravity * game_framework.frame_time

        player.block_collide_left()
        player.block_collide_right()
        player.landing_feet_head()
        if player.climb is True:
            player.angle = math.pi * 0.5
            player.step(player.col_right, player.col_top, player.frame_step_max_climb)
        else:
            player.angle = 0

    def draw(player):
        if player.jump_power - player.gravity >= 0:
            player.image_jump_up.clip_composite_draw(0, 0, player.image_jump_up.w, player.image_jump_up.h, 0, '',
                                                     player.cx, player.cy)
        else:
            player.image_jump_down.clip_composite_draw(0, 0, player.image_jump_up.w, player.image_jump_up.h,
                                                       player.angle, '',
                                                       player.cx, player.cy)
        pass


class BalloonState:
    def enter(player, event):

        pass

    def exit(player, event):
        pass

    def do(player):
        player.jump_gravity_balloon()
        player.x += player.velocity * game_framework.frame_time
        player.y += player.jump_power * game_framework.frame_time * 0.5
        player.y -= player.gravity * game_framework.frame_time * 0.5

        player.block_collide_left()
        player.block_collide_right()
        player.landing_feet_head()

    def draw(player):
        if player.dir > 0:
            player.image_balloon.clip_composite_draw(0, 0, player.image_balloon.w, player.image_balloon.h, 0, '',
                                                     player.cx, player.cy)
        else:
            player.image_balloon.clip_composite_draw(0, 0, player.image_balloon.w, player.image_balloon.h, 0, 'h',
                                                     player.cx + 10, player.cy)
        pass


class LeftBalloonState:
    def enter(player, event):
        player.velocity -= RUN_SPEED_PPS
        player.dir = clamp(-1, player.velocity, 1)

        pass

    def exit(player, event):
        player.velocity += RUN_SPEED_PPS
        pass

    def do(player):
        player.jump_gravity_balloon()
        player.x += player.velocity * game_framework.frame_time
        player.y += player.jump_power * game_framework.frame_time * 0.5
        player.y -= player.gravity * game_framework.frame_time * 0.5

        player.block_collide_left()
        player.block_collide_right()
        player.landing_feet_head()

    def draw(player):
        player.image_balloon.clip_composite_draw(0, 0, player.image_balloon.w, player.image_balloon.h, 0, 'h',
                                                 player.cx + 10, player.cy)
        pass


class RightBalloonState:
    def enter(player, event):
        player.velocity += RUN_SPEED_PPS
        player.dir = clamp(-1, player.velocity, 1)
        pass

    def exit(player, event):
        player.velocity -= RUN_SPEED_PPS
        pass

    def do(player):
        player.jump_gravity_balloon()
        player.x += player.velocity * game_framework.frame_time
        player.y += player.jump_power * game_framework.frame_time * 0.5
        player.y -= player.gravity * game_framework.frame_time * 0.5

        player.block_collide_left()
        player.block_collide_right()
        player.landing_feet_head()

    def draw(player):
        player.image_balloon.clip_composite_draw(0, 0, player.image_balloon.w, player.image_balloon.h, 0, '',
                                                 player.cx, player.cy)
        pass


class ShotIdleState:
    def enter(player, event):
        player.jump_count = player.jump_count_max
        if event == SHOT and server.missile is None:
            player.missile_charge()

        pass

    def exit(player, event):
        if event is None:
            player.frame = 0  # 프레임 초기화
            player.timer_shot = 0
        pass

    def do(player):
        player.frame = (player.frame + SHOT_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        player.timer_shot = player.timer_shot + player.timer_shot_speed * game_framework.frame_time
        if player.timer_shot >= player.timer_shot_max:  # 미사일 발사 시간 충전
            player.timer_shot = 0
            player.add_event(SHOT_END)  # 미사일 발사
        player.jumping_check()

    def draw(player):
        if player.dir > 0:
            player.image_shot_loop.clip_composite_draw(int(player.frame) * 256, 0, 256, 256, 0, '', player.cx,
                                                       player.cy,
                                                       256, 256)
        else:
            player.image_shot_loop.clip_composite_draw(int(player.frame) * 256, 0, 256, 256, 0, 'h', player.cx + 10,
                                                       player.cy, 256, 256)
        pass


class ShotLeftRunState:
    def enter(player, event):
        player.jump_count = player.jump_count_max
        player.velocity -= RUN_SPEED_PPS * 0.5
        if event == SHOT and server.missile is None:
            player.missile_charge()
        pass

    def exit(player, event):
        player.velocity += RUN_SPEED_PPS * 0.5
        if event is None:
            player.frame = 0  # 프레임 초기화
            player.timer_shot = 0
        pass

    def do(player):
        player.frame = (player.frame + SHOT_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        player.timer_shot = player.timer_shot + player.timer_shot_speed * game_framework.frame_time
        if player.timer_shot >= player.timer_shot_max:  # 미사일 발사 시간 충전
            player.timer_shot = 0
            player.add_event(SHOT_END)  # 미사일 발사

        player.x += player.velocity * game_framework.frame_time  # 플레이어 x축 이동
        player.jumping_check()
        player.block_collide_left()
        player.block_collide_right()
        pass

    def draw(player):
        if player.dir > 0:
            player.image_shot_loop.clip_composite_draw(int(player.frame) * 256, 0, 256, 256, 0, '', player.cx,
                                                       player.cy,
                                                       256, 256)
        else:
            player.image_shot_loop.clip_composite_draw(int(player.frame) * 256, 0, 256, 256, 0, 'h', player.cx + 10,
                                                       player.cy, 256, 256)
        pass


class ShotRightRunState:
    def enter(player, event):
        player.jump_count = player.jump_count_max
        player.velocity += RUN_SPEED_PPS * 0.5
        if event == SHOT and server.missile is None:
            player.missile_charge()
        pass

    def exit(player, event):
        player.velocity -= RUN_SPEED_PPS * 0.5
        if event is None:
            player.frame = 0  # 프레임 초기화
            player.timer_shot = 0
        pass

    def do(player):
        player.frame = (player.frame + SHOT_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        player.timer_shot = player.timer_shot + player.timer_shot_speed * game_framework.frame_time
        if player.timer_shot >= player.timer_shot_max:  # 미사일 발사 시간 충전
            player.timer_shot = 0
            player.add_event(SHOT_END)  # 미사일 발사

        player.x += player.velocity * game_framework.frame_time  # 플레이어 x축 이동
        player.jumping_check()
        player.block_collide_left()
        player.block_collide_right()
        pass

    def draw(player):
        if player.dir > 0:
            player.image_shot_loop.clip_composite_draw(int(player.frame) * 256, 0, 256, 256, 0, '', player.cx,
                                                       player.cy,
                                                       256, 256)
        else:
            player.image_shot_loop.clip_composite_draw(int(player.frame) * 256, 0, 256, 256, 0, 'h', player.cx + 10,
                                                       player.cy, 256, 256)
        pass


class ShotJumpState:
    def enter(player, event):
        if event == SHOT and server.missile is None:
            player.missile_charge()
        if event == JUMP and player.jump_count > 0:
            player.jump_power = player.jump_power_max
            player.gravity = 0
            player.jump_count -= 1
        elif event == JUMPING:
            player.gravity = 0
            player.jump_power = 0
            player.jump_count -= 1
        pass

    def exit(player, event):
        if event is None:
            player.frame = 0  # 프레임 초기화
            player.timer_shot = 0
        pass

    def do(player):
        player.frame = (player.frame + SHOT_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        player.timer_shot = player.timer_shot + player.timer_shot_speed * game_framework.frame_time
        if player.timer_shot >= player.timer_shot_max:  # 미사일 발사 시간 충전
            player.timer_shot = 0
            player.add_event(SHOT_END)  # 미사일 발사

        player.jump_gravity()
        player.x += player.velocity * game_framework.frame_time
        player.y -= player.gravity * game_framework.frame_time * 0.5
        player.y += player.jump_power * game_framework.frame_time * 0.5

        player.landing_feet_head()
        pass

    def draw(player):
        if player.dir > 0:
            player.image_shot_loop.clip_composite_draw(int(player.frame) * 256, 0, 256, 256, 0, '', player.cx,
                                                       player.cy,
                                                       256, 256)
        else:
            player.image_shot_loop.clip_composite_draw(int(player.frame) * 256, 0, 256, 256, 0, 'h', player.cx + 10,
                                                       player.cy, 256, 256)
        pass


class ShotLeftJumpState:
    def enter(player, event):
        player.velocity -= RUN_SPEED_PPS * 0.5
        if event == SHOT and server.missile is None:
            player.missile_charge()
        if event == JUMP and player.jump_count > 0:
            player.jump_power = player.jump_power_max
            player.gravity = 0
            player.jump_count -= 1
        elif event == JUMPING:
            player.gravity = 0
            player.jump_power = 0
            player.jump_count -= 1
        pass

    def exit(player, event):
        player.velocity += RUN_SPEED_PPS * 0.5
        if event is None:
            player.frame = 0  # 프레임 초기화
            player.timer_shot = 0
        pass

    def do(player):
        player.frame = (player.frame + SHOT_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        player.timer_shot = player.timer_shot + player.timer_shot_speed * game_framework.frame_time
        if player.timer_shot >= player.timer_shot_max:  # 미사일 발사 시간 충전
            player.timer_shot = 0
            player.add_event(SHOT_END)  # 미사일 발사

        player.jump_gravity()
        player.x += player.velocity * game_framework.frame_time
        player.y -= player.gravity * game_framework.frame_time * 0.5
        player.y += player.jump_power * game_framework.frame_time * 0.5
        player.block_collide_left()
        player.landing_feet_head()
        pass

    def draw(player):
        if player.dir > 0:
            player.image_shot_loop.clip_composite_draw(int(player.frame) * 256, 0, 256, 256, 0, '', player.cx,
                                                       player.cy,
                                                       256, 256)
        else:
            player.image_shot_loop.clip_composite_draw(int(player.frame) * 256, 0, 256, 256, 0, 'h', player.cx + 10,
                                                       player.cy, 256, 256)
        pass


class ShotRightJumpState:
    def enter(player, event):
        player.velocity += RUN_SPEED_PPS * 0.5
        if event == SHOT and server.missile is None:
            player.missile_charge()
        if event == JUMP and player.jump_count > 0:
            player.jump_power = player.jump_power_max
            player.gravity = 0
            player.jump_count -= 1
        elif event == JUMPING:
            player.gravity = 0
            player.jump_power = 0
            player.jump_count -= 1
        pass

    def exit(player, event):
        player.velocity -= RUN_SPEED_PPS * 0.5
        if event is None:
            player.frame = 0  # 프레임 초기화
            player.timer_shot = 0
        pass

    def do(player):
        player.frame = (player.frame + SHOT_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        player.timer_shot = player.timer_shot + player.timer_shot_speed * game_framework.frame_time
        if player.timer_shot >= player.timer_shot_max:  # 미사일 발사 시간 충전
            player.timer_shot = 0
            player.add_event(SHOT_END)  # 미사일 발사

        player.jump_gravity()
        player.x += player.velocity * game_framework.frame_time
        player.y -= player.gravity * game_framework.frame_time * 0.5
        player.y += player.jump_power * game_framework.frame_time * 0.5
        player.block_collide_right()
        player.landing_feet_head()
        pass

    def draw(player):
        if player.dir > 0:
            player.image_shot_loop.clip_composite_draw(int(player.frame) * 256, 0, 256, 256, 0, '', player.cx,
                                                       player.cy,
                                                       256, 256)
        else:
            player.image_shot_loop.clip_composite_draw(int(player.frame) * 256, 0, 256, 256, 0, 'h', player.cx + 10,
                                                       player.cy, 256, 256)
        pass


next_state_table = {
    IdleState: {RIGHT_DOWN: RightWalkState, LEFT_DOWN: LeftWalkState,
                JUMPING: JumpState, JUMP: JumpState, SHOT: ShotIdleState},
    LeftWalkState: {LEFT_UP: IdleState, RIGHT_DOWN: RightWalkState,
                    JUMPING: LeftJumpState, JUMP: LeftJumpState,
                    SHOT: ShotLeftRunState, RUN_DOWN: LeftRunState},
    RightWalkState: {RIGHT_UP: IdleState, LEFT_DOWN: LeftWalkState,
                     JUMPING: RightJumpState, JUMP: RightJumpState,
                     SHOT: ShotRightRunState, RUN_DOWN: RightRunState},
    LeftRunState: {LEFT_UP: IdleState, RIGHT_DOWN: RightRunState,
                   JUMPING: LeftJumpRunState, JUMP: LeftJumpRunState, LANDING: LeftWalkState,
                   SHOT: ShotLeftRunState, RUN_UP: LeftWalkState},
    RightRunState: {RIGHT_UP: IdleState, LEFT_DOWN: LeftRunState,
                    JUMPING: RightJumpRunState, JUMP: RightJumpRunState, LANDING: RightWalkState,
                    SHOT: ShotRightRunState, RUN_UP: RightWalkState},

    JumpState: {LEFT_DOWN: LeftJumpState, RIGHT_DOWN: RightJumpState,
                LANDING: IdleState, SHOT: ShotJumpState, UP_DOWN: BalloonState},
    LeftJumpState: {LEFT_UP: JumpState, RIGHT_DOWN: RightJumpState, LANDING: LeftWalkState,
                    SHOT: ShotLeftJumpState, RUN_DOWN: LeftJumpRunState, UP_DOWN: LeftBalloonState},
    RightJumpState: {RIGHT_UP: JumpState, LEFT_DOWN: LeftJumpState, LANDING: RightWalkState,
                     SHOT: ShotRightJumpState, RUN_DOWN: RightJumpRunState, UP_DOWN: RightBalloonState},

    LeftJumpRunState: {LEFT_UP: JumpState, RIGHT_DOWN: RightJumpRunState,
                       LANDING: LeftRunState, SHOT: ShotLeftJumpState, UP_DOWN: LeftBalloonState},
    RightJumpRunState: {RIGHT_UP: JumpState, LEFT_DOWN: LeftJumpRunState,
                        LANDING: RightRunState, SHOT: ShotRightJumpState, UP_DOWN: RightBalloonState},

    BalloonState: {LEFT_DOWN: LeftBalloonState, RIGHT_DOWN: RightBalloonState,
                   LANDING: IdleState, UP_UP: JumpState},
    LeftBalloonState: {LEFT_UP: BalloonState, RIGHT_DOWN: RightBalloonState,
                       LANDING: LeftWalkState, UP_UP: LeftJumpState},
    RightBalloonState: {RIGHT_UP: BalloonState, LEFT_DOWN: LeftBalloonState,
                        LANDING: RightWalkState, UP_UP: RightJumpState},

    ShotIdleState: {LEFT_DOWN: ShotLeftRunState, RIGHT_DOWN: ShotRightRunState,
                    JUMPING: ShotJumpState, JUMP: ShotJumpState, SHOT_END: IdleState},
    ShotLeftRunState: {LEFT_UP: ShotIdleState, RIGHT_DOWN: ShotRightRunState,
                       JUMPING: ShotLeftJumpState, JUMP: ShotLeftJumpState,
                       SHOT: ShotIdleState, SHOT_END: LeftWalkState},
    ShotRightRunState: {RIGHT_UP: ShotIdleState, LEFT_DOWN: ShotLeftRunState,
                        JUMPING: ShotRightJumpState, JUMP: ShotRightJumpState,
                        LANDING: ShotIdleState, SHOT_END: RightWalkState},

    ShotJumpState: {LEFT_DOWN: ShotLeftJumpState, RIGHT_DOWN: ShotRightJumpState,
                    LANDING: ShotIdleState, SHOT_END: JumpState},
    ShotLeftJumpState: {LEFT_UP: ShotJumpState, RIGHT_DOWN: ShotRightJumpState,
                        LANDING: ShotLeftRunState, SHOT_END: LeftJumpState},
    ShotRightJumpState: {RIGHT_UP: ShotJumpState, LEFT_DOWN: ShotLeftJumpState,
                         JUMPING: ShotJumpState, JUMP: ShotJumpState,
                         LANDING: ShotRightRunState, SHOT_END: RightJumpState},

}


class Player:
    def __init__(self):
        self.x, self.y = server.player_start_x, server.player_start_y
        self.cx, self.cy = 800, 450
        self.col_left = self.x - 30
        self.col_bottom = self.y - 40
        self.col_right = self.x + 40
        self.col_top = self.y + 40
        self.col_left_c = self.cx - 30
        self.col_bottom_c = self.cy - 40
        self.col_right_c = self.cx + 40
        self.col_top_c = self.cy + 40
        self.dir = 1  # 플레이어 방향
        self.velocity = 0  # 플레이어 속도 양수 오른쪽 음수 왼쪽
        self.distance = 0  # 플레이어 총 이동거리
        self.gravity = 0  # 플레이어 중력
        self.gravity_tic = 1000  # 프레임당 추가되는 중력
        self.gravity_max = 700  # 최대 중력
        self.jump_power = 0  # 점프 힘
        self.jump_power_tic = 1000  # 프레임당 줄어드는 점프힘
        self.jump_power_max = 1000  # 점프 힘 최대
        self.jump_count = 1  # 점프 카운트
        self.jump_count_max = 1  # 최대 가능 점프 횟수
        self.frame = 0
        self.timer_shot = 0  # 미사일 발사 준비 시간
        self.timer_shot_max = 200
        self.timer_shot_speed = 100
        self.shot_chance = 0  # 발사 남은 횟수
        self.shot_chance_max = 3  # 발사 저장가능 최대 횟수
        self.frame_step = 0  # 대쉬 구름 시간 카운트
        self.frame_step_max = 100
        self.climb = False  # 벽타기 상태
        self.power = 0  # 가해지는 힘
        self.power_climb = 800
        self.frame_step_max_climb = 500
        self.angle = 0  # 플레이어 그림 각도
        self.balloon_timer = 0
        self.balloon_timer_max = 0
        # ---------------------------------------------- 플레이어 상태
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        # ----------------------------------------------
        self.font = load_font('ENCR10B.TTF', 16)
        self.image_idle = load_image('Mayreel/idle/idle.png')
        self.image_walk = load_image('Mayreel/walk/walk.png')
        self.image_jump_up = load_image('Mayreel/jump_up/jump_up.png')
        self.image_jump_down = load_image('Mayreel/jump_down/jump_down.png')
        self.image_shot_loop = load_image('Mayreel/shot/shot_loop.png')
        self.image_balloon = load_image('Mayreel/balloon/balloon.png')
        # ---------------------------------------------- 음악
        self.jump_sound = load_wav('Mayreel/01_player_jump_01.wav')
        self.jump_sound.set_volume(100)

    # ---------------------------------------------------------------- 플레이어 콜라이더
    def get_col(self):
        return self.x - 30, self.y - 40, self.x + 40, self.y + 40

    def get_col_feet(self):
        return self.x - 20, self.y - 40, self.x + 30, self.y - 20

    def get_col_head(self):
        return self.x - 20, self.y + 20, self.x + 30, self.y + 40

    def get_col_body_left(self):
        return self.x - 30, self.y - 35, self.x - 20, self.y + 35

    def get_col_body_right(self):
        return self.x + 30, self.y - 35, self.x + 40, self.y + 35

    # ---------------------------------------------------------------- 플레이어 콜라이더 카메라
    def get_col_c(self):
        return self.cx - 30, self.cy - 40, self.cx + 40, self.cy + 40

    def get_col_feet_c(self):
        return self.cx - 20, self.cy - 40, self.cx + 30, self.cy - 20

    def get_col_head_c(self):
        return self.cx - 20, self.cy + 20, self.cx + 30, self.cy + 40

    def get_col_body_left_c(self):
        return self.cx - 30, self.cy - 35, self.cx - 20, self.cy + 35

    def get_col_body_right_c(self):
        return self.cx + 30, self.cy - 35, self.cx + 40, self.cy + 35

    # ----------------------------------------------------------------
    def add_event(self, event):
        self.event_que.insert(0, event)

    def step(self, x, y, timer):  # 대쉬 시에 달린 자리에 구름 만들기
        self.frame_step = self.frame_step + 1000 * game_framework.frame_time
        if self.frame_step >= timer:
            smoke = Stepsmoke(x, y)
            game_world.add_object(smoke, 3)
            self.frame_step -= timer

    def missile_charge(self):
        if self.shot_chance > 0:
            missile = Missile()
            game_world.add_object(missile, 4)
            server.missile = 1
            self.shot_chance -= 1
            self.shot_chance = clamp(0, self.shot_chance, self.shot_chance_max)

    def update(self):
        temp_x = server.player_area_x
        temp_y = server.player_area_y
        if self.power != 0:
            self.x += self.power * game_framework.frame_time
            self.x -= self.velocity * game_framework.frame_time
        if 40 >= self.power >= -40:
            self.power = 0
        elif self.power > 40:
            self.power -= 6
        elif self.power < -40:
            self.power += 6
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            if event not in next_state_table[self.cur_state]:  # 다음 키값이 없으면 그대로
                pass
            else:
                self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)
        # ---------------------------- 플레이어 콜라이더 위치 변경

        self.x = clamp(30, self.x, server.map_area_size_x * server.map_area_x - 40)  # 플레이어 위치 제한
        self.y = clamp(-500, self.y, server.map_area_size_y * server.map_area_y - 40)
        if self.y < -300:
            self.x = server.player_start_x
            self.y = server.player_start_y
        server.player_area_x = self.x // server.map_area_size_x
        server.player_area_y = self.y // server.map_area_size_y
        if temp_x != server.player_area_x:  # 플레이어가 있는 구역이 변화되면
            for block in (server.block + server.block_sleep):  # 블럭 상태 업데이트
                block.block_update()
            for monster in (server.monster + server.monster_sleep):  # 몬스터 상태 업데이트
                monster.monster_update()
            for background in (server.background + server.background_sleep):  # 배경 물건 상태 업데이트
                background.background_update()
        elif temp_y != server.player_area_y:
            for block in (server.block + server.block_sleep):  # 블럭 상태 업데이트
                block.block_update()
            for monster in (server.monster + server.monster_sleep):  # 몬스터 상태 업데이트
                monster.monster_update()
            for background in (server.background + server.background_sleep):  # 배경 물건 상태 업데이트
                background.background_update()

        self.col_left = self.x - 30
        self.col_bottom = self.y - 40
        self.col_right = self.x + 40
        self.col_top = self.y + 40
        # ----------------------------
        if self.x <= 800:
            self.cx = self.x
        elif self.x > 800:
            self.cx = 800
        if self.y <= 450:
            self.cy = self.y
        elif self.y > 450:
            self.cy = 450
        server.cx = -self.x + self.cx
        server.cy = -self.y + self.cy
        # ----------------------------
        pass

    def draw(self):
        self.cur_state.draw(self)
        """draw_rectangle(*self.get_col_c())
        draw_rectangle(*self.get_col_feet_c())
        draw_rectangle(*self.get_col_head_c())
        draw_rectangle(*self.get_col_body_right_c())
        draw_rectangle(*self.get_col_body_left_c())

        self.font.draw(self.cx - 60, self.cy + 50, '%s' % self.cur_state, (255, 255, 0))
        self.font.draw(self.cx - 60, self.cy + 70, '(%.2f %.2f)' % (self.x, self.y), (255, 255, 0))
        self.font.draw(self.cx - 60, self.cy + 90, '(%d %d)' % (server.cx, server.cy), (255, 255, 0))"""
        pass

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
        pass

    def jump_gravity(self):
        if self.gravity < self.gravity_max:  # 최대까지 중력 증가
            self.gravity += self.gravity_tic * game_framework.frame_time
        elif self.gravity >= self.gravity_max:
            self.gravity = self.gravity_max
        if self.jump_power > 0:
            self.jump_power -= self.jump_power_tic * game_framework.frame_time
            if self.jump_power <= 0:
                self.jump_power = 0

    def jump_gravity_balloon(self):
        if self.gravity < self.gravity_max:  # 최대까지 중력 증가
            self.gravity += self.gravity_tic * game_framework.frame_time * 0.5
        elif self.gravity >= self.gravity_max:
            self.gravity = self.gravity_max
        if self.jump_power > 0:
            self.jump_power -= self.jump_power_tic * game_framework.frame_time * 0.5
            if self.jump_power <= 0:
                self.jump_power = 0

    def landing_feet_head(self):
        for block in server.block:
            if collision.collide(self.get_col_feet(), block.get_col()) and (
                    self.jump_power - self.gravity) <= 0:
                self.y = 40 + block.col_top
                self.add_event(LANDING)
                break
            elif collision.collide(self.get_col_head(), block.get_col()) and (
                    self.jump_power - self.gravity) > 0:
                self.y = -40 + block.col_bottom
                self.jump_power = 0
                if block.code == 8:
                    cushion = Cushion(block.x, block.y + 98)
                    game_world.add_object(cushion, 3)
                    block.code = 9

                break

    def block_collide_left(self):
        for block in server.block:
            if collision.collide(self.get_col_body_left(), block.get_col()):
                if block.code == 10 or block.code == 11: # 깃발에 부딪히면 끝
                    game_framework.change_state(start_state)
                self.x = 30 + block.col_right
                if self.cur_state is LeftJumpState or self.cur_state is LeftJumpRunState:  # 벽에 방향키 누르면서 붙어있으면
                    if self.jump_power <= self.gravity:
                        self.jump_power = 0
                        self.gravity = self.gravity_max * 0.2
                        self.climb = True
                else:
                    self.climb = False
                break
            self.climb = False

    def block_collide_right(self):
        for block in server.block:
            if collision.collide(self.get_col_body_right(), block.get_col()):
                if block.code == 10 or block.code == 11: # 깃발에 부딪히면 끝
                    game_framework.change_state(start_state)
                self.x = -40 + block.col_left
                if self.cur_state is RightJumpState or self.cur_state is RightJumpRunState:  # 벽에 방향키 누르면서 붙어있으면
                    if self.jump_power <= self.gravity:
                        self.jump_power = 0
                        self.gravity = self.gravity_max * 0.2
                        self.climb = True
                    else:
                        self.climb = False
                    break
                self.climb = False

    def jumping_check(self):
        for block in server.block:
            if collision.collide(self.get_col_feet(), block.get_col()):
                break
            if block == server.block[len(server.block) - 1]:
                self.add_event(JUMPING)

    def sound_jump(self):
        self.jump_sound.play()

    def balloon_time(self):  # 풍선 시간 타이머
        self.balloon_timer += 100 * game_framework.frame_time
        if self.balloon_timer > self.balloon_timer_max:
            self.balloon_timer -= self.balloon_timer_max
            self.add_event(UP_UP)

    # 저장할 정보를 선택하는 함수
    def __getstate__(self):
        state = {'x': self.x, 'y': self.y}
        return state

    # 정보를 복구하는 함수
    def __setstate__(self, state):
        self.__init__()
        self.__dict__.update(state)
