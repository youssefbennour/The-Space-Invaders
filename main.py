from Imports import *


pygame.init()
lives =  20
class Explosi(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 255, 255))
        pygame.draw.circle(self.image, (0, 0, 255), (25, 25), 25, 0)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

class Explosio():
    def __init__(self, x_pos, y_pos, radius = 1):
        self.radius = radius
        self.x_pos =x_pos
        self.y_pos = ŷ_pos

#functions
def explosion_stuff(x,y, screen):
    explosion_group.add(Explosion(x, y, screen))
    explosion_sound.play()

def collision():
    global lives
    craftLaserCollision = pygame.sprite.spritecollide(craft.sprite, lasers_group, True, pygame.sprite.collide_mask)
    craftInvaderCollision = pygame.sprite.spritecollide(craft.sprite, invaders_group, True, pygame.sprite.collide_mask)

    if craftLaserCollision:
        lives -=1

    if craftInvaderCollision:
        lives -= 2
        explosion_stuff(craft.sprite.x, craft.sprite.y, screen)

    if craft.sprite.lasers:
        for laser in craft.sprite.lasers:
           if pygame.sprite.spritecollide(laser, invaders_group, True, pygame.sprite.collide_mask):
               explosion_stuff(laser.rect.x, laser.rect.y, screen)
               laser.destroy_laser()

    if invaders_group.sprites():
        for invader in invaders_group.sprites():
            if invader.rect.top>= 650:
                lives -= 1



fromY = 100
toY = 0
maxPosInterval = [500, 400]

def generate_enemies(fromY, toY):
    invaders_group.add(Invader(randint( 50, 150), randint(-fromY, -toY)))
    invaders_group.add(Invader(randint(250, 350), randint(-fromY, -toY)))
    invaders_group.add(Invader(randint(400, 600), randint(-fromY, -toY)))
    fromY += 100
    toY += 100
    if fromY%maxPosInterval[0]:
        fromY= 100
    if toY%maxPosInterval[1]:
        toY = 0
    return fromY, toY

def display_score(lives):
    score_surface = secondaryFont.render("lives: "+str(lives), False, (255,255,255))
    score_rect =  score_surface.get_rect(topright=(WIDTH,0))
    screen.blit(score_surface, score_rect)

def reset_game(lives, game_active, try_again):
    if lives <= 0:
        game_active = False
        try_again = True
        lives = 30
        craft.empty()
        craft.add(MainCraft(5))
        invaders_group.empty()
        lasers_group.empty()
    return lives, game_active, try_again


explosion_sound = pygame.mixer.Sound('assets/audio/explosion.wav')
explosion_sound.set_volume(0.1)
#main game
WIDTH, HEIGHT = 750, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Invaders Clone')

#starting game message
mainFont = pygame.font.Font('assets/font/Pixeltype.ttf', 100)
game_starting_msg = mainFont.render('Press any key to begin...', False, (255, 255, 255))
game_starting_rect = game_starting_msg.get_rect(center=(375, 375))

#display score
secondaryFont = pygame.font.Font('assets/font/Pixeltype.ttf', 50)

try_again_surface = secondaryFont.render('Press any key to try again', False, (255,255,255))
try_again_rect = try_again_surface.get_rect(center=(375, 325))
#background stuff
background_image = pygame.image.load(os.path.join('assets', 'background-black.png')).convert()
background_image = pygame.transform.scale(background_image, (750, 750))

clock = pygame.time.Clock()
FramePerSecond = 60

craft = pygame.sprite.GroupSingle()
craft.add(MainCraft(5))

lasers_group = pygame.sprite.Group()

invaders_group = pygame.sprite.Group()
invaders_timer = pygame.USEREVENT + 1
pygame.time.set_timer(invaders_timer, 5000)
invader_shoot_timer = 0

explosion_group = pygame.sprite.Group()

game_active = False
try_again = False

while True:
    for event in pygame.event.get():
        current_time = pygame.time.get_ticks()
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:

            if event.type == invaders_timer:
                fromY, toY = generate_enemies(fromY, toY)

            if (current_time-invader_shoot_timer)>= randint(500, 1200) and invaders_group.sprites():
                invader_shoot_timer = current_time
                random_invader  = choice(invaders_group.sprites())
                if random_invader.rect.top > 0:
                      lasers_group.add(Laser(random_invader.invader_type, random_invader.rect.x,random_invader.rect.y))

        if not game_active and try_again and event.type == pygame.KEYDOWN:
            game_active = True
            try_again = False

        elif not game_active and event.type == pygame.KEYDOWN:
            game_active = True

    screen.blit(background_image, (0,0))
    if game_active:
        explosion_group.update()
        explosion_group.draw(screen)

        craft.sprite.lasers.draw(screen)
        lasers_group.update()
        lasers_group.draw(screen)

        craft.update()
        craft.draw(screen)
        invaders_group.update()
        invaders_group.draw(screen)


        collision()
        display_score(lives)
        lives, game_active, try_again = reset_game(lives, game_active, try_again)
    if  not game_active and try_again:
        screen.blit(try_again_surface, try_again_rect)
    elif not game_active:
        screen.blit(game_starting_msg, game_starting_rect)


    pygame.display.update()
    clock.tick(FramePerSecond)
