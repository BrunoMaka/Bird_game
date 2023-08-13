import pygame
import random
from settings import *

# Inicialização do Pygame
pygame.init()



# Criação da tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo")
clock = pygame.time.Clock()

# Variável para armazenar a pontuação máxima
max_score = 0   

num_obstaculos = 0

# Classe do jogador
# Classe do jogador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 4
        self.rect.bottom = HEIGHT // 2
        self.velocity = 0
        self.score = 0  # Pontuação do jogador
    
    def update(self):
        self.rect.y += self.velocity
        
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def increase_score(self, num_obstaculos):
        if num_obstaculos >= 3:
            self.score += 1

# Fonte para a pontuação
font = pygame.font.Font(None, 36)

# Classe do obstáculo
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, y_pos, height):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_WIDTH, height))
        self.image.fill(OBSTACLE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = y_pos
    
    def update(self):
        self.rect.x += OBSTACLE_VELOCITY

# Criação dos grupos de sprites
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

# Criação do jogador
player = Player()
all_sprites.add(player)

# Variável de estado da tela
current_screen = SCREEN_MENU

# Função para criar o botão
def create_button(t):
    button_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - BUTTON_HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    
    button_font = pygame.font.SysFont(BUTTON_FONT, BUTTON_FONT_SIZE)
    button_text = button_font.render(t, True, BLACK)
    button_text_rect = button_text.get_rect(center=button_rect.center)
    
    screen.blit(button_text, button_text_rect)

# Loop principal do jogo
# Loop principal do jogo
running = True
jumping = False
game_over = False
while running:
    # Processamento de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if current_screen == SCREEN_MENU:
                    current_screen = SCREEN_GAME
                elif current_screen == SCREEN_GAME_OVER:
                    current_screen = SCREEN_GAME
                    player.score = 0
                    game_over = False
                    player.rect.centerx = WIDTH // 4
                    player.rect.bottom = HEIGHT // 2
                    num_obstaculos = 0
                    obstacles.empty()
                    all_sprites.empty()
                    all_sprites.add(player)
                elif current_screen == SCREEN_GAME:
                    

                    if not jumping:
                        player.velocity = -PLAYER_JUMP_VELOCITY
                        jumping = True
            elif event.key == pygame.K_RETURN:
                if current_screen == SCREEN_GAME_OVER:
                    current_screen = SCREEN_MENU
                    player.score = 0
                    game_over = False
                    player.rect.centerx = WIDTH // 4
                    player.rect.bottom = HEIGHT // 2
                    obstacles.empty()
                    all_sprites.empty()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and jumping:
                player.velocity = PLAYER_JUMP_VELOCITY
                jumping = False

    if current_screen == SCREEN_MENU:
        # Renderização da tela de menu
        screen.fill(BLACK)
        create_button("Iniciar Jogo")

    elif current_screen == SCREEN_GAME:
        # Atualização dos sprites
        all_sprites.update()

        # Atualização da pontuação máxima
        if player.score > max_score:
            max_score = player.score

        # Verificação de colisão com obstáculos
        if pygame.sprite.spritecollide(player, obstacles, False):
            current_screen = SCREEN_GAME_OVER
            game_over = True

        # Criação de novos obstáculos
        if not game_over and (len(obstacles) == 0 or obstacles.sprites()[-1].rect.x <= WIDTH - OBSTACLE_GAP):
            obstacle_height = random.randint(100, 400)
            obstacle_top = Obstacle(0, obstacle_height)
            obstacle_bottom = Obstacle(obstacle_height + OBSTACLE_GAP, HEIGHT - obstacle_height - OBSTACLE_GAP)
            obstacles.add(obstacle_top, obstacle_bottom)
            all_sprites.add(obstacle_top, obstacle_bottom)
            player.increase_score(num_obstaculos)  # Incrementa a pontuação do jogador ao passar pelo obstáculo
            num_obstaculos +=1
        # Remoção de obstáculos que saíram da tela
        for obstacle in obstacles.copy():
            if obstacle.rect.right < 0:
                obstacles.remove(obstacle)
                all_sprites.remove(obstacle)

        # Renderização
        screen.fill(SKY_BLUE)
        all_sprites.draw(screen)

        score_text = font.render("Pontuação: {}".format(player.score), True, BLACK)
        max_score_text = font.render("Máx: {}".format(max_score), True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(max_score_text, (10, 50))

    elif current_screen == SCREEN_GAME_OVER:
        # Renderização da tela de Game Over
        screen.fill(BLACK)
        game_over_text = font.render("GAME OVER", True, WHITE)
        game_over_rect = game_over_text.get_rect()
        game_over_rect.center = (WIDTH // 2, HEIGHT // 2 - 50)
        screen.blit(game_over_text, game_over_rect)

        # Exibição da pontuação atual, máxima e botão para jogar novamente
        score_text = font.render("Pontuação: {}".format(player.score), True, WHITE)
        max_score_text = font.render("Pontuação Máx: {}".format(max_score), True, WHITE)

        score_rect = score_text.get_rect()
        max_score_rect = max_score_text.get_rect()

        score_rect.center = (WIDTH // 2, HEIGHT // 2 + 50)
        max_score_rect.center = (WIDTH // 2, HEIGHT // 2 + 100)

        screen.blit(score_text, score_rect)
        screen.blit(max_score_text, max_score_rect)
        
        create_button("Jogar Novamente")

    pygame.display.flip()
    clock.tick(FPS)

# Encerramento do Pygame
pygame.quit()
