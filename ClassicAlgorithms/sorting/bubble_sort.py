"""
A bubble sort algorithm.
"""

import random


def main():
    unsorted_array = [random.randint(0, 1000) for _ in range(100)]
    sorted_array = bubble_sort(unsorted_array)
    print("Sorted array:\n")
    for index in range(len(sorted_array)):
        print(f"\t {index + 1} --> {sorted_array[index]}")


def bubble_sort(lst):
    sorted_lst = list.copy(lst)
    is_sorted = False
    if len(lst) < 2:
        return sorted_lst
    while not is_sorted:
        has_switched = False
        for i in range(len(lst) - 1):
            if sorted_lst[i] > sorted_lst[i + 1]:
                temp = sorted_lst[i + 1]
                sorted_lst[i + 1] = sorted_lst[i]
                sorted_lst[i] = temp
                has_switched = True
        if not has_switched:
            break
    return sorted_lst


if __name__ == '__main__':
    main()
