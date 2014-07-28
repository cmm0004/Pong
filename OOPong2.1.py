import pygame, sys, random
from pygame.locals import *

"""
Version 2.1

##########
What's new
##########

ball respawns after a set number of collisions

points are not assigned for a fresh ball going into goal.

paddles get smaller, but not smaller than 10px

#############
Plans for 2.2
#############

make the left and right paddle objects a separate class
main paddle class > paddle location class
so, left and right paddles will be instances of the child class,
and the main class will hold the info thats the same between them.
this may or may not be a cleaner way to do the paddles.

"""

pygame.init()
MONOSPACE = pygame.font.SysFont("monospace", 15)
## HELPER FUNCTIONS
    
## CLASSES
class Pong:
    """Class to hold game state"""
    def __init__(self):
        self.running = True

    def update_collisions(self):
        """
        after a certian number of collisions without a point
        being scored, ball will reset.
        this may be removed later.
        """
        self.collisions += 1
        
    def _get_collision_text(self):
        """
        used for debugging, not part of game
        """
        return MONOSPACE.render(str(self.collisions), 1, (255, 255, 255))

    def _is_running(self):
        return self.running

    def _get_collisions(self):
        return self.collisions

    def draw(self):
        """
        draws the game board lines
        """
        #lines
        pygame.draw.line(SCREEN, (255,255,255), (WIDTH-20, 0), (WIDTH-20, HEIGHT-1), 1)
        pygame.draw.line(SCREEN, (255,255,255), (20, 0), (20, HEIGHT-1), 1)
        pygame.draw.line(SCREEN, (128,128,128), (SCREENRECT.midtop), (SCREENRECT.midbottom), 1)

    def new_game(self):
        #need a button or something for this
        player1.reset_score()
        player2.reset_score()
        ball.new_ball()
    
class PlayerScore:
    """
    This is for displaying the scores, and updating them
    """

    def __init__(self, pos):
        self.score = 0
        self.pos = pos
    def get_score(self):
        return self.score
    
    def update_score(self):
        self.score += 1
        
    def reset_score(self):
        self.score = 0

    def draw_score(self):
        """
        shows score on screen at the position passed to the PlayerScore obj
        """
        self.score_text = MONOSPACE.render(str(self.score), 1, (255, 255, 255))
        SCREEN.blit(self.score_text, self.pos)


class Ball:
    def __init__(self):
        self.radius = 10
        self.pos = [SCREENRECT.centerx, SCREENRECT.centery]
        self.vel = [random.choice([-7,-6, 6, 7]), random.choice([-7,-6, 6, 7])]
        #self.accel = 0
        self.is_bouncable = True
        self.collisions = 0
        self.fresh_ball = True
        self.color = (255, 255, 255)

    def draw(self):
        """
        draws ball on screen and updates position
        """
        if self.collisions == 8:
            self.color = (128, 128, 128)
        elif self.collisions == 9:
            self.color = (64, 64, 64)
        pygame.draw.circle(SCREEN, self.color, self.pos, self.radius)
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
    def bounce(self):
        """
        logic for: wall bounces, paddle bounces, collision counting,
        point scoring, tracking if ball is fresh, calling new ball.
        """
        #is this a fresh ball?
        #a fresh ball is a ball that hasn't hit a paddle yet, walls dont
        #count. points are not added for fresh balls that go in the goals.

        #keep track of age of ball
        if self.collisions == 0:
            self.fresh_ball = True
        elif self.collisions == 10:
            self.new_ball()
        else:
            self.fresh_ball = False

        #reset is_bouncable flag
        if SCREENRECT.centerx == self.pos[0]:
            self.is_bouncable = True
            
        #bounce off paddles
        if self.is_bouncable:
            #bounce off left paddle
            if (self.pos[0] - self.vel[0] - self.radius < 20) and (leftPaddle.pos[1] - leftPaddle.height/2) <= self.pos[1] <= leftPaddle.pos[1] + leftPaddle.height/2:
                self.vel[0] *= -1
                if leftPaddle.height != 10:
                    leftPaddle.height -= 10
                    rightPaddle.height -= 10
                self.collisions += 1
                self.is_bouncable = False
            #bounce off right paddle
            elif (self.pos[0] + self.vel[0] + self.radius > 620) and (rightPaddle.pos[1] - rightPaddle.height/2) <= self.pos[1] <= rightPaddle.pos[1] + rightPaddle.height/2:
                self.vel[0] *= -1
                
                #mwaha
                if leftPaddle.height != 10:
                    rightPaddle.height -= 10
                    leftPaddle.height -= 10
                self.collisions += 1
                self.is_bouncable = False
                
        #bounce off top and bottom
        if self.pos[1] >= (SCREENRECT.bottom - self.radius - 1) or self.pos[1] <= (SCREENRECT.top + self.radius):
            if self.collisions > 0:
                self.collisions += 1
            self.vel[1] *= -1

        
        elif self.pos[0] >= (640 - self.radius - 1):
            if not self.fresh_ball:
                player1.update_score()
            self.new_ball()
        elif self.pos[0] <= (SCREENRECT.left + self.radius):
            if not self.fresh_ball:
                player2.update_score()
            self.new_ball()
        else:
            return
        
        
    def new_ball(self):
        """
        spawns a fresh ball in the middle of the screen.
        """
        self.is_bouncable = True
        self.collisions = 0
        self.color = (255, 255, 255)
        self.pos = [SCREENRECT.centerx, SCREENRECT.centery]
        self.vel = [random.randrange(-5, 6, 2), random.randrange(-5, 6, 2)]
        leftPaddle.height = 50
        rightPaddle.height = 50
        print self.vel
