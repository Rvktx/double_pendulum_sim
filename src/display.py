import pygame


class Display:
    # RGB tuples dictionary
    COLORS = {
        'BLACK': (0, 0, 0),
        'RED': (255, 0, 0),
        'WHITE': (255, 255, 255)
    }

    def __init__(self, res):
        # Setting resolution of the simulation
        self. width, self.height = res

        # Initializing pygame window
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Double pendulum simulation')
        pygame.display.flip()

        # Initializing pygame font
        pygame.font.init()
        self.font = pygame.font.Font('resources/RobotoMono.ttf', 18)

    def draw_rod(self, start, end):
        """ Draw a rod. """
        pygame.draw.line(self.window, self.COLORS['WHITE'], start, end, 4)

    def draw_body(self, pos):
        """ Draw a body. """
        pygame.draw.circle(self.window, self.COLORS['WHITE'], pos, 20)

    def draw_path(self, path, path_depth):
        """ Draw a path. """

        # Doesn't do anything if path contains too few elements
        if len(path) > 1:
            start = len(path) - path_depth if path_depth <= len(path) else 1

            for point in range(start, len(path)):
                pygame.draw.line(self.window, self.COLORS['RED'], path[point], path[point - 1], 2)

    def draw_info(self, info_str, pos):
        """ Draw a line of text at given position. """
        text = self.font.render(info_str, 1, self.COLORS['WHITE'])
        self.window.blit(text, pos)

    @staticmethod
    def handle_events():
        """ Handles events in window loop. """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    def next_frame(self, delay):
        """ Update a frame, and prepare surface for next one after given delay. """
        pygame.display.update()
        pygame.time.wait(delay)
        self.window.fill(self.COLORS['BLACK'])
