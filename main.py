import pygame, sys, random

sWidth, sHeight = 576, 1024


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + sWidth, 900))


def draw_bg():
    screen.blit(bg_surface, (bg_x_pos, 0))
    screen.blit(bg_surface, (bg_x_pos + sWidth, 0))


def draw_night():
    fade = int((score * 4) % 1024)
    if 256 < fade < 511:
        bg_surface_night.set_alpha(fade - 256)
    elif 767 < fade < 1024:
        bg_surface_night.set_alpha(1023 - fade)
    elif fade > 256:
        bg_surface_night.set_alpha(255)
    else:
        bg_surface_night.set_alpha(0)

    screen.blit(bg_surface_night, (bg_x_pos, 0))
    screen.blit(bg_surface_night, (bg_x_pos + sWidth, 0))


def create_laser(color):
    return red_laser.get_rect(midtop=(700, -100))


def create_pipe():
    global last_gap
    if pipe_list:
        last_pipe_height = pipe_list[-2].top
        height = random.randint(max(400, last_pipe_height - 100), min(last_pipe_height + 100, 800))
        gap = random.randint(max(GAP_SIZE[0], last_gap - 50), min(GAP_SIZE[1], last_gap + 50))
        last_gap = gap
        bottom_pipe = pipe_surface.get_rect(midtop=(700, height))
        top_pipe = pipe_surface.get_rect(midbottom=(700, height - gap))
        return bottom_pipe, top_pipe
    else:
        height = random.choice(pipe_starting_height)
        bottom_pipe = pipe_surface.get_rect(midtop=(700, height))
        top_pipe = pipe_surface.get_rect(midbottom=(700, height - 300))
        return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
        if pipe.centerx < - 50:
            pipes.pop(pipes.index(pipe))
    return pipes


def move_lasers(lasers):
    for laser in lasers:
        laser.centerx -= 3
        if laser.centerx < - 50:
            lasers.pop(lasers.index(laser))
    return lasers


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def draw_lasers(lasers):
    for laser in lasers:
        screen.blit(red_laser, laser)

def night_pipes(pipes):
    global score
    fade = (score * 4) % 1024
    if 256 < fade < 511:
        red_pipe_surface.set_alpha(fade - 256)
    elif 767 < fade < 1023:
        red_pipe_surface.set_alpha(1023 - fade)
    elif fade > 256:
        red_pipe_surface.set_alpha(255)
    else:
        red_pipe_surface.set_alpha(0)

    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(red_pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(red_pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        death_sound.play()
        return True
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return True
    return False


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    global score
    global high_score
    if game_state == 'main_game':
        score_surface = game_font.render('Score: ' + str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)
    else:
        high_score = max(high_score, score)
        score_surface = game_font.render('Score: ' + str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

        score_surface = game_font.render('High Score: ' + str(int(high_score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 850))
        screen.blit(score_surface, score_rect)


def pipe_score_check():
    global score, can_score
    if not pipe_list:
        return
    for pipe in pipe_list:
        if 95 < pipe.centerx < 105 and can_score:
            score += 1
            can_score = False
        if pipe.centerx < 0:
            can_score = True


def score_based_upgrades():
    global score, bg_surface, pipe_surface
    if 50 < score < 51:
        bg_surface = pygame.image.load('assets/background-night.png').convert()
        bg_surface = pygame.transform.scale2x(bg_surface)

        pipe_surface = pygame.image.load('assets/pipe-red.png')
        pipe_surface = pygame.transform.scale2x(pipe_surface)


pygame.mixer.pre_init()
pygame.init()
screen = pygame.display.set_mode((sWidth, sHeight))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf', 40)

# Game Variables
gravity = 0.15
bird_movement = -4
game_active = True
score = 0
high_score = 0
can_score = True
last_gap = 300
GAP_SIZE = [250, 500]
laser_color = random.randint(0, 2)
bird_color = 0

controls_surface = pygame.transform.scale2x(pygame.image.load('assets/base_controls.png').convert_alpha())

bg_surface = pygame.transform.scale2x(pygame.image.load('assets/background-day.png').convert())
bg_surface_night = pygame.transform.scale2x(pygame.image.load('assets/background-night.png').convert_alpha())
bg_x_pos = 0

floor_surface = pygame.transform.scale2x(pygame.image.load('assets/base.png').convert())
floor_x_pos = 0

laser_list = []
red_laser = pygame.image.load('assets/laser.png').convert_alpha()
laser_types = [red_laser]

bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 50)

pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
red_pipe_surface = pygame.image.load('assets/pipe-green-night.png')
red_pipe_surface = pygame.transform.scale2x(red_pipe_surface)

SPAWNLASER = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWNLASER, 1200)

pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 300)
pipe_starting_height = [400, 600, 800]

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(288, 512))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 300

while True:
    keys = pygame.key.get_pressed()

    if game_active:
        if keys[pygame.K_SPACE]:
            bird_movement -= .3

        if keys[pygame.K_q]:
            bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
            bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
            bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
            bird_frames = [bird_downflap, bird_midflap, bird_upflap]
            bird_color = 'blue'

        if keys[pygame.K_w]:
            bird_downflap = pygame.transform.scale2x(
                pygame.image.load('assets/yellowbird-downflap.png').convert_alpha())
            bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png').convert_alpha())
            bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())
            bird_frames = [bird_downflap, bird_midflap, bird_upflap]
            bird_color = 'yellow'

        if keys[pygame.K_e]:
            bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/redbird-downflap.png').convert_alpha())
            bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/redbird-midflap.png').convert_alpha())
            bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/redbird-upflap.png').convert_alpha())
            bird_frames = [bird_downflap, bird_midflap, bird_upflap]
            bird_color = 'red'

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not game_active:
            game_active = True
            pipe_list.clear()
            laser_list.clear()
            bird_rect.center = (100, 512)
            bird_movement = -4
            score = 0
            score_sound_countdown = 300
            bg_surface_night.set_alpha(0)

        if event.type == SPAWNPIPE and game_active:
            print('pipe')
            pipe_list.extend(create_pipe())

        if event.type == SPAWNLASER and game_active:
            print('laser')
            laser_list.append(create_laser(laser_color))

        if event.type == BIRDFLAP and keys[pygame.K_SPACE]:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()
        else:
            bird_index = 0
            bird_surface, bird_rect = bird_animation()
    # BG
    bg_x_pos -= 1
    draw_bg()
    draw_night()

    if bg_x_pos <= -576:
        bg_x_pos = 0

    if game_active == True:
        # Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = not check_collision(pipe_list)

        # Lasers
        laser_list = move_lasers(laser_list)
        draw_lasers(laser_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        night_pipes(pipe_list)


        # Score
        score_display('main_game')
        pipe_score_check()
        score += .01
        # score_based_upgrades()

    else:
        screen.blit(game_over_surface, game_over_rect)
        score_display('game_over')

    # Floor
    floor_x_pos -= 3
    draw_floor()
    # screen.blit(controls_surface, (0, 900))

    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
