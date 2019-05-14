import os

import pygame

SCREEN_TITLE = 'Crossy Road'
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)

clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.Font('fonts/prstart.ttf', 20)


class Game:
    TICK_RATE = 60

    def __init__(self, title, width, height):
        self.title = title
        self.width = width
        self.height = height
        self.center = (self.width / 2, self.height / 2)
        self.game_screen = pygame.display.set_mode((self.width, self.height))
        self.game_screen.fill(WHITE_COLOR)
        pygame.display.set_caption(self.title)

    def run_game_loop(self, level):
        direction = 0
        background = GameObject('img/background.png', 0, 0, self.width, self.height)
        treasure = GameObject('img/treasure.png', self.center[0] - 24, 20, 48, 36)
        player = PlayerCharacter('img/player.png', self.center[0] - 18, self.height - 100, 36, 48)
        enemy0 = EnemyCharacter('img/enemy.png', 20, self.height - 150, 48, 36)
        enemy0.SPEED += level
        enemy1 = EnemyCharacter('img/enemy.png', self.center[0], self.height - 300, 48, 36)
        enemy1.SPEED += level
        enemy1.active = False
        enemy2 = EnemyCharacter('img/enemy.png', self.width - 20, self.height - 450, 48, 36)
        enemy2.SPEED += level
        enemy2.active = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        direction = -1
                    elif event.key == pygame.K_DOWN:
                        direction = 1
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        direction = 0

            background.draw(self.game_screen)
            treasure.draw(self.game_screen)

            player.move(direction, self.height)
            player.draw(self.game_screen)

            enemy0.move(self.width)
            enemy0.draw(self.game_screen)

            if level > 2:
                enemy1.active = True
                enemy1.move(self.width)
                enemy1.draw(self.game_screen)

            if level > 5:
                enemy2.active = True
                enemy2.move(self.width)
                enemy2.draw(self.game_screen)

            if player.detect_collision(enemy0) or player.detect_collision(enemy1) or player.detect_collision(enemy2):
                win = False
                text = font.render('You died after ' + str(level) + ' level(s)!', False, BLACK_COLOR, WHITE_COLOR)
                self.game_screen.blit(text, (50, self.center[1]))
                pygame.display.update()
                clock.tick(1)
                break
            elif player.detect_collision(treasure):
                win = True
                text = font.render('Level ' + str(level) + ' completed!', False, BLACK_COLOR, WHITE_COLOR)
                self.game_screen.blit(text, (100, self.center[1]))
                pygame.display.update()
                clock.tick(1)
                break

            pygame.display.update()
            clock.tick(self.TICK_RATE)

        if win:
            self.run_game_loop(level + 1)
        else:
            pygame.quit()
            quit()


class GameObject:
    def __init__(self, image_path, x_pos, y_pos, width, height):
        self.image = pygame.transform.scale(pygame.image.load(image_path), (width, height))
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.active = True

    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))


class PlayerCharacter(GameObject):
    SPEED = 5

    def __init__(self, image_path, x_pos, y_pos, width, height):
        super().__init__(image_path, x_pos, y_pos, width, height)

    def move(self, direction, max_height):
        self.y_pos += direction * self.SPEED
        if self.y_pos + self.height >= max_height - 20:
            self.y_pos = max_height - 20 - self.height
        elif self.y_pos <= 20:
            self.y_pos = 20

    def detect_collision(self, other):
        if not other.active:
            return False
        if self.y_pos > other.y_pos + other.height:
            return False
        elif self.y_pos + self.height < other.y_pos:
            return False
        elif self.x_pos > other.x_pos + other.width:
            return False
        elif self.x_pos + self.width < other.x_pos:
            return False
        return True


class EnemyCharacter(GameObject):
    SPEED = 5

    def __init__(self, image_path, x_pos, y_pos, width, height):
        super().__init__(image_path, x_pos, y_pos, width, height)

    def move(self, max_width):
        if self.x_pos <= 20:
            self.SPEED = abs(self.SPEED)
        elif (self.x_pos + self.width) >= max_width - 20:
            self.SPEED = -abs(self.SPEED)
        self.x_pos += self.SPEED


os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

logo_image = pygame.image.load('img/background.png')
pygame.display.set_icon(logo_image)

game = Game(SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
game.run_game_loop(1)
