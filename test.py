# class Solution:
#     def computeArea(self, ax1: int, ay1: int, ax2: int, ay2: int, bx1: int, by1: int, bx2: int, by2: int) -> int:
#         self.ax1 = ax1
#         self.ay1 = ay1
#         self.ax2 = ax2
#         self.ay2 = ay2
#
#         self.bx1 = bx1
#         self.by1 = by1
#         self.bx2 = bx2
#         self.by2 = by2
#
#         length_rect_1 = self.ax1 - self.ax2
#         width_rect_1 = self.ay1 - self.ay2
#         area_rect_1 = length_rect_1 * width_rect_1
#
#         length_rect_2 = self.bx1 -  self.bx2
#         width_rect_2 = self.by1 - self.by2
#
#         area_rect_2 = length_rect_2 * width_rect_2
#
#         return(area_rect_1,area_rect_2)


def computeArea( ax1: int, ay1: int, ax2: int, ay2: int, bx1: int, by1: int, bx2: int, by2: int) -> int:
    # ax1 = ax1
    # self.ay1 = ay1
    # self.ax2 = ax2
    # self.ay2 = ay2
    #
    # self.bx1 = bx1
    # self.by1 = by1
    # self.bx2 = bx2
    # self.by2 = by2

    length_rect_1 = ax1 - ax2
    width_rect_1 = ay1 - ay2
    area_rect_1 = length_rect_1 * width_rect_1

    length_rect_2 = bx1 -  bx2
    width_rect_2 = by1 - by2

    area_rect_2 = length_rect_2 * width_rect_2

    print(area_rect_1,area_rect_2)
    # Input: ax1 = -3, ay1 = 0, ax2 = 3, ay2 = 4, bx1 = 0, by1 = -1, bx2 = 9, by2 = 2
computeArea(-3,0,3, 4,0, -1, 9, 2)