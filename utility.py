#!usr/bin/env python

"""utility.py: An implementation of merge sort, ultimately used to find the 2D convex hull of a set of 2D points."""

__author__ = 'John Snow'
__date__ = 'Spring 2015'


def merge(array, array2, d):
    ret = []
    i = 0
    j = 0
    while i < len(array) or j < len(array2):
        if i == len(array):
            ret.append(array2[j])
            j += 1
        elif j == len(array2):
            ret.append(array[i])
            i += 1
        elif array[i][d] < array2[j][d]:
            ret.append(array[i])
            i += 1
        else:
            ret.append(array2[j])
            j += 1

    return ret


def merge_sort(array, d):
    if len(array) == 1:
        return array

    midpoint = int(len(array)/2)

    sub_a = array[0:midpoint]
    sub_b = array[midpoint:]

    sub_a = merge_sort(sub_a, d)
    sub_b = merge_sort(sub_b, d)

    return merge(sub_a, sub_b, d)


if __name__ == "__main__":
    a = [[4, 5], [5, 6], [9, 8], [7, 3]]
    print(merge_sort(a, 0))

    print(merge_sort(a, 1))

    print("\n")

    b = [[3, 1], [1, 4], [0, 0], [2, 2]]

    print(merge_sort(b, 0))

    print(merge_sort(b, 1))
