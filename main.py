import math
import random
import time
import pygame
pygame.init()
WIDTH , HEIGHT = 800 , 600
WIN = pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption('Aim Trainer')

TARGET_INCREMENT = 400
TARGET_EVENT = pygame.USEREVENT

TARGET_PADDING = 30
BG_COLORS = (0,25,40)
LIVES = 3
TOP_BAR_HEIGHT = 50

LABEL_FONT = pygame.font.SysFont("comicscans", 24)


class Target:
    max_size = 30
    GROWTH_RATE = 0.2
    color = 'red'
    second_color = 'white'

    def __init__(self, x , y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True

    def update(self):
        if self.size + self.GROWTH_RATE >= self.max_size:
            self.grow =False
        
        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE


    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y),self.size)
        pygame.draw.circle(win, self.second_color, (self.x, self.y),self.size * 0.8)
        pygame.draw.circle(win, self.color, (self.x, self.y),self.size * 0.6)
        pygame.draw.circle(win, self.second_color, (self.x, self.y),self.size * 0.4)
    
    def collide(self , x , y):
        dis = math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
        return dis <= self.size

def draw(win , targets):
    win.fill(BG_COLORS)
    for target in targets:
        target.draw(win)

    

def formatted_time(secs):
    mili = math.floor(int(secs *1000 % 1000)/ 1000)
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)

    return f'{minutes: 02d}:{seconds:02d}.{mili}'

def draw_top_bar(win, elapsed_time, target_pressed, misses):
    pygame.draw.rect(win, "grey", (0,0, WIDTH, TOP_BAR_HEIGHT))
    time_label = LABEL_FONT.render(f"time: {formatted_time(elapsed_time)}", 1, "black")

    speed = round(target_pressed/ elapsed_time, 1)
    speed_label = LABEL_FONT.render(f'speed: {speed} t/s', 1 , 'black')
    hitts_label = LABEL_FONT.render(f'hits: {target_pressed}', 1, "black")
    lives_label = LABEL_FONT.render(f'lives: {LIVES - misses}', 1, "black")

    win.blit(time_label, (5 , 5))
    win.blit(speed_label, (200 , 5))
    win.blit(hitts_label, (450 , 5))
    win.blit(lives_label, (650 , 5))

def end_screen(win , elapsed_time, targets_pressed, clicks):
    win.fill(BG_COLORS)
    time_label = LABEL_FONT.render(f"time: {formatted_time(elapsed_time)}", 1, "white")

    speed = round(targets_pressed/ elapsed_time, 1)
    speed_label = LABEL_FONT.render(f'speed: {speed} t/s', 1 , 'white')

    hitts_label = LABEL_FONT.render(f'hits: {targets_pressed}', 1, "white")


    accuracy = round(targets_pressed / clicks * 100, 1) 
    accuracy_label = LABEL_FONT.render(f'Accuracy: {accuracy}%', 1, "white")

    win.blit(time_label, (get_middle(time_label) , 100))
    win.blit(speed_label, (get_middle(speed_label) , 200))
    win.blit(hitts_label, (get_middle(hitts_label) , 300))
    win.blit(accuracy_label, (get_middle(accuracy_label) , 400))

    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()


def get_middle(surface):
    return WIDTH / 2 - surface.get_width() / 2


def main():
    run = True
    targets = []
    clock = pygame.time.Clock()

    target_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()
    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

    while run:
        clock.tick(60)
        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING , WIDTH - TARGET_PADDING)
                y = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT , HEIGHT - TARGET_PADDING)
                target = Target(x, y)
                targets.append(target)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1

        for target in targets:
            target.update()

            if target.size <= 0:
                targets.remove(target)
                misses += 1

            if click and target.collide(*mouse_pos):
                targets.remove(target)
                
                target_pressed += 1

            if misses >= LIVES:
                end_screen(WIN, elapsed_time, target_pressed, clicks)

               
        draw(WIN, targets)
        draw_top_bar(WIN, elapsed_time, target_pressed, misses)
        pygame.display.update()


    pygame.quit()



if __name__ == '__main__':
    main()

