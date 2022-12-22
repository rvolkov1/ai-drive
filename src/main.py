import pyglet
from aiDrive.src.utils.car import Car
from aiDrive.src.utils.path import Path
import datetime

class app_window(pyglet.window.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.init_objects()

    def init_objects(self):
        self.cars = []
        self.keys = pyglet.window.key.KeyStateHandler()
        self.path = Path(width, height, 100, 100)
        self.batch = pyglet.graphics.Batch()
        self.barrier_lines = []
        self.road_sprites = []
        color = (255, 255, 255)

        self.road_group = pyglet.graphics.OrderedGroup(0)
        self.car_group = pyglet.graphics.OrderedGroup(1)

        car = Car(batch=self.batch, group=self.car_group)

        self.cars.append(car)
            
        for line in self.path.border_segments:
            self.barrier_lines.append(pyglet.shapes.Line(line[0][0], line[0][1], line[1][0], line[1][1], color=color, batch=self.batch))

        self.add_road_sprites_to_batch()

        
    def add_road_sprites_to_batch(self):
        spritesheet = pyglet.image.load('assets/spritesheet_tiles.png')
        forward_img = spritesheet.get_region(640, spritesheet.height-1664, 128, 128)
        turn_img = spritesheet.get_region(640, spritesheet.height-1664 + 128, 128, 128)

        forward_img.anchor_x = self.path.trackWidth // 2
        forward_img.anchor_y = self.path.trackWidth // 2
        turn_img.anchor_x = self.path.trackWidth // 2
        turn_img.anchor_y = self.path.trackWidth // 2

        for tile in self.path.tiles:
            if tile[0] != "forward":
                new_tile_img = turn_img
            else:
                new_tile_img = forward_img
                rotation = 0 if tile[1][2][0] != 0 else -90

            
            print(tile[1][0], tile[1][1])
            new_tile = pyglet.sprite.Sprite(new_tile_img, tile[1][0], tile[1][1], batch=self.batch, group=self.road_group)
            new_tile.scale = self.path.trackWidth/128
            new_tile.rotation = rotation
            self.road_sprites.append(new_tile)
            #raise Exception(tile[1][0], tile[1][1])

    def on_draw(self):
        self.clear()
        self.batch.draw()    



    def update(self, dt):
        for car in self.cars:
            if (not car.isWrecked):
                car.update(self.keys, dt)
            
            if (self.path.check_border_collision(car.calculate_car_lines()) != None):
                car.isWrecked = True



                


    def on_key_press(self, symbol, modifiers):
        self.keys[symbol] = True

    def on_key_release(self, symbol, modifiers):
        self.keys.pop(symbol)

if __name__ == '__main__':
    width, height = 800, 500
    window = app_window(width=width, height=height)
    pyglet.clock.schedule_interval(window.update, 1/60.0)  # update at 60Hz
    pyglet.app.run()
