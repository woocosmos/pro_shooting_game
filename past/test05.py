# http://suanlab.com/assets/slectures/python/PyShooting.pdf
# https://www.youtube.com/watch?v=W92RjjptAsM

import random
from time import sleep
import sys

import pygame
from pygame.locals import *

# 전체 윈도우 크기
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 640

# 기본적으로 사용할 색(255에 가까울수록 가까움)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (250, 250, 50)
RED = (250, 50, 50)

FPS = 60 # 프레임 / SEC

# 비행기
class Fighter(pygame.sprite.Sprite):
    def __init__(self):
        super(Fighter, self).__init__()
        # 이미지
        self.image = pygame.image.load('fighter.png')
        self.rect = self.image.get_rect() # 크기
        self.rect.x = int(WINDOW_WIDTH / 2) # 처음 위치 (화면의 가운데, 반)
        self.rect.y = WINDOW_HEIGHT - self.rect.height # (우주선의 높이만큼 뺌)
        # 움직임 정의
        self.dx = 0
        self.dy = 0

    def update(self): # 비행기 움직임 처리
        self.rect.x += self.dx
        self.rect.y += self.dy

        # 비행기가 화면을 나가면 안 됨
        if self.rect.x < 0 or self.rect.x + self.rect.width > WINDOW_WIDTH:
            self.rect.x -= self.dx # 더이상 움직이지 않게 바꿈

        if self.rect.y < 0 or self.rect.y + self.rect.height > WINDOW_HEIGHT:
            self.rect.y -= self.dy # 더이상 움직이지 않게 바꿈

    def draw(self, screen): # 그려주는 부분
        screen.blit(self.image, self.rect) # rect=현재 위치

    def collide(self, sprites): # 충돌, sprites=객체 관리
        for sprite in sprites:
            # 충돌검사, self:우주선, sprite와 비교하여 충돌이 났으면 리턴, 충돌난 애를 return
            if pygame.sprite.collide_rect(self, sprite):
                return sprite

# 미사일
class Missile(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed):
        super(Missile, self).__init__()
        self.image = pygame.image.load('missile.png')
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = speed
        self.sound = pygame.mixer.Sound('missile.wav') # 미사일 사운드

    def launch(self): # 발사
        self.sound.play()

    def update(self): # 미사일이 화면에 반영될 때 정의
        self.rect.y -= self.speed # 위로 발사되니 좌표값이 -임.
        if self.rect.y + self.rect.height < 0: # 미사일이 화면 밖으로 나간다면
            self.kill() # 없애줌, 모든 미사일을 관리할 수 없음

    def collide(self, sprites): # 충돌 관리
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite # 충돌 반환

# 운석
class Rock(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed):
        super(Rock, self).__init__()
        rock_images = ('rock01.png', 'rock02.png', 'rock03.png', 'rock04.png', 'rock05.png') # 다양한 돌 이미지 적용
        self.image = pygame.image.load(random.choice(rock_images)) # 랜덤으로 운석이미지 호출
        self.rect = self.image.get_rect() # 크기를 가져옴
        self.rect.x = xpos # 위치값
        self.rect.y = ypos # 위치값
        self.speed = speed

    def update(self): # 화면에 업데이트
        # y값만 증가시키면됨 위에서 아래로 내려오기 때문
        self.rect.y += self.speed

    def out_of_screen(self): # 화면에 나간것을 체크
        if self.rect.y > WINDOW_HEIGHT:
            return True

 # https://app.monopro.org/pixel/
