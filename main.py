from Imports import *
pygame.init()

#constants
MIN_SHOOT_TIME, MAX_SHOOT_TIME = 500,1200
WIDTH, HEIGHT = 750, 650
CRAFT_SPEED = 10
MAX_Y_POS = [500, 400]
INITIAL_INVADER_TIMER = 5000
#end constants

#variables initial values
lives = 5
alive_invaders = 15
level = 1
level_up = False #used later to give the player the choice to either pass to another level or not
increasingFactor = 1.0
laser_speed = 10

#functions

#clear everything in game
def reset_game():
    craft.empty()
    craft.add(MainCraft(CRAFT_SPEED))
    invaders_group.empty()
    lasers_group.empty()

#when he loses, we give the player the option to try again from the latest level he's reached
def check_try_again():
    global game_active, try_again,lives
    if lives<=0:
        game_active = False
        try_again = True
        lives = 5
        reset_game()

#level up
def change_level():
    global lives, alive_invaders, level, increasingFactor, laser_speed
    if alive_invaders <= 0:
        level += 1
        increasingFactor += 0.2 #In this and the next line of code I'm just making things complex Idk why
        alive_invaders = int(15*increasingFactor) #Increase The number of "To be killed invaders" in order to pass to next level
        reset_game()
        lives = 5
        laser_speed += 2
        craft.sprite.laser_speed += 2
        return True
    return False

#check for collision between different types of sprite in handles remaining craft health and alive invaders
def collision():
    global alive_invaders, lives
    craftLaserCollision = pygame.sprite.spritecollide(craft.sprite, lasers_group, True, pygame.sprite.collide_mask)
    craftInvaderCollision = pygame.sprite.spritecollide(craft.sprite, invaders_group, True, pygame.sprite.collide_mask)

    if craftLaserCollision:
        lives -=1

    if craftInvaderCollision:
        lives -= 2
        alive_invaders -= 1
        #prevent negative width health bar
        if lives < 0:
            lives = 0
        explosion_stuff(craft.sprite.rect.x, craft.sprite.rect.y, screen)

    if craft.sprite.lasers:
        for laser in craft.sprite.lasers:
           if pygame.sprite.spritecollide(laser, invaders_group, True, pygame.sprite.collide_mask):
               explosion_stuff(laser.rect.x, laser.rect.y, screen)
               laser.destroy_laser()
               alive_invaders -= 1

    if invaders_group.sprites():
        for invader in invaders_group.sprites():
            if invader.rect.top>= 650:
                lives -= 1

"""Making things complex once more
   generate enemies at a different vertical position
"""
fromY = 100
toY = 0
def generate_enemies(fromY, toY):
    invaders_group.add(Invader(randint( 50, 150), randint(-fromY, -toY)))
    invaders_group.add(Invader(randint(250, 350), randint(-fromY, -toY)))
    invaders_group.add(Invader(randint(400, 600), randint(-fromY, -toY)))
    fromY += 100
    toY += 100
    if fromY%MAX_Y_POS[0]:
        fromY= 100
    if toY%MAX_Y_POS[1]:
        toY = 0
    return fromY, toY


#display health bar
def health_bar(x,y,lives):
    y += 30
    red_surface = pygame.Surface([100,10])
    red_rect = red_surface.get_rect(bottomleft = (x,y))
    green_surface = pygame.Surface([lives*20,10])
    green_rect = red_surface.get_rect(bottomleft=(x,y))
    red_surface.fill((255,0,0))
    green_surface.fill((0,255,0))
    screen.blit(red_surface, red_rect)
    screen.blit(green_surface, green_rect)

#explosion effect for mainLaser collision with invaders
def explosion_stuff(x,y, screen):
    explosion_group.add(Explosion(x, y, screen))
    explosion_sound.play()

def display_score(lives):
    score_surface = secondaryFont.render("lives: "+str(lives), False, (255,255,255))
    score_rect =  score_surface.get_rect(topright=(WIDTH,0))
    screen.blit(score_surface, score_rect)

def display_level(level):
    level_surface = secondaryFont.render('level: '+str(level), False, (255,255,255))
    level_rect = level_surface.get_rect(topleft=(0,0))
    screen.blit(level_surface, level_rect)

def display_levelup(level):
    level_passed_surface1 = secondaryFont.render("Congrats, you've passed level "+str(level)+" !!", False, (255,255,255))
    level_passed_surface2 = secondaryFont.render("Press the  Space key to enter level "+str(level+1), False, (255,255,255))
    level_passed_rect1 = level_passed_surface1.get_rect(center=(375, 325))
    level_passed_rect2 = level_passed_surface2.get_rect(center=(357, 375))
    screen.blit(level_passed_surface1, level_passed_rect1)
    screen.blit(level_passed_surface2, level_passed_rect2)


explosion_sound = pygame.mixer.Sound('assets/audio/explosion.wav')
explosion_sound.set_volume(0.1)

#main game
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
FramePerSecond = 30

craft = pygame.sprite.GroupSingle()
craft.add(MainCraft(CRAFT_SPEED))

lasers_group = pygame.sprite.Group()

invaders_group = pygame.sprite.Group()
invaders_timer = pygame.USEREVENT + 1
pygame.time.set_timer(invaders_timer, INITIAL_INVADER_TIMER)
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

            if (current_time-invader_shoot_timer)>= randint(MIN_SHOOT_TIME, MAX_SHOOT_TIME ) and invaders_group.sprites():
                invader_shoot_timer = current_time
                random_invader  = choice(invaders_group.sprites())
                if random_invader.rect.top > 0:
                      lasers_group.add(Laser(random_invader.invader_type, random_invader.rect.center[0],random_invader.rect.center[1], laser_speed))

        if level_up and event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            level_up= False

        if not game_active and try_again and event.type == pygame.KEYDOWN:
            game_active = True
            try_again = False

        elif not game_active and event.type == pygame.KEYDOWN:
            game_active = True

    screen.blit(background_image, (0,0))
    if level_up:
        display_levelup(level)
    elif  game_active:
        display_score(lives)
        display_level(level)

        craft.sprite.lasers.draw(screen)
        lasers_group.update()
        lasers_group.draw(screen)

        craft.update()
        craft.draw(screen)

        invaders_group.update()
        invaders_group.draw(screen)

        explosion_group.update()
        explosion_group.draw(screen)

        collision()

        check_try_again()

        level_up = change_level()

        health_bar(craft.sprite.rect.bottomleft[0], craft.sprite.rect.bottomleft[1], lives )

    if  not game_active and try_again:
        screen.blit(try_again_surface, try_again_rect)
    elif not game_active:
        screen.blit(game_starting_msg, game_starting_rect)


    pygame.display.update()
    clock.tick(FramePerSecond)

