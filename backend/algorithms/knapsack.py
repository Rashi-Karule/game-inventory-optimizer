"""
0/1 Knapsack via Dynamic Programming.

We have n items, each with weight w_i and value v_i, and a knapsack capacity W.
Each item can be taken at most once (0/1). Maximize total value without exceeding W.

Time complexity: O(n * W) where n = number of items, W = capacity.
Space complexity: O(n * W) for the DP table (can be reduced to O(W) with rolling array).
"""


def solve_knapsack(items, capacity):
    """
    Solve 0/1 knapsack using a 2D DP table.

    dp[i][w] = maximum achievable value using only the first i items
               with total weight at most w.

    Args:
        items: list of dicts with keys "name", "weight", "value"
        capacity: non-negative integer knapsack capacity

    Returns:
        dict with keys:
            selected_items: list of chosen item dicts (original objects not required; we rebuild dicts)
            total_weight: sum of weights of selected items
            total_value: sum of values of selected items
    """
    n = len(items)
    weights = [int(items[i]["weight"]) for i in range(n)]
    values = [int(items[i]["value"]) for i in range(n)]
    W = int(capacity)

    # Base case: dp[0][w] = 0 for all w (no items → no value)
    # Rows 1..n correspond to considering items 0..n-1
    # dp[i][w] uses first i items (indices 0 .. i-1)
    dp = [[0] * (W + 1) for _ in range(n + 1)]

    # Fill the table: for each item count i and each capacity w
    for i in range(1, n + 1):
        item_weight = weights[i - 1]
        item_value = values[i - 1]
        for w in range(W + 1):
            # Option 1: do not take item (i-1) → best value is same as with i-1 items
            best = dp[i - 1][w]
            # Option 2: take item (i-1) only if it fits (w >= item_weight)
            if w >= item_weight:
                # Value = value of this item + best value for remaining capacity with fewer items
                take = item_value + dp[i - 1][w - item_weight]
                if take > best:
                    best = take
            dp[i][w] = best

    # Backtrack from dp[n][W] to recover which items were selected
    selected_indices = []
    w = W
    for i in range(n, 0, -1):
        # If value changed from row i-1 to row i at capacity w, item i-1 was included
        if dp[i][w] != dp[i - 1][w]:
            selected_indices.append(i - 1)
            w -= weights[i - 1]

    selected_indices.reverse()
    selected_items = [
        {
            "name": items[idx]["name"],
            "weight": items[idx]["weight"],
            "value": items[idx]["value"],
        }
        for idx in selected_indices
    ]
    total_weight = sum(items[idx]["weight"] for idx in selected_indices)
    total_value = sum(items[idx]["value"] for idx in selected_indices)

    return {
        "selected_items": selected_items,
        "total_weight": total_weight,
        "total_value": total_value,
    }
