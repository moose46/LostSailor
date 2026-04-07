"""https://nostarch.com/download/realWorldPython_errata_p3.pdf"""
import itertools

"""https://nostarch.com/real-world-python"""
import random
import sys

import cv2 as cv
import numpy as np

MAP_FILE = 'cape_python.png'

SA1_CORNERS = (130, 265, 180, 315)  # (UL-X, UL-Y,LR-X,LR-Y)
SA2_CORNERS = (80, 255, 130, 305)  # (UL-X, UL-Y,LR-X,LR-Y)
SA3_CORNERS = (105, 205, 155, 255)  # (UL-X, UL-Y,LR-X,LR-Y)


class Search:
    def __init__(self, name):
        self.name = name
        self.img = cv.imread(MAP_FILE, cv.IMREAD_COLOR)
        if self.img is None:
            print(f'{self.name} has not been loaded')
            sys.exit(-1)
        self.area_actual = 0
        self.sailor_actual = [0, 0]  # as local coords within search area
        self.sa1 = self.img[SA1_CORNERS[1]:SA1_CORNERS[3], SA1_CORNERS[0]:SA1_CORNERS[2]]
        self.sa2 = self.img[SA2_CORNERS[1]:SA2_CORNERS[3], SA2_CORNERS[0]:SA2_CORNERS[2]]
        self.sa3 = self.img[SA3_CORNERS[1]:SA3_CORNERS[3], SA3_CORNERS[0]:SA3_CORNERS[2]]
        self.p1 = .2
        self.p2 = .5
        self.p3 = .3

        self.sep1 = 0
        self.sep2 = 0
        self.sep3 = 0

    def draw_map(self, last_known):
        """display basemap with scale, last_known xy location, search areas"""
        cv.line(self.img, (20, 370), (70, 370), (0, 0, 0), 2)
        cv.putText(self.img, '0', (8, 370), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2)
        cv.putText(self.img, '50 Nautical Miles', (71, 370), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))

        cv.rectangle(self.img, (SA1_CORNERS[0], SA1_CORNERS[1]), (SA1_CORNERS[2], SA1_CORNERS[3]), (0, 0, 0), 1)
        cv.putText(self.img, '1', (SA1_CORNERS[0] + 3, SA1_CORNERS[1] + 15), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), )

        cv.rectangle(self.img, (SA2_CORNERS[0], SA2_CORNERS[1]), (SA2_CORNERS[2], SA2_CORNERS[3]), (0, 0, 0), 1)
        cv.putText(self.img, '2', (SA2_CORNERS[0] + 3, SA2_CORNERS[1] + 15), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), )

        cv.rectangle(self.img, (SA3_CORNERS[0], SA3_CORNERS[1]), (SA3_CORNERS[2], SA3_CORNERS[3]), (0, 0, 0), 1)
        cv.putText(self.img, '3', (SA3_CORNERS[0] + 3, SA3_CORNERS[1] + 15), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), )

        cv.putText(self.img, '+', last_known, cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), )
        cv.putText(self.img, '+ = Last Known Position', (274, 355), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), )
        cv.putText(self.img, '* = Actual Position', (275, 370), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), )

        cv.imshow("Search Area", self.img)
        cv.moveWindow("Search Area", 750, 10)
        cv.waitKey(15000)

    def sailor_final_location(self, num_search_areas):
        """ return the actual x,y location of the missing sailor."""
        self.sailor_actual[0] = np.random.choice(self.sa1.shape[1], )
        self.sailor_actual[1] = np.random.choice(self.sa1.shape[0], )

        area = int(random.triangular(1, num_search_areas, num_search_areas + 1))

        if area == 1:
            x = self.sailor_actual[0] + SA1_CORNERS[0]
            y = self.sailor_actual[1] + SA1_CORNERS[1]
            self.area_actual = 1
        elif area == 2:
            x = self.sailor_actual[0] + SA2_CORNERS[0]
            y = self.sailor_actual[1] + SA2_CORNERS[1]
            self.area_actual = 2
        elif area == 3:
            x = self.sailor_actual[0] + SA3_CORNERS[0]
            y = self.sailor_actual[1] + SA3_CORNERS[1]
            self.area_actual = 3
        return x, y

    def calc_search_effectiveness(self):
        """Set decimal search effectiveness value per search area"""
        self.sep1 = random.uniform(0.2, 0.9)
        self.sep2 = random.uniform(0.2, 0.9)
        self.sep3 = random.uniform(0.2, 0.9)

    def conduct_search(self,area_num,area_array,effectiveness_prob):
        """Return search results and list of search coordinates"""
        local_y_range = range(area_array.shape[0])
        local_x_range = range(area_array.shape[1])

        coords = list(itertools.product(local_x_range, local_y_range))
        random.shuffle(coords)
        coords = coords[:int((len(coords) * effectiveness_prob))]
        loc_actual = (self.sailor_actual[0], self.sailor_actual[1])
        if area_num == self.area_actual and self.loc_actual in coords:
            return f"Found in Area {area_num}", coords
        else:
            return f"Not Found in Area {area_num}", coords

def main():
    search = Search('cape_python.png')
    search.draw_map(last_known=(160, 290))
    sailor_x, sailor_y = search.sailor_final_location(num_search_areas=3)


if __name__ == '__main__':
    main()
