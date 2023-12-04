import pyglet
import math
import numpy as np

class Car(pyglet.sprite.Sprite):
    def __init__(self, network=None, batch=None, group=None):
        car_img = pyglet.image.load("assets/cars.png").get_region(241, 0, 72, 39)
        car_img.anchor_x = car_img.width // 2
        car_img.anchor_y = car_img.height // 2
        super().__init__(car_img, batch=batch, group=group)

        self.x = 100
        self.y = 200
        self.startX = 100
        self.startY = 200
        self.dx = 0
        self.dy = 0
        #self.width = car_img.width
        #self.height = car_img.height
        self.speed = 300
        self.scale = 0.5
        self.rotation_speed = 150
        self.rotation = -90
        self.wrecked = False
        self.sensor_rays = []
        self.direction_vector = ((-1,0), (0, 1), (1,0), (0, -1))
        self.direction_idx = 0
        self.curr_tile = None
        self.checkpoints_passed = 0
        self.network = network


    def update(self, keys, map, dt):
        if (self.wrecked or self.check_if_wrecked(map)): return

        curr_tile = map.idx_from_pt((self.x, self.y))

        if (self.curr_tile is None):
            self.curr_tile = curr_tile
        elif (curr_tile == (self.curr_tile[0] + self.direction_vector[self.direction_idx][0], self.curr_tile[1] + self.direction_vector[self.direction_idx][1])):
            self.curr_tile = curr_tile
            self.checkpoints_passed += 1

            if self.direction_idx == 0:
                self.direction_idx = 3
            else:
                self.direction_idx -= 1

            while (map.tilemap[curr_tile[0] + self.direction_vector[self.direction_idx][0]][curr_tile[1] + self.direction_vector[self.direction_idx][1]] == 0):
                self.direction_idx += 1
                self.direction_idx %= 4

            #print(self.direction_idx)

        self.x += self.dx * dt
        self.y += self.dy * dt
            
        #self.keyboard_input(keys, dt)
        self.ai_input(map, dt)
        #self.update_checkpoints(map)
        self.calculate_fitness(map)

        #print(self.network.fitness)

        self.apply_drag(dt)
        self.apply_traction(dt)
        #self.apply_rotation(keys, dt)

    def check_if_wrecked(self, map):
        if (not map.in_bounds(self.get_vertices())):
            self.wrecked = True

        return self.wrecked

    def calculate_fitness(self, map):
        curr_tile = map.idx_from_pt((self.x, self.y))
        next_tile = (curr_tile[0] + self.direction_vector[self.direction_idx][0], curr_tile[1] + self.direction_vector[self.direction_idx][1])
        next_tile_center = map.get_tile_center(next_tile)

        #d = math.dist((self.x, self.y), next_tile_center)

        dist_to_next = map.dist_to_next_tile(next_tile, (self.x, self.y), next_tile_center, self.get_vertices())

        #print("d", int(dist_to_next))
        self.network.fitness = self.checkpoints_passed * 64 #+ dist_to_next
        #print(int(self.network.fitness))
        #print(self.network.fitness)


        #self.network.fitness = math.dist((self.x, self.y), (self.startX, self.startY))
