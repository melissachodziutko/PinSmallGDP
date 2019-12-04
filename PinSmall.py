import math
from typing import Tuple

import random

import pygame
import random

'''
Thank you for the feedback by the way!
I really appreciated it and implemented the things you suggested.
(I was REALLY looking for other things to do with the game
so I was very thankful)
Author: Melissa Chodziutko
version 3
This is a mix of pinball and breakout, where you have two paddles
(laid out like the paddles in breakout)
and you're trying to hit the ball (moves like a breakout style ball)
to pinball-style obstacles for points
How to play: in this version, move the paddle using your mouse
and try to score as many points as possible
before the ball falls off the bottom of the screen
What's not working: sometimes you can get caught in the purple bounce at the
top of the screen and bounce inside
New bug: sometimes the game just hard locks. No clue why.
I don't know how to fix it, or why it happens.
'''
# define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 40)
PRETTY = (96, 41, 124)
IDK = (140, 30, 240)
IDK2 = (20, 100, 70)
IDK3 = (86, 20, 50)
IDK4 = (73, 112, 147)
PINK = (110, 0, 0)
GRAY = (140, 140, 140)
YELLOW = (255, 255, 204)
SCORE = 0
BLOCK_COUNT = 0
BOUNCE_COUNT = 0
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 300
pygame.mixer.init()
SE = pygame.mixer.Sound("blip.ogg")
SE2 = pygame.mixer.Sound("ding.ogg")
SE3 = pygame.mixer.Sound("dong.ogg")
SE4 = pygame.mixer.Sound("dang.ogg")
SE5 = pygame.mixer.Sound("dzwon.ogg")
SE6 = pygame.mixer.Sound("all.ogg")


def get_high_score():
    # Default high score
    high_score = 0

    # Try to read the high score from a file
    try:
        high_score_file = open("high_score.txt", "r")
        high_score = int(high_score_file.read())
        high_score_file.close()
        print("The high score is", high_score)
    except IOError:
        # Error reading file, no high score
        print("There is no high score yet.")
    except ValueError:
        # There's a file there, but we don't understand the number.
        print("I'm confused. Starting with no high score.")

    return high_score


def save_high_score(new_high_score):
    try:
        # Write the file to disk
        high_score_file = open("high_score.txt", "w")
        high_score_file.write(str(new_high_score))
        high_score_file.close()
    except IOError:
        # Hm, can't write it.
        print("Unable to save the high score.")


class Bounce(pygame.sprite.Sprite):
    """
    This class represents the ball.
    It derives from the "Sprite" class in Pygame.
    """
    WIDTH = 40
    HEIGHT = 20

    def __init__(self):
        """ Constructor. Pass in the color of the block,
        and its x and y position. """

        # Call the parent class (Sprite) constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([Bounce.WIDTH, Bounce.HEIGHT])
        self.image = pygame.image.load("bounce.png")

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
        # Set location
        self.rect.x = 50
        self.rect.y = 0


class Block(pygame.sprite.Sprite):
    """
    This class represents the ball.
    It derives from the "Sprite" class in Pygame.
    """
    WIDTH = 20
    HEIGHT = 20

    def __init__(self):
        """ Constructor. Pass in the color of the block,
        and its x and y position. """

        # Call the parent class (Sprite) constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([Block.WIDTH, Block.HEIGHT])
        self.image = pygame.image.load("block.png")

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
        # Set location
        self.rect.x = 130


class GreenBlock(Block):
    # Constructor -- takes a block to copy
    def __init__(self, block):
        super().__init__()
        # Copy block parameters to this subclass of Block.

        self.image = pygame.image.load("lblock.png")
        self.rect.x = block.rect.x
        self.rect.y = block.rect.y


class Lights(pygame.sprite.Sprite):
    """
    This class represents the ball.
    It derives from the "Sprite" class in Pygame.
    """
    WIDTH = 5
    HEIGHT = SCREEN_HEIGHT

    def __init__(self, color):
        """ Constructor. Pass in the color of the block,
        and its x and y position. """

        # Call the parent class (Sprite) constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([Lights.WIDTH, Lights.HEIGHT])
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()


