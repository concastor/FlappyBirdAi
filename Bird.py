import pygame
from neuralNetwork import NeuralNetwork

BLUE = (0,   191, 255)
BLACK = (0, 0, 0)


class Bird:
    #constructor
    def __init__(self, canvas, colour, y):
        self.brain = NeuralNetwork(4, 4, 1)
        self.move = 0
        self.x = 70
        self.y = y
        self.isDead = False
        self.canvas = canvas
        self.colour = colour
        self.prevLoc = None
        self.radius = 10
        self.surface = pygame.Surface((self.radius * 2, self.radius * 2))
        self.surface.fill(BLUE)
        self.prevLoc = (self.x - self.radius, self.y - self.radius)
        self.fitness = 0
        # self.score = 0
        self.isChamp = False
        self.distance = 0

    #draws the "bird" to the canvas
    def draw(self):
        pygame.draw.circle(self.canvas, self.colour, [self.x, int(self.y)], self.radius)

    #how the screen updates every frame
    def update(self, pipe_x):
        if not self.isDead:

            # wont fly of the screen
            if self.y - 10 <= 0:
                self.y = 10
                self.isDead = True

            #kills it if it hits the bottom
            elif self.y+10 >= self.canvas.get_height():
                self.y = self.canvas.get_height() - 10
                self.isDead = True

            #update screen and send information to canvas
            first_rect = self.create_rect(self.x, self.y, self.radius)
            self.canvas.blit(self.surface, self.prevLoc)

            #movement if its flapping up
            if self.move != 0:
                self.y -= 8
                self.move -= 1
            else:
                self.y += 7

            #increase the total distance that the birds have travelled
            self.distance += 2
            self.prevLoc = (self.x - self.radius, self.y - self.radius)
            self.draw()
            second_rect = self.create_rect(self.x, self.y, self.radius)
            return first_rect, second_rect

        elif self.fitness == 0:
            pipe_distance = pipe_x - self.x
            self.fitness = self.distance - pipe_distance

        return [self.create_rect(self.x, self.y, self.radius)]

    @staticmethod
    #convience function for creating rectangles
    def create_rect(x, y, radius):
        return pygame.Rect(x - radius, y - radius, x + radius, y + radius)

    #use the neural network to decide if it should fly
    def flap(self, inputs):
        inputs.append(self.y)
        inputs = self.normalize(inputs)
        output = self.brain.guess_ff(inputs)

        #jumps if more than 50% confident
        return True if output[0] > .50 else False

    @staticmethod
    #normalizes the data to a range between 0 and 1
    def normalize(data):
        normalized = []
        mini = min(data)
        maxi = max(data)
        for i in data:
            normalized.append((i - mini)/(maxi - mini))
        return normalized





