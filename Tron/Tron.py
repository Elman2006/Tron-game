# ------------------------------ Modules ----------------------------------------------
import pygame
import os
import sys

# ------------------------------ Classes & settings --------------------------------------
pygame.init() # initialize pygame

WIN_WIDTH = 800
BG_CLR = "#113F67"
WIN_HEIGHT = 600
display = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
# Get the path to the folder where your script is located
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# Safely join the image path
icon_path = os.path.join(base_path, "TronIdentity.png")

# Load and set icon
icon_img = pygame.image.load(icon_path)
pygame.display.set_icon(icon_img)
pygame.display.set_caption("Tron Game")

GRID_CLR = "#9ECAD6"
GRID_WIDTH = 1

clock = pygame.time.Clock()
running = True
gameover = False
winner = ""

font = pygame.font.SysFont("Agency FB", 65)
font_clr = "#F3E2D4"

class Tron_bike:
    """ A class to create an object of the trons """

    def __init__(self, head_color, body_color, start_x, start_y):
        """ Initialize the trons """
        # Colors
        self.head_clr = head_color
        self.body_clr = body_color
        # Position & size
        self.x = start_x
        self.y = start_y
        self.w = self.h = 10
        # squares (list of [x,y] segments)
        self.squares = [[self.x, self.y]]
        self.length = 1
        # Movement speed
        self.tron_speed = 5
        # Direction vector (dx, dy)
        self.dx, self.dy = 0, 0
   
    def draw(self):
        """ A method to draw the bikes """
        for i in range(len(self.squares)):
            if i == self.length - 1:
                pygame.draw.rect(display, self.head_clr, (self.squares[i][0], self.squares[i][1], self.w, self.h))
            else:    
                pygame.draw.rect(display, self.body_clr, (self.squares[i][0], self.squares[i][1], self.w, self.h))
    
    def move(self):
        """Moves the bike continuously in its current direction."""
        if self.dx != 0 or self.dy != 0:
            self.x += self.dx * self.tron_speed
            self.y += self.dy * self.tron_speed
            self.squares.append([self.x, self.y])
            self.length += 1

    def set_direction(self, dx, dy):
        """Update movement direction unless it's directly opposite."""
        if (dx, dy) != (-self.dx, -self.dy):  # Prevent reversing
            self.dx = dx
            self.dy = dy



# ------------------------------- functions  ------------------------------------------------
def draw_grid():
    """ A function to draw the grids """

    squares = 50
    for i in range(WIN_HEIGHT//squares):
        pygame.draw.line(display, GRID_CLR, (0, i*squares), (WIN_WIDTH, i*squares), GRID_WIDTH)
    
    for i in range(WIN_WIDTH//squares):
        pygame.draw.line(display, GRID_CLR, (i*squares, 0), (i*squares, WIN_HEIGHT), GRID_WIDTH)


def check_collision(tron, other):
    """
    Return True if:
      - tron head is outside the play area (wall collision), or
      - tron head overlaps any earlier segment in its own squares (self-collision), or
      - tron head overlaps any segment of the other tron's squares (opponent-collision).
    """

    tron_head = tron.squares[-1]
    x, y = tron_head

    # Wall collisin
    if x<0 or x+tron.w > WIN_WIDTH or y<0 or y+tron.h > WIN_HEIGHT:
        return True
    
    # Self collision
    elif tron_head in tron.squares[:-1]: return True
    
    # Self other collision
    elif tron_head in other.squares: return True

    # Self other collision
    elif tron_head in other.squares[-1]: return True
    
    else: return False


def show_gameover(text, restart_txt):
    """Render a Game Over message centered on the screen."""
    pause_txt = font.render(text, True, font_clr)
    reload_txt = font.render(restart_txt, True, font_clr)
    display.blit(pause_txt, (WIN_WIDTH//2 - pause_txt.get_width()//2, WIN_HEIGHT//2 - 50))
    display.blit(reload_txt, (WIN_WIDTH//2 - reload_txt.get_width()//2, WIN_HEIGHT//2 + 50))


# ------------------------------- Main code ------------------------------------------------
TRON_HCLR_L = "#004030"
TRON_CLR_L = "#4A9782"
tron_l = Tron_bike(TRON_HCLR_L, TRON_CLR_L, WIN_WIDTH//2 - 200, WIN_HEIGHT//2)

TRON_HCLR_R = "#555879"
TRON_CLR_R = "#98A1BC"
tron_r = Tron_bike(TRON_HCLR_R, TRON_CLR_R,  WIN_WIDTH//2 + 200, WIN_HEIGHT//2)

# Main game loop
while running:

    for event in pygame.event.get():
        # This loop, gets each event that user do in the pygame screen

        if event.type == pygame.QUIT:
            # if user press the cross button in top-right of window:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gameover = not gameover  # Toggle game pause
            
            elif event.key == pygame.K_RETURN and gameover:
                # Reset game state
                gameover = False
                tron_l = Tron_bike(TRON_HCLR_L, TRON_CLR_L, WIN_WIDTH//2 - 200, WIN_HEIGHT//2)
                tron_r = Tron_bike(TRON_HCLR_R, TRON_CLR_R, WIN_WIDTH//2 + 200, WIN_HEIGHT//2)



    keys = pygame.key.get_pressed()
    display.fill(BG_CLR)
    draw_grid()
    tron_l.draw()
    tron_r.draw()

    if not gameover:
        # ---- Handle player direction input ----
        if keys[pygame.K_w]: tron_l.set_direction(0, -1)
        elif keys[pygame.K_s]: tron_l.set_direction(0, 1)
        elif keys[pygame.K_a]: tron_l.set_direction(-1, 0)
        elif keys[pygame.K_d]: tron_l.set_direction(1, 0)

        if keys[pygame.K_UP]: tron_r.set_direction(0, -1)
        elif keys[pygame.K_DOWN]: tron_r.set_direction(0, 1)
        elif keys[pygame.K_LEFT]: tron_r.set_direction(-1, 0)
        elif keys[pygame.K_RIGHT]: tron_r.set_direction(1, 0)

        # ---- Auto-move bikes every frame ----
        tron_l.move()
        tron_r.move()


        # ---- Collision Detection ----
        left_crashed = check_collision(tron_l, tron_r)
        right_crashed = check_collision(tron_r, tron_l)
        if left_crashed and right_crashed:
            gameover = True
            winner = "Both bikes crashed! No winner."
        elif left_crashed:
            gameover = True
            winner = "Right bike wins!"
        elif right_crashed:
            gameover = True
            winner = "Left bike wins!"

    if gameover:
        show_gameover(winner, "press ENTER to restart")

    pygame.display.update() # To update each frame in game
    clock.tick(60) # set FPS for game

pygame.quit()
