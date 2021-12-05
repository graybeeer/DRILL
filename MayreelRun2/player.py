from pico2d import *

import collision
import game_framework
import game_world
import server
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

RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, JUMP, JUMPING, LANDING, SHOT, SHOT_END, HIT_BLOCK, HIT_MONSTER = range(11)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_z): JUMP,
    (SDL_KEYDOWN, SDLK_x): SHOT
}


class IdleState:
    def enter(player, event):
        player.jump_count = player.jump_count_max
        pass

    def exit(player, event):
        player.frame = 0  # 프레임 초기화
        pass

    def do(player):

        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 14
        for block in server.block:
            if collision.collide(player.get_col_feet(), block.get_col()):
                break
            if block == server.block[len(server.block) - 1]:
                player.add_event(JUMPING)
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


class LeftRunState:
    def enter(player, event):
        player.jump_count = player.jump_count_max
        player.velocity -= RUN_SPEED_PPS
        player.dir = clamp(-1, player.velocity, 1)
        pass

    def exit(player, event):
        player.velocity += RUN_SPEED_PPS
        player.frame = 0  # 프레임 초기화
        player.frame_step = 0  # 달리기 구름 초기화
        pass

    def do(player):

        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 11
        player.x += player.velocity * game_framework.frame_time
        # 달리기 구름 생성 주기
        player.frame_step = player.frame_step + player.frame_step_speed * game_framework.frame_time
        if player.frame_step >= player.frame_step_max:
            player.step(player.col_right, player.col_bottom)
            player.frame_step -= player.frame_step_max
        for block in server.block:
            if collision.collide(player.get_col_feet(), block.get_col()):
                break
            elif block == server.block[len(server.block) - 1]:
                player.add_event(JUMPING)
        for block in server.block:
            if collision.collide(player.get_col_body_left(), block.get_col()):
                player.x = 30 + block.col_right
        pass

    def draw(player):
        player.image_walk.clip_composite_draw(int(player.frame) * 256, 0, 256, 256, 0, 'h', player.cx + 10, player.cy,
                                              256, 256)


class RightRunState:
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
        # 달리기 구름 생성 주기
        player.frame_step = player.frame_step + player.frame_step_speed * game_framework.frame_time
        if player.frame_step >= player.frame_step_max:
            player.step(player.col_left, player.col_bottom)
            player.frame_step -= player.frame_step_max

        for block in server.block:
            if collision.collide(player.get_col_feet(), block.get_col()):
                break
            elif block == server.block[len(server.block) - 1]:
                player.add_event(JUMPING)
        for block in server.block:
            if collision.collide(player.get_col_body_right(), block.get_col()):
                player.x = -40 + block.col_left

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
        elif event == JUMPING:  # 발판에서 떨어져서 점프 상태가 됨
            player.jump_power = 0
            player.gravity = 0
            player.jump_count -= 1
        pass

    def exit(player, event):
        pass

    def do(player):
        if player.gravity < player.gravity_max:
            player.gravity += player.gravity_tic * game_framework.frame_time
        elif player.gravity >= player.gravity_max:
            player.gravity = player.gravity_max
        if player.jump_power > 0:
            player.jump_power -= player.jump_power_tic * game_framework.frame_time
            if player.jump_power <= 0:
                player.jump_power = 0
        player.x += player.velocity * game_framework.frame_time
        player.y -= player.gravity * game_framework.frame_time
        player.y += player.jump_power * game_framework.frame_time

        for block in server.block:
            if collision.collide(player.get_col_feet(), block.get_col()) and (
                    player.jump_power - player.gravity) <= 0:
                player.y = 40 + block.col_top
                player.add_event(LANDING)
                break
            elif collision.collide(player.get_col_head(), block.get_col()) and (
                    player.jump_power - player.gravity) > 0:
                player.y = -40 + block.col_bottom
                player.jump_power = 0
                break

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
        elif event == JUMPING:
            player.gravity = 0
            player.jump_power = 0
            player.jump_count -= 1
        player.dir = clamp(-1, player.velocity, 1)

        pass

    def exit(player, event):
        player.velocity += RUN_SPEED_PPS
        pass

    def do(player):
        if player.gravity < player.gravity_max:
            player.gravity += player.gravity_tic * game_framework.frame_time
        elif player.gravity >= player.gravity_max:
            player.gravity = player.gravity_max
        if player.jump_power > 0:
            player.jump_power -= player.jump_power_tic * game_framework.frame_time
            if player.jump_power <= 0:
                player.jump_power = 0
        player.x += player.velocity * game_framework.frame_time
        player.y += player.jump_power * game_framework.frame_time
        player.y -= player.gravity * game_framework.frame_time

        for block in server.block:
            if collision.collide(player.get_col_body_left(), block.get_col()):
                player.x = 30 + block.col_right
                break
        for block in server.block:
            if collision.collide(player.get_col_feet(), block.get_col()) and (
                    player.jump_power - player.gravity) <= 0:
                player.y = 40 + block.col_top
                player.add_event(LANDING)
                break
        for block in server.block:
            if collision.collide(player.get_col_head(), block.get_col()) and (
                    player.jump_power - player.gravity) > 0:
                player.y = -40 + block.col_bottom
                player.jump_power = 0
                break

    def draw(player):
        if player.jump_power - player.gravity >= 0:
            player.image_jump_up.clip_composite_draw(0, 0, player.image_jump_up.w, player.image_jump_up.h, 0, 'h',
                                                     player.cx + 10, player.cy)
        else:
            player.image_jump_down.clip_composite_draw(0, 0, player.image_jump_up.w, player.image_jump_up.h, 0, 'h',
                                                       player.cx + 10, player.cy)
        pass


