import pygame
import random
import math
import sys
import time

from pygame.locals import *
from sprite import Sprite  # import sprite class

''' main executable file
    Includes Character, Projectile, Line and Level classes
'''
BONUS_HP = 0  # increase to give characters more hp

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

CHARA_WIDTH = 100
CHARA_HEIGHT = 100

PROJ_WIDTH = 35
PROJ_HEIGHT = 35

HEALTH_WIDTH = 113
HEALTH_HEIGHT = 250

frame_rate = 40
delta_time = 1 / frame_rate

def main():
    ''' the main function '''
    pygame.init()

    screen = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Finding Light')

    clock = pygame.time.Clock()
    game_data = {}

    game_data["screen"] = screen
    game_data["quit_game"] = False
    game_data["levels"] = [[],[]] # list of levels
    game_data["characters"] = [] # list of playable characters
    game_data["score"] = 0
    game_data["replay"] = False
    game_data["songs"] = []   # indexes 0 to 2 are used for game screen songs 0-menu 1-player death 2-victory screen
    game_data["cutscenes"] = [] # sprites for game 'cutscenes' menu has its own sprite and will be stored at index 0
                                # all other scenes are stores in 1 sprite at index 1
                                # the tutorial + intro story will be stored in 1 sprite at index 2
                                # numbers from 0 to 9 will be stored in a sprite at index 3
    
    ''' NOTE: To change characters or levels, modify the initialize function '''
    initialize(game_data) 

    while not game_data["quit_game"]:
        choice = menu(game_data,clock)-1
        player = game_data["characters"][choice] # set the player to the character object chosen on the main menu

        if(game_data["replay"] == False):
            ''' The tutorial will not be replayed if the player has finished the game '''
            for cutscene in game_data["cutscenes"][2].getAll(0):
                game_data["screen"].blit(cutscene,[0,0])  # the health bar sprite doesn't match the charcter but it's too late to fix it :(
                time.sleep(5)
                pygame.display.update()
                
            pygame.mixer.music.load(game_data["songs"][1])
            pygame.mixer.music.play(-1)

            game_data["screen"].blit(game_data["cutscenes"][2].getAll(1)[4],[0,0])
            pygame.display.update()
            time.sleep(2)
            
            for cutscene in game_data["cutscenes"][2].getAll(1):
                game_data["screen"].blit(cutscene,[0,0])
                pygame.display.update()
                time.sleep(5)

            pygame.mixer.music.stop()

        for level in game_data["levels"][choice]:
            if (level.run(game_data, player, clock) == -1): # the player died
                game_data["screen"].blit(game_data["cutscenes"][1].getAll(0)[2],[0,0])
                pygame.display.update()
                pygame.mixer.music.load(game_data["songs"][1])
                pygame.mixer.music.play(-1)
                reset(game_data)
                time.sleep(5)
                pygame.mixer.music.stop()
                time.sleep(1)
                break
            else:
                upgrade(player, game_data, clock)
            time.sleep(1)
        else:                           # the player won
            win(game_data)  
    pygame.quit
    sys.exit     
    


