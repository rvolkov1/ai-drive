import pyglet
from aiDrive.src.utils.car import Car
from aiDrive.src.utils.path import Path
from aiDrive.src.utils.map import TileMap

class app_window(pyglet.window.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.drawLines = False
        self.drawSprites = True
        self.cars = []
        self.keys = pyglet.window.key.KeyStateHandler()
        self.map = TileMap(self.width, self.height)
        self.batch = pyglet.graphics.Batch()
        self.checkpoint_gates = []

    def create_new_generation(self, neural_networks):
        self.cars = []
        self.keys = pyglet.window.key.KeyStateHandler()
        self.batch = pyglet.graphics.Batch()
        self.checkpoint_gates = []
        self.road_sprites = []
        color = (255, 255, 255)

        self.road_group = pyglet.graphics.OrderedGroup(0)
        self.car_group = pyglet.graphics.OrderedGroup(1)

        for network in neural_networks:
            car = Car(network=network, batch=self.batch, group=self.car_group)
            self.cars.append(car)

        if (self.drawSprites):
            self.road_sprites = self.map.get_road_sprites(batch=self.batch, group=self.road_group)

    def on_draw(self):
        self.clear()
        #print("batch", self.batch)
        self.batch.draw()    

    def update(self, dt):
        count = 0
        for car in self.cars:
            car.update(self.keys, self.map, dt)
            
    def on_key_press(self, symbol, modifiers):
        self.keys[symbol] = True

    def on_key_release(self, symbol, modifiers):
        self.keys.pop(symbol)
    

