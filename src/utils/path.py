import math
import pyglet

class Path():
    def __init__(self, winWidth, winHeight, startX, startY):
        self.winWidth = winWidth
        self.winHeight = winHeight
        self.trackWidth = 64
        self.startX = startX
        self.startY = startY
        self.tiles = []
        self.border_segments = []
        self.checkpoint_lines = []

        self.createPath()

    def add_border(self, start, end):
        #if (start == end): return
        self.border_segments.append((start, end))

    def get_middle_of_tile(self, location, direction):
        # pyglet draws stuff off by 15.5 in each direction for some reason
        x = location[0] + direction[0] * self.trackWidth/2 - 15.5
        y = location[1] + direction[1] * self.trackWidth/2 - 15.5


        return (x, y, direction)
        

    def createPath(self):
        directions = ["forward", "forward", "forward", "forward", "right", "right", "left", "left","right","forward","forward","forward","left","right", "forward", "forward", "right","forward", "forward", "right","forward","forward","forward","left","forward", "forward", "right","forward", "forward", "forward", "forward", "right"]
        
        curr_facing_x = 0
        curr_facing_y = 1

        segment_start_right_x = self.startX + self.trackWidth
        segment_start_right_y = self.startY
        segment_start_left_x = self.startX
        segment_start_left_y = self.startY

        curr_right_x = self.startX+ self.trackWidth
        curr_right_y = self.startY
        curr_left_x = self.startX 
        curr_left_y = self.startY


        count = 0

        for direction in directions:
            count+=1

            self.tiles.append((direction, self.get_middle_of_tile(((curr_right_x + curr_left_x) / 2, (curr_right_y + curr_left_y) / 2), (curr_facing_x, curr_facing_y))))

            if (direction == "forward"):
                dx = curr_facing_x * self.trackWidth
                dy = curr_facing_y * self.trackWidth

                curr_right_x += dx
                curr_right_y += dy
                curr_left_x += dx
                curr_left_y += dy

                if (count == len(directions)):
                    self.add_border((segment_start_left_x, segment_start_left_y), (curr_left_x, curr_left_y))
                    self.add_border((segment_start_right_x, segment_start_right_y), (curr_right_x, curr_right_y))

            elif (direction == "left"):
                # update left side
                self.add_border((segment_start_left_x, segment_start_left_y), (curr_left_x, curr_left_y))
                segment_start_left_x = curr_left_x
                segment_start_left_y = curr_left_y

                # go to end of right side
                curr_right_x += curr_facing_x * self.trackWidth
                curr_right_y += curr_facing_y * self.trackWidth

                self.add_border((segment_start_right_x, segment_start_right_y), (curr_right_x, curr_right_y))

                # create new segement
                segment_start_right_x = curr_right_x
                segment_start_right_y = curr_right_y

                # rotate curr_facing left
                if (curr_facing_y == 0):
                    curr_facing_y = curr_facing_x
                    curr_facing_x = 0
                else:
                    curr_facing_x = -curr_facing_y
                    curr_facing_y = 0

                curr_right_x += curr_facing_x * self.trackWidth
                curr_right_y += curr_facing_y * self.trackWidth

                # if last tile, clean up
                if (count == len(directions)):
                    self.add_border((segment_start_left_x, segment_start_left_y), (curr_left_x, curr_left_y))
                    self.add_border((segment_start_right_x, segment_start_right_y), (curr_right_x, curr_right_y)) 


            elif (direction == "right"):
                # update right side
                self.add_border((segment_start_right_x, segment_start_right_y), (curr_right_x, curr_right_y))
                segment_start_right_x = curr_right_x
                segment_start_right_y = curr_right_y

                # go to end of left side
                curr_left_x += curr_facing_x * self.trackWidth
                curr_left_y += curr_facing_y * self.trackWidth

                self.add_border((segment_start_left_x, segment_start_left_y), (curr_left_x, curr_left_y))

                # create new segement
                segment_start_left_x = curr_left_x
                segment_start_left_y = curr_left_y


                if (curr_facing_x == 0):
                    curr_facing_x = curr_facing_y
                    curr_facing_y = 0
                else:
                    curr_facing_y = -curr_facing_x
                    curr_facing_x = 0

                # add finish last bit of barrier
                curr_left_x += curr_facing_x * self.trackWidth
                curr_left_y += curr_facing_y * self.trackWidth

                # if last tile, clean up
                if (count == len(directions)):
                    self.add_border((segment_start_left_x, segment_start_left_y), (curr_left_x, curr_left_y))
                    self.add_border((segment_start_right_x, segment_start_right_y), (curr_right_x, curr_right_y)) 

            elif (direction == "slant_right"):
                pass
            elif (direction == "slant_left"):
                pass
            else:
                raise Exception("undefined direction")

            self.checkpoint_lines.append(((curr_right_x, curr_right_y), (curr_left_x, curr_left_y)))


    def check_border_collision(self, entity_lines):
        for entity_line in entity_lines:
            for border_segment in self.border_segments:
                result = self.intersect(entity_line, border_segment)
                if (result != None):
                    return result

    def get_road_sprites(self, batch=None, group=None):
        spritesheet = pyglet.image.load('assets/spritesheet_tiles.png')
        images = []
        road_sprites = []
        
        images.append(spritesheet.get_region(640, spritesheet.height-1664, 128, 128))
        images.append(spritesheet.get_region(640, spritesheet.height-1664 - 128, 128, 128))

        images.append(spritesheet.get_region(640, spritesheet.height-1664 + 128, 128, 128))
        images.append(spritesheet.get_region(640, spritesheet.height-1664 + 128 * 3, 128, 128))
        images.append(spritesheet.get_region(640 - 128 * 2, spritesheet.height-1664 + 128 * 3, 128, 128))
        images.append(spritesheet.get_region(640 - 128 * 2, spritesheet.height-1664 + 128, 128, 128))
        images.append(spritesheet.get_region(0, 0, 128, 128))


        for image in images:
            image.anchor_x = self.trackWidth // 2
            image.anchor_y = self.trackWidth // 2

        for tile in self.tiles:
            # i hate everything about this
            if (tile[0] == "forward" and tile[1][2][0] == 0):
                new_tile_img = images[1]
            elif (tile[0] == "forward" and tile[1][2][0] != 0):
                new_tile_img = images[0]
            elif (tile[0] == 'right' and tile[1][2][1] == 1):
                new_tile_img = images[2]
            elif (tile[0] == 'right' and tile[1][2][1] == -1):
                new_tile_img = images[4]
            elif (tile[0] == 'left' and tile[1][2][1] == -1):
                new_tile_img = images[5]
            elif (tile[0] == 'left' and tile[1][2][1] == 1):
                new_tile_img = images[3]
            elif (tile[0] == 'right' and tile[1][2][0] == -1):
                new_tile_img = images[5]
            elif (tile[0] == 'right' and tile[1][2][0] == 1):
                new_tile_img = images[3]
            elif (tile[0] == 'left' and tile[1][2][0] == 1):
                new_tile_img = images[4]
            elif (tile[0] == 'left' and tile[1][2][0] == -1):
                new_tile_img = images[2]
            else:
                # something is wrong
                new_tile_img = images[6]

            new_tile = pyglet.sprite.Sprite(new_tile_img, tile[1][0], tile[1][1], batch=batch, group=group)
            new_tile.scale = self.trackWidth/128
            new_tile.rotation = 0
            road_sprites.append(new_tile)

        return road_sprites

    def intersect(self, line1, line2):
        # algorithm inspired by kylemcdonald
        x1,y1 = line1[0]
        x2,y2 = line1[1]
        x3,y3 = line2[0]
        x4,y4 = line2[1]
        denom = (y4-y3)*(x2-x1) - (x4-x3)*(y2-y1)
        if denom == 0: # parallel
            return None
        ua = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / denom
        if ua < 0 or ua > 1: # out of range
            return None
        ub = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / denom
        if ub < 0 or ub > 1: # out of range
            return None
        x = x1 + ua * (x2-x1)
        y = y1 + ua * (y2-y1)
        return (x,y)


