import pygame as pg
import pytmx
pg.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
FPS = 80
TILE_SCALE = 2

font = pg.font.Font(None, 36)
class Platform(pg.sprite.Sprite):
    def __init__(self,image,x,y,width,height):
        super(Platform,self).__init__()
        self.image = pg.transform.scale(image,(width * TILE_SCALE,height * TILE_SCALE))
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SCALE
        self.rect.y = y * TILE_SCALE
        




class Player(pg.sprite.Sprite):
    def __init__(self, map_width, map_height):
        super(Player, self).__init__()
        self.load_animations()
        self.current_animation = self.idle_animatoins_left
        self.image = pg.Surface((50,50))
        self.image.fill("red")
        self.timer = pg.time.get_ticks()
        self.interval = 200
        self.rect = self.current_animation[0].get_rect()
        self.rect.center = (500, 50)  # Начальное положение персонажа
        self.rect_mini = pg.Rect([self.rect.x,self.rect.y],[self.rect.width / 1.5, self.rect.height / 1.5])
        self.current_image = 0
        # Начальная скорость и гравитация
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 2
        self.is_jumping = False
        self.map_width = map_width
        self.map_height = map_height
        self.hp = 10
        self.damage_timer = pg.time.get_ticks()
        self.damage_interval = 1000
        self.exp = pg.mixer.Sound("exp.wav")
    def load_animations(self):
        tile_size = 32
        tile_scale = 4
        self.idle_animatoins_right = []
        num_images = 5
        num_images_running = 6
        self.running_animatoins_right = []
        spritesheet = pg.image.load("maps/Sprites/Sprite Pack 3/3 - Robot J5/Idle (32 x 32).png")
        for i in range(num_images):
            x = i * tile_size
            y = 0
            rect = pg.Rect(x,y,tile_size,tile_size)
            image = spritesheet.subsurface(rect)
            image = pg.transform.scale(image, (tile_size * tile_scale,tile_size * tile_scale))
            self.idle_animatoins_right.append(image)
        self.idle_animatoins_left = []
        for image in self.idle_animatoins_right:
            self.idle_animatoins_left.append(pg.transform.flip(image, True,False))
        self.spritesheet_running = pg.image.load("maps/Sprites/Sprite Pack 3/3 - Robot J5/Walking (32 x 32).png")
        for i in range(num_images_running):
            x = i * tile_size
            y = 0
            rect = pg.Rect(x,y,tile_size,tile_size)
            image_running = self.spritesheet_running.subsurface(rect)
            image_running = pg.transform.scale(image_running, (tile_size * tile_scale,tile_size * tile_scale))
            self.running_animatoins_right.append(image_running)
        self.running_animatoins_left = [pg.transform.flip(image, True,False) for image in self.running_animatoins_right]
    
    def get_damage(self):
        if pg.time.get_ticks() - self.damage_timer > self.damage_interval:
            self.hp -= 1
            self.damage_timer = pg.time.get_ticks()
    

    
    def update(self, platforms):
        keys = pg.key.get_pressed()
        
        if keys[pg.K_SPACE] and not self.is_jumping:
            self.jump()
        
        if keys[pg.K_a]:
            if self.current_animation != self.running_animatoins_left:
                self.current_animation = self.running_animatoins_left
                self.current_image = 0
            self.velocity_x = -10
        
        elif keys[pg.K_d]:
            if self.current_animation != self.running_animatoins_right:
                self.current_animation = self.running_animatoins_right
                self.current_image = 0
            self.velocity_x = 10
        
        else:
            if self.current_animation == self.running_animatoins_right:
                self.current_animation = self.idle_animatoins_right
                self.current_image = 0
            elif self.current_animation == self.running_animatoins_left:
                self.current_animation = self.idle_animatoins_left
                self.current_image = 0
            self.velocity_x = 0
        
        new_x = self.rect.x + self.velocity_x
        if 0 <= new_x <= self.map_width - self.rect.width:
            self.rect.x = new_x


        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        self.rect_mini.midbottom = self.rect.midbottom
        for platform in platforms:

            if platform.rect.collidepoint(self.rect_mini.midbottom):
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.is_jumping = False
            if platform.rect.collidepoint(self.rect_mini.midtop):
                self.rect.top = platform.rect.bottom
                self.velocity_y = 0
            
            if platform.rect.collidepoint(self.rect_mini.midleft):
                self.rect.midleft = platform.rect.midright
                self.velocity_x = 0
                
            if platform.rect.collidepoint(self.rect_mini.midright):
                self.rect.midright = platform.rect.midleft
                self.velocity_x = 0
                
        
        if pg.time.get_ticks() - self.timer > self.interval:
            self.current_image += 1
            if self.current_image >= len(self.current_animation):
                self.current_image = 0
            self.image = self.current_animation[self.current_image]
            self.timer = pg.time.get_ticks()
        
        
    
    def jump(self):
        self.velocity_y = -25
        self.is_jumping = True
        


