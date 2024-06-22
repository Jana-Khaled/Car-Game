import pygame
from pygame.locals import *
import random

pygame.init()

# screen properties
width = 500
height = 500
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)

#background colours, lane and stroke sizes
gray=(100,100,100)
purple=(132, 91, 171)
red=(200,0,0)
white=(255,255,255)

road_width = 300
stroke_width = 10
stroke_height = 50

# lane coordinates
left_lane = 150
center_lane = 250
right_lane = 350
lanes = [left_lane, center_lane, right_lane]

# road and edge strokes positioning
road = (100, 0, road_width, height)
left_edge_stroke = (95, 0, stroke_width, height)
right_edge_stroke = (395, 0, stroke_width, height)

# animating of the lane strokes
lane_stroke_move_y = 0

# starting coordinates
player_x = 250
player_y = 400


# game and frame settings
clock = pygame.time.Clock()
fps = 120
gameover = False
gamecomplete=False
speed = 2
score = 0
level=0


class Car(pygame.sprite.Sprite):
    
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        # scale the image down so it's not wider than the lane
        image_scale = 45 / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (new_width, new_height))
        
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        
class PlayerVehicle(Car):
    
    def __init__(self, x, y):
        image = pygame.image.load('images/Black_viper.png')
        super().__init__(image, x, y)
        

player_group = pygame.sprite.Group()
vehicle_group = pygame.sprite.Group()

# player's car
player = PlayerVehicle(player_x, player_y)
player_group.add(player)

# other cars images
image_filenames = ['truck.png', 'Police.png', 'taxi.png','Car.png','Audi.png','Mini_truck.png']
vehicle_images = []
for image_filename in image_filenames:
    image = pygame.image.load('images/' + image_filename)
    vehicle_images.append(image)
    
# crash image
crash = pygame.image.load('images/crash.png')
crash_rect = crash.get_rect()

confetti= pygame.image.load('images/confetti.png')
confetti_rect= confetti.get_rect()
confetti_rect.center = (width / 2, 350)


# main game loop
running = True
while running:
    
    clock.tick(fps)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

                
            
        # move the player's car using the left/right arrow keys
        if event.type == KEYDOWN:
            
            if event.key == K_LEFT and player.rect.center[0] > left_lane:
                player.rect.x -= 100
            elif event.key == K_RIGHT and player.rect.center[0] < right_lane:
                player.rect.x += 100
                
            # check if there's a collision after changing lanes
            for vehicle in vehicle_group:
                if pygame.sprite.collide_rect(player, vehicle):
                    
                    gameover = True
                    
                    # position of the crash image
                    if event.key == K_LEFT:
                        player.rect.left = vehicle.rect.right
                        crash_rect.center = [player.rect.left, (player.rect.center[1] + vehicle.rect.center[1]) / 2]
                    elif event.key == K_RIGHT:
                        player.rect.right = vehicle.rect.left
                        crash_rect.center = [player.rect.right, (player.rect.center[1] + vehicle.rect.center[1]) / 2]
            
            
    # draw the background and car
    screen.fill(purple)
    
    pygame.draw.rect(screen, gray, road)
    
    pygame.draw.rect(screen, white, left_edge_stroke)
    pygame.draw.rect(screen, white, right_edge_stroke)
    
    lane_stroke_move_y += speed * 2
    if lane_stroke_move_y >= stroke_height * 2:
        lane_stroke_move_y = 0
    for y in range(stroke_height * -2, height, stroke_height * 2):
        pygame.draw.rect(screen, white, (left_lane + 45, y + lane_stroke_move_y, stroke_width, stroke_height))
        pygame.draw.rect(screen, white, (center_lane + 45, y + lane_stroke_move_y, stroke_width, stroke_height))
        
    player_group.draw(screen)
    
    # add an obstacle car
    if len(vehicle_group) < 2:
        
        # make sure there is a gap between cars
        add_vehicle = True
        for vehicle in vehicle_group:
            if vehicle.rect.top < vehicle.rect.height * 1.5:
                add_vehicle = False
                
        if add_vehicle:
            
            # random lane
            lane = random.choice(lanes)
            
            # random car image
            image = random.choice(vehicle_images)
            vehicle = Car(image, lane, height / -2)
            vehicle_group.add(vehicle)
    
    # make the cars move
    for vehicle in vehicle_group:
        vehicle.rect.y += speed
        
        # remove car once we pass it
        if vehicle.rect.top >= height:
            vehicle.kill()
            
            score += 1
            
            # speeding after determined score and leveling up
           
            if score==30:
                gamecomplete=True
                pygame.draw.rect(screen,(5, 110, 35), (0, 50, width, 100))
                
                #game complete screen
                font = pygame.font.Font(pygame.font.get_default_font(), 20)
                text = font.render('YOU PASSED ALL THE LEVELS CONGRATS!!', True, white)
                text_rect = text.get_rect()
                text_rect.center = (width / 2, 100)
                screen.blit(text, text_rect)
                screen.blit(confetti, confetti_rect)
                vehicle_group.empty()
                
            elif score==5:
                speed += 1
                
            elif score==10:
                level+=1
                speed += 1.5
               
            elif score==20:
                speed += 2

        # show a message when leveling up
        if score==5:
            font = pygame.font.Font(pygame.font.get_default_font(), 22)
            text = font.render('LEVEL 2', True, white)
            text_rect = text.get_rect()
            text_rect.center = (250,70)
            screen.blit(text, text_rect)

        elif score==10:
            font = pygame.font.Font(pygame.font.get_default_font(), 22)
            text = font.render('LEVEL 3', True, white)
            text_rect = text.get_rect()
            text_rect.center = (250,70)
            screen.blit(text, text_rect)

        elif score==20:
            font = pygame.font.Font(pygame.font.get_default_font(), 22)
            text = font.render('LEVEL 4', True, white)
            text_rect = text.get_rect()
            text_rect.center = (250,70)
            screen.blit(text, text_rect)
           

           

    vehicle_group.draw(screen)
    
    # score
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render('Score: ' + str(score), True, white)
    text_rect = text.get_rect()
    text_rect.center = (50, 400)
    screen.blit(text, text_rect)
    
    # check if there's collision
    if pygame.sprite.spritecollide(player, vehicle_group, True):
        gameover = True
        crash_rect.center = [player.rect.center[0], player.rect.top]
            


            
    # game over screen
    if gameover:
        screen.blit(crash, crash_rect)
        
        pygame.draw.rect(screen,(219, 18, 18), (0, 50, width, 100))
        
        font = pygame.font.Font(pygame.font.get_default_font(), 20)
        text = font.render('GAME OVER YOU CRASHED', True, white)
        text_rect = text.get_rect()
        text_rect.center = (width / 2, 100)
        screen.blit(text, text_rect)
       

            
    pygame.display.update()

    while gameover:
        
        clock.tick(fps)
        
        for event in pygame.event.get():
            
            if event.type == QUIT:
                gameover = False
                running = False


    while gamecomplete:
        
        clock.tick(fps)
        
        for event in pygame.event.get():
            
            if event.type == QUIT:
                gamecomplete = False
                running = False
                
            
pygame.quit()
