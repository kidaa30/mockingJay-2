__author__ = 'Nathan'
import pygame


class GameView(object):
    """
    GameView constructs the main GUI window and handles all the drawing routines
    """

    def __init__(self, width, height, cell_size=(10, 10)):
        self.size = self.width, self.height = width * 10, height * 10
        self.screen = pygame.display.set_mode(self.size)
        self.state = None
        self.cell_size = cell_size
        self.layers = {
            'ground': (pygame.Surface(self.size), 0),
            'particle': (pygame.Surface(self.size), 1)
        }

        self.layers['particle'][0].set_colorkey((255, 0, 255))
        self.layers['particle'][0].fill((255, 0, 255))

    def draw(self, tribute, tributes, alive):
        self.layers['particle'][0].fill((255, 0, 255))
        if bool(self.state):
            for layer in self.layers:
                for x, y, color, p in self.state.grid[layer]:
                    tile = pygame.Rect(x * self.cell_size[0], y * self.cell_size[1], *self.cell_size)
                    pygame.draw.rect(self.layers[layer][0], pygame.Color(*color), tile, 0)

        layers_ordered = sorted(self.layers.iteritems(), key=lambda g: g[1][1])
        for layer in layers_ordered:
            self.screen.blit(layer[1][0], (0, 0))

        self.textTribute(tribute)
        self.textStats(tributes, alive)
        pygame.display.flip()

    def render(self, gs, tribute, tributes, alive):
        """
        here, we set the game state to render
        @param gs: the game state to render
        """
        self.state = gs
        self.draw(tribute, tributes, alive)

    def textStats(self, tributes, alive):
        fontobject = pygame.font.SysFont('Arial', 18)
        s_x = 5
        s_y = 520
        for district, t1, t2 in tributes:
            self.screen.blit(fontobject.render('District ' + district[1:], 1, (255, 255, 255)), (s_x, s_y))
            color = ()
            if t1 not in alive:
                color = (255, 1, 0)
            else:
                color = (0, 255, 1)
            self.screen.blit(fontobject.render(t1.first_name, 1, color), (s_x, s_y + 25))
            if t2.killed:
                color = (255, 1, 0)
            else:
                color = (0, 255, 1)
            self.screen.blit(fontobject.render(t2.first_name, 1, color), (s_x, s_y + 50))
            s_x += 90

    def textTribute(self, tribute):
        fontobject=pygame.font.SysFont('Arial', 18)
        self.screen.blit(fontobject.render((tribute.first_name+ ' ' + tribute.last_name), 1, (255, 255, 255)), (510, 20))
        self.screen.blit(fontobject.render(('*****************************************'), 1, (255, 255, 255)), (505, 55))
        self.screen.blit(fontobject.render(('Size: ' +str(tribute.attributes['size'])), 1, (255, 255, 255)), (510, 80))
        self.screen.blit(fontobject.render(('Strength: ' +str(tribute.attributes['strength'])), 1, (255, 255, 255)), (650, 80))
        self.screen.blit(fontobject.render(('Speed: ' +str(tribute.attributes['speed'])), 1, (255, 255, 255)), (510, 120))
        self.screen.blit(fontobject.render(('Hunting: ' +str(tribute.attributes['hunting_skill'])), 1, (255, 255, 255)), (650, 120))
        self.screen.blit(fontobject.render(('Fighting: ' +str(tribute.attributes['fighting_skill'])), 1, (255, 255, 255)), (510, 160))
        self.screen.blit(fontobject.render(('Camo Skill: ' +str(tribute.attributes['camouflage_skill'])), 1, (255, 255, 255)), (650, 160))
        self.screen.blit(fontobject.render(('Friendliness: ' +str(tribute.attributes['friendliness'])), 1, (255, 255, 255)), (510, 200))
        self.screen.blit(fontobject.render(('Stamina: ' +str(tribute.attributes['stamina'])), 1, (255, 255, 255)), (650, 200))
        self.screen.blit(fontobject.render(('Endurance: ' +str(tribute.attributes['endurance'])), 1, (255, 255, 255)), (510, 240))
        self.screen.blit(fontobject.render(('Health: ' +str(tribute.stats['health'])) + ' / ' +
                                           str(tribute.attributes['max_health']), 1, (255, 255, 255)), (650, 240))
        self.screen.blit(fontobject.render('Last Action: ' + str(tribute.last_action), 1, (255, 255, 255)), (510, 275))
        self.screen.blit(fontobject.render('Fighting: ' + str(tribute.fighting_state), 1, (255, 255, 255)), (510, 315))
        self.screen.blit(fontobject.render('****************GOALS*****************', 1, (255, 255, 255)), (505, 350))

        for i, goal in enumerate(tribute.goals):
            self.screen.blit(fontobject.render(goal.name + ': ' + ('%.2f' % goal.value), 1, (255, 255, 255)), (510 + 140 * (i % 2), 385 + (35 * (i / 2))))