def initialize(game_data):
    ''' takes the game_data dictionary with 2 empty lists of the levels and playable characters,
        and fills the lists with level and character objects
    '''
    bg1 = pygame.transform.scale(pygame.image.load("resources/backgrounds/background1.png").convert_alpha(), (SCREEN_WIDTH,SCREEN_HEIGHT))
    bg2 = pygame.transform.scale(pygame.image.load("resources/backgrounds/background2.png").convert_alpha(), (SCREEN_WIDTH,SCREEN_HEIGHT))
    bg3 = pygame.transform.scale(pygame.image.load("resources/backgrounds/background3.png").convert_alpha(), (SCREEN_WIDTH,SCREEN_HEIGHT))
    bg4 = pygame.transform.scale(pygame.image.load("resources/backgrounds/background4.png").convert_alpha(), (SCREEN_WIDTH,SCREEN_HEIGHT))

    bg1_1 = pygame.transform.scale(pygame.image.load("resources/backgrounds/background1_1.png").convert_alpha(), (SCREEN_WIDTH,SCREEN_HEIGHT))
    bg2_1 = pygame.transform.scale(pygame.image.load("resources/backgrounds/background2_1.png").convert_alpha(), (SCREEN_WIDTH,SCREEN_HEIGHT))
    bg3_1 = pygame.transform.scale(pygame.image.load("resources/backgrounds/background3_1.png").convert_alpha(), (SCREEN_WIDTH,SCREEN_HEIGHT))
    bg4_1 = pygame.transform.scale(pygame.image.load("resources/backgrounds/background4_1.png").convert_alpha(), (SCREEN_WIDTH,SCREEN_HEIGHT))

    bg1_2 = pygame.transform.scale(pygame.image.load("resources/backgrounds/background1_2.png").convert_alpha(), (SCREEN_WIDTH,SCREEN_HEIGHT))
    bg2_2 = pygame.transform.scale(pygame.image.load("resources/backgrounds/background2_2.png").convert_alpha(), (SCREEN_WIDTH,SCREEN_HEIGHT))
    bg3_2 = pygame.transform.scale(pygame.image.load("resources/backgrounds/background3_2.png").convert_alpha(), (SCREEN_WIDTH,SCREEN_HEIGHT))
    bg4_2 = pygame.transform.scale(pygame.image.load("resources/backgrounds/background4_2.png").convert_alpha(), (SCREEN_WIDTH,SCREEN_HEIGHT))

    img1 = pygame.transform.scale(pygame.image.load("resources/characters/sprite1.png").convert_alpha(), (CHARA_WIDTH*4, CHARA_HEIGHT*3))
    img2 = pygame.transform.scale(pygame.image.load("resources/characters/sprite2.png").convert_alpha(), (CHARA_WIDTH*4, CHARA_HEIGHT*3))

    sprite1 = Sprite(img1,4,3,40) # meep
    sprite2 = Sprite(img2,4,3,40) # tiny
    
    imgp1 = pygame.transform.scale(pygame.image.load("resources/projectiles/s1_attack.png").convert_alpha(), (PROJ_WIDTH*2, PROJ_HEIGHT))
    imgp2 = pygame.transform.scale(pygame.image.load("resources/projectiles/s2_attack.png").convert_alpha(), (PROJ_WIDTH*2, PROJ_HEIGHT))

    proj1 = Sprite(imgp1,2,1,40)
    proj2 = Sprite(imgp2,2,1,40)

    line = Sprite(pygame.image.load("resources/characters/line.png").convert_alpha(),1,1,40)
    
    level1 = pygame.image.load("resources/backgrounds/level1.png").convert_alpha()
    level2 = pygame.image.load("resources/backgrounds/level2.png").convert_alpha()
    level3 = pygame.image.load("resources/backgrounds/level3.png").convert_alpha()
    level4 = pygame.image.load("resources/backgrounds/level4.png").convert_alpha()

    cutscene1 = Sprite(level1,4,2,1)    # stored as a sprite for convenience 
    cutscene2 = Sprite(level2,4,2,1)    # getSprite() should never be called on these so frame rate does not matter
    cutscene3 = Sprite(level3,3,2,1)
    cutscene4 = Sprite(level4,4,2,1)

    # animated menu stored as it's own sprite, only cutscene sprite that will be called by getSprite()
    menu_img = pygame.transform.scale(pygame.image.load("resources/backgrounds/menu.png").convert_alpha(), (SCREEN_WIDTH*4, SCREEN_HEIGHT))
    game_data["cutscenes"].append(Sprite(menu_img,4,1,60))  # uses 60 as frame rate instead to slow down animation

    game_screens = pygame.transform.scale(pygame.image.load("resources/backgrounds/screens.png").convert_alpha(), (SCREEN_WIDTH*3, SCREEN_HEIGHT))
    game_data["cutscenes"].append(Sprite(game_screens,3,1,40))

    tutorial = pygame.transform.scale(pygame.image.load("resources/backgrounds/tutorial.png").convert_alpha(), (SCREEN_WIDTH*5, SCREEN_HEIGHT*2))
    game_data["cutscenes"].append(Sprite(tutorial,5,2,40))
    
    numbers = pygame.transform.scale(pygame.image.load("resources/backgrounds/numbers.png").convert_alpha(), (500, 50))
    game_data["cutscenes"].append(Sprite(numbers,10,1,40))

    health1 = pygame.transform.scale(pygame.image.load("resources/backgrounds/health1.png").convert_alpha(), (HEALTH_WIDTH, HEALTH_HEIGHT))
    health2 = pygame.transform.scale(pygame.image.load("resources/backgrounds/health2.png").convert_alpha(), (HEALTH_WIDTH, HEALTH_HEIGHT))

    song0 = "resources/songs/song0.mp3"   # menu song
    song01 = "resources/songs/song01.mp3"  # player died song
    
    song1 = "resources/songs/song1.mp3"   # songs for each level
    song2 = "resources/songs/song2.mp3"
    song3 = "resources/songs/song3.mp3"
    song4 = "resources/songs/song4.mp3"
    
    screen_size = (SCREEN_WIDTH,SCREEN_HEIGHT)
    char_size = (CHARA_WIDTH,CHARA_HEIGHT)
    proj_size = (PROJ_WIDTH,PROJ_HEIGHT)

    game_data["songs"].append(song0)
    game_data["songs"].append(song01)
    game_data["songs"].append(song1)
    game_data["songs"].append(song2)
    game_data["songs"].append(song3)
    game_data["songs"].append(song4)

    game_data["characters"].append(Character(130+BONUS_HP,5,sprite1,char_size,screen_size,[[0,0],100,10,proj_size,proj1]))
    game_data["characters"].append(Character(100+BONUS_HP,7,sprite2,char_size,screen_size,[[0,0],70,13,proj_size,proj2]))

    # NOTE TO SELF: cutscene changed to sprite object
    # 2 seperate sets of backgrounds for 2 characters
    game_data["levels"][0].append(Level(0,1,1,0.03,bg1_1,bg1,screen_size,[CHARA_WIDTH*2,8000,10,line],song1,health1,cutscene1))
    game_data["levels"][0].append(Level(0,0.6,1,0,bg2_1,bg2,screen_size,[CHARA_WIDTH*2,10000,10,line],song2,health1,cutscene2))
    game_data["levels"][0].append(Level(0.1,0.8,1,0,bg3_1,bg3,screen_size,[CHARA_WIDTH*2,13000,10,line],song3,health1,cutscene3))
    game_data["levels"][0].append(Level(0,0.8,1.4,-0.04,bg4_1,bg4,screen_size,[CHARA_WIDTH*2,17000,10,line],song4,health1,cutscene4))

    game_data["levels"][1].append(Level(0,1,1,0.02,bg1_2,bg1,screen_size,[CHARA_WIDTH*2,8000,10,line],song1,health2,cutscene1))
    game_data["levels"][1].append(Level(0,0.6,1,0,bg2_2,bg2,screen_size,[CHARA_WIDTH*2,10000,10,line],song2,health2,cutscene2))
    game_data["levels"][1].append(Level(0.1,0.8,1,0,bg3_2,bg3,screen_size,[CHARA_WIDTH*2,13000,10,line],song3,health2,cutscene3))
    game_data["levels"][1].append(Level(0,0.8,1.4,-0.04,bg4_2,bg4,screen_size,[CHARA_WIDTH*2,15000,10,line],song4,health2,cutscene4))

    return

