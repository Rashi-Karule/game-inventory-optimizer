"""
Linear Search through a list of items by name.

Scans the list from the start; returns the first item whose name contains
the search term (case-insensitive substring match).

Time complexity: O(n) in the worst case (must scan entire list).
Space complexity: O(1) extra space.
"""


def linear_search(items, search_term):
    """
    Find the first item where item['name'] contains search_term (case-insensitive).

    Args:
        items: list of dicts with a "name" string field
        search_term: string to look for inside names

    Returns:
        The matching item dict, or None if no match.
    """
    if search_term is None:
        return None
    needle = str(search_term).lower()
    if needle == "":
        return None
    for item in items:
        name = item.get("name")
        if name is None:
            continue
        if needle in str(name).lower():
            return item
    return None
