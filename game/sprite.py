import pygame

class Sprite:
    ''' The sprite class, takes an image and parses it into a list of images of
        the frames of the sprite.
        Can be called to return the current sprite frame
        sprites: list of all sprite frames
        frames: based on the fps of the program where the sprite is being used, used to determine when the sprite frame will change
        currFrame: the index of the current frame
        couter: a counter to keep track of when to change the frame
        width: width of each frame
        height: height of each frames
        total_frames: the total number of frames for one of the sprites states
        state: the current state of the sprite
    '''

    def __init__(self,img,column,row,frames):
        ''' takes a sprite sheet image and the number of colums and rows to
            divide the sprite sheet into
        '''
        # sprite_sheet = pygame.image.load(img).convert_alpha()
        self.width = img.get_width()/column
        self.height = img.get_height()/row
        
        self.curr_frame = 0
        self.counter = 0
        self.total_frames = column
        self.state = 0
        self.frames = frames/column/3
        self.sprites = []

        self.cutFrames(img,column,row)

    def cutFrames(self,img,column,row):
        ''' takes a loaded sprite sheet image and cuts it into frames
            each row represents a different state the sprite can be in
            each column is a frame of the sprite in that state
        '''
        for r in range(row):
            self.sprites.append([])
            for c in range(column):
                frame = pygame.Surface([self.width, self.height]).convert_alpha()
                frame.blit(img, [0,0], [c*self.width, r*self.height,self.width,self.height])
                self.sprites[r].append(frame)

    def setState(self,new_state):
        ''' change the state of the sprite '''
        self.state = new_state

    def getState(self):
        ''' returns the current state '''
        return self.state
        
    def reset(self):
        ''' reset sprite '''
        self.curr_frame = 0
        self.counter = 0
        self.state = 0

    def getAll(self,state):
        ''' returns the list of all sprite frames of a state of this sprite '''
        return self.sprites[state]
        
    def getSprite(self):
        ''' returns the current frame of the sprite '''
        self.counter += 1
        if self.counter > self.frames:
            self.counter = 0
            self.curr_frame += 1

        if self.curr_frame >= self.total_frames:
            self.curr_frame = 0

        return self.sprites[self.state][self.curr_frame]