class Paddle:
    """
    needs the top left starting position of the paddle
    """
    def __init__(self, pos):
        self.height = 50
        self.width = 10
        self.pos = pos
        #since they only move up and down..
        #self.vel_y = 0
        self.moving_up = False
        self.moving_down = False

    def _move(self, delta_y):
        """
        updates the position of paddleobj
        """
        if (self.pos[1] + self.height/2) +delta_y <= SCREENRECT.bottom and (self.pos[1] - self.height/2) + delta_y >= 0:
            
            self.pos[1] += delta_y
        
    
    def draw(self):
        """
        draws paddle object on screen. uses position from Paddle Obj argument
        """
        #pointlists are no fun. centered the paddles along y
        pygame.draw.polygon(SCREEN, (255,255,255),((self.pos[0],self.pos[1] - self.height/2),
                                                   (self.pos[0] + self.width, self.pos[1] - self.height/2),
                                                   (self.pos[0] + self.width, self.pos[1] + self.height - self.height/2),
                                                   (self.pos[0], self.pos[1] + self.height - self.height/2)))
        if self.moving_up:
            self._move(-4)
        if self.moving_down:
            self._move(4)
    def get_smaller(self):
        """
        make paddles smaller, called per collision of paddle/ball 
        mwuahaahaha
        """
        self.height -= 5
        
## GAME SETUP

clock= pygame.time.Clock()
MODES= pygame.display.list_modes()
SCREEN= pygame.display.set_mode(MODES[-1])
SCREENRECT= SCREEN.get_rect()
WIDTH = SCREENRECT.right
HEIGHT = SCREENRECT.bottom
pygame.display.set_caption('PyPong - Candice McCollough')


## GAME INSTANCE SETUP
pong = Pong()
ball = Ball()
leftPaddle = Paddle([10, SCREENRECT.centery])
rightPaddle = Paddle([WIDTH-20, SCREENRECT.centery])
player1 = PlayerScore([WIDTH/4, 30])
player2 = PlayerScore([WIDTH - WIDTH/4, 30])
pong.running = True

## GAME LOOP
while pong.running:
    clock.tick(60)
    SCREEN.fill((0, 0, 0))
    pong.draw()
    leftPaddle.draw()
    rightPaddle.draw()
    player1.draw_score()
    player2.draw_score()
    ball.draw()
    ball.bounce()
    
    pygame.display.update()

    


    
#EVENT HANDLING

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            pong.running= False
            
        elif event.type == pygame.KEYDOWN:
            #move right player
            if event.key == pygame.K_UP:
                rightPaddle.moving_up = True
            elif event.key == pygame.K_DOWN:
                rightPaddle.moving_down = True
            #move left player
            elif event.key == pygame.K_a:
                leftPaddle.moving_up = True
            elif event.key == pygame.K_z:
                leftPaddle.moving_down = True

            #turn off the game
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
                pong.running= False

        elif event.type == pygame.KEYUP:
            #stop moving right player
            if event.key == pygame.K_UP:
                rightPaddle.moving_up = False
            elif event.key == pygame.K_DOWN:
                rightPaddle.moving_down = False
            #stop moving left player
            elif event.key == pygame.K_a:
                leftPaddle.moving_up = False
            elif event.key == pygame.K_z:
                leftPaddle.moving_down = False
