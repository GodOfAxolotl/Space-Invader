import pygame

pygame.init()

# window creation
win = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('data/Enemy.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
score = 0
level = 0
curr_bullet = 0
button_unpressed = True


class Bullet:
    bulletIMG = pygame.transform.scale(pygame.image.load('data/bullet.png'), (32, 32))

    def __init__(self):
        self.x_pos = 0
        self.y_pos = 480
        self.y_vel = 5
        self.x_acc = 0
        self.y_acc = 10
        self.state = False

    def fire_bullet(self, x, y):
        self.state = True
        win.blit(self.bulletIMG, (x + 16, y - 32))

    def get_mask(self):
        return pygame.mask.from_surface(self.bulletIMG)


class Player:
    playerIMG = pygame.transform.scale(pygame.image.load("data/Player.png"), (64, 64))

    def __init__(self):
        self.x_pos = 370
        self.y_pos = 480
        self.x_vel = 0
        self.x_acc = 10

    def player(self, x, y):
        win.blit(self.playerIMG, (x, y))

    def get_mask(self):
        return pygame.mask.from_surface(self.playerIMG)


class Enemy:
    enemyIMG = pygame.transform.scale(pygame.image.load("data/Enemy2.png"), (64, 64))
    enemy2IMG = pygame.transform.scale(pygame.image.load("data/Enemy3.png"), (64, 64))
    enemy3IMG = pygame.transform.scale(pygame.image.load("data/Enemy4.png"), (64, 64))
    enemy4IMG = pygame.transform.scale(pygame.image.load("data/Enemy5.png"), (64, 64))
    enemy5IMG = pygame.transform.scale(pygame.image.load("data/Enemy6.png"), (64, 64))
    enemyBossIMG = pygame.transform.scale(pygame.image.load("data/EnemyBoss.png"), (128, 64))

    def __init__(self, x, y, h):
        self.x_pos = x
        self.y_pos = y
        self.x_vel = 5
        self.x_acc = 5
        self.y_acc = 64
        self.health = h
        self.bossShield = 0

        if self.health > 5:
            self.bossShield = self.health - 5
            self.health = 5

        self.images = {
            0: self.enemyIMG,
            1: self.enemy2IMG,
            2: self.enemy3IMG,
            3: self.enemy4IMG,
            4: self.enemy5IMG,
            5: self.enemyBossIMG,
        }

    def enemy(self, x, y):
        if self.bossShield == 0:
            win.blit(self.images[self.health], (x, y))
        else:
            win.blit(self.images[5], (x, y))

    def get_mask(self):
        return pygame.mask.from_surface(self.enemyIMG)

class EnemyBunch:
    pass

bullets = []
player = Player()
enemys = []

for i in range(0, 20):
    y = int(i / 5) + 1
    x = i % 5
    enemys.append(Enemy(x * 80, y * 64 - 150, 0))


def is_collision(bul, enm):
    enemy_mask = bul.get_mask()
    bullet_mask = enm.get_mask()

    offset = (enm.x_pos - bul.x_pos, enm.y_pos - round(bul.y_pos))

    point = enemy_mask.overlap(bullet_mask, offset)

    if point:
        return True

    return False


# Game Loop
running = True
while running:
    clock.tick(60)
    win.fill((15, 0, 85))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.x_vel = -player.x_acc
                button_unpressed = False
            if event.key == pygame.K_RIGHT:
                player.x_vel = player.x_acc
                button_unpressed = False
            if event.key == pygame.K_SPACE and button_unpressed and curr_bullet < 3:
                bullets.append(Bullet())
                bullets[curr_bullet].x_pos = player.x_pos
                bullets[curr_bullet].fire_bullet(bullets[curr_bullet].x_pos, bullets[curr_bullet].y_pos)
                curr_bullet += 1
                button_unpressed = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_SPACE:
                player.x_vel = 0
                button_unpressed = True

    player.x_pos += player.x_vel
    if player.x_pos >= win.get_width() - 64:
        player.x_pos = win.get_width() - 64
    elif player.x_pos < 0:
        player.x_pos = 0

    for enemy in enemys:
        enemy.x_pos += enemy.x_vel
        if enemy.x_pos >= win.get_width() - 64:
            enemy.x_pos = win.get_width() - 64
            enemy.x_vel = -enemy.x_acc
            enemy.y_pos += enemy.y_acc
        elif enemy.x_pos < 0:
            enemy.x_pos = 0
            enemy.x_vel = enemy.x_acc
            enemy.y_pos += enemy.y_acc
    for bullet in bullets:
        if bullet.state:
            bullet.fire_bullet(bullet.x_pos, bullet.y_pos)
            bullet.y_pos -= bullet.y_acc
            if bullet.y_pos < 0:
                bullet.y_pos = player.y_pos
                bullet.state = False
                bullets.remove(bullet)
                curr_bullet -= 1
        for enemy in enemys:
            if is_collision(bullet, enemy):
                bullet.y_pos = player.y_pos
                bullet.state = False
                bullets.remove(bullet)
                curr_bullet -= 1
                if enemy.bossShield > 0:
                    enemy.bossShield -= 1
                else:
                    enemy.health -= 1
                if enemy.health < 0:
                    score += 1
                    print(score)
                    enemys.remove(enemy)

    player.player(player.x_pos, player.y_pos)
    for enemy in enemys:
        enemy.enemy(enemy.x_pos, enemy.y_pos)
    pygame.display.flip()
    pygame.display.update()

    if not enemys:
        level += 1
        if level == 1:
            enemys.append(Enemy(3 * 80, 2 * 64 - 150, 15))
        else:
            for i in range(0, 20):
                y = int(i / 5) + 1
                x = i % 5
                if level == 1:
                    enemys.append(Enemy(x * 80, y * 64 - 150, 1))
                elif level == 2:
                    enemys.append(Enemy(x * 80, y * 64 - 150, 2))
                elif level == 3:
                    enemys.append(Enemy(x * 80, y * 64 - 150, 3))
                else:
                    enemys.append(Enemy(x * 80, y * 64 - 150, 4))
