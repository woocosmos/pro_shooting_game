# http://suanlab.com/assets/slectures/python/PyShooting.pdf
# https://www.youtube.com/watch?v=W92RjjptAsM

import random
from time import sleep
import sys
import numpy as np
from os import path


import pygame
from pygame.locals import *

# 절대경로
file_dir = path.join(path.dirname(__file__))+'/sources'
print(file_dir)

# 전체 윈도우 크기
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 640

# 색깔
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (250, 100, 50)
RED = (250, 50, 50)

# 프레임 / SEC
FPS = 60

# 비행기
class Fighter(pygame.sprite.Sprite):
    def __init__(self):
        super(Fighter, self).__init__()
        self.image = pygame.image.load(path.join(file_dir, 'fighter.png'))
        self.rect = self.image.get_rect()
        self.rect.x = int(WINDOW_WIDTH / 2)
        self.rect.y = WINDOW_HEIGHT - self.rect.height
        self.dx = 0
        self.dy = 0
        self.shoot_delay = 50
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.rect.x < 0 or self.rect.x + self.rect.width > WINDOW_WIDTH:
            self.rect.x -= self.dx
        if self.rect.y < 0 or self.rect.y + self.rect.height > WINDOW_HEIGHT:
            self.rect.y -= self.dy

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite

    def bomb(self):
        return Bomb(self)


