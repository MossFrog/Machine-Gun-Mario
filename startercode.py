from pygamehelper import *
from pygame import *
from pygame.locals import *
from vec2d import *
from math import e, pi, cos, sin, sqrt
from random import uniform
import random
import os
import pygame.mixer

class Starter(PygameHelper):
    def __init__(self):
        self.w, self.h = 800, 600
        PygameHelper.__init__(self, size=(self.w, self.h), fill=((255,255,255)))

        #-- Scoreboard methods / Fonts --#
        # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
        self.myfont = pygame.font.SysFont("monospace", 35)
        self.myfont2 = pygame.font.SysFont("monospace", 45)
        self.label = self.myfont.render(str(0), 5, (255,255,0))
        self.level = self.myfont2.render("", 5, (255,255,0))
        self.gameOver = self.myfont2.render("GAME OVER !", 5, (255,255,0))
        self.gameOver2 = self.myfont2.render("PRESS ENTER TO RESTART", 5, (255,255,0))

        self.score = 0
        
        

        #Music Functions, Must be of WAV format
        pygame.mixer.init(frequency=22050,size=-16,channels=4)
        self.chan4 = pygame.mixer.find_channel(4)
        self.chan3 = pygame.mixer.find_channel(3)
        self.chan2 = pygame.mixer.find_channel(2)
        pygame.mixer.music.load("Background.wav")
        pygame.mixer.music.play(-1,0.0)  

        self.boing = pygame.mixer.Sound("Jump.wav")
        self.machine = pygame.mixer.Sound("machine.wav")
        self.boom = pygame.mixer.Sound("Explosion2.wav")
        self.pain = pygame.mixer.Sound("ow.wav")

        #-- Random choices --#

        self.tup12 = (1 , 2)
        self.tup25 = (2 , 5)

        #-- Rock Variables --#

        self.rockx = -100
        self.rocky = 600 - 65
        self.rockSpeed = self.rockSpeed = 0.6 + random.choice(self.tup25)
        self.rockCounter = 0
        self.rockHealth = 100
        self.rockSwitch = True

        self.rockHit = False
        self.hitCounter = 0
        self.rockDir = 1
        self.randSpeed = 1

        self.gameBool = True
        
        self.x = 400 - 30
        self.y = 600 - 40
        self.spriteswitch = 1
        self.flipswitch = 1
        self.airbool = False
        self.spacebool = False
        self.spaceCounter = 0
        
        self.gravity = 0.5
        self.upForce = 0
        self.lastkey = "none"

        self.health = 100
        self.damage = 2
        self.killVal = 100
        
        self.shot = False
        self.shotc = 0
        self.bulletdir = "RIGHT"

        self.player1img = pygame.image.load(os.path.join('MarioSprites','Mario1.png')).convert_alpha()
        self.player1 = pygame.transform.scale(self.player1img, (30,40))

        self.rockimg = pygame.image.load(os.path.join('MarioSprites/Rocks','Rock1.png')).convert_alpha()
        self.rock1 = pygame.transform.scale(self.rockimg, (60,64))

        backgroundimg = pygame.image.load(os.path.join('Resources','Background.png')).convert()
        self.background = pygame.transform.scale(backgroundimg, (800,600))

        

    def update(self):
        #uncomment to check mixer state
        #print pygame.mixer.get_busy()
        
        #Checking pressed keys
        if(self.gameBool == True):
            key = pygame.key.get_pressed()

        if(self.y >= 560):
            self.y = 560
            self.gravity = 0.5

        if(self.y < 560):
            self.gravity += 0.1

        if key[pygame.K_SPACE]:
            self.spacebool = True
            if(self.y == 560):
                self.boing.play()
                self.airbool = True
                self.upForce = 20
                self.spaceCounter = 0

        if(self.airbool == True):
            self.player1img = pygame.image.load(os.path.join("MarioSprites", "MarioJump.png")).convert_alpha()
            self.player1 = pygame.transform.scale(self.player1img, (30,40))
            if(self.upForce > -10*self.gravity):
                self.upForce -= self.gravity + 0.5
            self.y -= self.upForce
            if key[pygame.K_RIGHT]:
                pass
            elif key[pygame.K_LEFT]:
                self.player1 = pygame.transform.flip(self.player1, True, False)
            elif(self.lastkey == "LEFT"):
                self.player1 = pygame.transform.flip(self.player1, True, False)

        if(self.y >= 560):
            self.airbool = False
            self.upForce = 0
            self.gravity = 0.5
            self.spaceCounter += 1
            if(self.spaceCounter >= 15):
                self.spacebool = False
            

        if key[pygame.K_RIGHT]:
            if(self.x < 770):
                self.x = self.x + 5

            if(self.airbool == False):
                self.spriteswitch += 0.2

            if(self.spriteswitch == 1):
                self.player1img = pygame.image.load(os.path.join('MarioSprites','Mario2.png')).convert_alpha()
                self.player1 = pygame.transform.scale(self.player1img, (30,40))

            if(self.spriteswitch >= 2):
                self.spriteswitch = 0
                self.player1img = pygame.image.load(os.path.join('MarioSprites','Mario1.png')).convert_alpha()
                self.player1 = pygame.transform.scale(self.player1img, (30,40))
            
        

        elif key[pygame.K_LEFT]:
            if(self.x > 0):
                self.x = self.x - 5

            if(self.airbool == False):
                self.spriteswitch += 0.2

            if(self.spriteswitch == 1):
                self.player1img = pygame.image.load(os.path.join('MarioSprites','Mario2.png')).convert_alpha()
                self.player1 = pygame.transform.scale(self.player1img, (30,40))
                self.player1 = pygame.transform.flip(self.player1, True, False)

            elif(self.spriteswitch >= 2.5):
                self.spriteswitch = 0
                self.player1img = pygame.image.load(os.path.join('MarioSprites','Mario1.png')).convert_alpha()
                self.player1 = pygame.transform.scale(self.player1img, (30,40))
                self.player1 = pygame.transform.flip(self.player1, True, False)

            #Flipping the image if left button pressed
            if(self.flipswitch == 1):
                self.player1 = pygame.transform.flip(self.player1, True, False)

                self.flipswitch = 0

        else:
            #Resetting "Jump Sprite" if not in air and not moving.
            if(self.airbool != True):
                self.player1img = pygame.image.load(os.path.join('MarioSprites','Mario1.png')).convert_alpha()
                self.player1 = pygame.transform.scale(self.player1img, (30,40))
                if(self.lastkey == "LEFT"):
                    self.player1 = pygame.transform.flip(self.player1, True, False)
                    


        # -- Shooting Methods -- #

        if key[pygame.K_z]:
            if(self.spacebool == False):
                if(self.shot == False):
                    self.machine.play()
                    
                    self.player1img = pygame.image.load(os.path.join('MarioSprites','mariogun1.png')).convert_alpha()
                    self.player1 = pygame.transform.scale(self.player1img, (60,40))

                    self.shotc = self.shotc + 5


                    if(self.shotc > 10):
                        self.player1img = pygame.image.load(os.path.join('MarioSprites','mariogun2.png')).convert_alpha()
                        self.player1 = pygame.transform.scale(self.player1img, (60,40))

                    if(self.shotc > 20):
                        self.shotc = 0

                    if(self.bulletdir == "LEFT"):
                        self.player1 = pygame.transform.flip(self.player1, True, False)
                        if((self.x - self.rockx) >= 0):
                            self.rockHealth -= self.damage
                            self.rockx -= self.damage
                            
                        

                    if(self.bulletdir == "RIGHT"):
                        if((self.x - self.rockx) <= 0):
                            self.rockHealth -= self.damage
                            self.rockx += self.damage
                            
                        
                    
                        

        #-- Prevent player from exiting screen
        if(self.x > 800):
            self.x = 770

        #-- Health Bar status
        if(self.health <= 0):
            self.health = 0
            self.gameBool = False
            self.rockSpeed = 0

            
        self.hitCounter += 0.3
        if(self.hitCounter >= 3):
            self.rockHit = False
        

        #-- Rocky Methods --#

        self.rockx = self.rockx + self.rockSpeed
        self.rockCounter += 0.3
        
        if(self.rockCounter <= 2.5):
            self.rockimg = pygame.image.load(os.path.join('MarioSprites/Rocks','Rock1.png')).convert_alpha()
            self.rock1 = pygame.transform.scale(self.rockimg, (60,64))
            if(self.rockDir == 2):
                self.rock1 = pygame.transform.flip(self.rock1, True, False)
            else:
                self.rock1 = pygame.transform.scale(self.rockimg, (60,64))

        elif(self.rockCounter <= 5):
            self.rockimg = pygame.image.load(os.path.join('MarioSprites/Rocks','Rock2.png')).convert_alpha()
            self.rock1 = pygame.transform.scale(self.rockimg, (60,64))
            if(self.rockDir == 2):
                self.rock1 = pygame.transform.flip(self.rock1, True, False)
            else:
                self.rock1 = pygame.transform.scale(self.rockimg, (60,64))
            
        elif(self.rockCounter <= 7.5):
            self.rockimg = pygame.image.load(os.path.join('MarioSprites/Rocks','Rock3.png')).convert_alpha()
            self.rock1 = pygame.transform.scale(self.rockimg, (60,64))
            if(self.rockDir == 2):
                self.rock1 = pygame.transform.flip(self.rock1, True, False)
            else:
                self.rock1 = pygame.transform.scale(self.rockimg, (60,64))
            
        elif(self.rockCounter <= 10):
            self.rockimg = pygame.image.load(os.path.join('MarioSprites/Rocks','Rock4.png')).convert_alpha()
            self.rock1 = pygame.transform.scale(self.rockimg, (60,64))
            if(self.rockDir == 2):
                self.rock1 = pygame.transform.flip(self.rock1, True, False)
            else:
                self.rock1 = pygame.transform.scale(self.rockimg, (60,64))

        #-- Reset the rock animation loop --#
        if(self.rockCounter >= 10):
            self.rockCounter = 0

            
        #- Rock is kill randomly reset rock -#
        random.seed()
        if(self.rockHealth <= 0):
            if(self.rockSwitch == True):
                self.rockDir = random.choice(self.tup12)
                self.randSpeed = random.choice(self.tup25)
                self.rockSwitch = False
            
            if(self.rockx > -100 and self.rockx < 900):
                self.score += self.killVal
                self.chan2.queue(self.boom)
                
         
            if(self.rockDir == 2):
                self.rockHealth = 100
                self.rockx = 900
                self.rockSpeed = -(0.6 + self.randSpeed)
                

            if(self.rockDir == 1):
                self.rockHealth = 100
                self.rockx = -100
                self.rockSpeed = 0.6 + self.randSpeed

            
                
        self.rockSwitch = True
            

        #-- Rock dies if out of bounds --#
        if(self.rockx < -100):
                self.rockHealth = 0
        elif(self.rockx > 900):
                self.rockHealth = 0
        
                
        #- Player hit by rock -#
        if(abs((self.rockx + 30) - (self.x + 15)) <= 30):
            if(abs((self.y + 20) - (self.rocky + 30)) <= 30):
                if(self.rockHit == False):
                    self.health -= 10
                    self.rockHit = True
                    self.hitCounter = 0
                    self.chan4.queue(self.pain)


        #- Update the score -#
        self.label = self.myfont.render("Score: " + str(self.score), 5, (255,255,0))
        if(self.score == 2000):
            self.level = self.myfont2.render("LEVEL 2", 5, (255,255,0))
            self.damage = 1
            self.killVal = 200
            
            
        if(self.score == 5000):
            self.level = self.myfont2.render("LEVEL 3", 5, (255,255,0))
            self.damage = 0.5
            self.killVal = 500
            
        
    def keyUp(self, key):
        if(self.airbool == False):
            #Resetting player image after keyup event
            if(key == pygame.K_RIGHT):
                self.player1img = pygame.image.load(os.path.join('MarioSprites','Mario1.png')).convert_alpha()
                self.player1 = pygame.transform.scale(self.player1img, (30,40))

                #Resetting flipswitch after right keyup event
                self.flipswitch = 1

                #Modifying Lastkey
                self.lastkey = "RIGHT"

            if(key == pygame.K_LEFT):
            
                self.player1img = pygame.image.load(os.path.join('MarioSprites','Mario1.png')).convert_alpha()
                self.player1 = pygame.transform.scale(self.player1img, (30,40))
                self.player1 = pygame.transform.flip(self.player1, True, False)

                #Modifying Lastkey
                self.lastkey = "LEFT"
            if(key == pygame.K_z):
                pygame.mixer.stop()


    #-- Handling keydown events --#
    def keyDown(self, key):
        if(key == pygame.K_LEFT):
            self.bulletdir = "LEFT"
        elif(key == pygame.K_RIGHT):
            self.bulletdir = "RIGHT"
        
            

    def mouseUp(self, button, pos):
        pass

    def mouseMotion(self, buttons, pos, rel):
        pass

    def draw(self):
        self.screen.blit(self.background, (0,0))

        self.screen.blit(self.player1, (self.x,self.y))

        if(self.rockHealth >= 0):
            self.screen.blit(self.rock1, (self.rockx, self.rocky))
            pygame.draw.rect(self.screen, (255,0,0), [self.rockx + 8, self.rocky - 5, self.rockHealth/2, 10], 0)
        
        if(self.health <= 0):
            self.screen.blit(self.gameOver, (50,260))
            
        else:
            pygame.draw.rect(self.screen, (255,0,0), [690, 10, self.health, 20], 0)
            
        self.screen.blit(self.label, (10, 10))

        if(self.score == 2000 and self.health > 0):
            self.screen.blit(self.level, (320,260))
        if(self.score == 5000 and self.health > 0):
            self.screen.blit(self.level, (320,260))
            

s = Starter()
s.mainLoop(60)

# http://www.pygame.org/docs/ref/key.html
# http://www.pygame.org/docs/ref/mixer.html
# http://soundbible.com/
