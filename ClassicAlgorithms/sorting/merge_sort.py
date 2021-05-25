"""
A merge sort algorithm. Takes in an array and sorts it 'in place'.

Conceptually, a merge sort works as follows:
    - Divide the unsorted list into n sublists, each containing one element (a
      list of one element is considered sorted).
    - Repeatedly merge sublists to produce new sorted sublists until there is
      only one sublist remaining. This will be the sorted list.
"""


import random


def main():
    array_a = [num for num in range(1, 100)]
    random.shuffle(array_a)
    array_b = array_copy(array_a, 0, len(array_a))

    splitter(array_b, 0, len(array_a), array_a)

    for i in array_a:
        print(i)


# Returns a copy of array_a
def array_copy(array_a, start_index, end_index):
    return [array_a[index] for index in range(start_index, end_index)]


# Splitting arrays
def splitter(array_b, start_index, end_index, array_a):
    # Checking if the array is of size 1
    if end_index - start_index <= 1:
        return

    # Find the middle to split at
    middle_index = (start_index + end_index) // 2

    # Recursively sorting
    splitter(array_a, start_index, middle_index, array_b)
    splitter(array_a, middle_index, end_index, array_b)

    merger(array_b, start_index, middle_index, end_index, array_a)


def merger(array_a, start_index, middle_index, end_index, array_b):
    i = start_index
    j = middle_index
    # Merging while there are two arrays
    for k in range(i, end_index):
        # If left run head exists and is <= existing right run head
        if i < middle_index and (j >= end_index or array_a[i] <= array_a[j]):
            array_b[k] = array_a[i]
            i += 1
        else:
            array_b[k] = array_a[j]
            j += 1


if __name__ == '__main__':
    main()