class PinkBounce(Bounce):
    # Constructor -- takes a block to copy
    def __init__(self, bounce):
        super().__init__()
        # Copy block parameters to this subclass of Block.

        self.image = pygame.image.load("lbounce.png")
        self.rect.x = bounce.rect.x
        self.rect.y = bounce.rect.y


class Back(pygame.sprite.Sprite):
    """
    This class represents the ball.
    It derives from the "Sprite" class in Pygame.
    """

    def __init__(self):
        """ Constructor. Pass in the color of the block,
        and its x and y position. """

        # Call the parent class (Sprite) constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([300, 500])
        self.image = pygame.image.load("background.png")
        self.rect = self.image.get_rect()
        # Set location
        self.rect.x = 0
        self.rect.y = 0


class Target(pygame.sprite.Sprite):
    """
    This class represents the ball.
    It derives from the "Sprite" class in Pygame.
    """

    def __init__(self, image, posx, posy, x, y):
        """ Constructor. Pass in the color of the block,
        and its x and y position. """

        # Call the parent class (Sprite) constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([x, y])
        self.image = pygame.image.load(image)

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
        # Set location
        self.rect.x = posx
        self.rect.y = posy


class Ball(pygame.sprite.Sprite):
    # speed is determined by pixels/cycle
    speed = 10.0

    # ball's coordinates
    x = 0.0
    y = 180.0

    # where the ball is pointing in degrees
    direction = random.randint(0, 50)

    # width and height of the ball
    width = 10
    height = 10

    def __init__(self):

        super().__init__()

        # create the ball
        self.image = pygame.Surface([self.width, self.height])

        # color the ball
        # self.image.fill(WHITE)
        self.image = pygame.image.load("ball.png")

        # Get a rectangle object that shows where our image is
        self.rect = self.image.get_rect()

        # assign screen height/width attributes based on how big the screen is
        self.screenHeight = pygame.display.get_surface().get_height()
        self.screenWidth = pygame.display.get_surface().get_width()

    def bounce(self, diff):
        # bounces off horizontal surfaces but not vertical
        self.direction = (180 - self.direction) % 360
        self.direction -= diff

    def update(self):
        # convert sine and cosine to degrees
        direction_radians = math.radians(self.direction)

        # Change the position (x and y) according to the speed and direction
        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)

        # Move the image to where our x and y are
        self.rect.x = self.x
        self.rect.y = self.y

        # Do we bounce off the top of the screen?
        if self.y <= 0:
            self.bounce(0)
            self.y = 1
            SE.play()

        # Do we bounce off the left of the screen?
        if self.x <= 0:
            self.direction = (360 - self.direction) % 360
            self.x = 1
            SE.play()

        # Do we bounce of the right side of the screen?
        if self.x > self.screenWidth - self.width:
            self.direction = (360 - self.direction) % 360
            self.x = self.screenWidth - self.width - 1
            SE.play()

        # Did we fall off the bottom edge of the screen?
        if self.y > self.screenHeight:
            return True
        else:
            return False


class MovingBlock(pygame.sprite.Sprite):
    # speed is determined by pixels/cycle
    speed = 5.0

    # ball's coordinates
    x = 0.0
    y = 100.0

    # where the block is pointing in degrees
    direction = 90

    # width and height of the block
    width = 40
    height = 10

    def __init__(self):

        super().__init__()

        # create the ball
        self.image = pygame.Surface([self.width, self.height])

        # color the ball
        self.image.fill(IDK4)

        # Get a rectangle object that shows where our image is
        self.rect = self.image.get_rect()

        # assign screen height/width attributes based on how big the screen is
        self.screenHeight = pygame.display.get_surface().get_height()
        self.screenWidth = pygame.display.get_surface().get_width()

    def update(self):
        # convert sine and cosine to degrees
        direction_radians = math.radians(self.direction)

        # Change the position (x and y) according to the speed and direction
        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)

        # Move the image to where our x and y are
        self.rect.x = self.x
        self.rect.y = self.y

        # Do we bounce off the left of the screen?
        if self.x <= 0:
            self.direction = (360 - self.direction) % 360
            self.x = 1

        # Do we bounce of the right side of the screen?
        if self.x > self.screenWidth - self.width:
            self.direction = (360 - self.direction) % 360
            self.x = self.screenWidth - self.width - 1

    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)


