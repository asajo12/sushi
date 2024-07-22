import pygame,random

pygame.display.set_caption('I Wanna Eat Sushi')
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

font_large = pygame.font.Font(None, 64)
font_medium = pygame.font.Font(None, 36)

class StartScreen:
    def __init__(self):
        self.title_text = font_large.render("I wanna eat sushi :(", True, BLACK)
        self.title_rect = self.title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))

        self.instruction_text = font_medium.render("Press SPACE to Start", True, BLACK)
        self.instruction_rect = self.instruction_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))

    def draw(self, screen):
        start_img = pygame.image.load('img/start_img.png').convert()
        screen.blit(start_img, (0,0))
        
class EndScreen:
    def __init__(self):
        self.title_text = font_large.render("Game Over", True, BLACK)
        self.title_rect = self.title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))

        self.instruction_text = font_medium.render("Press SPACE to Try again", True, BLACK)
        self.instruction_rect = self.instruction_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))

    def draw(self, screen):
        start_img = pygame.image.load('img/end_img.png').convert()
        screen.blit(start_img, (0,0))

        

class FallingObj:
    def __init__(self, screen_width):
        self.image = pygame.image.load('img/chopsticks.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed_y = random.randint(3,6)
        
    def update(self):
        self.rect.y += self.speed_y
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
def paused():
    pygame.mixer.music.pause()
    
def unpause():
    global pause
    pygame.mixer.music.unpause()
    pause = False
        
def music():
    pygame.mixer.music.load('audio/aisha_music.wav')
    pygame.mixer.music.play(-1)


def draw_health_bar(screen, x, y, health):
    max_health = 100
    pygame.draw.rect(screen, (255,0,0), (x, y, max_health, 40))
    pygame.draw.rect(screen, (0,255,0), (x, y, health, 40))


def main():
    music()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('I Wanna Eat Sushi')

##############
#IMPORTING IMAGES
##############
    sushi_img = pygame.image.load('img/sushi2.png')
    bg_img = pygame.image.load('img/bg.png').convert()

    sushi_rect = sushi_img.get_rect(center=(SCREEN_WIDTH // 1.10, SCREEN_HEIGHT // 1.10))
    
    max_health = 100
    sushi_health = max_health
    
    falling_obj = []
    
    start = StartScreen()
    end = EndScreen()
    
    clock = pygame.time.Clock()
    game_state = "START"
    
    while True:
        paused()
        if game_state == "START":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_state = "RUNNING"
        
            start.draw(screen)
            pygame.display.update()
        
        elif game_state == "RUNNING":
            unpause()
            screen.fill((0, 0, 0)) 
            screen.blit(bg_img, (0,0))
            
            #basic states
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        sushi_health = max_health
                        falling_obj.clear()
                        game_state = "RUNNING"
                    elif sushi_health <= 0:
                        game_state = "GAME_OVER"
            
            #movement controls
            key = pygame.key.get_pressed()
            if key[pygame.K_a]:
                sushi_rect.x -= 10
            elif key[pygame.K_d]:
                sushi_rect.x += 10
                
            #screen boundary
            if sushi_rect.left < 0:
                sushi_rect.left = 0
            elif sushi_rect.right > SCREEN_WIDTH:
                sushi_rect.right = SCREEN_WIDTH
            
            time = pygame.time.get_ticks()
                        
            #rounds
            if time >= 3000: #round 1
                if random.random() < 0.01:
                    new_object = FallingObj(SCREEN_WIDTH)
                    falling_obj.append(new_object)
            elif time >= 10000: #round 2
                if random.random() < 0.02:
                    new_object = FallingObj(SCREEN_WIDTH)
                    new_object.speed_y = random.randint(9,10)
                    falling_obj.append(new_object)
            elif time >= 20000: #round 3
                if random.random() < 0.03:
                    new_object = FallingObj(SCREEN_WIDTH)
                    new_object.speed_y = random.randint(35,40)
                    falling_obj.append(new_object)
            
            for obj in falling_obj:
                obj.update()
                obj.draw(screen)
                
                if obj.rect.colliderect(sushi_rect):
                    sushi_health -= 10 
                    falling_obj.remove(obj)
                
            falling_obj = [obj for obj in falling_obj if obj.rect.y <= SCREEN_HEIGHT]
    
            screen.blit(sushi_img, sushi_rect)
            draw_health_bar(screen, 650, 10, sushi_health)
            
            pygame.display.update()
            clock.tick(60)
        
        elif game_state == "GAME_OVER":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        sushi_health = max_health
                        falling_obj.clear()
                        game_state = "RUNNING"
            
            end.draw(screen)
            pygame.display.update()
            
if __name__ == "__main__":
    main()