#        point_1, point_2 = path.checkpoint_lines[self.next_checkpoint]
#        mid_x = (point_1[0] + point_2[0]) / 2
#        mid_y = (point_1[1] + point_2[1]) / 2
#
        #distance_to_next_checkpoint = math.dist((self.x, self.y), (mid_x, mid_y))

        #self.network.fitness = self.num_laps * len(path.checkpoint_lines) * path.trackWidth + self.next_checkpoint * path.trackWidth - distance_to_next_checkpoint

    def ai_input(self, map, dt):
        inputs = self.get_sensor_data(map)
        inputs = self.flatten_inputs(inputs)

        if inputs.shape != (9,): return
        outputs = self.network.forward_propagation(inputs)

        direction = 0.5 - outputs[0]

        self.dx += direction * math.cos(math.radians(self.rotation)) * self.speed * dt
        self.dy += - direction * math.sin(math.radians(self.rotation)) * self.speed * dt

        self.rotation += outputs[1] * self.rotation_speed * dt

    def flatten_inputs(self, inputs):
        return np.asarray(inputs).flatten()

    def get_sensor_data(self, map):
        # shoot a 8 lines out at interval of pi/4 radians and get the distance of the closest border they intersect
        sensor_data = []

        normalization_factor = max(map.width, map.height) # value to use to normalize all input values to model

        sensor_data.append(self.x / map.width)
        sensor_data.append(self.y / map.height)
        sensor_data.append(abs(self.rotation) % 360 / 360)

        rotation = - self.rotation

        for angle in np.linspace(rotation - 90, rotation + 90, num=6):
            dx = math.cos(math.radians(angle))
            dy = math.sin(math.radians(angle))

            dist_to_wall = map.dist_to_wall(dx, dy, self.get_vertices(), self.width, self.height, self.rotation)

            #print("dist_to_wall", dist_to_wall)

            sensor_data.append(dist_to_wall / normalization_factor)

        return sensor_data


    def keyboard_input(self, keys, dt):
        if (keys[pyglet.window.key.UP]):
            self.dx += math.cos(math.radians(self.rotation)) * self.speed * dt
            self.dy += -math.sin(math.radians(self.rotation)) * self.speed * dt
        elif (keys[pyglet.window.key.DOWN]):
            self.dx += -math.cos(math.radians(self.rotation)) * self.speed * dt
            self.dy += math.sin(math.radians(self.rotation)) * self.speed * dt


    def apply_rotation(self, keys, dt):
        #if (self.dx <= 1 and self.dy <= 1): return

        if (keys[pyglet.window.key.RIGHT]):
            self.rotation += self.rotation_speed * dt
        if (keys[pyglet.window.key.LEFT]):
            self.rotation += -self.rotation_speed * dt


    def apply_traction(self, dt):
        # traction forces
        moving_direction = math.atan2(self.dy, self.dx)
        #if (moving_direction < 0): moving_direction = abs(moving_direction) + math.pi

        facing_direction = math.pi*2 - math.radians(self.rotation) % (math.pi * 2)
        if (facing_direction == math.pi*2): facing_direction = 0

        facing_direction = self.normalize_angle(facing_direction)
        moving_direction = self.normalize_angle(moving_direction)

        drift_constant = 10

        dot_product = abs(math.cos(abs(facing_direction - moving_direction))) * 1/drift_constant + (drift_constant - 1) / drift_constant

        dot_product *= (1-dt)

        self.dx = dot_product * self.dx 
        self.dy = dot_product * self.dy 


    def normalize_angle(self, angle):
        # returns respective angle in first quadrant

        if (angle > math.pi):
            angle = math.pi - (math.pi*2 - angle)

        return angle


    def apply_drag(self, dt):
        drag_coefficient = 0.99

        drag_factor = (1 - drag_coefficient * dt)

        self.dx *= drag_factor
        self.dy *= drag_factor

    def rotate_point(self, point):
        # xprime = xcos(theta) - ysin(theta)
        # yprime = ycos(theta) + xsin(theta)
        x = point[0] - self.x
        y = point[1] - self.y
        theta = math.radians(-self.rotation + 90)

        new_x = x * math.cos(theta) - y * math.sin(theta)
        new_y = x * math.sin(theta) + y * math.cos(theta)

        return (self.x + new_x, self.y + new_y)

    def calculate_car_lines(self):
        # get 4 line segments which represent the car
        car_lines = []

        # make hitbox more lenient
        hitbox_padding = 2
        hitbox_width = self.height/2 - hitbox_padding
        hitbox_height = self.width/2 - hitbox_padding

        top_left_x = self.x - hitbox_width
        top_left_y = self.y + hitbox_height

        top_right_x = self.x + hitbox_width
        top_right_y = self.y + hitbox_height

        bot_left_x = self.x - hitbox_width
        bot_left_y = self.y - hitbox_height

        bot_right_x = self.x + hitbox_width
        bot_right_y = self.y - hitbox_height


        new_top_left = self.rotate_point((top_left_x, top_left_y))
        new_top_right = self.rotate_point((top_right_x, top_right_y))
        new_bot_left = self.rotate_point((bot_left_x, bot_left_y))
        new_bot_right = self.rotate_point((bot_right_x, bot_right_y))       

        car_lines.append((new_top_right, new_top_left))
        car_lines.append((new_bot_right, new_bot_left))
        car_lines.append((new_top_right, new_bot_right))
        car_lines.append((new_top_left, new_bot_left))

    def get_vertices(self):
        hitbox_padding = 2
        hitbox_width = self.height/2 - hitbox_padding
        hitbox_height = self.width/2 - hitbox_padding

        top_left_x = self.x - hitbox_width
        top_left_y = self.y + hitbox_height

        top_right_x = self.x + hitbox_width
        top_right_y = self.y + hitbox_height

        bot_left_x = self.x - hitbox_width
        bot_left_y = self.y - hitbox_height

        bot_right_x = self.x + hitbox_width
        bot_right_y = self.y - hitbox_height


        new_top_left = self.rotate_point((top_left_x, top_left_y))
        new_top_right = self.rotate_point((top_right_x, top_right_y))
        new_bot_left = self.rotate_point((bot_left_x, bot_left_y))
        new_bot_right = self.rotate_point((bot_right_x, bot_right_y))       
        return (new_top_left, new_top_right, new_bot_left, new_bot_right)

        # car_lines.append(((self.x - self.height/2, self.y - self.width/2), (self.x + self.height/2, self.y - self.width/2)))
        
        # car_lines.append(((self.x - self.height/2, self.y - self.width/2), (self.x - self.height/2, self.y + self.width/2)))

        # car_lines.append(((self.x + self.height/2, self.y - self.width/2), (self.x + self.height/2, self.y + self.width/2)))

        return car_lines

        




    