class Crab(pg.sprite.Sprite):
    def __init__(self, map_width, map_height):
        super(Crab, self).__init__()
        self.load_animations()
        self.current_animation = self.animation
        self.image = pg.Surface((50,50))
        self.image.fill("red")
        self.timer = pg.time.get_ticks()
        self.interval = 200
        self.rect = self.current_animation[0].get_rect()
        self.rect.center = (500, 50)  # Начальное положение персонажа
        self.rect_mini = pg.Rect([self.rect.x,self.rect.y],[self.rect.width / 1.5, self.rect.height / 1.5])
        self.current_image = 0
        self.left_edge = 50
        self.right_edge = 700
        # Начальная скорость и гравитация
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 2
        self.is_jumping = False
        self.map_width = map_width
        self.map_height = map_height
        self.direction = "left"

    def load_animations(self):
        tile_scale = 4
        tile_size = 32

        self.animation = []
        image = pg.image.load("maps/Sprites/Sprite Pack 3/9 - Snip Snap Crab/Movement_(Flip_image_back_and_forth) (32 x 32).png")
        image = pg.transform.scale(image, (tile_size * tile_scale,tile_size * tile_scale))
        self.animation.append(image)
        self.animation.append(pg.transform.flip(image, True, False))


    def update(self, platforms):
        

        if self.direction == "right":
            self.velocity_x = 5
            if self.rect.right >= self.right_edge:
                self.directoin == "left"
        elif self.direction == "left":
            self.velocity_x = -5
            if self.rect.left <= self.left_edge:
                self.direction == "right"





        new_x = self.rect.x + self.velocity_x
        if 0 <= new_x <= self.map_width - self.rect.width:
            self.rect.x = new_x


        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        self.rect_mini.midbottom = self.rect.midbottom
        for platform in platforms:

            if platform.rect.collidepoint(self.rect_mini.midbottom):
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.is_jumping = False
            if platform.rect.collidepoint(self.rect_mini.midtop):
                self.rect.top = platform.rect.bottom
                self.velocity_y = 0
            
            if platform.rect.collidepoint(self.rect_mini.midleft):
                self.rect.midleft = platform.rect.midright
                self.velocity_x = 0
                
            if platform.rect.collidepoint(self.rect_mini.midright):
                self.rect.midright = platform.rect.midleft
                self.velocity_x = 0
                
        
        if pg.time.get_ticks() - self.timer > self.interval:
            self.current_image += 1
            if self.current_image >= len(self.current_animation):
                self.current_image = 0
            self.image = self.current_animation[self.current_image]
            self.timer = pg.time.get_ticks()

class Ball(pg.sprite.Sprite):
    def __init__(self, player_rect, direction):
        super(Ball, self).__init__()

        self.direction = direction
        self.speed = 10
        self.image = pg.image.load("maps/Sprites/шар.png")
        self.image = pg.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        if self.direction == "right":
            self.rect.x = player_rect.right
        else:
            self.rect.x = player_rect.left
        self.rect.y = player_rect.centery
    def update(self):
        if self.direction == "right":
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
    



