import pygame
import random
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('POOPOO')

font_large = pygame.font.Font(None, 64)
font_medium = pygame.font.Font(None, 36)

class start_screen:
    def __init__(self):
        self.title_text = font_large.render("Try to eat sushi", True, BLACK)
        self.title_rect = self.title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))

        self.instruction_text = font_medium.render("Press SPACE to Start", True, BLACK)
        self.instruction_rect = self.instruction_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))

    def draw(self, screen):
        screen.fill(WHITE)
        screen.blit(self.title_text, self.title_rect)
        screen.blit(self.instruction_text, self.instruction_rect)
        
class end_screen:
    def __init__(self):
        self.title_text = font_large.render("try again", True, BLACK)
        self.title_rect = self.title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))

        self.instruction_text = font_medium.render("Press SPACE to Try again", True, BLACK)
        self.instruction_rect = self.instruction_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))

    def draw(self, screen):
        screen.fill(WHITE)
        screen.blit(self.title_text, self.title_rect)
        screen.blit(self.instruction_text, self.instruction_rect)
        

#class for the obsticles
class FallingObj:
    def __init__(self, screen_width):
        #first object (chopsticks)
        self.image = pygame.image.load('img/chopsticks.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed_y = random.randint(3,6)
        
        #second object (idk yet lol)
        # self.image = pygame.image.load('img/chopsticks.png')
        # self.rect = self.image.get_rect()
        # self.rect.x = random.randint(0, screen_width - self.rect.width)
        # self.rect.y = -self.rect.height
        # self.speed_y = random.randint(3,6)
        
    def update(self):
        self.rect.y += self.speed_y
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        

#method to 
def draw_sprites(screen, image, x, y):
    screen.blit(image, (x, y))

def main():
    #setting up screen window
    screen_width = 800
    screen_height = 600
    player_speed = 10

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('i wanna eat sushi')

    #importing sprites
    sushi_img = pygame.image.load('img/sushi.png')
    sushi_rect = sushi_img.get_rect() 
    bg_img = pygame.image.load('img/bg.png').convert()

    #initial position of sushi
    sushi_rect.center = (screen_width // 1.05, screen_height // 1.05)
    
    #HEALTH
    max_health = 100
    sushi_health = max_health
    
    def draw_health_bar(screen, x, y, health):
        pygame.draw.rect(screen, (255,0,0), (x,y, max_health, 40))
        pygame.draw.rect(screen, (0,255,0), (x, y, health, 40))
    
    
    falling_obj = []

    #game loop
    start = start_screen()
    end = end_screen()
    run = False
    game_over = False
    clock = pygame.time.Clock()
    
    while not run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    run = True
        start.draw(screen)
        pygame.display.update()
    
    
    while run:
        screen.fill((232, 244, 234))  # Fill screen with light green color
        screen.blit(bg_img, (0,0))
        
        #close out
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    run = True
                    if sushi_health <= 0:
                        run = False
                        sushi_health = max_health
                        falling_obj.clear()
                        game_over = False
                    elif not game_over:
                        game_over = True
    
            

        #movement 
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            sushi_rect.x -= player_speed  # Move left
        elif key[pygame.K_d]:
            sushi_rect.x += player_speed  # Move right
            
            
        #boundary 
        if sushi_rect.left <0:
            sushi_rect.left = 0
        elif sushi_rect.right > screen_width:
            sushi_rect.right = screen_width
            
        #falling obj at random intervals   
        if random.random() < 0.01:
            new_object = FallingObj(screen_width)
            falling_obj.append(new_object)
        
        #update + draw the object
        for obj in falling_obj:
            obj.update()
            obj.draw(screen)
            
            if obj.rect.colliderect(sushi_rect):
                sushi_health -= 10 
                falling_obj.remove(obj)
            
        #remove from the screen
        falling_obj = [obj for obj in falling_obj if obj.rect.y <= screen_height]

        # Draw sushi on the screen
        screen.blit(sushi_img, sushi_rect)
        
        draw_health_bar(screen, 650, 10, sushi_health)
        
        if sushi_health == 0:
            end.draw(screen)
            game_over = True

        pygame.display.update()  
        
        clock.tick(160)

    pygame.quit()

if __name__ == '__main__':
    main()