class RightJumpState:
    def enter(player, event):
        player.velocity += RUN_SPEED_PPS
        if event == JUMP and player.jump_count > 0:
            player.jump_power = player.jump_power_max
            player.gravity = 0
            player.jump_count -= 1
        elif event == JUMPING:
            player.gravity = 0
            player.jump_power = 0
            player.jump_count -= 1
        player.dir = clamp(-1, player.velocity, 1)
        pass

    def exit(player, event):
        player.velocity -= RUN_SPEED_PPS
        pass

    def do(player):
        if player.gravity < player.gravity_max:
            player.gravity += player.gravity_tic * game_framework.frame_time
        elif player.gravity >= player.gravity_max:
            player.gravity == player.gravity_max
        if player.jump_power > 0:
            player.jump_power -= player.jump_power_tic * game_framework.frame_time
            if player.jump_power <= 0:
                player.jump_power = 0
        player.x += player.velocity * game_framework.frame_time
        player.y += player.jump_power * game_framework.frame_time
        player.y -= player.gravity * game_framework.frame_time

        for block in server.block:
            if collision.collide(player.get_col_body_right(), block.get_col()):
                player.x = -40 + block.col_left
                break
        for block in server.block:
            if collision.collide(player.get_col_feet(), block.get_col()) and (
                    player.jump_power - player.gravity) <= 0:
                player.y = 40 + block.col_top
                player.add_event(LANDING)
                break
        for block in server.block:
            if collision.collide(player.get_col_head(), block.get_col()) and (
                    player.jump_power - player.gravity) > 0:
                player.y = -40 + block.col_bottom
                player.jump_power = 0
                break

    def draw(player):
        if player.jump_power - player.gravity >= 0:
            player.image_jump_up.clip_composite_draw(0, 0, player.image_jump_up.w, player.image_jump_up.h, 0, '',
                                                     player.cx, player.cy)
        else:
            player.image_jump_down.clip_composite_draw(0, 0, player.image_jump_up.w, player.image_jump_up.h, 0, '',
                                                       player.cx, player.cy)
        pass


class LeftBounceState:
    def enter(player, event):
        pass

    def exit(player, event):
        pass

    def do(player):
        player.x += player.velocity * game_framework.frame_time
        player.y += player.jump_power * game_framework.frame_time
        player.y -= player.gravity * game_framework.frame_time
        for block in server.block:
            if collision.collide(player.get_col_feet(), block.get_col()) and (
                    player.jump_power - player.gravity) <= 0:
                player.y = 40 + block.col_top
                player.add_event(LANDING)
                break
        pass

    def draw(player):
        pass


class RightBounceState:
    def enter(player, event):
        pass

    def exit(player, event):
        pass

    def do(player):
        pass

    def draw(player):
        pass


