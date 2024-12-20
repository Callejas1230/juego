import pygame
import sys
import random
pygame.init()
pygame.display.set_caption("Sidescrolling Shooter by @Callejas Torrico Cristopher")
clock = pygame.time.Clock()
WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
class Player():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dy = 0
        self.dx = 0
        self.surface = pygame.image.load('player.png').convert()
        self.score = 0
        self.max_health = 20
        self.health = self.max_health
        self.kills = 0      
    def up(self):
        self.dy = -6
    def down(self):
        self.dy = 6
    def left(self):
        self.dx = -6
    def right(self):
        self.dx = 6
    def move(self):
        self.y = self.y + self.dy
        self.x = self.x + self.dx
        #colision
        if self.y < 0:
            self.y = 0
            self.dy = 0  
        elif self.y > 550 :
            self.y = 550    
            self.dy = 0
        if self.x < 0:
            self.x = 0
            self.dx = 0
        elif self.x > 200:
            self.x = 200
            self.dx = 0
    def distance(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
    def render(self):
        screen.blit(self.surface, (int(self.x), int(self.y)))
        pygame.draw.line(screen, GREEN, (int(self.x), int(self.y)), (int(self.x + (40 * (self.health/self.max_health))), int(self.y)), 2)
class Missile():
    def __init__(self):
        self.x = 0
        self.y = 1000
        self.dx = 0
        self.surface = pygame.image.load('missile.png').convert()
        self.state = "ready"
    def fire(self):
        self.state = "firing"
        self.x = player.x + 25
        self.y = player.y + 16
        self.dx = 10
    def move(self):
        if self.state == "firing":
            self.x = self.x + self.dx 
        if self.x > 800:
            self.state = "ready"
            self.y = 1000
    def distance(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
    def render(self):
        screen.blit(self.surface, (int(self.x), int(self.y)))
class Enemy():
    def __init__(self):
        self.x = 800
        self.y = random.randint(0, 550)
        self.dx = random.randint(10, 50) / -10
        self.dy = 0
        self.surface = pygame.image.load('enemy.png')
        self.max_health = random.randint(5, 15)
        self.health = self.max_health
        self.type = "enemy"
    def move(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        if self.x < -30:
            self.x = random.randint(800, 900)
            self.y = random.randint(0, 550) 
        if self.y < 0:
            self.y = 0
            self.dy *= -1
        elif self.y > 550 :
            self.y = 550    
            self.dy *= -1
    def distance(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
    def render(self):
        screen.blit(self.surface, (int(self.x), int(self.y)))
        pygame.draw.line(screen, GREEN, (int(self.x), int(self.y)), (int(self.x + (30 * (self.health/self.max_health))), int(self.y)), 2)
class Star():
    def __init__(self):
        self.x = random.randint(0, 1000)
        self.y = random.randint(0, 550)
        self.dx = random.randint(10, 50) / -30
        images = ["yellow_star.png", "red_star.png", "white_star.png"]
        self.surface = pygame.image.load(random.choice(images))
    def move(self):
        self.x = self.x + self.dx
        if self.x < 0:
            self.x = random.randint(800, 900)
            self.y = random.randint(0, 550)        
    def distance(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
    def render(self):
        screen.blit(self.surface, (int(self.x), int(self.y)))
# sonido
missile_sound = pygame.mixer.Sound("missile.wav")
explosion_sound = pygame.mixer.Sound("explosion.wav")
font = pygame.font.SysFont("comicsansms", 24)       
player = Player()
missiles = [Missile(), Missile(), Missile()]
enemies = []
for _ in range(5):
    enemies.append(Enemy())
stars = []
for _ in range(30):
    stars.append(Star())
def fire_missile():
    for missile in missiles:
        if missile.state == "ready":
            missile.fire()
            missile_sound.play()
            break
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.up()
            elif event.key == pygame.K_s:
                player.down()
            elif event.key == pygame.K_a:
                player.left()
            elif event.key == pygame.K_d:
                player.right()
            elif event.key == pygame.K_SPACE:
                fire_missile()
    player.move()
    for missile in missiles:
        missile.move()
    for star in stars:
        star.move()
    for enemy in enemies:
        enemy.move()
        for missile in missiles:
            if enemy.distance(missile) < 20:
                explosion_sound.play()
                enemy.health -= 4
                if enemy.health <= 0:
                    enemy.x = random.randint(800, 900)
                    enemy.y = random.randint(0, 550)
                    player.kills += 1
                    if player.kills % 10 == 0:
                        enemy.surface = pygame.image.load('boss.png').convert()
                        enemy.max_health = 50
                        enemy.health = enemy.max_health
                        enemy.dy = random.randint(-5, 5)
                        enemy.type = "boss"
                    else:
                        enemy.type = "enemy"
                        enemy.dy = 0
                        enemy.surface = pygame.image.load('enemy.png').convert()
                        enemy.max_health = random.randint(5, 15)
                        enemy.health = enemy.max_health
                else:
                    enemy.x += 20
                missile.dx = 0
                missile.x = 0
                missile.y = 1000
                missile.state = "ready"
                player.score += 10
        if enemy.distance(player) < 20:
            explosion_sound.play()
            player.health -= random.randint(5, 10)
            enemy.health -= random.randint(5, 10)
            enemy.x = random.randint(800, 900)
            enemy.y = random.randint(0, 550)
            if player.health <= 0:
                print("Game over!")
                pygame.quit()
                exit()    
    screen.fill(BLACK)
    for star in stars:
        star.render()
    player.render()
    for missile in missiles: 
        missile.render()
    for enemy in enemies:
        enemy.render()  
    ammo = 0
    for missile in missiles:
        if missile.state == "ready":
            ammo += 1
    for x in range(ammo):
        screen.blit(missile.surface, (700 + 30 * x, 20))
    score_surface = font.render(f"Score: {player.score} Kills: {player.kills}", True, WHITE)
    screen.blit(score_surface, (380, 20))
    pygame.display.flip()
    clock.tick(30)  