import pygame, random

pygame.init()

noquit = 1
version = "a.1"
window = pygame.display.set_mode([600, 600])
pygame.display.set_caption("RoghtEngine Free License " + version)

objects = []
actors = []
cursor = [0,0]
mode = "editor"
cursor_tile = 40
camera = [0,0]

class block_collision:
    def __init__(self, ix, iy, w):
        self.x = 0
        self.y = 0
        self.ix = ix
        self.iy = iy
        self.size = 40
        self.image = pygame.image.load("block.png")
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.w = w
        self.class_name = "block"
        pass
    
    def draw(self):
        self.x = (self.ix + camera[0])
        self.y = (self.iy + camera[1])
        self.w.blit(self.image, (self.x, self.y))
        if mode == "play":
            self.collision()
        pass
    
    def collision(self):
        for o in actors:
            col = o.x + o.size >= self.x and o.x <= self.x + self.size and o.y + o.size >= self.y and o.y <= self.y + self.size
            k = pygame.key.get_pressed()
            if col:
                if o.velx > 0 and o.x < self.x + self.size:
                    o.x -= o.vel
                elif o.velx < 0 and o.x + o.size > self.x:
                    o.x += o.vel
            if col:
                if o.vely > 0 and o.y < self.y + self.size:
                    o.y -= o.vel
                    o.on_floor = True
                elif o.vely < 0 and o.y + o.size > self.y:
                    o.y += o.vel
            
        pass

class Cursor:
    def __init__(self, ix, iy, w):
        self.ix = ix
        self.iy = iy
        self.x = 0
        self.y = 0
        self.image = pygame.image.load("cursor.png")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.w = w
        pass
    
    def draw(self):
        self.x = (self.ix + camera[0] + cursor[0])
        self.y = (self.iy + camera[1] + cursor[1])
        self.w.blit(self.image, (self.x, self.y))
        self.cursor_icon()
        pass
    
    def cursor_icon(self):
        if mode == "editor":
            self.image = pygame.image.load("cursor.png")
            self.image = pygame.transform.scale(self.image, (40, 40))
        elif mode == "play":
            self.image = pygame.image.load("cursor_play.png")
            self.image = pygame.transform.scale(self.image, (40, 40))
        pass

class actor:
    def __init__(self, x, y, w, class_name):
        self.x = x
        self.y = y
        self.size = 40
        self.image = pygame.image.load("actor.png")
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.w = w
        self.g = 1
        self.velx = 0
        self.vely = 0
        self.vel = 2
        self.class_name = class_name
        self.on_floor = False
        self.sheets = 1
        self.j = 80
        pass
    
    def draw(self):
        if mode == "play":
            if self.class_name == "platformer":
                self.vely = self.g
            self.x += self.velx
            self.y += self.vely
            self.controls()
            self.flip()
        self.w.blit(self.image, (self.x, self.y))
        self.move_cam()
        pass
    
    def flip(self):
        if self.velx > 0:
            self.image = pygame.image.load("actor.png")
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        elif self.velx < 0:
            self.image = pygame.image.load("actor_flip.png")
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        pass
    
    def controls(self):
        if self.class_name == "top-down":
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                self.velx = -self.vel
            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                self.velx = self.vel
            else:
                self.velx = 0
                
            if pygame.key.get_pressed()[pygame.K_UP]:
                self.vely = -self.vel
            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                self.vely = self.vel
            else:
                self.vely = 0
        elif self.class_name == "platformer":
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                self.velx = -self.vel
            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                self.velx = self.vel
            else:
                self.velx = 0
                
            if pygame.key.get_pressed()[pygame.K_UP]:
                if self.on_floor == True:
                    self.y = (self.y - (self.j ** 1.0))
                    self.on_floor = False
        pass
    
    def move_cam(self):
        if self.x >= 600 - 160:
            camera[0] -= self.vel
            self.x -= self.vel
        elif self.x <= 160:
            camera[0] += self.vel
            self.x += self.vel
        
        if self.y >= 600 - 160:
            camera[1] -= self.vel
            self.y -= self.vel
        elif self.y <= 160:
            camera[1] += self.vel
            self.y += self.vel
        pass

c = Cursor(cursor[0], cursor[1], window)
print("[info] = Start RoghtEngine -> Free License")

while noquit:
    window.fill([0, 0, 0])
    
    #DRAW OBJECTS ON THE LISTS
    for o in objects:
        o.draw()
    for o in actors:
        o.draw()
    
    #DRAW CURSOR
    c.draw()
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            noquit = 0
        
        #SWITCH MODES
        if pygame.key.get_pressed()[pygame.K_q] and mode == "editor":
            mode = "play"
        elif pygame.key.get_pressed()[pygame.K_q] and mode == "play":
            mode = "editor"
        
        if mode == "editor":
            #KEYS TO ADD OBJS
            if pygame.key.get_pressed()[pygame.K_a]:
                objects.append(block_collision(cursor[0] , cursor[1], window))
                print("[info] new obj -> block_collision")
                
            elif pygame.key.get_pressed()[pygame.K_b]:
                for o in objects:
                    if o.x == cursor[0] and o.y == cursor[1]:
                        objects.remove(o)
                        print("[WARN] obj in " + str(cursor) + " deleted on the scene")
                for a in actors:
                    if a.x == cursor[0] and a.y == cursor[1]:
                        actors.remove(a)
                        print("[WARN] actor removed on the scene")
                
            elif pygame.key.get_pressed()[pygame.K_n]:
                act = actor(cursor[0], cursor[1], window, "platformer")
                if not act in objects:
                    actors.append(act)
                    print("[info] new obj -> actor:top-down")
            
            #MOVE CURSOR EDITOR
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                cursor[0] -= cursor_tile
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                cursor[0] += cursor_tile
            if pygame.key.get_pressed()[pygame.K_UP]:
                cursor[1] -= cursor_tile
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                cursor[1] += cursor_tile
    
    pygame.display.flip()