def menu(game_data, clock):
    ''' The main menu, will run a while loop that
        takes user input from mouse until the user selects a character
        returns index of the character selected
        takes the song to play and the list of images to display for the cutscene
    '''
    # game_data["screen"].blit(game_data["cutscenes"][0],[0,0])
    
    char = 0
    pygame.mixer.music.load(game_data["songs"][0])
    pygame.mixer.music.play(-1)
        
    while(True):
        game_data["screen"].blit(game_data["cutscenes"][0].getSprite(),[0,0])  # changed menu to be animated
        pygame.display.update()
        char = handleMouseInput()
        if(char != 0):
            break
        clock.tick(frame_rate)

    time.sleep(1)
    pygame.mixer.music.stop()
    return char

def handleMouseInput():
    ''' Handles mouse click event in the main menu
    '''
    events = pygame.event.get()
    for event in events:
        
        # Handle [x] Press
        if event.type == pygame.QUIT:
            print("exit :(")
            pygame.quit()
            sys.exit()
            
        # Handle Key Presses
        if event.type == pygame.KEYDOWN:
                
            # Handle 'Escape' Key
            if event.key == pygame.K_ESCAPE:
                print("exit :)")
                pygame.quit()
                sys.exit()

        # Handle Mouse Click
        if event.type == pygame.MOUSEBUTTONUP:        
            if(160 <= pygame.mouse.get_pos()[0] <= 310):  # select character 1
                return 1
            elif(390 <= pygame.mouse.get_pos()[0] <= 640):  # select character 2
                return 2

    return 0
    
def reset(game_data):
    ''' restart the game, reset everything to default values '''
    game_data["score"] = 0

    for character in game_data["characters"]:
        character.complete_reset()

    # levels will reset their own lines when the level is finished
    return

