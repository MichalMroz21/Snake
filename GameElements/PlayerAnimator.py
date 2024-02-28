import pygame
import random as rand
import math


class PlayerAnimator:

    MAX_TRANSPARENCY = 255

    def __init__(self, player):
        self.player = player

    def animate_death(self, board_fill, color_board, particle_amount_min, particle_amount_max):

        circle_center = (self.player.pos_x, self.player.pos_y)

        screen_width = self.player.screen_width
        screen_height = self.player.screen_height
        screen = self.player.screen

        player_color = self.player.color
        game_background_color = self.player.game_background_color
        thickness = self.player.thickness

        player_speed = self.player.speed
        fps = self.player.fps

        particles_amount = rand.randint(particle_amount_min, particle_amount_max)
        particles_alphas = []
        particles_sizes = []
        particles_transparency = []
        particles_max_radiuses = []
        particles_velocities = []

        base_radius = (screen_width * screen_height)/2 / (thickness * 1.5) / (1280 * 720 / (1280 + 720))
        previous_alpha = 0

        for i in range(0, particles_amount):

            particles_alphas.append(rand.randint(0 + round(previous_alpha/2), 360))
            particles_sizes.append(rand.randint(round(thickness / 2), round(thickness / 1.5)))

            particles_transparency.append(rand.uniform(PlayerAnimator.MAX_TRANSPARENCY / 2, PlayerAnimator.MAX_TRANSPARENCY))
            particles_max_radiuses.append(rand.uniform(base_radius, base_radius * 1.75))
            particles_velocities.append(rand.uniform(player_speed/2, player_speed * 1.5))

            previous_alpha = particles_alphas[-1]

        max_radius = max(particles_max_radiuses)

        previous_radiuses = [0 for radius in range(0, particles_amount)]
        particle_radiuses = [1 for particle in range(0, particles_amount)]
        final_clears = [False for particle in range(0, particles_amount)]

        clock = pygame.time.Clock()

        while False in final_clears:

            i = 0
            for alpha, size, transparency in zip(particles_alphas, particles_sizes, particles_transparency):

                if previous_radiuses[i] != 0 and not final_clears[i]:

                    x_prev = previous_radiuses[i] * math.cos(math.radians(alpha)) + circle_center[0]
                    y_prev = previous_radiuses[i] * math.sin(math.radians(alpha)) + circle_center[1]

                    for a in range(0, size):
                        for b in range(0, size):

                            y = round(y_prev) + b
                            x = round(x_prev) + a

                            if x >= screen_width or x < 0 or y < 0 or y >= screen_height:
                                continue

                            if board_fill[y][x] != 1:
                                pygame.draw.rect(screen, game_background_color, pygame.Rect(x, y, 1, 1))

                            else:
                                pygame.draw.rect(screen, color_board[y][x], pygame.Rect(x, y, 1, 1))

                if particle_radiuses[i] >= particles_max_radiuses[i]:
                    final_clears[i] = True
                    previous_radiuses[i] = particle_radiuses[i]
                    i += 1
                    continue

                x_top = particle_radiuses[i] * math.cos(math.radians(alpha)) + circle_center[0]
                y_top = particle_radiuses[i] * math.sin(math.radians(alpha)) + circle_center[1]

                for a in range(0, size):
                    for b in range(0, size):

                        y = round(y_top) + b
                        x = round(x_top) + a

                        if x >= screen_width or x < 0 or y < 0 or y >= screen_height:
                            continue

                        s = pygame.Surface((1, 1))
                        s.set_alpha(transparency)
                        s.fill(player_color)

                        screen.blit(s, (x, y))

                previous_radiuses[i] = particle_radiuses[i]
                particle_radiuses[i] += particles_velocities[i]
                i += 1

                pygame.display.update()

            clock.tick(fps)

    def animate_movement(self, board_fill, color_board):

        screen_width = self.player.screen_width
        screen_height = self.player.screen_height
        screen = self.player.screen

        player_color = self.player.color
        game_background_color = self.player.game_background_color
        thickness = self.player.thickness

        player_speed = self.player.speed
        fps = self.player.fps

        alpha = self.player.alpha
        alpha += 180
        alpha += rand.randint(-45, 45)

        particle_size = rand.randint(round(thickness / 2), thickness)
        particle_transparency = rand.uniform(PlayerAnimator.MAX_TRANSPARENCY / 2, PlayerAnimator.MAX_TRANSPARENCY / 1.4)
        max_travel_distance = rand.randint(round((screen_width + screen_height) / 80), round((screen_width + screen_height) / 40))

        travel_distance = 0

        prev_x = None
        prev_y = None

        curr_x = self.player.pos_x
        curr_y = self.player.pos_y

        clock = pygame.time.Clock()

        while True:

            if prev_x is not None and prev_y is not None:

                for a in range(0, particle_size):
                    for b in range(0, particle_size):

                        y = round(prev_y) + b
                        x = round(prev_x) + a

                        if x >= screen_width or x < 0 or y < 0 or y >= screen_height:
                            continue

                        if board_fill[y][x] != 1:
                            pygame.draw.rect(screen, game_background_color, pygame.Rect(x, y, 1, 1))

            if travel_distance >= max_travel_distance:
                break

            for a in range(0, particle_size):
                for b in range(0, particle_size):

                    y = round(curr_y) + b
                    x = round(curr_x) + a

                    if x >= screen_width or x < 0 or y < 0 or y >= screen_height:
                        continue

                    if board_fill[y][x] != 1:
                        s = pygame.Surface((1, 1))
                        s.set_alpha(round(particle_transparency))
                        s.fill(player_color)

                        screen.blit(s, (x, y))

            prev_x, prev_y = curr_x, curr_y
            curr_x, curr_y = (curr_x + player_speed * math.cos(math.radians(alpha)), curr_y + player_speed * math.sin(math.radians(alpha)))

            player_speed -= player_speed * 0.01

            travel_distance += math.sqrt(pow(abs(curr_x - prev_x), 2) + pow(abs(curr_y - prev_y), 2))

            clock.tick(fps)
            pygame.display.update()
