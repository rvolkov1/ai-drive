import pyglet
from aiDrive.src.utils.car import Car
from aiDrive.src.utils.path import Path
import datetime

class app_window(pyglet.window.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.drawLines = True
        self.drawSprites = False
        self.init_objects()

    def init_objects(self):
        self.cars = []
        self.keys = pyglet.window.key.KeyStateHandler()
        self.path = Path(width, height, 100, 100)
        self.batch = pyglet.graphics.Batch()
        self.barrier_lines = []
        self.car_lines = []
        self.road_sprites = []
        color = (255, 255, 255)

        self.road_group = pyglet.graphics.OrderedGroup(0)
        self.car_group = pyglet.graphics.OrderedGroup(1)

        car = Car(batch=self.batch, group=self.car_group)

        self.cars.append(car)

        if (self.drawSprites):
            self.road_sprites = self.path.get_road_sprites(batch=self.batch, group=self.road_group)

            
        if (self.drawLines):
            for line in self.path.border_segments:
                self.barrier_lines.append(pyglet.shapes.Line(line[0][0], line[0][1], line[1][0], line[1][1], color=color, batch=self.batch, group=self.road_group))
            
            for car in self.cars:
                for line in car.calculate_car_lines():
                    self.car_lines.append(pyglet.shapes.Line(line[0][0], line[0][1], line[1][0], line[1][1], color=color, batch=self.batch, group=self.car_group))

    def on_draw(self):
        self.clear()
        self.batch.draw()    

    def update(self, dt):
        count = 0
        for car in self.cars:
            if (not car.isWrecked):
                car.update(self.keys, dt)
            
            car_lines = car.calculate_car_lines()

            if (self.drawLines):
                for line in car_lines:
                    self.car_lines[count].x = line[0][0]
                    self.car_lines[count].y = line[0][1]
                    self.car_lines[count].x2 = line[1][0]
                    self.car_lines[count].y2 = line[1][1]
                    count += 1

            if (self.path.check_border_collision(car_lines) != None):
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
