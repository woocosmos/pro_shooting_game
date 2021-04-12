# http://suanlab.com/assets/slectures/python/PyShooting.pdf
# https://www.youtube.com/watch?v=W92RjjptAsM

import random
from time import sleep
import sys
import numpy as np
from os import path

import pygame
from pygame.locals import *

file_dir = path.join(path.dirname(__file__))
print(file_dir)

# 전체 윈도우 크기
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 640

# 기본적으로 사용할 색(255에 가까울수록 가까움)
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
        if self.rect.y + self.rect.height < 0: # 미사일이 화면 밖으로 나간다면
            self.kill()

    def collide(self, sprites): # 충돌 관리
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite

class Bomb(pygame.sprite.Sprite):
    def __init__(self, fighter):
        super().__init__()
        self.image = None
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.radius = 20
        self.radiusIncrement = 4
        self.rect = fighter.rect
        self.sound = pygame.mixer.Sound('bomb.ogg')

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

    def collide(self, sprites): # 충돌 관리
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return self # 충돌 반환

class Bomb_item(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed):
        super(Bomb_item, self).__init__()
        self.image = pygame.image.load(path.join(file_dir, 'bomb.png'))
        self.rect = self.image.get_rect()
        self.rect.x = xpos # 위치값
        self.rect.y = ypos # 위치값
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

    def out_of_screen(self): # 화면에 나간것을 체크
        if self.rect.y > WINDOW_HEIGHT:
            return True

 # https://app.monopro.org/pixel/ 픽셀아트 -> 110*110 (3cm*3cm)
 # 선물 박스
class Butterfly(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed):
        super(Butterfly, self).__init__()
        self.image = pygame.image.load(path.join(file_dir, 'gift01.png'))
        self.rect = self.image.get_rect()
        self.rect.x = xpos  # 위치값
        self.rect.y = ypos  # 위치값
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

 # 추천
class Recommendation(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed):
        super(Recommendation, self).__init__()
        recommendations = ['recommend01.png', 'recommend02.png', 'recommend03.png', 'recommend04.png', 'recommend05.png',
                           'recommend06.png', 'recommend07.png', 'recommend08.png', 'recommend09.png', 'recommend10.png']
        self.image = pygame.image.load(path.join(file_dir, random.choice((recommendations))))
        self.rect = self.image.get_rect()  # 크기를 가져옴
        self.rect.x = xpos  # 위치값
        self.rect.y = ypos  # 위치값
        self.speed = speed
        pygame.mixer.Sound(path.join(file_dir, 'change2.wav')).play()

    def update(self):  # 화면에 업데이트
        self.rect.y += self.speed

    def out_of_screen(self):  # 화면에 나간것을 체크
        if self.rect.y > WINDOW_HEIGHT:
            return True

    def collide(self, sprite):  # 충돌 관리 = 아이템 먹기
        if pygame.sprite.collide_rect(self, sprite):
            pygame.mixer.Sound(path.join(file_dir, 'get.wav')).play()
            return sprite


def draw_text(text, font, surface, x, y, main_color): # 게임 점수 or 다앙햔 것을 출력
    text_obj = font.render(text, True, main_color) # render로 font를 정의
    text_rect = text_obj.get_rect() #위치를 가져옴
    text_rect.centerx = x
    text_rect.centery = y
    surface.blit(text_obj, text_rect) # 화면 출력


def occur_explosion(surface, x, y): # 폭발 이미지
    explosion_image = pygame.image.load(path.join(file_dir, 'explosion.png'))
    explosion_rect = explosion_image.get_rect()
    explosion_rect.x = x
    explosion_rect.y = y
    surface.blit(explosion_image, explosion_rect)

    explosion_sound = pygame.mixer.Sound(path.join(file_dir, 'explosion.wav'))
    explosion_sound.play()


