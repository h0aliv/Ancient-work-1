import pygame, sys, random
import pygame.freetype

def calculate_distance(x):
        return x // 64


class Field:
    def __init__(self,image, startx, starty, row , col):
        self.image = image
        self.rect = self.image.get_rect()
        self.x = startx + 64 * row
        self.y = starty + 64 * col
        self.rect.topleft = (self.x, self.y)

    def draw(self,screen):
        screen.blit(self.image,self.rect)


class bullet:
    def __init__(self,image,topleft):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft
        self.x = self.rect.topleft[0]
        self.y = self.rect.topleft[1]
        self.collide = 0
    def move(self):
        self.x += 10
        self.rect.topleft = (self.x, self.y)
    def draw(self, screen):

        screen.blit(self.image, self.rect)
def shoot(image,coordinate):
    return bullet(image, coordinate)
class Defense:
    cost = 40
    def __init__(self, image,row, col, startx, starty):
        self.pos = 0
        self.image = image
        self.health = 100
        self.attack = 37
        self.action = 0
        self.property = 0
        self.in_battle = False
        self.rect = self.image.get_rect()
        self.x = startx + 64 * row
        self.y = starty + 64 * col
        self.rect.topleft = (self.x, self.y)
        self.actiontime = 35
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    def act(self):
        if self.action == 0:
            self.action = self.actiontime
        self.action -= 1
class D1(Defense):
    cost = 20
    def __init__(self, image, row, col, startx, starty):
        super(D1, self).__init__(image, row, col, startx, starty)
        self.actiontime = 18
        self.property = 1
        self.attack = 35
class DK(Defense):
    cost = 100
    def __init__(self,image, row, col, startx, starty):
        super(DK, self).__init__(image, row, col, startx, starty)
        self.actiontime = 10
        self.property = 1
        self.health = 150
        self.attack = 37