class Player(pygame.sprite.Sprite):
    # bars at the bottom of the screen

    def __init__(self):
        """ Constructor for Player. """
        # Call the parent's constructor
        super().__init__()

        self.width = 15
        self.height = 5
        self.image = pygame.Surface([self.width, self.height])

        self.image = pygame.image.load("paddle.png")

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

        self.rect.x = 0
        self.rect.y = self.screenheight - self.height

    def update(self):
        """ Update the player position. """
        # Get where the mouse is
        pos = pygame.mouse.get_pos()
        # Set the left side of the player bar to the mouse position
        self.rect.x = pos[0]
        # Make sure we don't push the player paddle
        # off the right side of the screen
        if self.rect.x > self.screenwidth - self.width:
            self.rect.x = self.screenwidth - self.width


# class Background(pygame.sprite.Sprite):
#   def __init___(self):
#      super().__init__()
#     self.rect = self.image.get_rect()
# self.image = pygame.Surface([SCREEN_WIDTH, SCREEN_HEIGHT])
#    self.image = pygame.image.load("wood.png")
#   self.rect.x = 0
#  self.rect.y = 0


def main():
    """ Main function for the game. """
    pygame.init()

    high_score = get_high_score()
    # Set the width and height of the screen [width,height]

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    pygame.mouse.set_visible(0)

    balls = pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    bounces = pygame.sprite.Group()
    targets = pygame.sprite.Group()
    allsprites = pygame.sprite.Group()
    back = Back()
    allsprites.add(back)
    for i in range(3):
        block = Block()
        block.rect.y = 100 + 40 * i
        allsprites.add(block)
        blocks.add(block)

    light = Lights(GRAY)
    light.rect.y = 0
    light.rect.x = 0
    allsprites.add(light)

    light2 = Lights(GRAY)
    light2.rect.y = 0
    light2.rect.x = SCREEN_WIDTH - Lights.WIDTH
    allsprites.add(light2)

    bounce = Bounce()
    bounces.add(bounce)
    allsprites.add(bounce)

    for i in range(2):
        outer_target = Target("otarget.png", 30 + 180 * i, 300, 50, 50)
        targets.add(outer_target)
        allsprites.add(outer_target)

        inner_target = Target("itarget.png", 45 + 180 * i, 315, 20, 20)
        targets.add(inner_target)
        allsprites.add(inner_target)

    # Create the player paddle object
    player = Player()
    allsprites.add(player)

    Music = pygame.mixer.Sound("music.ogg")

    Music.play()
    move = MovingBlock()
    allsprites.add(move)
    # Create the ball
    ball = Ball()
    allsprites.add(ball)
    balls.add(ball)

    pygame.display.set_caption("PinSmall")

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # beginning splash screen
    display_instructions = True
    splash = 1

    while not done and display_instructions:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                splash += 1
                if splash == 2:
                    display_instructions = False

        screen.fill(PRETTY)

        if splash == 1:
            # draw all of the splash screen

            font = pygame.font.SysFont("serif", 20)
            text = font.render("PinSmall", True, WHITE)
            screen.blit(text, [100, 10])

            text = font.render("By Melissa Chodziutko", True, WHITE)
            screen.blit(text, [55, 40])

            text = font.render("Instructions", True, WHITE)
            screen.blit(text, [92, 70])

            text = font.render("To play, use your mouse to", True, WHITE)
            screen.blit(text, [40, 140])

            text = font.render("move the paddle", True, WHITE)
            screen.blit(text, [80, 170])

            text \
                = font.render("Accrue as many points as possible", True, WHITE)
            screen.blit(text, [15, 300])

            text = font.render("Click to start", True, WHITE)
            screen.blit(text, [90, 450])
        pygame.display.flip()

    # -------- Main Program Loop -----------
    while not done and display_instructions is False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

                # Update the player and ball positions

        if ball.y <= 500:
            player.update()
            ball.update()
            move.update()
            # See if the ball hits the player paddle
            if pygame.sprite.spritecollide(player, balls, False):
                ''' diff just means where the ball will bounce to
                depending on where the paddle hit it'''
                diff = (player.rect.x + player.width / 2) \
                    - (ball.rect.x + ball.width / 2)

                ''' update the ball's y position if the ball
                hits the edge of the paddle'''
                ball.rect.y = screen.get_height() \
                    - player.rect.height - ball.rect.height - 1
                ball.bounce(diff)
                SE.play()
                light.image.fill(YELLOW)
                light2.image.fill(YELLOW)

            if ball.rect.y <= 450:
                light.image.fill(GRAY)
                light2.image.fill(GRAY)
        target_hit_list = pygame.sprite.spritecollide(ball, targets, False)

        for outer_target in target_hit_list:
            global SCORE
            SE4.play()
            SCORE += 1
        for inner_target in target_hit_list:
            SCORE += 2

        blocks_hit_list = pygame.sprite.spritecollide(ball, blocks, True)

        # Check the list of collisions.
        for block in blocks_hit_list:
            global BLOCK_COUNT
            points = 10
            SE2.play()
            SCORE += points
            block = GreenBlock(block)
            allsprites.add(block)
            BLOCK_COUNT += 1

        if move.is_collided_with(ball):
            ball.bounce(0)
            SE5.play()
            SCORE += 50

        if BLOCK_COUNT == 3:
            light.image.fill(YELLOW)
            light2.image.fill(YELLOW)
            SE6.play()
        if BLOCK_COUNT == 3 and (ball.y >= 300 or ball.y <= 100):
            BLOCK_COUNT = 0
            SCORE += 50
            light.image.fill(GRAY)
            light2.image.fill(GRAY)
            for i in range(3):
                block = Block()
                block.rect.y = 100 + 40 * i
                allsprites.add(block)
                blocks.add(block)

        if pygame.sprite.spritecollide(bounce, balls, False):
            ball.bounce(0)

        bounce_hit_list = pygame.sprite.spritecollide(ball, bounces, True)

        for bounce in bounce_hit_list:
            global BOUNCE_COUNT
            SE3.play()
            points = 70
            SCORE += points
            bounce = PinkBounce(bounce)
            allsprites.add(bounce)
            BOUNCE_COUNT += 1

        if BOUNCE_COUNT == 1:
            light.image.fill(YELLOW)
            light2.image.fill(YELLOW)
        if BOUNCE_COUNT == 1 and ball.y >= 50:
            BOUNCE_COUNT = 0
            light.image.fill(GRAY)
            light2.image.fill(GRAY)
            bounce = Bounce()
            bounces.add(bounce)
            allsprites.add(bounce)

        screen.fill(BLACK)

        # while Time > 0:
        #    light.image.fill(GRAY)
        #   Time -= 1
        #  print(Time)
        # if Time == 0:
        #   light.image.fill(PINK)
        #  Time = 4000

        # print(pygame.time.get_ticks())

        # pygame.time.set_timer(light.image.fill(PINK), 6500)
        # if pygame.time.get_ticks() >= 1000:
        #   light.image.fill(PINK)
        # if pygame.time.get_ticks() <= 29:
        #   light.image.fill(GRAY)

        # background = Background()
        # allsprites.add(background)
        # draw all the sprites
        allsprites.draw(screen)
        # self.image = pygame.image.load("ball.png")
        font = pygame.font.SysFont("serif", 20)
        score_str = "Score: " + str(SCORE)
        text = font.render(score_str, True, WHITE)
        screen.blit(text, [100, 1])

        # flip displays
        if ball.rect.y >= SCREEN_HEIGHT:
            game_over_font = pygame.font.SysFont("serif", 20)
            gametext = "Game Over"
            text = game_over_font.render(gametext, True, WHITE)

            screen.blit(text, [100, 190])
            if high_score <= SCORE:
                save_high_score(SCORE)
                text = "High Score:" + str(SCORE)
                text = game_over_font.render(text, True, WHITE)
                screen.blit(text, [90, 30])
            else:
                text = "High Score:" + str(high_score)
                text = game_over_font.render(text, True, WHITE)
                screen.blit(text, [80, 30])

            pygame.display.flip()
        else:
            pygame.display.flip()

        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
