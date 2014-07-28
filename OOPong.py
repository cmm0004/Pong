import pygame, sys, random
from pygame.locals import *

pygame.init()
MONOSPACE = pygame.font.SysFont("monospace", 15)
## HELPER FUNCTIONS

def is_collided(ballObj, paddleObj):
    """
    detects if a ball object has collided with a paddle object, returns boolean
    may move inside ball class
    """
    #should return true or false
    pass    
    
## CLASSES
class Pong:
    """Class to hold game state"""
    def __init__(self):
        self.collisions = 0
        self.running = True

    def update_collisions(self):
        """
        after a certain number of collisions without a point
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
        self.vel = [random.randrange(-5, 6, 2), random.randrange(-5, 6, 2)]
        #self.accel = 0
        #ballcan bounce off a paddle when true, and cant when true
        #this keeps the ball from bouncing off the paddle, and then reversing direction
        #again because it is still in the paddle range when the game ticks again.
        self.bouncable = True

    def draw(self):
        """
        draws ball on screen and updates position
        """
        pygame.draw.circle(SCREEN, (255, 255, 255), self.pos, self.radius)
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
    def bounce(self):
        """
        keeps ball from being drawn off-screen and detects when a point is scored.
        this is probably where I should put the paddle collision logic.
        """
        #this bounces off rightpaddle
##        #start here, ball position plus ball velocity less than ball radius or something.
##        if (WIDTH - 20 == (self.pos[0] + self.radius)):#or (SCREENRECT.left + 18 <= (self.pos[0] - self.radius) <= SCREENRECT.left + 22):
##            if rightPaddle.pos[1] <= self.pos[1] <= rightPaddle.pos[1] + rightPaddle.height:
##                self.vel[1] *= -1
        #this checks to see if the ball should be bounceable
        if SCREENRECT.centerx -10 <= self.pos[0] <= SCREENRECT.centerx + 10:
            self.bouncable = True
            print self.bouncable
        if self.bouncable:
            if (WIDTH - 25 <= self.pos[0] <= WIDTH - 15) and ((rightPaddle.pos[1] + rightPaddle.height) <= self.pos[1] <= rightPaddle.pos[1]):
                self.vel[1] *= -1
                self.bouncable = False
                print self.bouncable
            
        
        #this bounces off top and bottom
        if self.pos[1] >= (SCREENRECT.bottom - self.radius - 1) or self.pos[1] <= (SCREENRECT.top + self.radius):
            #pong.update_collisions()
            self.vel[1] *= -1

        #this scores on right side
        elif self.pos[0] >= (640 - self.radius - 1):
            player1.update_score()
            self.new_ball()
            
        #this scores on left side
        elif self.pos[0] <= (SCREENRECT.left + self.radius):
            player2.update_score()
            self.new_ball()
        else:
            return
    def new_ball(self):
        """
        spawns a fresh ball in the middle of the screen.
        """
        self.pos = [SCREENRECT.centerx, SCREENRECT.centery]
        self.vel = [random.randrange(-5, 6, 2), random.randrange(-5, 6, 2)]

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
