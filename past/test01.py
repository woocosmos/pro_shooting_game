import pygame
import sys
import random
from time import sleep, time

# 화면 구성
BLACK = (0, 0, 0)
padWidth= 480
padHeight = 640

# 이미지, 효과음
rockImage = ['rock01.png', 'rock02.png', 'rock03.png', 'rock04.png', 'rock05.png']
butterflies = ['red_butterfly.png', 'blue_butterfly.png', 'green_butterfly.png']

# 객체 드로잉
def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))

# 게임 메세지 출력
def writeMessage(text):
    global gamePad, gameOverSound
    font = pygame.font.Font('DungGeunMo.ttf', 50)
    text = font.render(text, True, (255,0,0))
    textpos = text.get_rect()
    textpos.center = (padWidth/2, padHeight/2)
    gamePad.blit(text, textpos)
    pygame.display.update()
    pygame.mixer.music.stop()
    gameOverSound.play()
    sleep(2)
    pygame.mixer.music.play(-1)
    runGame()

# 충돌시 문구
def crash():
    global gamePad
    writeMessage('우주선 파괴!')

# 게임 종료 문구
def gameOver():
    global gamePad
    writeMessage('게임 오버!')

# 맞힌 물고기 개수
def writeScore(count):
    global gamePad
    font = pygame.font.Font('DungGeunMo.ttf', 30)
    text = font.render('파괴한 운석 ' + str(count) + '개', True, (255, 255, 255))
    gamePad.blit(text, (10, 0))

# 놓친 물고기 개수
def writePassed(count):
    global gamePad
    font = pygame.font.Font('DungGeunMo.ttf', 30)
    text = font.render('놓친 운석 ' + str(count) + '개', True, (255,255,255))
    gamePad.blit(text, (280, 0))

# 초기화
def initGame():
    global gamePad, clock, background, fighter, missile, explosion, missileSound, gameOverSound, explosionSound
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('우주 슈팅 게임 - WYS')          # 게임 이름
    background = pygame.image.load('background.png')  # 배경
    fighter = pygame.image.load('./fighter.png')        # 전투기
    missile = pygame.image.load('missile.png')          # 미사일
    explosion = pygame.image.load('explosion.png')      # 폭발
    pygame.mixer.music.load('music.wav')                # 배경음악
    pygame.mixer.music.play(-1)
    missileSound = pygame.mixer.Sound('missile.wav')
    gameOverSound = pygame.mixer.Sound('gameover.mp3')
    explosionSound = pygame.mixer.Sound('explosion.wav')
    clock = pygame.time.Clock()                         # 초 계산