class Butterfly(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed):
        super(Butterfly, self).__init__()
        self.butterfly_images = ['gift01.png', 'gift02.png']  # 다양한 돌 이미지 적용
        self.recommendations = ['recommend01.png', 'recommend02.png', 'recommend03.png', 'recommend04.png']
        self.image = pygame.image.load(self.butterfly_images[0])  # 랜덤으로 운석이미지 호출
        self.rect = self.image.get_rect()  # 크기를 가져옴
        self.rect.x = xpos  # 위치값
        self.rect.y = ypos  # 위치값
        self.speed = speed
        self.sound = pygame.mixer.Sound('change1.wav')

    def update(self):  # 화면에 업데이트
        # y값만 증가시키면됨 위에서 아래로 내려오기 때문
        self.rect.y += self.speed

    def out_of_screen(self):  # 화면에 나간것을 체크
        if self.rect.y > WINDOW_HEIGHT:
            return True

    def change_color(self): # 색깔 바꾸기
        self.image = pygame.image.load(self.butterfly_images[1])
        self.sound.play()


class Recommendation(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed):
        super(Recommendation, self).__init__()
        recommendations = ['recommend01.png', 'recommend02.png', 'recommend03.png', 'recommend04.png']
        self.image = pygame.image.load(random.choice(recommendations))
        self.rect = self.image.get_rect()  # 크기를 가져옴
        self.rect.x = xpos  # 위치값
        self.rect.y = ypos  # 위치값
        self.speed = speed
        pygame.mixer.Sound('change2.wav').play()

    def update(self):  # 화면에 업데이트
        # y값만 증가시키면됨 위에서 아래로 내려오기 때문
        self.rect.y += self.speed

    def out_of_screen(self):  # 화면에 나간것을 체크
        if self.rect.y > WINDOW_HEIGHT:
            return True

    def collide(self, sprite):  # 충돌 관리
        if pygame.sprite.collide_rect(self, sprite):
            pygame.mixer.Sound('get.wav').play()
            return sprite




def draw_text(text, font, surface, x, y, main_color): # 게임 점수 or 다앙햔 것을 출력
    text_obj = font.render(text, True, main_color) # render로 font를 정의
    text_rect = text_obj.get_rect() #위치를 가져옴
    text_rect.centerx = x
    text_rect.centery = y
    surface.blit(text_obj, text_rect) # 화면 출력


def occur_explosion(surface, x, y): # 폭발 이미지
    explosion_image = pygame.image.load('explosion.png')
    explosion_rect = explosion_image.get_rect()
    explosion_rect.x = x
    explosion_rect.y = y
    surface.blit(explosion_image, explosion_rect)

    explosion_sound = pygame.mixer.Sound('explosion.wav')
    explosion_sound.play()


