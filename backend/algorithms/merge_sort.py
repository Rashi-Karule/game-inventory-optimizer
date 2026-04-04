"""
Merge Sort (Divide and Conquer) for lists of item dictionaries.

Divide: split the list into two halves until sublists have size 0 or 1.
Conquer: a single element is already sorted.
Combine: merge two sorted halves by repeatedly taking the larger front element
         (descending order by the chosen key).

We do not use Python's built-in list.sort() or sorted() — only explicit comparisons.

Time complexity: O(n log n) for all cases (unlike quicksort's worst case).
Space complexity: O(n) for the temporary merged arrays.
"""


def _merge(left, right, key, descending=True):
    """
    Merge two sorted lists into one sorted list.

    Both left and right are sorted by `key` in descending order if descending is True.
    """
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        a = left[i][key]
        b = right[j][key]
        # Descending: take the larger key first
        if descending:
            take_left = a >= b
        else:
            take_left = a <= b
        if take_left:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    # Remaining elements (one side exhausted)
    while i < len(left):
        result.append(left[i])
        i += 1
    while j < len(right):
        result.append(right[j])
        j += 1
    return result


def _merge_sort_recursive(arr, key, descending=True):
    """Recursively split, sort halves, and merge."""
    n = len(arr)
    # Base case: 0 or 1 element — already sorted
    if n <= 1:
        return list(arr)
    mid = n // 2
    # Divide
    left_half = _merge_sort_recursive(arr[:mid], key, descending)
    right_half = _merge_sort_recursive(arr[mid:], key, descending)
    # Conquer + combine
    return _merge(left_half, right_half, key, descending)


def merge_sort_items(items, key, descending=True):
    """
    Return a new list of items sorted by `key` ("weight" or "value").

    Default order is descending (highest first), as typical for "best items first" UIs.

    Args:
        items: list of dicts with numeric fields for `key`
        key: "weight" or "value"
        descending: if True, sort high to low

    Returns:
        New list (original list is not mutated).
    """
    # Shallow copy so we never mutate caller's dicts
    copies = [{**item} for item in items]
    return _merge_sort_recursive(copies, key, descending)
