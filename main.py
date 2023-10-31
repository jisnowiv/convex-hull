#!usr/bin/env python

"""convexHull.py: Finds the convex hull of a set of 2D points using the gift wrap algorithm (December 2015)
    or the graham scan algorithm (July 2021)"""

__author__ = 'John Snow'

import utility
import random
from math import atan2

DEBUGMODE = True


# If debug mode is enabled, print whatever string (or array) is passed
def debug_print(string):
    if DEBUGMODE:
        print(string)


# Calculates the polar angle (in radians) between two (x, y) points
def polar_angle(anchor, p):
    y_span = anchor[1] - p[1]
    x_span = anchor[0] - p[0]
    return atan2(y_span, x_span)


TURN_LEFT, TURN_RIGHT, TURN_NONE = (1, -1, 0)


# Returns turn direction of three points
def ccw(a, b, c):
    res = (b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])

    if res > 0:
        return TURN_LEFT
    if res == 0:
        return TURN_NONE
    else:
        return TURN_RIGHT


class Hull:
    def __init__(self):
        self.points = []
        self.num = 0
        self.hull = []

    def print_points(self):
        if len(self.points) == 0:
            print("The set is empty")
        else:
            print("The points in the set are:")
            for p in range(len(self.points)):
                print("[" + str(self.points[p][0]) + ", " + str(self.points[p][1]) + "]")

    def print_hull(self):
        if len(self.hull) == 0:
            print("The hull is empty")
        else:
            print("The hull has the following points:")
            for h in range(len(self.hull)):
                if len(self.hull[h]) > 2:
                    print(self.hull[h][:-1])
                else:
                    print(self.hull[h])

    def add_point(self, p):
        self.points.append(p)
        self.num += 1

    @staticmethod
    def orient_num(a, b, point):
        return ((point[0] - a[0]) * (b[1] - a[1])) - ((point[1] - a[1]) * (b[0] - a[0]))

    def orient_bool(self, a, b, point):
        r = self.orient_num(a, b, point)
        if r > 0 or r == 0:
            return True
        else:
            return False

    def graham_scan(self):
        #   There shouldn't be any points in the hull, but clear it all the same
        self.hull.clear()

        debug_print("Entering Graham Scan")

        #   find the lowest y-coordinate and leftmost point, called p0
        p0 = self.points[0]
        for p in self.points:
            if p[1] < p0[1]:
                p0 = p
            elif p[1] == p0[1] and p[0] < p0[0]:
                p0 = p

        debug_print("Anchor Point:")
        debug_print(p0)

        self.hull.append(p0)

        debug_print("Points before sort:")
        debug_print(self.points)

        points_and_angles = []

        for p in self.points:
            # calculate the polar angle w/ p0 (anchor point)
            angle = polar_angle(p0, p)
            points_and_angles.append([p, angle])

        points_and_angles.sort(key=lambda x: x[1])

        debug_print("Points and angles after sort:")
        debug_print(points_and_angles)

        for point in points_and_angles:
            if point[0] == p0:
                continue
            debug_print(point)
            #   append each point to the hull (treated as a stack)
            self.hull.append(point[0])
            #   if the last three points in the hull form a clockwise turn, the middle point is not on the hull
            while len(self.hull) > 2 and ccw(self.hull[-3], self.hull[-2], self.hull[-1]) == TURN_RIGHT:
                #   pop the second to last point on the hull
                debug_print("Popping a point")
                debug_print(self.hull[-3])
                debug_print(self.hull[-2])
                debug_print(self.hull[-1])
                self.hull.pop(-2)

    def gift_wrap(self):
        if len(self.points) < 3:
            print("There must be at least 3 points")
            return

        # Sort the points in the set by their x coordinate
        self.points = utility.merge_sort(self.points, 0)
        debug_print(self.points)

        idx = 0
        next_idx = 0

        while True:
            for j in range(len(self.points)):
                continue_condition = False

                if j == idx:
                    continue

                for k in range(len(self.points)):
                    if k == j or k == idx:
                        continue

                    res = self.orient_bool(self.points[idx], self.points[j], self.points[k])

                    if not res:
                        continue_condition = True
                        break

                if continue_condition:
                    continue
                else:
                    self.hull.append(self.points[j])
                    next_idx = j

            idx = next_idx

            if idx == 0:
                break


if __name__ == "__main__":
    ch = Hull()

    ch.print_points()

    choice = input('Would you like debug print statements?\n\t(1) Yes\n\t(2) No\n')
    DEBUGMODE = choice == '1'

    choice = input('Would you like random points or pre-programmed?\n\t(1) Random\n\t(2) Pre-programmed\n')
    if choice == '1':
        print("random")

        choice = input('How many points would you like to generate? (at least 3)')

        count = int(choice)

        ch.points = [(random.randint(0, 100), random.randint(0, 100)) for i in range(count)]

    else:
        # Expected hull contains:
        #       [10, 1] [5, 12.4] [3, 11] [2, 5] [11, 10]
        ch.add_point([2, 5])
        ch.add_point([6.7, 6])
        ch.add_point([7, 5.4])
        ch.add_point([11, 10])
        ch.add_point([3, 11])
        ch.add_point([10, 1])
        ch.add_point([5, 12.4])
        ch.add_point([10, 7])
        ch.add_point([5, 8])

    ch.print_points()
    ch.print_hull()

    choice = input('How would you like to compute the convex hull?\n\t(1) Gift Wrap\n\t(2) Graham Scan\n')

    if choice == '1':
        ch.gift_wrap()
        ch.print_hull()
    elif choice == '2':
        ch.graham_scan()
        ch.print_hull()
    else:
        print("Invalid choice, exiting now.")
