import pygame
from body import Body
from random import randint, choice


class Game():
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.init()

    def init(self):
        pygame.mixer.music.load('Code/Sounds/bg_music.mp3')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        self.windowConfig()
        self.snakeConfig(), self.bodyConfig()
        self.foodImages(), self.foodConfig()

    def windowConfig(self):
        self.displayX, self.displayY = 600, 500
        self.display = pygame.display.set_mode((self.displayX, self.displayY))
        icon = pygame.image.load('Code/Images/snake_head.png')
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()

    def snakeConfig(self):
        self.snakeX, self.snakeY = 85, 150
        self.snakeXb, self.snakeYb = -50, -50
        self.snakeX_change, self.snakeY_change = 0, 0
        self.snake_change = 5
        self.score = 0
        self.snakeA, self.snakeBlock = 0, -1
        self.snakeHead = pygame.image.load('Code/Images/snake_head.png')
        self.snakeHead = pygame.transform.scale(self.snakeHead, (80, 80))

    def snakeRotate(self, angle):
        self.snakeBlock = angle
        self.snakeHead = pygame.transform.rotate(self.snakeHead, self.snakeA)
        self.snakeHead = pygame.transform.rotate(self.snakeHead, angle)
        self.snakeA = abs(angle - 360)

    def foodImages(self):
        self.foodSize = (30, 30)
        self.grape = pygame.image.load('Code/Images/grapes.png')
        self.grape = pygame.transform.scale(self.grape, self.foodSize)
        self.strawb = pygame.image.load('Code/Images/strawberry.png')
        self.strawb = pygame.transform.scale(self.strawb, self.foodSize)
        self.cherry = pygame.image.load('Code/Images/cherry.png')
        self.cherry = pygame.transform.scale(self.cherry, self.foodSize)

    def foodConfig(self):
        self.foodX = randint(0, 11)*50+10
        self.foodY = randint(0, 9)*50+10
        self.foodChoice = choice([self.grape, self.strawb, self.cherry])

    def write(self, msg, color, x=0, y=0, center=None):
        font = pygame.font.SysFont('Consolas', 20)
        mensg = font.render(msg, True, color)
        width = mensg.get_rect().width if center == True else 0
        self.display.blit(mensg, (x-width/2, y))

    def bodyConfig(self):
        self.bodyNumber = 1
        self.gameOver, self.canWalk = False, True
        self.body_01 = Body(self.display, 100, 150, 50, 50)
        self.bodyList = [self.body_01]
        self.bodyXY_list = [(100, 150), (100, 150)]

    def bodyXY(self):
        for body in self.bodyList:
            body.x = round(body.x/50)*50
            body.y = round(body.y/50)*50

    def moveBody(self):
        self.bodyXY_list[0] = (self.snakeX, self.snakeY)
        for pos, body in enumerate(self.bodyList):
            body.x, body.y = self.bodyXY_list[pos]
            self.bodyXY()

    def moveLeftRight(self, angle, signal):
        self.snakeX_change = signal*self.snake_change
        self.snakeRotate(angle), self.moveBody()
        self.snakeX += self.snakeX_change*4

    def moveUpDown(self, angle, signal):
        self.snakeY_change = signal*self.snake_change
        self.snakeRotate(angle), self.moveBody()
        self.snakeY += self.snakeY_change*4

    def playSound(self, file):
        sound = pygame.mixer.Sound('Code\Sounds\{}'.format(file))
        sound.play()

    def mainloop(self):
        running = True
        self.bodyConfig()
        while running:
            self.bgColor = ['#8ECC39', '#A7D948']
            for y in range(0, 501, 50):
                self.bgColor = self.bgColor[::-1]
                for x in range(0, 601, 50):
                    color = self.bgColor[0] if x % 100 == 0 else self.bgColor[1]
                    pygame.draw.rect(self.display, color, (x, y, 50, 50))

            if self.gameOver == True:
                self.write('Game Over', (255, 0, 0),
                           self.displayX/2, 200, center=True)
                self.write('Q-Quit or P-Play', (255, 0, 0),
                           self.displayX/2, 225, center=True)
                self.write(f'Your score: {self.score}', (255, 0, 0),
                           self.displayX/2, 250, center=True)
                for event in pygame.event.get():
                    running = False if event.type == pygame.QUIT else True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            pygame.quit(), quit()
                        if event.key == pygame.K_p:
                            self.init()
                self.clock.tick(30)
            else:
                self.write(f'Score: {self.score}', (255, 0, 0), 5, 0)
                for event in pygame.event.get():
                    running = False if event.type == pygame.QUIT else True
                    if event.type == pygame.KEYDOWN:
                        if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                            self.snakeY = round(self.snakeY/50)*50-15
                            self.snakeY_change = 0
                        elif event.key in [pygame.K_UP, pygame.K_DOWN]:
                            self.snakeX = round(self.snakeX/50)*50-15
                            self.snakeX_change = 0

                        if event.key == pygame.K_LEFT and self.snakeBlock not in [90, 270]:
                            self.moveLeftRight(270, -1)
                        elif event.key == pygame.K_RIGHT and self.snakeBlock not in [90, 270]:
                            self.moveLeftRight(90, 1)
                        if event.key == pygame.K_UP and self.snakeBlock not in [180, 0]:
                            self.moveUpDown(180, -1)
                        elif event.key == pygame.K_DOWN and self.snakeBlock not in [180, 0]:
                            self.moveUpDown(0, 1)

                self.display.blit(self.foodChoice, (self.foodX,
                                                    self.foodY))
                self.snakeX += self.snakeX_change
                self.snakeY += self.snakeY_change

                if self.snakeBlock in [0, 90]:
                    if self.snakeX % 50 == 0 or self.snakeY % 50 == 0:
                        self.moveBody()
                elif self.snakeBlock in [180, 270]:
                    if (self.snakeX-80) % 50 == 0 or (self.snakeY-80) % 50 == 0:
                        self.moveBody()

                for pos, body in enumerate(self.bodyList):
                    if body.x % 50 == 0 or body.y % 50 == 0:
                        self.bodyXY_list[pos+1] = (body.x, body.y)

                [body.createBody() for body in self.bodyList]

                headX, headY = self.bodyXY_list[0]
                first_bodyX, first_bodyY = self.bodyXY_list[1]
                plusX = 15 if self.snakeBlock in [0, 180] else 0
                plusY = 15 if self.snakeBlock in [90, 270] else 0
                for body in self.bodyList[2:]:
                    if body.x in [headX+plusX, first_bodyX] and \
                            body.y in [headY+plusY, first_bodyY]:
                        self.gameOver = True

                if self.snakeX >= 550 or self.snakeX < -15 or \
                        self.snakeY >= 455 or self.snakeY < -15:
                    self.gameOver = True

                if self.gameOver == True:
                    self.playSound('crash.wav')
                    pygame.mixer.music.pause()

                self.display.blit(self.snakeHead, (self.snakeX, self.snakeY))
                if self.foodX in [self.snakeX+5, self.snakeX+25, first_bodyX+10] and \
                        self.foodY in [self.snakeY+25, self.snakeY-5, first_bodyY+10]:
                    self.foodConfig()
                    self.playSound('eat.wav')
                    while (self.foodX-10, self.foodY-10) in self.bodyXY_list:
                        self.foodConfig()
                    x, y = self.bodyList[-1].x, self.bodyList[-1].y
                    x, y = round(x/50)*50, round(y/50)*50
                    self.bodyList.append(Body(self.display, x, y, 50, 50))
                    self.bodyXY_list.append((x, y))
                    self.score += 1

            pygame.display.update()
            self.clock.tick(60)


SnakeGame = Game()
SnakeGame.mainloop()