def game_loop(): # 게임에서 반복되는 부분 처리
    global final
    default_font = pygame.font.Font('DungGeunMo.ttf', 28) # 28은 크기
    background_image = pygame.image.load(path.join(file_dir, 'background1.png')) # 배경
    gameover_sound = pygame.mixer.Sound(path.join(file_dir, 'gameover.mp3')) # 게임오버 사운드
    pygame.mixer.music.load(path.join(file_dir, 'music.wav')) # 게임음악
    pygame.mixer.music.play(-1) # 재생 횟수, -1은 무한 반복
    fps_clock = pygame.time.Clock()
    change_sound = pygame.mixer.Sound(path.join(file_dir, 'change2.wav'))
    get_sound = pygame.mixer.Sound(path.join(file_dir, 'get.wav'))

    fighter = Fighter()
    missiles = pygame.sprite.Group() # 미사일은 여러개가 들어갈 수 있기 때문에 그룹을 사용
    rocks = pygame.sprite.Group() # 운석은 여러개가 들어갈 수 있기 때문에 그룹을 사용
    butterflies = pygame.sprite.Group()
    items = pygame.sprite.Group()
    recommendations = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    alldrawings = pygame.sprite.Group()

    occur_prob = 60
    shot_count = 0 # 맞춘 운석 갯수
    count_missed = 0 # 놓치 운석 갯수

    occur_prob2 = 600
    shot_count2 = 0
    count_missed2 = 0

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
    while not done: # False가 not이니 True가되어 반복이 됨. 만약 done이 True가 되면 종료
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:         # 창이 닫히는 이벤트
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN: # 키가 눌림
                if event.key == pygame.K_LEFT: # 왼쪽 키가 눌림
                    fighter.dx -= 5 # 5만큼 이동
                elif event.key == pygame.K_RIGHT:
                    fighter.dx += 5
                elif event.key == pygame.K_UP:
                    fighter.dy -= 5
                elif event.key == pygame.K_DOWN:
                    fighter.dy += 5
                elif event.key == pygame.K_SPACE: # 미사일 쏘는 키
                    missile = Missile(fighter.rect.centerx, fighter.rect.y, 10) # 미사일 생성, 우주선 정가운데 위치, 속도 10
                    missile.launch() # 발사 사운드 재생
                    missiles.add(missile)
                elif event.key == pygame.K_b:
                    if bomb_held > 0:
                        newBomb = fighter.bomb()
                        newBomb.add(bombs, alldrawings)
                        bomb_held -= 1

            if event.type == pygame.KEYUP: # 키에서 손을 뗄때
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

        # 운석 등장(얼만큼의 볼드를 발생할 것인지)
        occur_of_rocks = 1 + int(shot_count / 150) # 점수에 따라서 점점 돌을 많이 등장
        min_rock_speed = 1 + int(shot_count / 100) # 운석의 최소 스피드
        max_rock_speed = 1 + int(shot_count / 50) # 운석의 최대 스피드

        if random.randint(1, occur_prob) == 1: # 1부터 40사이에 1이 등장할 확률
            for i in range(occur_of_rocks): # 운석 생성, 운석이 얼만큼 등장할 것인가
                speed = random.randint(min_rock_speed, max_rock_speed) # 속도는 랜덤
                rock = Rock(random.randint(0, WINDOW_WIDTH - 30), 0, speed) # 운석이 화면박으로 안나가도록
                rocks.add(rock)

        min_butterfly_speed = 1 + int(shot_count2 / 200)  # 운석의 최소 스피드
        max_butterfly_speed = 1 + int(shot_count2 / 100)  # 운석의 최대 스피드

        if timing:
            speed = random.randint(min_butterfly_speed, max_butterfly_speed)  # 속도는 랜덤
            butterfly = Butterfly(random.randint(0, WINDOW_WIDTH - 30), 0, speed)  # 최초 객체 생성 = 빨간색
            butterflies.add(butterfly)
            timing = False

        if bomb_timing:
            speed = random.randint(min_butterfly_speed, max_butterfly_speed) # 일단 속도는 나비와 같게
            item = Bomb_item(random.randint(0, WINDOW_WIDTH - 30), 0, speed)
            items.add(item)
            bomb_timing = False


        draw_text('놓친 쓰레기 {}개'.format(count_missed), default_font, screen, 360, 20, YELLOW)
        draw_text('나의 취향', default_font, screen, 80, 20, WHITE)

        for bomb in bombs:
            try:
                if pygame.sprite.collide_circle(bomb, rock):
                    rock.kill()
                    occur_explosion(screen, rock.rect.x, rock.rect.y)
            except:
                pass

        for missile in missiles:
            rock = missile.collide(rocks) # 미사일과 운석의 충돌을 반환
            butterfly = missile.collide(butterflies)
            recommendation = missile.collide(recommendations)

            if rock: # 충돌시
                missile.kill()
                rock.kill()
                occur_explosion(screen, rock.rect.x, rock.rect.y) # 돌에 위치값에 터지는것을 스크린에 출력
                shot_count += 1 # 파괴시 샷카운트

            if butterfly:
                count += 1
                if count == 1:
                    missile.kill()
                    butterfly.change_color()
                elif count == 2:
                    missile.kill()
                    butterfly.kill()
                    recommendation = Recommendation(butterfly.rect.x, butterfly.rect.y, speed)  # 운석이 화면 밖으로 안나가도록
                    recommendations.add(recommendation)
                    count = 0

            if recommendation:
                missile.kill()

        for rock in rocks:
            if rock.out_of_screen(): # 운석이 만약 화면을 나간다면
                rock.kill() # 제거
                count_missed += 1 # 놓친갯수로 카운트


        for butterfly in butterflies:
            if butterfly.out_of_screen(): # 나비가 화면을 나간다면
                butterfly.kill() # 제거

        for item in items:
            powerup = item.collide(fighter)

            if item.out_of_screen():
                item.kill()

            if powerup:
                item.kill()
                bomb_held += 1
                # if bomb_held > 5:
                #     bomb_held = 5
                bomb_held = min(bomb_held, 5)

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


        for recommendation in recommendations:
            eating = recommendation.collide(fighter)

            if recommendation.out_of_screen():
                recommendation.kill()

            if eating:
                take = recommendation.image
                recommendation.kill()

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
        pygame.display.flip() # pygame display에 flip으로 지금 현재 업데이트 된 값을 전체 반영

        # 게임이 끝나는 조건
        if fighter.collide(rocks): #or count_missed >= 3: # 운석과 충돌 혹은 3개이상 놓쳤을 때
            pygame.mixer_music.stop() # 배경음악 끄기
            occur_explosion(screen, fighter.rect.x, fighter.rect.y) # 비행기 위치 폭발
            pygame.display.update()
            gameover_sound.play()
            sleep(1)
            done=True # 반복문 종료

        fps_clock.tick(FPS)
    return 'results'

