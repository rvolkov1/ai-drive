import pyglet
import math
import numpy as np

class Car(pyglet.sprite.Sprite):
    def __init__(self, network=None, batch=None, group=None):
        car_img = pyglet.image.load("assets/cars.png").get_region(241, 0, 72, 39)
        car_img.anchor_x = car_img.width // 2
        car_img.anchor_y = car_img.height // 2
        super().__init__(car_img, batch=batch, group=group)

        self.x = 130
        self.y = 100
        self.dx = 0
        self.dy = 0
        self.speed = 300
        self.scale = 0.5
        self.rotation_speed = 150
        self.rotation = -90
        self.isWrecked = False
        self.sensor_rays = []
        self.intersections = []
        self.next_checkpoint = 0
        self.num_laps = 0
        self.network = network


    def update(self, keys, path, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt
            
        self.keyboard_input(keys, dt)
        self.ai_input(path, dt)
        self.update_checkpoints(path)

        self.apply_drag(dt)
        self.apply_traction(dt)
        self.apply_rotation(keys, dt)

    def update_checkpoints(self, path):
        curr_checkpoint_line = path.checkpoint_lines[self.next_checkpoint]

        for line in self.calculate_car_lines():
            if (path.intersect(line, curr_checkpoint_line)):
                if (self.next_checkpoint < len(path.checkpoint_lines)-1):
                    self.next_checkpoint += 1
                else:
                    self.num_laps += 1
                    self.next_checkpoint = 0
                print(self.next_checkpoint)
                return

    def calculate_fitness(self, path):
        point_1, point_2 = path.checkpoint_lines[self.next_checkpoint]
        mid_x = (point_1[0] + point_2[0]) / 2
        mid_y = (point_1[1] + point_2[1]) / 2

        distance_to_next_checkpoint = math.dist((self.x, self.y), (mid_x, mid_y))

        self.network.fitness = self.num_laps * len(path.checkpoint_lines) * path.trackWidth + self.next_checkpoint * path.trackWidth - distance_to_next_checkpoint

    def ai_input(self, path, dt):
        inputs = self.get_sensor_data(path)

    def get_sensor_data(self, path):
        # shoot a 8 lines out at interval of pi/4 radians and get the distance of the closest border they intersect

        ray_length = 1000 # must be longer than any distance on the screen
        self.intersections = []
        self.sensor_rays = []

        rotation = - self.rotation

        for angle in np.arange(rotation, rotation + 360, 10):
            theta = math.radians(angle)
            x_sign = -1 if math.cos(theta) >= 0 else 1
            y_sign = -1 if math.sin(theta) >= 0 else 1

            line = ((self.x, self.y), (self.x + ray_length * x_sign, self.y + ray_length * abs(math.tan(theta)) * y_sign))
            self.sensor_rays.append(pyglet.shapes.Line(line[0][0], line[0][1], line[1][0], line[1][1]))

            closest_intersection = None

            for line_segment in path.border_segments:
                intersection = path.check_border_collision([line])

                if (intersection == None): continue
                if (closest_intersection == None or math.floor(math.dist(intersection, (self.x, self.y))) < math.floor(closest_intersection)):
                    closest_intersection = math.floor(math.dist(intersection, (self.x, self.y)))
            
            self.intersections.append(intersection)

        return self.intersections


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


        # car_lines.append(((self.x - self.height/2, self.y - self.width/2), (self.x + self.height/2, self.y - self.width/2)))
        
        # car_lines.append(((self.x - self.height/2, self.y - self.width/2), (self.x - self.height/2, self.y + self.width/2)))

        # car_lines.append(((self.x + self.height/2, self.y - self.width/2), (self.x + self.height/2, self.y + self.width/2)))

        return car_lines

        




    


