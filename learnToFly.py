import pygame
import sys
import random

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Learn to Fly Simulator")

white = (255, 255, 255)
blue = (0, 0, 255)
gray = (200, 200, 200)
yellow = (255, 255, 0)

class Penguin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(blue)
        self.rect = self.image.get_rect()
        self.rect.center = (100, height // 2)
        self.velocity = 0
        self.max_velocity = 10  # Velocidad máxima hacia abajo
        self.distance = 0
        self.game_started = False
        self.jumping = False
        self.jump_count = 0
        self.max_jumps = 4
        self.space_pressed = False  # Bandera para detectar presión de la tecla de espacio

    def reset_jump(self):
        self.velocity = -10
        self.jumping = True
        self.space_pressed = True

    def update(self):
        if not self.game_started:
            return

        keys = pygame.key.get_pressed()
        if self.rect.bottom == height:
            self.jump_count = 0
            self.jumping = False

        # Detectar presión inicial de la tecla de espacio
        if keys[pygame.K_SPACE] and not self.space_pressed and self.jump_count < self.max_jumps:
            self.reset_jump()

        # Restablecer la bandera cuando la tecla de espacio se suelta
        if not keys[pygame.K_SPACE]:
            self.space_pressed = False

        if self.jumping:
            self.jump_count += 1
            # Ajustar la lógica del salto para que la velocidad sea más pronunciada inicialmente
            self.velocity += 0.8
            self.rect.y += self.velocity
            if self.velocity <= 0:
                self.jumping = False
        else:
            # Aceleración constante hacia abajo solo cuando no se está saltando
            if not keys[pygame.K_SPACE] and self.rect.y < height:  # Evitar que el pingüino baje más allá del límite inferior
                self.velocity += 0.8
                if self.velocity > self.max_velocity:
                    self.velocity = self.max_velocity
                self.rect.y += self.velocity

        if self.rect.bottom > height:
            self.rect.bottom = height
            self.velocity = 0
            if not keys[pygame.K_SPACE]:
                self.jump_count = 0  # Reiniciar el contador de saltos solo cuando no se está saltando

        self.distance += abs(self.velocity)

# Clase para representar nubes en el fondo
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 30), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, gray, (0, 0, 50, 30))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(width, width + 200)
        self.rect.y = random.randint(50, 150)

    def update(self):
        self.rect.x -= 2
        if self.rect.right < 0:
            self.rect.x = random.randint(width, width + 200)
            self.rect.y = random.randint(50, 150)

# Clase para representar monedas
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, yellow, (15, 15), 15)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(width, width + 200)
        self.rect.y = random.randint(50, 150)

    def update(self):
        self.rect.x -= 2
        if self.rect.right < 0:
            self.rect.x = random.randint(width, width + 200)
            self.rect.y = random.randint(50, 150)

# Crear grupos de sprites
all_sprites = pygame.sprite.Group()
clouds = pygame.sprite.Group()
coins = pygame.sprite.Group()

penguin = Penguin()
all_sprites.add(penguin)

# Crear nubes y monedas iniciales
for _ in range(5):
    cloud = Cloud()
    all_sprites.add(cloud)
    clouds.add(cloud)

for _ in range(3):
    coin = Coin()
    all_sprites.add(coin)
    coins.add(coin)

font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Agregar cuenta regresiva
countdown_font = pygame.font.Font(None, 72)
countdown = 3
countdown_timer = pygame.time.get_ticks()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_time = pygame.time.get_ticks()
    if current_time - countdown_timer >= 1000 and countdown > 0:
        countdown -= 1
        countdown_timer = current_time
        if countdown == 0:
            penguin.game_started = True
            penguin.reset_jump()  # Realizar el primer salto al iniciar el juego

    all_sprites.update()

    # Verificar colisiones con las monedas
    hits = pygame.sprite.spritecollide(penguin, coins, True)
    if hits:
        penguin.jump_count = min(penguin.max_jumps, penguin.jump_count + 1)

    screen.fill(white)
    all_sprites.draw(screen)

    if countdown > 0:
        countdown_text = countdown_font.render(str(countdown), True, (0, 0, 0))
        screen.blit(countdown_text, (width // 2 - 20, height // 2 - 30))

    text = font.render(f"Distancia: {penguin.distance} pixels", True, (0, 0, 0))
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