def results(): # 결과창
    global final
    start_image = pygame.image.load(path.join(file_dir, 'background1.png'))
    screen.blit(start_image, [0, 0])  # 0, 0 딱 그 크기 위치에 맞게
    draw_x = int(WINDOW_WIDTH / 2)
    draw_y = int(WINDOW_HEIGHT / 8)
    font_70 = pygame.font.Font('DungGeunMo.ttf', 70)
    font_40 = pygame.font.Font('DungGeunMo.ttf', 40)
    draw_text('GAME OVER', font_70, screen, draw_x, draw_y, WHITE)
    draw_text('당신의 취향을', font_40, screen, draw_x, draw_y + 100, WHITE)
    draw_text('저격하는 앱은', font_40, screen, draw_x, draw_y + 150, WHITE)
    draw_text('다시 시작하려면', font_40, screen, draw_x, draw_y + 400, BLACK)
    draw_text('엔터 키를 누르세요', font_40, screen, draw_x, draw_y + 450, BLACK)

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

    for event in pygame.event.get(): # pygame.event를 받아옴
        if event.type == pygame.KEYDOWN: # 키가 눌림
            if event.key == pygame.K_RETURN: # 키가 눌린값이 엔터(K_RETURN)일시
                return 'game_menu'
        if event.type == QUIT:  # 게임 종료를 누르면 게임 종료
                return 'quit'

    return 'results'


def game_menu():
    start_image = pygame.image.load(path.join(file_dir, 'background1.png'))
    screen.blit(start_image, [0, 0]) # 0, 0 딱 그 크기 위치에 맞게
    draw_x = int(WINDOW_WIDTH / 2)
    draw_y = int(WINDOW_HEIGHT / 4)
    font_60 = pygame.font.Font('DungGeunMo.ttf', 60)
    font_40 = pygame.font.Font('DungGeunMo.ttf', 40)
    font_20 = pygame.font.Font('DungGeunMo.ttf', 20)


    draw_text('정보의 바다 속에서', font_40, screen, draw_x, draw_y-60, YELLOW)
    draw_text('당신의 취향은', font_60, screen, draw_x, draw_y, YELLOW)
    draw_text('무엇인가요?', font_60, screen, draw_x, draw_y+60, YELLOW)

    draw_text('엔터 키를 눌러', font_40, screen, draw_x, draw_y + 200, (0, 0, 0))
    draw_text('취향을 찾아보세요!', font_40, screen, draw_x, draw_y + 250, (0, 0, 0))
    draw_text('made by 강인, 용빈, 연수', font_20, screen, draw_x, draw_y + 300, (0, 0, 0))


    pygame.display.update()

    for event in pygame.event.get(): # pygame.event를 받아옴
        if event.type == pygame.KEYDOWN: # 키가 눌림
            if event.key == pygame.K_RETURN: # 키가 눌린값이 엔터(K_RETURN)일시
                return 'play'
        if event.type == QUIT: # 게임 종료를 누르면 게임 종료
            return 'quit'

    return 'game_menu'

def main(): # 게임에 처음 들어가기전
    global screen # 게임 전체에서 screen을 사용

    pygame.init() # pygame.init 초창기에 초기화
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) # 실제 윈도우의 크기
    pygame.display.set_caption('취향저격 게임 by Bernice') # 윈도우에 띄울 이름

    action = 'game_menu'
    while action != 'quit': # action이 quit이 아니면
        if action == 'game_menu':
            action = game_menu()
        elif action == 'results':
            action = results()
        elif action == 'play':
            action = game_loop()

    pygame.quit() # pygame을 끝냄

# 메인 실행
if __name__ == "__main__":
    main()