def win(game_data):
    ''' only gets called when the player finishes the game by winning
        gives the player their final score
    '''

    # calculate each digit of the score
    score = int(3000//game_data["score"])
    hundreds = int(score//100)
    tens = int((score - 100*hundreds)//10)
    ones = int((score - 100*hundreds - 10*tens))

    game_data["screen"].blit(game_data["cutscenes"][1].getAll(0)[1],[0,0])
    game_data["screen"].blit(game_data["cutscenes"][3].getAll(0)[hundreds],[325,300])
    game_data["screen"].blit(game_data["cutscenes"][3].getAll(0)[tens],[375,300])
    game_data["screen"].blit(game_data["cutscenes"][3].getAll(0)[ones],[425,300])
    pygame.display.update()
    
    pygame.mixer.music.load(game_data["songs"][1])
    pygame.mixer.music.play(-1)
    reset(game_data)
    game_data["replay"] = True  # player has finished game, do not replay story
    time.sleep(10)
    pygame.mixer.music.stop()
    time.sleep(1)



def upgrade(player, game_data, clock):
    ''' show the upgrade screen and upgrade the player's character '''
    game_data["screen"].blit(game_data["cutscenes"][1].getAll(0)[0],[0,0])
    pygame.display.update()
    
    while(True):
        events = pygame.event.get()
        for event in events:
        
            # Handle [x] Press
            if event.type == pygame.QUIT:
                pygame.quit
                sys.exit
            
            # Handle Key Presses
            if event.type == pygame.KEYDOWN:
                
                # Handle 'Escape' Key
                if event.key == pygame.K_ESCAPE:
                    pygame.quit
                    sys.exit

            # Handle Mouse Click
            if event.type == pygame.MOUSEBUTTONUP:
            
                if(100 <= pygame.mouse.get_pos()[0] <= 250):  # health
                    player.increaseStats(1)
                    return
                elif(325 <= pygame.mouse.get_pos()[0] <= 475): # attack
                    player.increaseStats(2)
                    return
                elif(550 <= pygame.mouse.get_pos()[0] <= 700): # speed
                    player.increaseStats(0)
                    return
        clock.tick(frame_rate)
    

'''

    Classes ---------------------------------------------------------------------


'''


class Character:
    ''' class for the character that the player controls, only 1 character object should be used at a time
        should be created in main function
        The run function should be called once every iteration of the game loop, will handle user input,
        update, and render
        the character object will also manage its own list of projectile objects 
    '''
    
    def __init__(self,health,speed,sprite,size,screenSize,projectile):
        self.max_health = health   # character's max health
        self.health = health       # character's current health, starts at 0
        self.speed = speed
        self.velocity = [0,0]
        self.location = [screenSize[0]/4,screenSize[1]/2]
        self.size = size
        self.is_hit = False  
        self.is_attacking = False
        self.died = False
        self.horizontal = "still"
        self.vertical = "still"      
        self.invulnerable = -1
        self.screen_size = screenSize
        self.counter = 0 # a counter used to space out when projectiles are launched
        self.projectiles = []

        # default stats used for resetting to start of game
        self.init_health = health
        self.init_speed = speed

        self.sprite = sprite # sprite object
        for i in range(5):
            self.projectiles.append(Projectile(projectile,screenSize)) # initialize list of 5 projectiles

    def reset(self):
        ''' resets the character at the start of each level '''
        self.health = self.max_health
        self.velocity = [0,0]
        self.is_hit = False  
        self.is_attacking = False
        self.died = False
        self.horizontal = "still"
        self.vertical = "still"       
        self.invulnerable = -1
        self.location = [self.screen_size[0]/4,self.screen_size[1]/2]
        self.sprite.reset()

        for projectile in self.projectiles:   # reset each projectile just in case
            projectile.reset()
        
    def complete_reset(self):
        ''' completely resets the characters stats, used when restarting the game '''
        self.health = self.init_health
        self.speed = self.init_speed
        self.velocity = [0,0]
        self.is_hit = False  
        self.is_attacking = False
        self.died = False
        self.horizontal = "still"
        self.vertical = "still"
        self.invulnerable = -1
        self.location = [self.screen_size[0]/4,self.screen_size[1]/2]
        self.sprite.reset()

        for projectile in self.projectiles: 
            projectile.complete_reset()
    
    def run(self, game_data, level, line):
        ''' the main run function for character object, will call handle_input, update and render '''
        self.handle_input(game_data)
        self.update(game_data,line,level)
        self.render(game_data)
        
    def handle_input(self, game_data):
        ''' input handler for character '''
        events = pygame.event.get()
        for event in events:    
        # Handle [x] Press
            if event.type == pygame.QUIT:
                game_data['quit_game'] = True
                pygame.quit()
                sys.exit()
                
            keys = pygame.key.get_pressed()
        
            if keys[pygame.K_LEFT]:    # left is pressed
                self.horizontal = "left"
            elif keys[pygame.K_RIGHT]: # right is pressed
                self.horizontal = "right"
            else:                      # left nor right are being pressed
                self.horizontal = "still"

            if keys[pygame.K_UP]:      # up is being pressed
                self.vertical = "up"
            elif keys[pygame.K_DOWN]:  # down is being pressed
                self.vertical = "down"
            else:                      # up nor down is being pressed
                self.vertical = "still"

            if keys[pygame.K_SPACE]:   # space is being pressed
                self.is_attacking = True
            else:                      # space is not being pressed
                self.is_attacking = False
            
            if keys[pygame.K_ESCAPE]:  # exiting
                game_data['quit_game'] = True
                pygame.quit()
                sys.exit()

    def update(self, game_data, line, level):
        ''' updates the character '''
        if(self.died == True):
            #the player is dead
            level.finished = -1
        else:   
            self.updateLocation(level)
            self.checkCollision(line)
            self.updateStats(line,level)

            for projectile in self.projectiles: # for each launched projectile
                if projectile.launched == True:
                    projectile.update(game_data, line, level)
           

    def updateLocation(self,level):
        ''' updates the characters location '''
 
        if level.acceleration == 0:             # no movement modification from level
            if self.horizontal == "left":       # moving left
                self.velocity[0] = self.speed * -1 * level.speed_modifier
            elif self.horizontal == "right":    # moving right
                self.velocity[0] = self.speed * level.speed_modifier
            else:                               # not moving
                self.velocity[0] = 0

            if self.vertical == "up":           # same as above but for up and down
                self.velocity[1] = self.speed * -1 * level.speed_modifier
            elif self.vertical == "down":    
                self.velocity[1] = self.speed * level.speed_modifier
            else:                              
                self.velocity[1] = 0
                
        else:                                   # with acceleration from level
            if self.horizontal == "left":       # moving left
                self.velocity[0] -= self.speed * level.acceleration * level.speed_modifier
            elif self.horizontal == "right":    # moving right
                self.velocity[0] += self.speed * level.acceleration * level.speed_modifier
            else:                               # trying to stop moving
                if self.velocity[0] < 0:        # currently moving left
                    self.velocity[0] = min(0,self.velocity[0] + self.speed * level.acceleration * level.speed_modifier)
                elif self.velocity[0] > 0:      # currently moving right
                    self.velocity[0] = max(0,self.velocity[0] - self.speed * level.acceleration * level.speed_modifier)

            if self.vertical == "up":       
                self.velocity[1] -= self.speed * level.acceleration * level.speed_modifier
            elif self.vertical == "down":    
                self.velocity[1] += self.speed * level.acceleration * level.speed_modifier
            else:                               
                if self.velocity[1] < 0:           
                    self.velocity[1] = min(0,self.velocity[1] + self.speed * level.acceleration * level.speed_modifier)
                elif self.velocity[1] > 0:           
                    self.velocity[1] = max(0,self.velocity[1] - self.speed * level.acceleration * level.speed_modifier)

        self.location[0] += self.velocity[0]
        if self.location[0] < 0:
            self.location[0] = 0
            self.velocity[0] = 0
        elif self.location[0]+self.size[0] > self.screen_size[0]:
            self.location[0] = self.screen_size[0]-self.size[0]
            self.velocity[0] = 0

        self.location[1] += self.velocity[1]
        if self.location[1] < 0:
            self.velocity[1] = 0
            self.location[1] = 0
        elif self.location[1]+self.size[1] > self.screen_size[1]:
            self.location[1] = self.screen_size[1]-self.size[1]
            self.velocity[1] = 0
        
        
    def checkCollision(self,line):
        ''' check for collision between the player and the line '''
        for line_points in line.location:
            
            (u_sol, u_eol) = line_points
            (u_sol_x, u_sol_y) = u_sol
            (u_eol_x, u_eol_y) = u_eol

            (v_ctr, v_rad) = ((self.location[0]+self.size[0]/2,self.location[1]+self.size[1]/2), self.size[0]/2)
            (v_ctr_x, v_ctr_y) = v_ctr

            t = ((v_ctr_x - u_sol_x) * (u_eol_x - u_sol_x) + (v_ctr_y - u_sol_y) * (u_eol_y - u_sol_y)) / ((u_eol_x - u_sol_x) ** 2 + (u_eol_y - u_sol_y) ** 2)

            t = max(min(t, 1), 0)
    
            # so the nearest point on the line segment, w, is defined as
            w_x = u_sol_x + t * (u_eol_x - u_sol_x)
            w_y = u_sol_y + t * (u_eol_y - u_sol_y)
    
            # Euclidean distance squared between w and v_ctr
            d_sqr = (w_x - v_ctr_x) ** 2 + (w_y - v_ctr_y) ** 2
    
            # if the Eucliean distance squared is less than the radius squared
            if(self.invulnerable == -1): # player has not been hit by the current line yet
                if (d_sqr <= v_rad ** 2):
                    # the line collides
                    self.is_hit = True
                    self.invulnerable = 0
                    self.sprite.setState(2) # set the sprite to the is hit state
                    return
            else:   # the player is in their invulnerable state
                self.invulnerable += 1 # acts as a time, the player will have 1 seconds where they will not be hit
                if self.invulnerable >= 40: # after 1 second has passed they will go back to normal
                    self.invulnerable = -1
                    self.sprite.setState(0)
        return

    def updateStats(self,line,level):
        ''' updates the character's stats '''
        if self.is_hit == True and self.invulnerable == -1:
            self.health -= line.attack*level.damage_modifier
            self.is_hit = False

        self.health += level.env_damage     # constant damage or healing from level

        if self.health > self.max_health: # character hp cannot pass max hp
            self.health = self.max_health

        if self.health <= 0:
                self.died = True
            
        ''' if the user is attacking, launch prokectiles '''
        if self.is_attacking == True:
            if(self.sprite.getState() == 0): # set the sprite to attacking state if the character is currently in default state
                self.sprite.setState(1)
                
            if(self.counter == 10):
                for projectile in self.projectiles:
                    if projectile.launched == False: #launch a not yet launched projectile
                        projectile.launched = True
                        projectile.location = [self.location[0]+self.size[0],self.location[1]+self.size[1]/3]
                        self.counter = 0 #reset the counter when a projectile is launched
                        break
            else:
                self.counter += 1  #increase the counter
        elif self.sprite.getState() == 1:  # character is no longer attacking, change sprite state
                self.sprite.setState(0)
                
    def render(self,game_data):
        ''' renders the character '''
        game_data["screen"].blit(self.sprite.getSprite(),self.location) 

    def increaseStats(self,stat):
        ''' called by level object at the end of each level
            stat is an int from 1 to 3 representing the stat of the character to increase
            1: health
            2: attack
            3: speed
        '''
        if stat == 1:
            self.max_health += 10
        elif stat == 2:
            for projectile in self.projectiles:
                projectile.attack += 20
        else:
            self.speed += 1

        



'''

    end of Character class---------------------------------------------------------------------


'''



class Projectile:
    ''' the projectile class
        initialized by a character object with a list of 5 values in the order of
        location: list of 2 elements storing the current x and y values
        attack: the amount of damage this projectile will do per hit
        speed: integer representing the horizontal speed of the projectile
        size: the size of the sprite
        sprite: a Sprite object
        
        also has launched: boolean representing if the projectile has been launched, will be set to true when
            launched by character, resets to false when colliding with line or border, initialized to false by default
        screen_size is a tuple of the width and height of the screen
    '''

    def __init__(self,values,screenSize):
        self.location = values[0]
        self.attack = values[1]
        self.speed = values[2]
        self.size = values[3]
        self.sprite = values[4]

        ''' default stats, used when restarting game '''
        self.init_attack = values[1]
        
        self.launched = False
        self.screen_size = screenSize

    def update(self,game_data,line,level):
        ''' update the projectile's position, should only be called on launched projectiles by the character
            object's update
            update for projectiles will also call the render function
        '''
        self.location[0] += self.speed
        if self.location[0] > self.screen_size[0]: #hit the right border
            self.reset()
        else:
            self.checkCollision(line,level)
            self.render(game_data)
        

    def checkCollision(self, line, level):
        ''' check for collision between the projectile and the line '''
        for line_points in line.location:
            
            (u_sol, u_eol) = line_points
            (u_sol_x, u_sol_y) = u_sol
            (u_eol_x, u_eol_y) = u_eol

            (v_ctr, v_rad) = ((self.location[0]+self.size[0]/2,self.location[1]+self.size[1]/2), self.size[0]/2)
            (v_ctr_x, v_ctr_y) = v_ctr

            t = ((v_ctr_x - u_sol_x) * (u_eol_x - u_sol_x) + (v_ctr_y - u_sol_y) * (u_eol_y - u_sol_y)) / ((u_eol_x - u_sol_x) ** 2 + (u_eol_y - u_sol_y) ** 2)

            t = max(min(t, 1), 0)
    
            # so the nearest point on the line segment, w, is defined as
            w_x = u_sol_x + t * (u_eol_x - u_sol_x)
            w_y = u_sol_y + t * (u_eol_y - u_sol_y)
    
            # Euclidean distance squared between w and v_ctr
            d_sqr = (w_x - v_ctr_x) ** 2 + (w_y - v_ctr_y) ** 2
    
            # if the Eucliean distance squared is less than the radius squared
            if (d_sqr <= v_rad ** 2):
                    # the line collides
                    self.reset()
                    line.hit(self,level)
        return

    def render(self, game_data):
        ''' draws the projectile '''
        screen = game_data["screen"]
        screen.blit(self.sprite.getSprite(),self.location)


    def reset(self):
        self.launched = False
        self.sprite.reset()

    def complete_reset(self):
        self.launched = False
        self.attack = self.init_attack
        self.sprite.reset()

'''

    end of Projectile class---------------------------------------------------------------------


'''


class Line:
    ''' A line that rotates
        1 line object should be initialized in every level
        takes in screen size, health and attack and generates a line of appropriate length
        the location of the gap in the line will be randomly generated
        health: current health of the line
        max_health: max possible health of the line
        attack: the amount of damage the gap does to the player per hit
        angle: current angle of the line
        gap_side: the size of the gap
        screen_size: size of the screen
        Segments: list of 3 integers representing the length from the top of the line to the start of
            the gap and the length from the top of the line to the bottom of the gap and the length of the entire line
        location: list of 4 integer lists representing the x, y coordinates of the line segments,
            from the top of the line to the start of the gap, and from the bottom of the gap to the bottom of the line

    '''

    def __init__(self,screenSize, gapSize, health, attack,img):
        self.max_health = health
        self.health = health
        self.attack = attack
        self.gap_size = gapSize
        self.angle = 0
        self.screen_size = screenSize
        self.img = img
        self.is_dead = False
        
        self.segments = [screenSize[1]/3, 2*screenSize[1]/3, math.sqrt(screenSize[0]**2 + screenSize[1]**2)]
        self.location = [[[screenSize[0],0],[screenSize[0],self.segments[0]]],[[screenSize[0],self.segments[1]],[screenSize[0],screenSize[0]]]]

    def update(self,game_data):
        ''' called by the level object once ever iteration of the loop
            rotates and updates the line segments
        '''
        if self.is_dead == False:
            if self.rotate(): # the line resets
                self.generateLine() # generate a new line
            self._update_line_segments()
            self.render(game_data["screen"])
        
    def rotate(self, deg=1):
        ''' Rotate the line by 1 degree
            Return TRUE if the line reset to 90 degrees, FALSE otherwise
        '''
        reset = False
        
        self.angle = (self.angle + deg) # increase the angle of the rotating line

        if self.angle > 90:          # the rotating line angle ranges between 90 and 180 degrees
            self.angle = 0       # when it reaches an angle of 180 degrees, reset it 
            reset = True
        self._update_line_segments()  
        return reset

    def generateLine(self):
        ''' generates the new location of the gap on the line '''
        rand = random.randint(100,(math.sqrt(self.screen_size[0]**2 + self.screen_size[1]**2) - 100) - self.gap_size) # randomly generate the start of the gap
        self.segments[0] = rand
        self.segments[1] = rand + self.gap_size

    def render(self, screen):
        ''' draw each of the rotating line segments '''
        # a = self.location[0][1]
        # b = self.location[1][0]
        # hyp = 1000
        x = self.location[1][0][0] - 1000*(math.sin(math.radians(self.angle)))
        y = self.location[0][1][1] - 1000*(math.cos(math.radians(self.angle)))


        screen.blit(pygame.transform.rotate(self.img.getAll(0)[0],360-self.angle),[self.location[0][1][0]-5,y-5])
        screen.blit(pygame.transform.rotate(self.img.getAll(0)[0],360-self.angle),[x-2,self.location[1][0][1]-15])
        
    def hit(self,projectile,level):
        ''' the line is hit with a projectile '''
        self.health -= projectile.attack
        if self.health <= 0:
            self.is_dead = True
            level.finished = 1
        
    def reset(self):
        self.health = self.max_health
        self.angle = 0
        self.is_dead = False

        screenSize = self.screen_size
        self.segments = [screenSize[1]/3, 2*screenSize[1]/3, math.sqrt(screenSize[0]**2 + screenSize[1]**2)]
        self.location = [[[screenSize[0],0],[screenSize[0],self.segments[0]]],[[screenSize[0],self.segments[1]],[screenSize[0],screenSize[0]]]]
        
    def _update_line_segments(self):
        ''' This function is going to set up the coordinates for the enpoints
            of each "segment" of our line.
        '''
        endx1 = self.screen_size[0] - math.sin(math.radians(self.angle)) * self.segments[0]  #x coordinate of a point
        endy1 = math.cos(math.radians(self.angle)) * self.segments[0]  #y coordinate of a point
        self.location[0][1] = [endx1,endy1]

        startx2 = self.screen_size[0] - math.sin(math.radians(self.angle)) * self.segments[1]
        starty2 = math.cos(math.radians(self.angle)) * self.segments[1]
        self.location[1][0] = [startx2,starty2]
        
        endx2 = self.screen_size[0] - math.sin(math.radians(self.angle)) * self.segments[2]
        endy2 = math.cos(math.radians(self.angle)) * self.segments[2]
        self.location[1][1] = [endx2,endy2]


'''

    end of Line class---------------------------------------------------------------------


'''



class Level:
    '''
        A level object
        takes ints acceleration, speed_modifier, damage_modifier, env_damage, a list of 2
        elements representing the screen dimensions, a sprite image, a list
        if 3 elements for initializing a line object
        has int finished representing if the level should be exited
        (1:level finished, 0:level ongoing, -1:player died exit) initializes to 0 by default
        score keeps track of the player's score on this level, and increase every iteration of the while loop
        will add itself to the game's total score when the level ends and reset to 0
    '''

    def __init__(self,acceleration,spd_mod,dmg_mod,env_dmg,img_f,img_b,screenSize,line,song,health,cutscene):
        self.acceleration = acceleration
        self.speed_modifier = spd_mod
        self.damage_modifier = dmg_mod
        self.env_damage = env_dmg
        self.img_f = img_f
        self.img_b = img_b
        self.screen_size = screenSize
        self.line = Line(screenSize,line[0],line[1],line[2],line[3])
        self.song = song
        self.health = health
        self.cutscene = cutscene
        
        self.finished = 0
        self.score = 0

    def run(self, game_data, player, clock):
        ''' game loop for current level, will run until the level is exited by the player winning or dying
            updates and renders itself, its line, and a given character object
            the clock is used to adjust the frame rate of the game
        '''
        screen = game_data["screen"]
        player.reset()     # reset the player at the start of the level
        self.finished = 0

        pygame.mixer.music.load(game_data["songs"][1])
        pygame.mixer.music.play(-1)

        if(game_data["replay"] == False):     # will not replay if the player has already finished the game
            for cutscene in self.cutscene.getAll(0):  # story cutscenes
                screen.blit(cutscene,[0,0])
                pygame.display.update()
                time.sleep(5)
        pygame.mixer.music.stop()

        screen.blit(self.cutscene.getAll(1)[0],[0,0])  # level details
        pygame.display.update()
        time.sleep(8)
            
        pygame.mixer.music.load(self.song)
        pygame.mixer.music.play(-1)
        
        
        while(self.finished == 0):
            y = (104/player.max_health)*(player.max_health-player.health)-113
            screen.blit(self.img_b,[0,0])  # background
            screen.blit(self.health,[0,y]) # health bar
            screen.blit(self.img_f,[0,0])  # forground
            self.line.update(game_data)
            player.run(game_data, self, self.line)

            self.score += 0.0025
            pygame.display.update()   

            clock.tick(frame_rate)

                
        # while loop has been exited, level finished
        # increase the user's score and reset the level's score to 0
        game_data["score"] += self.score
        self.score = 0

        pygame.mixer.music.stop() # stops the music
        
        self.line.reset()   # reset line
        return self.finished  # return status of self.finished



'''

    end of Line class---------------------------------------------------------------------


'''

if __name__ == "__main__":
    main()
