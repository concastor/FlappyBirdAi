import pygame
import random as rand

GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,   191, 255)


class Pipe:
    # constructor
    def __init__(self, canvas, x):
        self.x = x
        self.bottom_y = 0
        self.top_y = 0
        self.canvas = canvas
        self.colour = GREEN
        self.get_heights()
        self.surface = pygame.Surface((50, self.canvas.get_height()))
        self.surface.fill(BLUE)
        self.prevLoc = (self.x, 0)

    def get_heights(self):
        temp = rand.randint(200, self.canvas.get_height() - 100)
        self.bottom_y = temp
        #distance between top and bottom pipes
        self.top_y = temp - 150

    def draw(self):
        #bottom pipe
        height = self.canvas.get_height() - self.bottom_y
        pygame.draw.rect(self.canvas, self.colour, (self.x, self.bottom_y, 50, height))

        #top pipe
        pygame.draw.rect(self.canvas, self.colour, (self.x, 0, 50, self.top_y))

    def update(self):
        # wont update if off the screen
        first_rect = pygame.Rect(self.x, 0, self.x+50, self.canvas.get_height())
        self.canvas.blit(self.surface, self.prevLoc)
        self.x -= 2
        self.prevLoc = (self.x, 0)
        self.draw()
        second_rect = pygame.Rect(self.x, 0, self.x+50, self.canvas.get_height())
        return first_rect, second_rect

    def clear(self):
        first_rect = pygame.Rect(self.x, 0, self.x+50, self.canvas.get_height())
        self.canvas.blit(self.surface, self.prevLoc)
        return first_rect


#collection class for the pipes
class Course:
    def __init__(self, canvas, x):
        self.pipes = []
        self.x = x
        self.canvas = canvas
        self.fill()

    #fill in the list of pipes
    def fill(self):
        for i in range(4):
            temp = self.create_pipe()
            self.pipes.append(temp)

    #creates a new pipe
    def create_pipe(self):
        new_pipe = Pipe(self.canvas, self.x)
        self.x += 250
        return new_pipe

    def update(self):
        update_rects = []
        if self.pipes[0].x <= 0:
            update_rects.append(self.pipes[0].clear())
            self.pipes.pop(0)

            #add a new pipe to make it appear infinite
            self.pipes.append(Pipe(self.canvas, self.canvas.get_width()+150))

        #get sections that need to be updated
        for pipe in self.pipes:
            update_rects.extend(pipe.update())

        return update_rects

    #function to get the values of the pipes as inputs for neural network
    def get_inputs(self):
        val = self.pipes[0]
        return val.top_y, val.bottom_y, val.x

    #checks if the score should be increased
    def get_score(self, birds):
        pipe_x = self.pipes[0].x + 25
        for bird in birds:
            if bird.x - 1 == pipe_x:
                return True
