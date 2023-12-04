import sys
import math
import pyglet

class TileMap():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.trackWidth = 64

        self.tilemap = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 3, 1, 6, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 2, 0, 2, 0, 3, 1, 1, 1, 1, 6, 0],
                [0, 2, 0, 5, 1, 4, 0, 0, 0, 0, 2, 0],
                [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
                [0, 2, 0, 0, 0, 0, 3, 1, 6, 0, 2, 0],
                [0, 5, 1, 1, 1, 1, 4, 0, 5, 1, 4, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    def idx_from_pt(self, pt):
        return (len(self.tilemap) - 1 - int(pt[1] / self.trackWidth), int(pt[0] / self.trackWidth))

    def in_bounds(self, vertices):
        for vertex in vertices:
            normalized_vertex = self.idx_from_pt(vertex)
            if (not self.idx_in_bounds(normalized_vertex) or self.tilemap[normalized_vertex[0]][normalized_vertex[1]] == 0):
                return False

        return True

    def idx_in_bounds(self, idx):
        return idx[0] >= 0 and idx[0] < len(self.tilemap) and idx[1] >= 0 and idx[1] < len(self.tilemap[0])

    def dist_to_wall(self, dx, dy, vertices, width, height, rot):
        dist = 0
        step_size = 10

        vertices = list(map(list, vertices))

        while(self.in_bounds(vertices)):
            for vertex in vertices:
                vertex[0] += dx * step_size
                vertex[1] += dy * step_size

            dist += step_size

        return dist

    def dist_to_next_tile(self, next_tile, pos, center, vertices):
        dist = 0
        step_size = 4

        dx = center[0] - pos[0]
        dy = center[1] - pos[1]

        sum = abs(dx) + abs(dy)

        dx = dx / sum
        dy = dy / sum

        vertices = list(map(list, vertices))
        i = 0
        while(True):
            for vertex in vertices:
                normalized_vertex = self.idx_from_pt(vertex)
                if normalized_vertex == next_tile:
                    return self.trackWidth - dist
                else:
                    vertex[0] += dx * step_size
                    vertex[1] += dy * step_size
            dist += step_size

            

    def get_tile_center(self, idx):
        x = idx[1] * self.trackWidth + self.trackWidth / 2
        y = self.height - (idx[0] * self.trackWidth + self.trackWidth / 2)

        return (x, y)
        
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
            image.anchor_x = 0
            image.anchor_y = self.trackWidth * 2

        for row, row_arr in enumerate(self.tilemap):
            for col, tile in enumerate(row_arr):
                # i hate everything about this
                new_tile_img = -1

                if tile == 1:
                    new_tile_img = images[0]
                elif tile == 2:
                    new_tile_img = images[1]
                elif tile == 3:
                    new_tile_img = images[2]
                elif tile == 4:
                    new_tile_img = images[4]
                elif tile == 5:
                    new_tile_img = images[5]
                elif tile == 6:
                    new_tile_img = images[3]

                if new_tile_img != -1:
                    new_tile = pyglet.sprite.Sprite(new_tile_img, col * self.trackWidth, self.height - row * self.trackWidth, batch=batch, group=group)
                    new_tile.scale = self.trackWidth/128
                    new_tile.rotation = 0
                    road_sprites.append(new_tile)

        return road_sprites
        