def game_loop(): # 게임에서 반복되는 부분 처리
    default_font = pygame.font.Font('DungGeunMo.ttf', 28) # 28은 크기
    background_image = pygame.image.load('background.png') # 배경
    gameover_sound = pygame.mixer.Sound('gameover.mp3') # 게임오버 사운드
    pygame.mixer.music.load('music.wav') # 게임음악
    pygame.mixer.music.play(-1) # 재생 횟수, -1은 무한 반복
    fps_clock = pygame.time.Clock()
    change_sound = pygame.mixer.Sound('change2.wav')
    get_sound = pygame.mixer.Sound('get.wav')

    fighter = Fighter()
    missiles = pygame.sprite.Group() # 미사일은 여러개가 들어갈 수 있기 때문에 그룹을 사용
    rocks = pygame.sprite.Group() # 운석은 여러개가 들어갈 수 있기 때문에 그룹을 사용
    butterflies = pygame.sprite.Group()
    recommendations = pygame.sprite.Group()


    occur_prob = 40
    shot_count = 0 # 맞춘 운석 갯수
    count_missed = 0 # 놓치 운석 갯수

    occur_prob2 = 600
    shot_count2 = 0
    count_missed2 = 0

    timing = False
    BUTTERFLY = pygame.USEREVENT+1
    pygame.time.set_timer(BUTTERFLY, 3000)

    count = 0

    takes = []

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

            if event.type == pygame.KEYUP: # 키에서 손을 뗄때
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighter.dx = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    fighter.dy = 0

            if event.type == BUTTERFLY:
                timing = True

        # 게임화면 배경
        screen.blit(background_image, background_image.get_rect())

        # 운석 등장(얼만큼의 볼드를 발생할 것인지)
        occur_of_rocks = 1 + int(shot_count / 300) # 점수에 따라서 점점 돌을 많이 등장
        min_rock_speed = 1 + int(shot_count / 200) # 운석의 최소 스피드
        max_rock_speed = 1 + int(shot_count / 100) # 운석의 최대 스피드

        if random.randint(1, occur_prob) == 1: # 1부터 40사이에 1이 등장할 확률
            for i in range(occur_of_rocks): # 운석 생성, 운석이 얼만큼 등장할 것인가
                speed = random.randint(min_rock_speed, max_rock_speed) # 속도는 랜덤
                rock = Rock(random.randint(0, WINDOW_WIDTH - 30), 0, speed) # 운석이 화면박으로 안나가도록
                rocks.add(rock)

        # 나비 등장(얼만큼의 볼드를 발생할 것인지)
        min_butterfly_speed = 1 + int(shot_count2 / 200)  # 운석의 최소 스피드
        max_butterfly_speed = 1 + int(shot_count2 / 100)  # 운석의 최대 스피드

        if timing:
            speed = random.randint(min_butterfly_speed, max_butterfly_speed)  # 속도는 랜덤
            butterfly = Butterfly(random.randint(0, WINDOW_WIDTH - 30), 0, speed)  # 최초 객체 생성 = 빨간색
            butterflies.add(butterfly)
            timing = False

        # draw_text('파괴한 운석 : {}'.format(shot_count), default_font, screen, 110, 20, YELLOW)
        draw_text('취향 저격', default_font, screen, 75, 20, YELLOW)
        draw_text('놓친 운석 {}개'.format(count_missed), default_font, screen, 380, 20, RED)



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
                    recommendation = Recommendation(butterfly.rect.x, butterfly.rect.y, speed)  # 운석이 화면박으로 안나가도록
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


        for recommendation in recommendations:
            eating = recommendation.collide(fighter)

            if recommendation.out_of_screen():
                recommendation.kill()

            if eating:
                take = recommendation.image
                recommendation.kill()
                take = pygame.transform.scale(take, (50, 50))
                if len(takes) == 3:
                    del takes[0]
                    takes.insert(2, take)
                else:
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
        recommendations.update()
        recommendations.draw(screen)
        missiles.update()
        missiles.draw(screen)
        fighter.update()
        fighter.draw(screen)
        pygame.display.flip() # pygame display에 flip으로 지금 현재 업데이트 된 값을 전체 반영

        # 게임이 끝나는 조건
        if fighter.collide(rocks) or count_missed >= 3: # 운석과 충돌 혹은 3개이상 놓쳤을 때
            pygame.mixer_music.stop() # 배경음악 끄기
            occur_explosion(screen, fighter.rect.x, fighter.rect.y) # 비행기 위치 폭발
            pygame.display.update()
            gameover_sound.play()
            sleep(1)
            done=True # 반복문 종료

        fps_clock.tick(FPS)

    return 'game_menu'

def game_menu():
    start_image = pygame.image.load('background.png')
    screen.blit(start_image, [0, 0]) # 0, 0 딱 그 크기 위치에 맞게
    draw_x = int(WINDOW_WIDTH / 2)
    draw_y = int(WINDOW_HEIGHT / 4)
    font_60 = pygame.font.Font('DungGeunMo.ttf', 60)
    font_40 = pygame.font.Font('DungGeunMo.ttf', 40)

    draw_text('지구를 지켜라!', font_60, screen, draw_x, draw_y, YELLOW)
    draw_text('엔터 키를 누르면', font_40, screen, draw_x, draw_y + 200, WHITE)
    draw_text('게임이 시작됩니다.', font_40, screen, draw_x, draw_y + 250, WHITE)

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
    pygame.display.set_caption('WYS 취향저격 게임') # 윈도우에 띄울 이름

    action = 'game_menu'
    while action != 'quit': # action이 quit이 아니면
        if action == 'game_menu':
            action = game_menu()
        elif action == 'play':
            action = game_loop()

    pygame.quit() # pygame을 끝냄

# 메인 실행
if __name__ == "__main__":
    main()