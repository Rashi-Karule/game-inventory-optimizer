"""
Flask API for Game Inventory Optimizer — DAA lab demo.
"""

import os

from flask import Flask, request, jsonify
from flask_cors import CORS

from algorithms.knapsack import solve_knapsack
from algorithms.merge_sort import merge_sort_items
from algorithms.linear_search import linear_search

app = Flask(__name__)
CORS(app)


def _bad(msg):
    return jsonify({"error": msg}), 400


def _is_number(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def _is_non_negative_whole_number(x):
    if not _is_number(x):
        return False
    if x < 0:
        return False
    if isinstance(x, float) and not x.is_integer():
        return False
    return True


def _validate_item(obj, idx=None):
    prefix = f"items[{idx}]: " if idx is not None else ""
    if not isinstance(obj, dict):
        return _bad(prefix + "each item must be an object")
    if "name" not in obj:
        return _bad(prefix + "missing field: name")
    if "weight" not in obj:
        return _bad(prefix + "missing field: weight")
    if "value" not in obj:
        return _bad(prefix + "missing field: value")
    if not isinstance(obj["name"], str):
        return _bad(prefix + "name must be a string")
    if not _is_number(obj["weight"]) or obj["weight"] < 0:
        return _bad(prefix + "weight must be a non-negative number")
    if not _is_number(obj["value"]) or obj["value"] < 0:
        return _bad(prefix + "value must be a non-negative number")
    return None


@app.route("/health", methods=["GET"])
def health():
    try:
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/optimize", methods=["POST"])
def optimize():
    try:
        data = request.get_json(silent=True)
        if data is None:
            return _bad("Expected JSON body")
        if "capacity" not in data:
            return _bad("missing field: capacity")
        if "items" not in data:
            return _bad("missing field: items")
        cap = data["capacity"]
        items = data["items"]
        if not _is_number(cap) or cap <= 0:
            return _bad("capacity must be a number greater than 0")
        if not isinstance(items, list) or len(items) == 0:
            return _bad("items must be a non-empty list")
        if not _is_non_negative_whole_number(cap):
            return _bad("capacity must be a whole number for knapsack DP")
        for i, it in enumerate(items):
            err = _validate_item(it, i)
            if err:
                return err
            if not _is_non_negative_whole_number(it["weight"]):
                return _bad(f"items[{i}]: weight must be a whole number for knapsack DP")

        result = solve_knapsack(items, int(cap))
        return jsonify(
            {
                "selected_items": result["selected_items"],
                "total_weight": result["total_weight"],
                "total_value": result["total_value"],
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/sort", methods=["POST"])
def sort_items():
    try:
        data = request.get_json(silent=True)
        if data is None:
            return _bad("Expected JSON body")
        if "items" not in data:
            return _bad("missing field: items")
        if "key" not in data:
            return _bad("missing field: key")
        items = data["items"]
        key = data["key"]
        if not isinstance(items, list) or len(items) == 0:
            return _bad("items must be a non-empty list")
        if key not in ("value", "weight"):
            return _bad('key must be "value" or "weight"')
        for i, it in enumerate(items):
            err = _validate_item(it, i)
            if err:
                return err

        sorted_items = merge_sort_items(items, key, descending=True)
        return jsonify({"sorted_items": sorted_items})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/search", methods=["POST"])
def search():
    try:
        data = request.get_json(silent=True)
        if data is None:
            return _bad("Expected JSON body")
        if "items" not in data:
            return _bad("missing field: items")
        if "name" not in data:
            return _bad("missing field: name")
        items = data["items"]
        name = data["name"]
        if not isinstance(items, list) or len(items) == 0:
            return _bad("items must be a non-empty list")
        if not isinstance(name, str):
            return _bad("name must be a string")
        for i, it in enumerate(items):
            err = _validate_item(it, i)
            if err:
                return err

        found = linear_search(items, name)
        if found is None:
            return jsonify({"result": None})
        # Return a plain dict snapshot for JSON
        return jsonify(
            {
                "result": {
                    "name": found["name"],
                    "weight": found["weight"],
                    "value": found["value"],
                }
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Default 5001: on many Windows setups port 5000 is reserved (Hyper-V / excluded ranges)
    # and fails with "socket forbidden by its access permissions".
    port = int(os.environ.get("PORT", "5001"))
    app.run(host="127.0.0.1", port=port, debug=True)