class ShotIdleState:
    def enter(player, event):
        player.jump_count = player.jump_count_max
        pass

    def exit(player, event):
        if event is None:
            player.frame = 0  # 프레임 초기화
            player.frame_shot = 0
        pass

    def do(player):
        player.frame = (player.frame + SHOT_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        player.frame_shot = player.frame_shot + player.frame_shot_speed * game_framework.frame_time
        if player.frame_shot >= player.frame_shot_max:  # 미사일 발사 시간 충전
            player.frame_shot = 0
            player.add_event(SHOT_END)  # 미사일 발사

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
        player.velocity -= RUN_SPEED_PPS
        pass

    def exit(player, event):
        player.velocity += RUN_SPEED_PPS
        if event is None:
            player.frame = 0  # 프레임 초기화
            player.frame_shot = 0
        pass

    def do(player):
        player.frame = (player.frame + SHOT_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        player.frame_shot = player.frame_shot + player.frame_shot_speed * game_framework.frame_time
        if player.frame_shot >= player.frame_shot_max:  # 미사일 발사 시간 충전
            player.frame_shot = 0
            player.add_event(SHOT_END)  # 미사일 발사

        player.x += player.velocity * game_framework.frame_time  # 플레이어 x축 이동
        for block in server.block:
            if collision.collide(player.get_col_feet(), block.get_col()):
                break
            if block == server.block[len(server.block) - 1]:
                player.add_event(JUMPING)
        for block in server.block:
            if collision.collide(player.get_col_body_left(), block.get_col()):
                player.x = 30 + block.col_right
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
        player.velocity += RUN_SPEED_PPS
        pass

    def exit(player, event):
        player.velocity -= RUN_SPEED_PPS
        if event is None:
            player.frame = 0  # 프레임 초기화
            player.frame_shot = 0
        pass

    def do(player):
        player.frame = (player.frame + SHOT_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        player.frame_shot = player.frame_shot + player.frame_shot_speed * game_framework.frame_time
        if player.frame_shot >= player.frame_shot_max:  # 미사일 발사 시간 충전
            player.frame_shot = 0
            player.add_event(SHOT_END)  # 미사일 발사

        player.x += player.velocity * game_framework.frame_time  # 플레이어 x축 이동
        for block in server.block:
            if collision.collide(player.get_col_feet(), block.get_col()):
                break
            if block == server.block[len(server.block) - 1]:
                player.add_event(JUMPING)

        for block in server.block:
            if collision.collide(player.get_col_body_right(), block.get_col()):
                player.x = -40 + block.col_left
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
            player.frame_shot = 0
        pass

    def do(player):
        player.frame = (player.frame + SHOT_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        player.frame_shot = player.frame_shot + player.frame_shot_speed * game_framework.frame_time
        if player.frame_shot >= player.frame_shot_max:  # 미사일 발사 시간 충전
            player.frame_shot = 0
            player.add_event(SHOT_END)  # 미사일 발사

        if player.gravity < player.gravity_max:  # 최대까지 중력 증가
            player.gravity += player.gravity_tic * game_framework.frame_time
        elif player.gravity >= player.gravity_max:
            player.gravity = player.gravity_max
        if player.jump_power > 0:
            player.jump_power -= player.jump_power_tic * game_framework.frame_time
            if player.jump_power <= 0:
                player.jump_power = 0
        player.x += player.velocity * game_framework.frame_time
        player.y -= player.gravity * game_framework.frame_time
        player.y += player.jump_power * game_framework.frame_time

        for block in server.block:
            if collision.collide(player.get_col_feet(), block.get_col()) and (player.jump_power - player.gravity) <= 0:
                player.y = 40 + block.col_top
                player.add_event(LANDING)
                break
            elif collision.collide(player.get_col_head(), block.get_col()) and (
                    player.jump_power - player.gravity) > 0:
                player.y = -40 + block.col_bottom
                player.jump_power = 0
                break
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
        player.velocity -= RUN_SPEED_PPS
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
        player.velocity += RUN_SPEED_PPS
        if event is None:
            player.frame = 0  # 프레임 초기화
            player.frame_shot = 0
        pass

    def do(player):
        player.frame = (player.frame + SHOT_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        player.frame_shot = player.frame_shot + player.frame_shot_speed * game_framework.frame_time
        if player.frame_shot >= player.frame_shot_max:  # 미사일 발사 시간 충전
            player.frame_shot = 0
            player.add_event(SHOT_END)  # 미사일 발사

        if player.gravity < player.gravity_max:  # 최대까지 중력 증가
            player.gravity += player.gravity_tic * game_framework.frame_time
        elif player.gravity >= player.gravity_max:
            player.gravity = player.gravity_max
        if player.jump_power > 0:
            player.jump_power -= player.jump_power_tic * game_framework.frame_time
            if player.jump_power <= 0:
                player.jump_power = 0
        player.x += player.velocity * game_framework.frame_time
        player.y -= player.gravity * game_framework.frame_time
        player.y += player.jump_power * game_framework.frame_time
        for block in server.block:
            if collision.collide(player.get_col_body_left(), block.get_col()):
                player.x = 30 + block.col_right
                break
        for block in server.block:
            if collision.collide(player.get_col_feet(), block.get_col()) and (
                    player.jump_power - player.gravity) <= 0:
                player.y = 40 + block.col_top
                player.add_event(LANDING)
                break
        for block in server.block:
            if collision.collide(player.get_col_head(), block.get_col()) and (
                    player.jump_power - player.gravity) > 0:
                player.y = -40 + block.col_bottom
                player.jump_power = 0
                break
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
        player.velocity += RUN_SPEED_PPS
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
        player.velocity -= RUN_SPEED_PPS
        if event is None:
            player.frame = 0  # 프레임 초기화
            player.frame_shot = 0
        pass

    def do(player):
        player.frame = (player.frame + SHOT_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        player.frame_shot = player.frame_shot + player.frame_shot_speed * game_framework.frame_time
        if player.frame_shot >= player.frame_shot_max:  # 미사일 발사 시간 충전
            player.frame_shot = 0
            player.add_event(SHOT_END)  # 미사일 발사

        if player.gravity < player.gravity_max:  # 최대까지 중력 증가
            player.gravity += player.gravity_tic * game_framework.frame_time
        elif player.gravity >= player.gravity_max:
            player.gravity = player.gravity_max
        if player.jump_power > 0:
            player.jump_power -= player.jump_power_tic * game_framework.frame_time
            if player.jump_power <= 0:
                player.jump_power = 0
        player.x += player.velocity * game_framework.frame_time
        player.y -= player.gravity * game_framework.frame_time
        player.y += player.jump_power * game_framework.frame_time
        for block in server.block:
            if collision.collide(player.get_col_body_right(), block.get_col()):
                player.x = -40 + block.col_left
                break
        for block in server.block:
            if collision.collide(player.get_col_feet(), block.get_col()) and (
                    player.jump_power - player.gravity) <= 0:
                player.y = 40 + block.col_top
                player.add_event(LANDING)
                break
        for block in server.block:
            if collision.collide(player.get_col_head(), block.get_col()) and (
                    player.jump_power - player.gravity) > 0:
                player.y = -40 + block.col_bottom
                player.jump_power = 0
                break
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
    IdleState: {RIGHT_UP: IdleState, LEFT_UP: IdleState,
                RIGHT_DOWN: RightRunState, LEFT_DOWN: LeftRunState,
                JUMPING: JumpState, JUMP: JumpState, LANDING: IdleState,
                SHOT: ShotIdleState},
    LeftRunState: {RIGHT_UP: LeftRunState, LEFT_UP: IdleState,
                   LEFT_DOWN: LeftRunState, RIGHT_DOWN: RightRunState,
                   JUMPING: LeftJumpState, JUMP: LeftJumpState, LANDING: LeftRunState,
                   SHOT: ShotLeftRunState},
    RightRunState: {RIGHT_UP: IdleState, LEFT_UP: RightRunState,
                    LEFT_DOWN: LeftRunState, RIGHT_DOWN: RightRunState,
                    JUMPING: RightJumpState, JUMP: RightJumpState, LANDING: RightRunState,
                    SHOT: ShotRightRunState},

    JumpState: {RIGHT_UP: JumpState, LEFT_UP: JumpState,
                LEFT_DOWN: LeftJumpState, RIGHT_DOWN: RightJumpState,
                LANDING: IdleState, JUMP: JumpState, JUMPING: JumpState,
                SHOT: ShotJumpState},
    LeftJumpState: {RIGHT_UP: LeftJumpState, LEFT_UP: JumpState,
                    LEFT_DOWN: LeftJumpState, RIGHT_DOWN: RightJumpState,
                    LANDING: LeftRunState, JUMP: LeftJumpState, JUMPING: LeftJumpState,
                    SHOT: ShotLeftJumpState},
    RightJumpState: {RIGHT_UP: JumpState, LEFT_UP: RightJumpState,
                     LEFT_DOWN: LeftJumpState, RIGHT_DOWN: RightJumpState,
                     LANDING: RightRunState, JUMP: RightJumpState, JUMPING: RightJumpState,
                     SHOT: ShotRightJumpState},

    ShotIdleState: {RIGHT_UP: ShotIdleState, LEFT_UP: ShotIdleState,
                    LEFT_DOWN: ShotLeftRunState, RIGHT_DOWN: ShotRightRunState,
                    JUMPING: ShotJumpState, JUMP: ShotJumpState, LANDING: ShotIdleState,
                    SHOT: ShotIdleState, SHOT_END: IdleState},
    ShotLeftRunState: {RIGHT_UP: ShotLeftRunState, LEFT_UP: ShotIdleState,
                       LEFT_DOWN: ShotLeftRunState, RIGHT_DOWN: ShotRightRunState,
                       JUMPING: ShotLeftJumpState, JUMP: ShotLeftJumpState, LANDING: ShotLeftRunState,
                       SHOT: ShotIdleState, SHOT_END: LeftRunState},
    ShotRightRunState: {RIGHT_UP: ShotIdleState, LEFT_UP: ShotRightRunState,
                        LEFT_DOWN: ShotLeftRunState, RIGHT_DOWN: ShotRightRunState,
                        JUMPING: ShotRightJumpState, JUMP: ShotRightJumpState, LANDING: ShotIdleState,
                        SHOT: ShotRightRunState, SHOT_END: RightRunState},

    ShotJumpState: {RIGHT_UP: ShotJumpState, LEFT_UP: ShotJumpState,
                    LEFT_DOWN: ShotLeftJumpState, RIGHT_DOWN: ShotRightJumpState,
                    JUMPING: ShotJumpState, JUMP: ShotJumpState, LANDING: ShotIdleState,
                    SHOT: ShotJumpState, SHOT_END: JumpState},
    ShotLeftJumpState: {RIGHT_UP: ShotLeftJumpState, LEFT_UP: ShotJumpState,
                        LEFT_DOWN: ShotLeftJumpState, RIGHT_DOWN: ShotRightJumpState,
                        JUMPING: ShotLeftJumpState, JUMP: ShotLeftJumpState, LANDING: ShotLeftRunState,
                        SHOT: ShotLeftJumpState, SHOT_END: LeftJumpState},
    ShotRightJumpState: {RIGHT_UP: ShotJumpState, LEFT_UP: ShotRightJumpState,
                         LEFT_DOWN: ShotLeftJumpState, RIGHT_DOWN: ShotRightJumpState,
                         JUMPING: ShotJumpState, JUMP: ShotJumpState, LANDING: ShotRightRunState,
                         SHOT: ShotRightJumpState, SHOT_END: RightJumpState},

}


class Player:
    def __init__(self):
        self.x, self.y = 900, 900
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
        self.gravity_tic = 500  # 프레임당 추가되는 중력
        self.gravity_max = 700  # 최대 중력
        self.jump_power = 0  # 점프 힘
        self.jump_power_tic = 200  # 프레임당 줄어드는 점프힘
        self.jump_power_max = 600  # 점프 힘 최대
        self.jump_count = 1  # 점프 카운트
        self.jump_count_max = 1  # 최대 가능 점프 횟수
        self.frame = 0
        self.frame_shot = 0  # 미사일 발사 준비 시간
        self.frame_shot_max = 100
        self.frame_shot_speed = 100
        self.frame_step = 0  # 대쉬 구름 시간 카운트
        self.frame_step_max = 100
        self.frame_step_speed = 900
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

    def step(self, x, y):  # 대쉬 시에 달린 자리에 구름 만들기
        smoke = Stepsmoke(x, y)
        game_world.add_object(smoke, 1)

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
        server.cx = -self.x + self.cx
        server.cy = -self.y + self.cy
        # ----------------------------
        pass

    def draw(self):
        self.cur_state.draw(self)
        draw_rectangle(*self.get_col_c())
        draw_rectangle(*self.get_col_feet_c())
        draw_rectangle(*self.get_col_head_c())
        draw_rectangle(*self.get_col_body_right_c())
        draw_rectangle(*self.get_col_body_left_c())

        self.font.draw(self.cx - 60, self.cy + 50, '%s' % self.cur_state, (255, 255, 0))
        self.font.draw(self.cx - 60, self.cy + 70, '(%.2f %.2f)' % (self.x, self.y), (255, 255, 0))
        self.font.draw(self.cx - 60, self.cy + 90, '(%d %d)' % (server.cx, server.cy), (255, 255, 0))
        pass

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
        pass