# 미사일
class Missile(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed):
        super(Missile, self).__init__()
        self.image = pygame.image.load(path.join(file_dir, 'missile.png'))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = speed
        self.sound = pygame.mixer.Sound(path.join(file_dir, 'missile.wav'))
        self.shoot_delay = 50
        self.last_shot = pygame.time.get_ticks()

    def launch(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_launchshot = now
        self.sound.play()

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y + self.rect.height < 0:
            self.kill()

    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite

# 필살기
class Bomb(pygame.sprite.Sprite):
    def __init__(self, fighter):
        super().__init__()
        self.image = None
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.radius = 20
        self.radiusIncrement = 4
        self.rect = fighter.rect
        self.sound = pygame.mixer.Sound('./sources/bomb.ogg')

    def update(self):
        self.sound.play()
        self.radius += self.radiusIncrement
        pygame.draw.circle(
            pygame.display.get_surface(),
            pygame.Color(250, 50, 50, 128),
            self.rect.center, self.radius, 3)
        if (self.rect.center[1] - self.radius <= self.area.top
            and self.rect.center[1] + self.radius >= self.area.bottom
            and self.rect.center[0] - self.radius <= self.area.left
                and self.rect.center[0] + self.radius >= self.area.right):
            self.kill()

    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite

# 필살기 아이템
class Bomb_item(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed):
        super(Bomb_item, self).__init__()
        self.image = pygame.image.load(path.join(file_dir, 'bomb.png'))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

    def out_of_screen(self):
        if self.rect.y > WINDOW_HEIGHT:
            return True

    def collide(self, sprite):
        if pygame.sprite.collide_rect(self, sprite):
            pygame.mixer.Sound(path.join(file_dir, 'get.wav')).play()
            return sprite

# 운석
class Rock(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed):
        super(Rock, self).__init__()
        rock_images = ('rock01.png', 'rock02.png', 'rock09.png', 'rock10.png')
        self.image = pygame.image.load((path.join(file_dir, random.choice(rock_images))))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

    def out_of_screen(self):
        if self.rect.y > WINDOW_HEIGHT:
            return True

 # 선물 박스
class Butterfly(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed):
        super(Butterfly, self).__init__()
        self.image = pygame.image.load(path.join(file_dir, 'gift01.png'))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = speed
        self.sound = pygame.mixer.Sound(path.join(file_dir, 'change1.wav'))

    def update(self):
        self.rect.y += self.speed

    def out_of_screen(self):
        if self.rect.y > WINDOW_HEIGHT:
            return True

    def change_color(self):
        self.image = pygame.image.load(path.join(file_dir, 'gift02.png'))
        self.sound.play()

 # 추천앱
class Recommendation(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed):
        super(Recommendation, self).__init__()
        recommendations = ['recommend01.png', 'recommend02.png', 'recommend03.png', 'recommend04.png', 'recommend05.png',
                           'recommend06.png', 'recommend07.png', 'recommend08.png', 'recommend09.png', 'recommend10.png']
        self.image = pygame.image.load(path.join(file_dir, random.choice((recommendations))))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = speed
        pygame.mixer.Sound(path.join(file_dir, 'change2.wav')).play()

    def update(self):
        self.rect.y += self.speed

    def out_of_screen(self):
        if self.rect.y > WINDOW_HEIGHT:
            return True

    def collide(self, sprite):
        if pygame.sprite.collide_rect(self, sprite):
            pygame.mixer.Sound(path.join(file_dir, 'get.wav')).play()
            return sprite

# 텍스트 띄우기
def draw_text(text, font, surface, x, y, main_color):
    text_obj = font.render(text, True, main_color)
    text_rect = text_obj.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    surface.blit(text_obj, text_rect)

# 폭발 이미지&소리
def occur_explosion(surface, x, y):
    explosion_image = pygame.image.load(path.join(file_dir, 'explosion.png'))
    explosion_rect = explosion_image.get_rect()
    explosion_rect.x = x
    explosion_rect.y = y
    surface.blit(explosion_image, explosion_rect)

    explosion_sound = pygame.mixer.Sound(path.join(file_dir, 'explosion.wav'))
    explosion_sound.play()

# 정지
def pause():
    image = pygame.Surface([WINDOW_WIDTH, WINDOW_HEIGHT])
    image.fill(BLACK)
    image.set_alpha(100)

    screen.blit(image, (0, 0))

    x = WINDOW_WIDTH / 2
    y = WINDOW_HEIGHT // 2
    font_40 = pygame.font.Font(path.join(file_dir, 'DungGeunMo.ttf'), 40)
    font_70 = pygame.font.Font(path.join(file_dir, 'DungGeunMo.ttf'), 70)


    draw_text('PAUSE', font_70, screen,  x, y-100, RED)
    draw_text('게임 재개 ESC', font_40,screen,  x, y, WHITE)
    draw_text('메인으로 돌아가기 Q', font_40,screen,  x, y+50, WHITE)
    pygame.mixer.music.set_volume(0.1)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.mixer.music.set_volume(1)
                    return True
                elif event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.set_volume(1)
                    return False


# 게임에서 반복되는 부분 처리
def game_loop():
    global final, score
    default_font = pygame.font.Font(path.join(file_dir, 'DungGeunMo.ttf'), 28)
    background_image = pygame.image.load(path.join(file_dir, 'background1.png'))
    gameover_sound = pygame.mixer.Sound(path.join(file_dir, 'gameover.mp3'))
    pygame.mixer.music.load(path.join(file_dir, 'music.wav'))
    pygame.mixer.music.play(-1)
    fps_clock = pygame.time.Clock()
    change_sound = pygame.mixer.Sound(path.join(file_dir, 'change2.wav'))
    get_sound = pygame.mixer.Sound(path.join(file_dir, 'get.wav'))

    fighter = Fighter()
    missiles = pygame.sprite.Group()
    rocks = pygame.sprite.Group()
    butterflies = pygame.sprite.Group()
    items = pygame.sprite.Group()
    recommendations = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    alldrawings = pygame.sprite.Group()

    occur_prob = 60
    shot_count = 0
    count_missed = 0

    occur_prob2 = 600
    shot_count2 = 0
    count_missed2 = 0

    score = 0
    bomb_held = 3

    timing = False
    BUTTERFLY = pygame.USEREVENT+1
    pygame.time.set_timer(BUTTERFLY, 3000)

    bomb_timing = False
    BOMB = pygame.USEREVENT + 1
    pygame.time.set_timer(BOMB, 10000)

    count = 0
    takes = []
    final = []

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    fighter.dx -= 6
                elif event.key == pygame.K_RIGHT:
                    fighter.dx += 6
                elif event.key == pygame.K_UP:
                    fighter.dy -= 6
                elif event.key == pygame.K_DOWN:
                    fighter.dy += 6
                elif event.key == pygame.K_SPACE:
                    missile = Missile(fighter.rect.centerx, fighter.rect.y, 10)
                    missile.launch()
                    missiles.add(missile)
                elif event.key == pygame.K_b:
                    if bomb_held > 0:
                        newBomb = fighter.bomb()
                        newBomb.add(bombs, alldrawings)
                        bomb_held -= 1
                elif event.key == pygame.K_ESCAPE:
                    # 게임 재개하면 저절로 움직이기에 추가
                    fighter.dx = 0
                    fighter.dy = 0

                    if pause():
                        pygame.display.update()
                        pygame.mixer.music.stop()
                        return 'game_menu'


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighter.dx = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    fighter.dy = 0

            if event.type == BUTTERFLY:
                timing = True

            if event.type == BOMB:
                bomb_timing = True

        # 게임화면 배경
        screen.blit(background_image, background_image.get_rect())

        # 운석 등장
        occur_of_rocks = 1 + int(shot_count / 150) # 점수에 따라서 점점 돌을 많이 등장
        min_rock_speed = 1 + int(shot_count / 100) # 운석의 최소 스피드
        max_rock_speed = 1 + int(shot_count / 50) # 운석의 최대 스피드

        if random.randint(1, occur_prob) == 1:
            for i in range(occur_of_rocks):
                speed = random.randint(min_rock_speed, max_rock_speed)
                rock = Rock(random.randint(0, WINDOW_WIDTH - 30), 0, speed)
                rocks.add(rock)

        # 나비 등장
        min_butterfly_speed = 1 + int(shot_count2 / 200)
        max_butterfly_speed = 1 + int(shot_count2 / 100)

        if timing:
            speed = random.randint(min_butterfly_speed, max_butterfly_speed)
            butterfly = Butterfly(random.randint(0, WINDOW_WIDTH - 30), 0, speed)
            butterflies.add(butterfly)
            timing = False

        # 폭탄 아이템 등장
        if bomb_timing:
            speed = random.randint(min_butterfly_speed, max_butterfly_speed)
            item = Bomb_item(random.randint(0, WINDOW_WIDTH - 30), 0, speed)
            items.add(item)
            bomb_timing = False

        draw_text('MY SCORE {}'.format(score), default_font, screen, 380, 20, WHITE)
        draw_text('나의 취향', default_font, screen, 80, 20, WHITE)

        # 필살기 충돌
        for bomb in bombs:
            try:
                if pygame.sprite.collide_circle(bomb, rock):
                    rock.kill()
                    occur_explosion(screen, rock.rect.x, rock.rect.y)
            except:
                pass

        # 미사일 충돌
        for missile in missiles:
            rock = missile.collide(rocks) # 미사일과 운석의 충돌을 반환
            butterfly = missile.collide(butterflies)
            recommendation = missile.collide(recommendations)

            if rock: # 충돌시
                missile.kill()
                rock.kill()
                occur_explosion(screen, rock.rect.x, rock.rect.y)
                shot_count += 1 # 파괴시 샷카운트
                score += 100

            if butterfly:
                count += 1
                if count == 1:
                    missile.kill()
                    butterfly.change_color()
                elif count == 2:
                    missile.kill()
                    butterfly.kill()
                    recommendation = Recommendation(butterfly.rect.x, butterfly.rect.y, speed)
                    recommendations.add(recommendation)
                    count = 0

            if recommendation:
                missile.kill()

        # 운석 관리
        for rock in rocks:
            if rock.out_of_screen():
                rock.kill()
                count_missed += 1

        # 나비 관리
        for butterfly in butterflies:
            if butterfly.out_of_screen():
                butterfly.kill()

        # 폭탄 관리
        for item in items:
            powerup = item.collide(fighter)

            if item.out_of_screen():
                item.kill()

            if powerup:
                item.kill()
                bomb_held += 1
                bomb_held = min(bomb_held, 5)

        # 폭탄 적립
        temp = pygame.image.load(path.join(file_dir, 'bomb.png'))

        if bomb_held == 5:
            screen.blit(temp, [280, 40])
            screen.blit(temp, [320, 40])
            screen.blit(temp, [360, 40])
            screen.blit(temp, [400, 40])
            screen.blit(temp, [440, 40])
        elif bomb_held == 4:
            screen.blit(temp, [360, 40])
            screen.blit(temp, [320, 40])
            screen.blit(temp, [400, 40])
            screen.blit(temp, [440, 40])
        elif bomb_held == 3:
            screen.blit(temp, [360, 40])
            screen.blit(temp, [400, 40])
            screen.blit(temp, [440, 40])
        elif bomb_held == 2:
            screen.blit(temp, [400, 40])
            screen.blit(temp, [440, 40])
        elif bomb_held == 1:
            screen.blit(temp, [440, 40])


        # 추천앱 관리
        for recommendation in recommendations:
            eating = recommendation.collide(fighter)

            if recommendation.out_of_screen():
                recommendation.kill()

            if eating:
                take = recommendation.image
                recommendation.kill()
                score += 300
                shot_count2 += 1

                james = np.concatenate(pygame.surfarray.array2d(take)).sum() # 현재 픽셀 정보
                infos = [np.concatenate(pygame.surfarray.array2d(j)).sum() for j in final] # 지금까지의 픽셀 정보

                if (len(takes) == 3) and (james not in infos):
                    del takes[0], final[0]
                    final.insert(2, take)
                    take = pygame.transform.scale(take, (50, 50))
                    takes.insert(2, take)
                elif (len(takes) < 3) and (james not in infos):
                    final.append(take)
                    take = pygame.transform.scale(take, (50, 50))
                    takes.append(take)

        try:
            screen.blit(takes[0], [10, 40])
            screen.blit(takes[1], [60, 40])
            screen.blit(takes[2], [110, 40])
        except:
            pass


        # 화면이 계속바뀌니 update함
        rocks.update()
        rocks.draw(screen)
        butterflies.update()
        butterflies.draw(screen)
        items.update()
        items.draw(screen)
        recommendations.update()
        recommendations.draw(screen)
        missiles.update()
        missiles.draw(screen)
        fighter.update()
        fighter.draw(screen)
        alldrawings.update()
        pygame.display.flip()

        # 게임이 끝나는 조건
        if fighter.collide(rocks) or count_missed >= 5: # 운석과 충돌 혹은 5개이상 놓쳤을 때
            pygame.mixer_music.stop()
            occur_explosion(screen, fighter.rect.x, fighter.rect.y)
            pygame.display.update()
            gameover_sound.play()
            sleep(1)
            done=True # 반복문 종료

        fps_clock.tick(FPS)
    return 'results'

 # 결과창
def results():
    global final, score
    start_image = pygame.image.load(path.join(file_dir, 'background1.png'))
    screen.blit(start_image, [0, 0])

    image = pygame.Surface([WINDOW_WIDTH, WINDOW_HEIGHT])
    image.fill(BLACK)
    image.set_alpha(60)
    screen.blit(image, (0, 0))

    draw_x = int(WINDOW_WIDTH / 2)
    draw_y = int(WINDOW_HEIGHT / 8)
    font_70 = pygame.font.Font(path.join(file_dir, 'DungGeunMo.ttf'), 70)
    font_40 = pygame.font.Font(path.join(file_dir, 'DungGeunMo.ttf'), 40)
    font_30 = pygame.font.Font(path.join(file_dir, 'DungGeunMo.ttf'), 30)

    draw_text('GAME OVER!', font_70, screen, draw_x, draw_y, WHITE)
    draw_text('SCORE : {}'.format(score), font_30, screen, draw_x, draw_y +60, WHITE)
    draw_text('당신에게 추천하는 앱', font_40, screen, draw_x, draw_y + 150, WHITE)
    # draw_text('저격하는 앱은', font_40, screen, draw_x, draw_y + 170, WHITE)
    draw_text('엔터 키를 누르면', font_30, screen, draw_x, draw_y + 400, WHITE)
    draw_text('메인으로 돌아갑니다', font_30, screen, draw_x, draw_y + 430, WHITE)

    if len(final) > 0:
        try:
            screen.blit(final[0], [draw_x-180, draw_y+200])
            screen.blit(final[1], [draw_x-60, draw_y+200])
            screen.blit(final[2], [draw_x+60, draw_y+200])
        except:
            pass
    else:
        draw_text('다시 도전해보세요!', font_40, screen, draw_x, draw_y+250, YELLOW)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return 'game_menu'
        if event.type == QUIT:
                return 'quit'

    return 'results'


def game_menu():
    start_image = pygame.image.load(path.join(file_dir, 'background1.png'))
    screen.blit(start_image, [0, 0])
    draw_x = int(WINDOW_WIDTH / 2)
    draw_y = int(WINDOW_HEIGHT / 4)
    font_60 = pygame.font.Font(path.join(file_dir, 'DungGeunMo.ttf'), 60)
    font_40 = pygame.font.Font(path.join(file_dir, 'DungGeunMo.ttf'), 40)
    font_20 = pygame.font.Font(path.join(file_dir, 'DungGeunMo.ttf'), 20)
    font_15 = pygame.font.Font(path.join(file_dir, 'DungGeunMo.ttf'), 15)


    draw_text('ver 1.1', font_15, screen, WINDOW_WIDTH-30, WINDOW_HEIGHT-10, WHITE)
    draw_text('github.com/woocosmos', font_15, screen, WINDOW_WIDTH-400, WINDOW_HEIGHT-10, WHITE)


    draw_text('정보의 바다 속에서', font_40, screen, draw_x, draw_y-60, YELLOW)
    draw_text('당신의 취향은', font_60, screen, draw_x, draw_y, YELLOW)
    draw_text('무엇인가요?', font_60, screen, draw_x, draw_y+60, YELLOW)

    draw_text('엔터 키를 눌러', font_40, screen, draw_x, draw_y + 200, (0, 0, 0))
    draw_text('취향을 찾아보세요!', font_40, screen, draw_x, draw_y + 250, (0, 0, 0))
    draw_text('made by Bernice', font_20, screen, draw_x, draw_y + 300, (0, 0, 0))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return 'play'
        if event.type == QUIT:
            return 'quit'

    return 'game_menu'

def main():
    global screen

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('취향저격 게임 by Bernice')

    action = 'game_menu'
    while action != 'quit':
        if action == 'game_menu':
            action = game_menu()
        elif action == 'results':
            action = results()
        elif action == 'play':
            action = game_loop()

    pygame.quit()


if __name__ == "__main__":
    main()