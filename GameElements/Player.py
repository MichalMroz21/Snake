import random as rand
import math
import pygame
import time

from threading import Thread
from collections import deque
from GameElements.PlayerAnimator import PlayerAnimator


class Player:
    # should work for 90, default: 3, max 90 test for others
    ALPHA_CHANGE = 3
    STEER_STRENGTH = 1

    def __init__(self, color, screen_width, screen_height, left, right, game_background_color, screen, fps, speed,
                 thickness, name, which_player):

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = screen

        # max 20, small optimization problems for more, collision problems for more, default: 5
        self.thickness = thickness
        self.spawnMargin = int((self.screen_width + self.screen_height) / 10)

        self.fps = fps
        self.name = name

        self.id = which_player

        self.pos_x = rand.randint(1 + self.spawnMargin, self.screen_width - self.thickness - self.spawnMargin)
        # todo: make so players cant spawn on each other
        self.pos_y = rand.randint(1 + self.spawnMargin, self.screen_height - self.thickness - self.spawnMargin)

        self.firstSquareClear = True
        self.saveFirstRectangle = []

        self.pause = 0

        self.range = 15 + round(math.sqrt(2) * self.thickness)
        self.rangeMax = 200

        self.alpha = rand.randint(1, 4) * 90

        # default: 1.75 no max test for speed
        self.speed = speed
        self.color = color
        self.game_background_color = game_background_color
        self.previousPosition = []

        self.left = left
        self.right = right

        self.isAlive = True

        self.previousHeadPositionsMaxSize = 0
        self.update_previous_head_positions_max_size()

        self.previousHeadPositionsMap = [[0 for x in range(screen_width)] for y in range(screen_height)]
        self.previousHeadPositions = deque()

        self.movement_animation_time_track = time.time()
        #Delay in milliseconds to animate 1 particle of movement
        self.movement_animation_delay = 100
        self.animator = PlayerAnimator(self)

    def update_previous_head_positions_max_size(self):
        alpha = Player.ALPHA_CHANGE % 90 if Player.ALPHA_CHANGE != 90 else 90

        # how many rectangles to consider as previous in collision
        self.previousHeadPositionsMaxSize = self.thickness * math.sqrt(2) * math.cos(math.radians(alpha)) + 1

    def calc_new_position(self):
        new_position = [self.pos_x + self.speed * math.cos(math.radians(self.alpha)),
                        self.pos_y + self.speed * math.sin(math.radians(self.alpha))]

        return new_position

    def calc_new_head_position(self):
        new_position = [self.pos_x + self.speed * Player.STEER_STRENGTH * math.cos(math.radians(self.alpha)),
                        self.pos_y + self.speed * Player.STEER_STRENGTH * math.sin(math.radians(self.alpha))]

        return new_position

    def update_position(self, x, y):
        self.pos_x = x
        self.pos_y = y

    def update_pause(self):
        self.pause += 1
        if self.pause >= self.rangeMax:
            self.pause = 0

    def check_if_creating_pass(self):
        return self.pause in range(self.rangeMax - self.range, self.rangeMax)

    def add_to_previous_position(self, pos_x, pos_y, alpha):

        if not self.check_if_creating_pass():
            self.firstSquareClear = True
            self.clear_previous_position()
            return False

        if len(self.previousPosition) > 0:
            return True

        self.previousPosition = [pos_x, pos_y, alpha]

        return False

    def clear_previous_position(self):
        self.previousPosition.clear()

    def clear_save_first_rectangle(self):
        self.saveFirstRectangle.clear()

    def handle_input_for_player(self, player_input):

        if self.isAlive:

            if player_input[ord(self.left)]:
                self.alpha -= Player.ALPHA_CHANGE

            elif player_input[ord(self.right)]:
                self.alpha += Player.ALPHA_CHANGE

    def death(self, board_fill, color_board, mixer):
        mixer.play_sound_effect(mixer.SoundBoard.death)
        self.animator.animate_death(board_fill, color_board, 10, 15)

    def movement_animation(self, board_fill, color_board):
        self.animator.animate_movement(board_fill, color_board)

    @staticmethod
    def check_if_point_is_in_area(po_round, square_po_round):

        angle = square_po_round[2]
        angle = angle % 360

        x = po_round[0]
        y = po_round[1]

        o = math.degrees(math.atan2(y, x))

        if o <= angle <= (-1) * (180 - o):
            return False
        else:
            return True

    def manage_previous_head_positions(self, new_position_head):
        self.update_previous_head_positions_max_size()

        temp_head_positions = [[-1 for x in range(self.thickness)] for y in range(self.thickness)]

        while len(self.previousHeadPositions) >= self.previousHeadPositionsMaxSize:
            removed_previous_rectangle = self.previousHeadPositions.popleft()

            for i in removed_previous_rectangle:
                for j in i:
                    self.previousHeadPositionsMap[j[0]][j[1]] = 0

        for a in range(0, self.thickness):
            for b in range(0, self.thickness):
                x = round(new_position_head[0]) + a
                y = round(new_position_head[1]) + b

                temp_head_positions[b][a] = (y, x)
                self.previousHeadPositionsMap[y][x] = 1

        self.previousHeadPositions.append(temp_head_positions)

    def move_player_onscreen(self, screen, screen_width, screen_height, board_fill,
                             color_board, animate_threads, mixer, death_order, players_alive, minimum_alive_players):

        if self.isAlive:

            new_position = self.calc_new_position()
            new_position_head = self.calc_new_head_position()

            self.update_position(new_position[0], new_position[1])

            if ((time.time() - self.movement_animation_time_track) * 1000 >= self.movement_animation_delay
                    and players_alive >= minimum_alive_players):

                self.movement_animation_time_track = time.time()
                movement_thread = Thread(target=self.movement_animation, args=(board_fill, color_board))
                animate_threads.append(movement_thread)
                movement_thread.start()

            self.update_pause()

            if self.add_to_previous_position(new_position_head[0], new_position_head[1], self.alpha):

                for a in range(0, self.thickness):
                    for b in range(0, self.thickness):
                        y = self.previousPosition[1] + b
                        x = self.previousPosition[0] + a

                        pygame.draw.rect(screen, self.game_background_color, pygame.Rect(x, y, 1, 1))

                        board_fill[round(y)][round(x)] = 0
                        color_board[(round(y))][round(x)] = self.game_background_color

                if self.firstSquareClear:
                    self.saveFirstRectangle = [self.previousPosition[0], self.previousPosition[1],
                                               self.previousPosition[2]]

                self.clear_previous_position()
                self.add_to_previous_position(new_position_head[0], new_position_head[1], self.alpha)
                self.firstSquareClear = False

            if len(self.saveFirstRectangle) > 0:

                for a in range(0, self.thickness):
                    for b in range(0, self.thickness):

                        y = self.saveFirstRectangle[1] + b
                        x = self.saveFirstRectangle[0] + a

                        if self.check_if_point_is_in_area([x, y], self.saveFirstRectangle):
                            pygame.draw.rect(screen, self.color, pygame.Rect(x, y, 1, 1))

                            board_fill[round(y)][round(x)] = 1
                            color_board[(round(y))][round(x)] = self.color

            if not self.check_if_creating_pass():
                self.clear_save_first_rectangle()

            pygame.draw.rect(screen, self.color,
                             pygame.Rect(new_position_head[0], new_position_head[1], self.thickness, self.thickness))

            for a in range(0, self.thickness):
                for b in range(0, self.thickness):

                    y = round(new_position_head[1]) + b
                    x = round(new_position_head[0]) + a

                    if (y >= screen_height or y < 0 or x >= screen_width or x < 0) or (board_fill[y][x] == 1 and
                                                                                       not
                                                                                       self.previousHeadPositionsMap[y][
                                                                                           x]):
                        self.isAlive = False
                        death_order.append(self.id)
                        death_thread = Thread(target=self.death, args=(board_fill, color_board, mixer))
                        animate_threads.append(death_thread)
                        death_thread.start()

                        return

            for a in range(0, self.thickness):
                for b in range(0, self.thickness):
                    board_fill[round(new_position_head[1]) + b][round(new_position_head[0]) + a] = 1
                    color_board[round(new_position_head[1]) + b][round(new_position_head[0]) + a] = self.color

            self.manage_previous_head_positions(new_position_head)