class enemy:
    def __init__(self, max_cols, startx, starty, image):
        # An animal shows up in a random row and col for a random number of frames.
        self.image = image
        self.attack = 1
        self.col = random.randint(0, max_cols)
        self.health = 100
        self.rect = self.image.get_rect()
        self.speed = 1
        self.x = startx
        self.y = starty + 64 * self.col
        self.rect.topleft = (self.x,self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


    def move(self):
        self.x -= self.speed
        self.rect.topleft = (self.x,self.y)
class E2(enemy):
    def __init__(self, max_cols, startx, starty, image):
        super(E2, self).__init__(max_cols, startx, starty, image)
        self.health = 100
        self.speed = 3
        self.attack = 3
class E3(enemy):
    def __init__(self, max_cols, startx, starty, image):
        super(E3, self).__init__( max_cols, startx, starty, image)
        self.health = 200
        self.speed = 4
        self.attack = 2
def draw_health_bar(screen, health, position_rect):
    health_bar = position_rect.copy()
    health_bar.height = 5
    health_bar.y -= position_rect.h/2 - 25
    pygame.draw.rect(screen, (50,50,50), health_bar, 1)
    health_bar.width = health_bar.width * health / 100
    pygame.draw.rect(screen, (50,250,50), health_bar)
def draw_enemy_health_bar(screen, health, position_rect):
    health_bar = position_rect.copy()
    health_bar.height = 5
    health_bar.y -= position_rect.h/2 - 25
    pygame.draw.rect(screen, (50,50,50), health_bar, 1)
    health_bar.width = health_bar.width * health / 100
    pygame.draw.rect(screen, (250,50,50), health_bar)
def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    clock = pygame.time.Clock()
    frame_count = 0
    GAME_FONT = pygame.freetype.SysFont('Consolas', 18)
    done = False
    enemies = []
    defense = []
    ene_image = pygame.image.load("black.png").convert_alpha()
    ene_lv2 = pygame.image.load("black_s1.png").convert_alpha()
    ene_lv3 = pygame.image.load("black_s2.png").convert_alpha()
    unit_image = pygame.image.load("white.png").convert_alpha()
    d1_image = pygame.image.load("white_melee.png").convert_alpha()
    dk_image = pygame.image.load("white_knight.png").convert_alpha()
    unit_rect = unit_image.get_rect()
    unit_rect.center = (150,20)
    D1_rect = d1_image.get_rect()
    D1_rect.center = (200,20)
    Dk_rect = d1_image.get_rect()
    Dk_rect.center = (250, 20)
    fieldimage = pygame.image.load("mud.png").convert_alpha()
    greenzone = pygame.image.load("green.png").convert_alpha()
    build = 0
    player1_gold = 50
    infotime = 0
    bullet_image = pygame.image.load("bullet.png").convert_alpha()
    bullets = []
    fields = []
    home = []
    vaild = 1
    f = Field(greenzone, 0, 0, -0.5, 2)
    f1 = Field(greenzone, 0, 0, -0.5, 1)
    f2 = Field(greenzone, 0, 0, -0.5, 3)
    f3 = Field(greenzone, 0, 0, -0.5, 4)
    f4 = Field(greenzone, 0, 0, -0.5, 5)
    home.append(f)
    home.append(f1)
    home.append(f2)
    home.append(f3)
    home.append(f4)
    for num in range(10):
        f = Field(fieldimage, 0, 0, num, 2)
        f1 = Field(fieldimage, 0, 0, num, 1)
        f2 = Field(fieldimage, 0, 0, num, 3)
        f3 = Field(fieldimage, 0, 0, num, 4)
        f4 = Field(fieldimage, 0, 0, num, 5)
        fields.append(f)
        fields.append(f1)
        fields.append(f2)
        fields.append(f3)
        fields.append(f4)
    inbound = 0
    contact = 0
    fail = False
    difficulty = 0
    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                pos = (mouse_pos[0], mouse_pos[1])
                for de in defense:
                    if de.rect.collidepoint(mouse_pos):
                        infotime = 19
                        vaild = 0
                        break
                    else:
                        vaild = 1
                if build == 1:

                    if calculate_distance(pos[1]) > 0 and vaild == 1:
                        defen = Defense(unit_image, calculate_distance(pos[0]), calculate_distance(pos[1]), 0, 0)
                        defense.append(defen)
                        build = 0
                        player1_gold = player1_gold - defen.cost
                elif build == 2:
                    if calculate_distance(pos[1]) > 0 and vaild == 1:
                        defen = D1(d1_image, calculate_distance(pos[0]), calculate_distance(pos[1]), 0, 0)
                        defense.append(defen)
                        build = 0
                        player1_gold = player1_gold - defen.cost
                elif build == 3:
                    if calculate_distance(pos[1]) > 0 and vaild == 1:
                        defen = DK(dk_image, calculate_distance(pos[0]), calculate_distance(pos[1]), 0, 0)
                        defense.append(defen)
                        build = 0
                        player1_gold = player1_gold - defen.cost
                if unit_rect.collidepoint(mouse_pos):
                    if build != 1:
                        if player1_gold > Defense.cost:
                            build = 1
                        else:
                            infotime = 20
                if D1_rect.collidepoint(mouse_pos):
                    if build != 2:
                        if player1_gold > D1.cost:
                            build = 2
                        else:
                            infotime = 20
                if Dk_rect.collidepoint(mouse_pos):
                    if build != 3:
                        if player1_gold > DK.cost:
                            build = 3
                        else:
                            infotime = 20
        for ene in enemies:
            if ene.health <= 0:
                player1_gold += 20
                difficulty += 1
        enemies = [ene for ene in enemies if ene.health > 0]
        defense = [de for de in defense if de.health > 0]
        if difficulty < 30:
            if random.randint(0, 100) > 94:
                ene = enemy(4, 550, 64, ene_image)
                enemies.append(ene)
        elif difficulty < 60:
            if random.randint(0, 100) > 97:
                ene = E2(4, 550, 64, ene_lv2)
                enemies.append(ene)
            elif random.randint(0, 100) < 5:
                ene = enemy(4, 550, 64, ene_image)
                enemies.append(ene)
        elif difficulty > 60:
            if random.randint(0, 100) > 98:
                ene = E3(4, 550, 64, ene_lv2)
                enemies.append(ene)
            elif random.randint(0, 100) < 5:
                ene = enemy(4, 550, 64, ene_image)
                enemies.append(ene)
            elif random.randint(0, 100) > 96:
                ene = E2(4, 550, 64, ene_lv3)
                enemies.append(ene)
        screen.fill((150, 200, 150))
        for field in fields:
            field.draw(screen)
        for fi in home:
            fi.draw(screen)
        for enem in enemies:

            for de in defense:
                if enem.rect.colliderect(de.rect):
                    de.health -= enem.attack
                    contact = 1
                    if de.property == 1:
                        if de.action == 0:
                            enem.health -= de.attack

            if contact == 0:
                enem.move()
            else:
                contact = 0
            enem.draw(screen)
            draw_enemy_health_bar(screen, enem.health, enem.rect)
        for bullet in bullets:
            for ene in enemies:
                if bullet.rect.colliderect(ene.rect):
                    ene.health -= 40
                    bullet.collide = 1
        bullets = [bullet for bullet in bullets if bullet.collide == 0]
        for de in defense:
            de.draw(screen)
            draw_health_bar(screen, de.health, de.rect)
            for ene in enemies:
                if ene.y == de.y:
                    inbound = 1
                    break
                else:
                    inbound = 0
                if de.rect.colliderect(ene.rect):
                    if de.property == 1:
                        if de.action == 0:
                            ene.health -= de.attack
            if inbound == 1:
                de.act()
                if de.action == 0:
                    if de.property == 0:
                        bullets.append(shoot(bullet_image, de.rect.topleft))

            else:
                de.action = 0

        for bullet in bullets:
            bullet.move()
            bullet.draw(screen)
        GAME_FONT.render_to(screen, (40, 20), "units: ", (200, 100, 120))
        GAME_FONT.render_to(screen, (300, 20), "fund: " + str(player1_gold), (200, 100, 120))
        if infotime > 0:
            if vaild == 0:
                text = "invalid position"
            elif fail == True:
                text = "u failed to protect ur home"
            else:
                text = "insufficient fund"
            GAME_FONT.render_to(screen, (200, 200), text, (200, 100, 120))
            infotime -= 1
        elif fail == True:
            done = True
        if fail == False:
            for enem in enemies:
                for f in home:
                    if enem.rect.colliderect(f.rect):
                        fail = True
                        infotime = 200

        screen.blit(unit_image, unit_rect)
        screen.blit(d1_image, D1_rect)
        screen.blit(dk_image, Dk_rect)
        frame_count += 1
        pygame.display.flip()
        pygame.event.peek()
        clock.tick(30)
    pygame.quit()
    sys.exit()
main()