# 게임 실행
def runGame():
    global gamePad, clock, background, fighter, missile, explosion, missileSound, explosionSound

    # 전투기
    fighterSize = fighter.get_rect().size       # 크기
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]
    x = padWidth * 0.45                         # 초기 위치
    y = padHeight * 0.8
    fighterX = 0

    # 운석
    rock = pygame.image.load(random.choice(rockImage))  # 랜덤 생성
    rockSize = rock.get_rect().size                     # 크기
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]
    rockX = random.randrange(0, padWidth - rockWidth)   # 초기 위치
    rockY = 0
    rockSpeed = 2
    isShot = False                                      # 미사일 맞았을 경우
    shotCount = 0
    rockPassed = 0

    # 나비
    butterfly = pygame.image.load(butterflies[0])           # 최초 빨간 나비
    butterflySize = butterfly.get_rect().size               # 크기
    butterflyWidth = butterflySize[0]
    butterflyHeight = butterflySize[1]
    butterflyX = random.randrange(0, padWidth - rockWidth)  # 초기 위치
    butterflyY = 0
    butterflySpeed = 4
    butterflyShot = False                                   # 미사일 맞았을 경우
    shotColor = 0

    timing = False
    BUTTERFLY = pygame.USEREVENT+1
    pygame.time.set_timer(BUTTERFLY, 3000)

    # 미사일 좌표 리스트
    missileXY = []

    # 다 셋팅한 다음에 게임 시작
    onGame = True

    while onGame:
        for event in pygame.event.get():            # onGame일 때 키보드 입력(event) 체크
            if event.type in [pygame.QUIT]:         # 창이 닫히는 이벤트
                pygame.quit()
                sys.exit()

            if event.type in [pygame.KEYDOWN]:      # 키보드 누르기
                if event.key == pygame.K_LEFT:      # 좌
                    fighterX -= 5
                elif event.key == pygame.K_RIGHT:   # 우
                    fighterX += 5
                elif event.key == pygame.K_SPACE:   # 스페이스바
                    missileSound.play()
                    missileX = x + fighterWidth/2
                    missileY = y - fighterHeight
                    missileXY.append([missileX, missileY]) # 전투기 기준으로 미사일 시작 위치 저장

            if event.type in [pygame.KEYUP]:        # 키보드 떼기
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighterX = 0

            if event.type == BUTTERFLY:             # 3초마다 나비 나타나는 이벤트
                timing = True

        drawObject(background, 0, 0) # 게임 화면

        # 이벤트에 따라 전투기 이동
        x += fighterX
        if x < 0:
            x = 0
        elif x > padWidth - fighterWidth:
            x = padWidth - fighterWidth

        # 전투기가 운석이나 나비와 충돌했을 때
        if (y < rockY + rockHeight) or (y < butterflyY + butterflyHeight):
            if (rockX > x and rockX < x + fighterWidth) or (rockX + rockWidth > x and rockX + rockWidth < x + fighterWidth) or (butterflyX > x and butterflyX < x + fighterWidth) or (butterflyX + butterflyWidth > x and butterflyX + butterflyWidth < x + fighterWidth):
                crash()

        drawObject(fighter, x, y)                                       # 전투기

        if len(missileXY) != 0:                                         # 미사일이 발사되면 (위치 존재)
            for i, bxy in enumerate(missileXY):                         # 미사일 위치 리스트에서 좌표
                bxy[1] -= 10                                            # 미사일 위로 이동 (for문 한번 돌 때마다 아래 내용 체크)
                missileXY[i][1] = bxy[1]

                if (bxy[1] < rockY) or (bxy[1] < butterflyY):           # 미사일이 운석이나 나비에 적중
                    if bxy[0] > rockX and bxy[0] < rockX + rockWidth:
                        missileXY.remove(bxy)                           # 리스트에서 그 좌표를 삭제한다 (미사일 없어진 거임)
                        isShot = True                                   # 운석 맞음
                        shotCount += 1                                  # 맞은 횟수
                    elif bxy[0] > butterflyX and bxy[0] < butterflyX + butterflyWidth:
                        missileXY.remove(bxy)
                        butterflyShot = True
                        shotColor += 1                                  # 색깔 바뀌어야 함

                if bxy[1] <= 0 :                                        # 화면 밖 미사일 제거
                    try:
                        missileXY.remove(bxy)
                    except:
                        pass

        if len(missileXY) != 0:
            for bx, by in missileXY:
                drawObject(missile, bx, by)

        writeScore(shotCount) # 맞힌 운석

        # 운석, 나비 아래로 이동
        rockY += rockSpeed
        butterflyY += butterflySpeed

        # 지구로 떨어진 경우 새로운 운석
        if rockY > padHeight:
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            rockPassed += 1

        if rockPassed == 3:
            gameOver()

        writePassed(rockPassed)

        if isShot: # 운석 맞춘 경우
            drawObject(explosion, rockX, rockY) # 폭발
            explosionSound.play()
            rock = pygame.image.load(random.choice(rockImage)) # 새로운 운석
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            isShot = False
            rockSpeed += 0.02
            if rockSpeed >= 10:
                rockSpeed = 10

        drawObject(rock, rockX, rockY)

        # 나비 지구로 떨어진 경우 게임 종료
        if butterflyY > padHeight:
            gameOver()

        # 나비 맞힌 경우
        if butterflyShot:
            if shotColor == 1:
                butterfly = pygame.image.load(butterflies[1]) # 파랑
                drawObject(butterfly, butterflyX, butterflyY)
                butterflyShot = False
            elif shotColor == 2:
                butterfly = pygame.image.load(butterflies[2]) # 초록
                drawObject(butterfly, butterflyX, butterflyY)
                butterflyShot = False
            elif shotColor == 3:
                drawObject(explosion, butterflyX, butterflyY)
                explosionSound.play()
                timing = False
                shotColor = 0
                butterflyShot = False

        if timing == False:
            butterfly = pygame.image.load(butterflies[0])
            butterflyX = random.randrange(0, padWidth - rockWidth)
            butterflyY = -100

        drawObject(butterfly, butterflyX, butterflyY)

        pygame.display.update() # 게임 화면 다시 그림
        clock.tick(60) # 초당 프레임수 60
    pygame.quit()

initGame() # 초기화
runGame() # 게임 실행


