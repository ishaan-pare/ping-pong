import pygame
from player import Paddle
from ball import Ball
from network import Network


BLACK = (0,0,0)
WHITE = (255,255,255)

class Game:
    # Define some colors
    
 
    global BLACK, WHITE
    def __init__(self):
        self.net = Network()
        pygame.init()
        size = (700, 500)
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Pong")
        
        self.paddleA = Paddle(WHITE, 10, 100)
        self.paddleA.rect.x = 20
        self.paddleA.rect.y = 20

        self.paddleB = Paddle(WHITE, 10, 100)
        self.paddleB.rect.x = 670
        self.paddleB.rect.y = 20
        
        self.ball = Ball(WHITE,10,10)
        self.ball.rect.x = 345
        self.ball.rect.y = 195
        
        #This will be a list that will contain all the sprites we intend to use in our game.
        self.all_sprites_list = pygame.sprite.Group()
        
        # Add the 2 paddles and the ball to the list of objects
        self.all_sprites_list.add(self.paddleA)
        self.all_sprites_list.add(self.paddleB)
        self.all_sprites_list.add(self.ball)
        
        # The loop will carry on until the user exits the game (e.g. clicks the close button).
        self.carryOn = True
        
        # The clock will be used to control how fast the screen updates
        self.clock = pygame.time.Clock()
        
        #Initialise player scores
        self.scoreA = 0
        self.scoreB = 0
        
    def run(self):
                
        # -------- Main Program Loop -----------
        while self.carryOn:
            # --- Main event loop
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    self.carryOn = False # Flag that we are done so we exit this loop
                elif event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_x: #Pressing the x Key will quit the game
                            self.carryOn=False
        
            #Moving the paddles when the use uses the arrow keys (player A) or "W/S" keys (player B) 
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.paddleA.moveUp(5)
            if keys[pygame.K_s]:
                self.paddleA.moveDown(5)
            # if keys[pygame.K_UP]:
            #     self.paddleB.moveUp(5)
            # if keys[pygame.K_DOWN]:
            #     self.paddleB.moveDown(5)

            # --- Game logic should go here
            self.paddleB.rect.x, self.paddleB.rect.y = self.parse_data(self.send_data())


            self.all_sprites_list.update()
            
            #Check if the ball is bouncing against any of the 4 walls:
            if self.ball.rect.x>=690:
                self.scoreA+=1
                self.ball.velocity[0] = -self.ball.velocity[0]
            if self.ball.rect.x<=0:
                self.scoreB+=1
                self.ball.velocity[0] = -self.ball.velocity[0]
            if self.ball.rect.y>490:
                self.ball.velocity[1] = -self.ball.velocity[1]
            if self.ball.rect.y<0:
                self.ball.velocity[1] = -self.ball.velocity[1]     
        
            #Detect collisions between the ball and the paddles
            if pygame.sprite.collide_mask(self.ball, self.paddleA) or pygame.sprite.collide_mask(self.ball, self.paddleB):
                self.ball.bounce()
            
            # --- Drawing code should go here
            # First, clear the screen to black. 
            self.screen.fill(BLACK)
            #Draw the net
            pygame.draw.line(self.screen, WHITE, [349, 0], [349, 500], 5)
            
            #Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
            self.all_sprites_list.draw(self.screen) 
        
            #Display scores:
            font = pygame.font.Font(None, 74)
            text = font.render(str(self.scoreA), 1, WHITE)
            self.screen.blit(text, (250,10))
            text = font.render(str(self.scoreB), 1, WHITE)
            self.screen.blit(text, (420,10))
        
            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
            
            # --- Limit to 60 frames per second
            self.clock.tick(60)
        
        #Once we have exited the main program loop we can stop the game engine:
        pygame.quit()


    def send_data(self):
        """
        Send position to server
        :return: None
        """
        if self.net.id==0:
            data = str(self.net.id) + ":" + str(20) + "," + str(self.paddleA.rect.y)
        else:
            data = str(self.net.id) + ":" + str(670) + "," + str(self.paddleA.rect.y)

        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1])
        except:
            return 0,0


a = Game()
a.run()