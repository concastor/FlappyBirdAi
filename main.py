import pygame
from population import Population as pop
from pipe import Course
from button import Button

# Define the colors for my sanity
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
BLUE = (0,   191, 255)
GREEN = (0, 255,   0)
YELLOW = (255, 255, 0)


#control class for the entire program
class Control:
    def __init__(self):
        #this font is absurd and I love it
        self.fnt = "sitkasmallsitkatextitalicsitkasubheadingitalicsitkaheadingitalicsitkadisplayitalicsitkabanneritalic"

        pygame.init()
        self.size = [800, 700]
        self.speed = 1  #multiplier for game speed
        self.canvas = pygame.display.set_mode(self.size)
        self.canvas.fill(BLUE)
        pygame.display.flip()
        pygame.display.set_caption('Flappy Bird Ai')
        self.flappies = pop(self.canvas)
        self.gen = 1
        self.high_score = 0
        self.active = None
        self.buttons = self.create_buttons()

    def create_buttons(self):
        half = Button(self.canvas.get_width()/2, 600, "x0.5", self.canvas, self.fnt, .5)
        one = Button(self.canvas.get_width()/2 + 100, 600, "x1", self.canvas, self.fnt, 1)
        two = Button(self.canvas.get_width()/2 + 200, 600, "x2", self.canvas, self.fnt, 2)
        three = Button(self.canvas.get_width()/2 + 300, 600, "x3", self.canvas, self.fnt, 3)

        #set default
        one.active = True
        self.active = one

        return [half, one, two, three]

    #change the active button and change game speed
    def change_active(self, button):
        self.active.active = False
        button.active = True
        self.active = button
        self.speed = button.speed

    #launch the simulation
    def launch(self):
        end = False
        while not end:
            score = self.start_game()

            #allows an error free exit
            if score == "end":
                break

            self.flappies.new_pop()

            self.gen += 1

        pygame.quit()

    @staticmethod
    #displays the current score of the generation
    def display_score(canvas, score, font):
        loc = [int(canvas.get_width() / 2) - 50, 50]
        label = font.render(str(score), 24, BLACK)
        canvas.blit(label, loc)

    @staticmethod
    #updates the background of the scores to prevent overlap
    def update_score(canvas, font, score):
        size = font.size(str(score))

        loc = (int(canvas.get_width() / 2) - 50, 50)
        high_loc = [canvas.get_width() - 120, 50]

        surface = pygame.Surface(size)
        surface.fill(BLUE)

        canvas.blit(surface, loc)
        canvas.blit(surface, high_loc)

    #displays the highest score of all generations
    def display_high(self, canvas, score):
        text = "High Score: " + str(score)
        font = pygame.font.SysFont(self.fnt, 20)
        loc = [canvas.get_width() - 225, 50]
        label = font.render(text, 24, BLACK)
        canvas.blit(label, loc)
        loc.extend(font.size(text))
        return loc

    #displays what generation the program is on
    def display_generation(self, canvas, gen):
        font = pygame.font.SysFont(self.fnt, 20)
        text = "Generation: " + str(gen)
        loc = [50, 50]
        label = font.render(text, 12, BLACK)
        canvas.blit(label, loc)
        loc.extend(font.size(text))
        return loc

    #convience function to draw all of the labels
    def draw_labels(self, score, font):
        gen_loc = self.display_generation(self.canvas, self.gen)
        high_loc = self.display_high(self.canvas, self.high_score)
        self.display_score(self.canvas, score, font)
        return self.create_rect([gen_loc, high_loc])

    @staticmethod
    def create_rect(coords):
        rects = []
        for c in coords:
            rects.append(pygame.Rect(c[0], c[1], c[0] + int(c[2]), c[1] + int(c[3])))
        return rects

    #starts the game for the current generation
    def start_game(self):
        #init variables
        pipes = Course(self.canvas, 300)
        self.canvas.fill(BLUE)
        pygame.display.flip()
        clock = pygame.time.Clock()
        score = 0
        my_font = pygame.font.SysFont(self.fnt, 50)

        done = False
        while not done:

            #gather nn inputs
            inputs = []
            inputs.extend(pipes.get_inputs())

            #sets frame rate of program
            clock.tick(60 * self.speed)

            #used to update only part of screen that's changed
            dirty_rects = []

            #gather nn inputs
            inputs = []
            inputs.extend(pipes.get_inputs())

            if not self.flappies.all_dead():
                for event in pygame.event.get():
                    #allows game to exit
                    if event.type == pygame.QUIT:
                        return "end"
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        pos = pygame.mouse.get_pos()
                        for b in self.buttons:
                            #check if button is pressed
                            if b.rect.collidepoint(pos):
                                self.change_active(b)

                #add pipe movement and check for collision
                dirty_rects.extend(pipes.update())
                self.flappies.collide(pipes.pipes)

                #birds brain guesses if it should jump
                self.flappies.movement(inputs)
                temp = self.flappies.update(pipes.pipes[0].x)

                #increases the score
                if pipes.get_score(self.flappies.birds):
                    self.update_score(self.canvas, my_font, score)
                    score += 1
                    if score > self.high_score:
                        self.high_score = score

                # if temp is not None:
                dirty_rects.extend(temp)

                #display labels and buttons
                dirty_rects.extend(self.draw_labels(score, my_font))
                for b in self.buttons:
                    dirty_rects.append(b.show())

                #update only frames that have been changed
                pygame.display.update(dirty_rects)

            else:
                done = True

        #compare score to high score
        return score


#run the program
main = Control()
main.launch()

