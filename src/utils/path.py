import math

class Path():
    def __init__(self, winWidth, winHeight, startX, startY):
        self.winWidth = winWidth
        self.winHeight = winHeight
        self.trackWidth = 64
        self.startX = startX
        self.startY = startY
        self.tiles = []
        self.border_segments = []

        self.createPath()

    def add_border(self, start, end):
        #if (start == end): return
        self.border_segments.append((start, end))

    def get_middle_of_tile(self, location, direction):
        print(self.startX, location[0])
        x = location[0] + direction[0] * self.trackWidth + 15.5
        y = location[1] + direction[1] * self.trackWidth - 15.5
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


    def check_border_collision(self, entity_lines):
        for entity_line in entity_lines:
            for border_segment in self.border_segments:
                result = self.intersect(entity_line, border_segment)
                if (result != None):
                    return True

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

    # def line_intersection(self, line1, line2):
    #     # line: ((startx, endx), (startY, endY))
    #     dx = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    #     dy = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    #     def determinant(a, b):
    #         return a[0] * b[1] - a[1] * b[0]

    #     div = determinant(dx, dy)
        
    #     if div == 0:
    #         # no intersection
    #         return False

    #     print(div)

    #     d = (determinant(*line1), determinant(*line2))
    #     x = determinant(d, dx) / div
    #     y = determinant(d, dy) / div
    #     return (x, y)