class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Платформер")
        self.setup()
    def setup(self):
        self.mode = "game"    
        self.clock = pg.time.Clock()
        self.is_running = False
        self.tmx_map = pytmx.load_pygame("maps/map.tmx")
        self.all_sprites = pg.sprite.Group()
        self.map_pixel_width = self.tmx_map.width * self.tmx_map.tilewidth * TILE_SCALE
        self.map_pixel_height = self.tmx_map.height * self.tmx_map.tileheight * TILE_SCALE
        self.enemies = pg.sprite.Group()
        self.player = Player(self.map_pixel_width,self.map_pixel_height)
        self.all_sprites.add(self.player)
        
        self.crab = Crab(self.map_pixel_width,self.map_pixel_height)
        self.all_sprites.add(self.crab)
        self.enemies.add(self.crab)
        self.bg = pg.image.load("Background_1.png")
        self.platforms = pg.sprite.Group()
        self.bg = pg.transform.scale(self.bg,(SCREEN_WIDTH, SCREEN_HEIGHT))
        self.player.hp = 3
        self.balls = pg.sprite.Group()
        
        
        # Остальной код класса
        self.camera_x = 0
        self.camera_y = 0
        self.camera_speed = 4

        for layer in self.tmx_map:
            for x, y, gid in layer:
                tile = self.tmx_map.get_tile_image_by_gid(gid)
                if tile:
                    platform = Platform(tile, x * self.tmx_map.tilewidth, y * self.tmx_map.tileheight, self.tmx_map.tilewidth, self.tmx_map.tileheight)
                    self.all_sprites.add(platform)
                    self.platforms.add(platform)


        self.run()

    def run(self):
        self.is_running = True
        while self.is_running:
            self.event()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pg.quit()
        quit()

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN: # нажатие на Enter (в pygame это pg.K_RETURN)
                    self.player.exp.play()
                    if self.player.current_animation in (self.player.idle_animatoins_right,self.player.running_animatoins_right):
                        direction = "right"
                    else:
                        direction = "left"
                    ball = Ball(self.player.rect, direction)
                    self.balls.add(ball)
                    self.all_sprites.add(ball)
            if self.mode == "game over":
                if event.type == pg.KEYDOWN:
                    self.setup()
        keys = pg.key.get_pressed()


    def update(self):
        if self.player.hp <= 0:
            self.mode = "game over"
            return
        
        
        for enemy in self.enemies.sprites():
            if pg.sprite.collide_mask(self.player, enemy):
                self.player.get_damage()
        
        
        self.player.update(self.platforms)
        self.crab.update(self.platforms)
        self.camera_x = self.player.rect.x - SCREEN_WIDTH // 2
        self.camera_y = self.player.rect.y - SCREEN_HEIGHT // 2
        self.balls.update()
        pg.sprite.groupcollide(self.balls, self.enemies, True, True)
        pg.sprite.groupcollide(self.balls, self.platforms, True, False)
        # self.camera_x = max(0, min(self.camera_x, self.map_pixel_width - SCREEN_WIDTH))
        # self.camera_y = max(0, min(self.camera_y, self.map_pixel_height - SCREEN_HEIGHT))
    def draw(self):
        self.screen.blit(self.bg,[0,0])
        #pg.draw.rect(self.screen,[0,0,0],self.player.rect_mini.move(-self.camera_x, -self.camera_y))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, sprite.rect.move(-self.camera_x, -self.camera_y))

        pg.draw.rect(self.screen, pg.Color("red"), (10, 10, self.player.hp * 10, 10))
        pg.draw.rect(self.screen,pg.Color("black"), (10,10,100,10), 1)
        if self.mode == "game over":
            txt = font.render("Вы проиграли", True, (255, 0, 0))
            txt_rect = txt.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(txt,txt_rect)
        
        
        
        pg.display.flip()


if __name__ == "__main__":
    game = Game()