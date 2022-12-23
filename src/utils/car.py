import pyglet
import math

class Car(pyglet.sprite.Sprite):
    def __init__(self, batch=None, group=None):
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

    def update(self, keys, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt
            
        self.keyboard_input(keys, dt)

        self.apply_drag(dt)
        self.apply_traction(dt)
        self.apply_rotation(keys, dt)

    def ai_input(self, dt):
        inputs = self.get_sensor_data()

    # def get_sensor_data():
    #     # shoot a bunch of lines out of the car and return the distance until they hit a border wall

        

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
    

        




    


