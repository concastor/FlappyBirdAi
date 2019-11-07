from Bird import Bird
import random as rand


class Population:
    #constructor
    def __init__(self, canvas):
        self.canvas = canvas
        self.y = self.canvas.get_height() / 2
        self.colours = self.create_colours()
        self.birds = []
        self.curr_best = 0
        self.champ = None
        self.pop_size = 20  #can be used to modify population size
        self.create_pop()

    #creates a population of birds
    def create_pop(self):
        for i in range(50):
            new_bird = Bird(self.canvas, self.pick_colour(), self.y)
            self.birds.append(new_bird)

    #pick a random colour from the random colour list
    def pick_colour(self):
        return rand.choice(self.colours)

    #creates a list of random colours for the birds
    @staticmethod
    def create_colours():
        colours = []
        for i in range(10):
            #random rgb values
            r = rand.randint(50, 255)
            g = rand.randint(50, 255)
            b = rand.randint(1, 128)
            colours.append((r, g, b))
        return colours

    #update the location of all the birds
    def update(self, pipe_x):
        rects = []
        for b in self.birds:
            rects.extend(b.update(pipe_x))
        return rects

    #check if all the birds are dead
    def all_dead(self):
        for b in self.birds:
            if not b.isDead:
                return False
        return True

    #check if any of the birds collided with the pipe
    def collide(self, pipes):
        pipe = pipes[0]
        for bird in self.birds:
            #check if its the right height and between pipe borders
            if bird.y < pipe.top_y or bird.y > pipe.bottom_y:
                if pipe.x <= bird.x <= pipe.x + 50:
                    bird.isDead = True

    #uses neural network to to decide which birds should flap
    def movement(self, inputs):
        temp = inputs
        for bird in self.birds:
            #doesent change its movement if its already moving
            if bird.move == 0:
                i = []
                i.extend(temp)

                output = bird.flap(i)

                #set movement depending on guess
                bird.move = 12 if output else 0

    #creates a new population of birds based on top 3 from last gen
    def new_pop(self):
        f_arr = self.fitness_arr()
        self.find_max(self.birds)
        self.birds = []
        for i in range(self.pop_size):
            #pick parent from list
            parent = rand.choice(f_arr)
            child = Bird(self.canvas, self.mutate_colour(parent.colour), self.y)
            child.brain = parent.brain.copy()
            #mutate the brains of the children
            child.brain.mutate()
            self.birds.append(child)

        #add champion from last gen to keep population performance equal or higher
        self.birds.append(self.champ)

    #finds the champion of generation
    def find_max(self, birds):
        maxi = birds[0]
        for b in birds:
            if b.fitness > maxi.fitness:
                maxi = b

        #checks if generation performed worse than last gen
        if not maxi.fitness > self.curr_best:
            self.champ = maxi
        else:
            self.curr_best = maxi.fitness
            self.champ = maxi

    #creates an array of objects that has as many spots as its fitness
    def fitness_arr(self):
        f_arr = []
        amount = self.find_best()
        x = 3
        for bird in amount:
            for i in range(x):
                f_arr.append(bird)
            x -= 1

        return f_arr

    #finds the top 3 fitness in the population
    def find_best(self):
        best = []
        first = second = third = self.birds[0]

        for b in self.birds:

            if b.fitness > first.fitness:
                third = second
                second = first
                first = b

            elif b.fitness > second.fitness:
                third = second
                second = b

            elif b.fitness > third.fitness:
                third = b

        #add and return top 3 to list
        best.extend([first, second, third])
        return best

    @staticmethod
    #slight modifies colour of next generation based on the parent
    def mutate_colour(colour):
        colour = [colour[0], colour[1], colour[2]]

        t = rand.randint(0, 2)
        index = rand.randint(0, 2)

        if t == 1:
            colour[index] -= 30
            if colour[index] < 0:
                colour[index] = 0
        else:
            colour[index] += 30
            if colour[index] > 255:
                colour[index] = 255

        return tuple(colour)


