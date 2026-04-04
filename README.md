# Game Inventory Optimizer

A production-style web application for **Design and Analysis of Algorithms (DAA)** — **Semester IV, AIML** — that lets users manage a game-style inventory and run three classic algorithms on it: **0/1 Knapsack (DP)**, **Merge Sort (divide & conquer)**, and **Linear Search**.

## Team

| Name            | Roll No. |
|-----------------|----------|
| Rashi Karule    | 45       |
| Vishakha Adtani | 56       |
| Sankalp Jain    | 43       |

## Algorithms (brief)

### 1. 0/1 Knapsack — Dynamic Programming

Each item has a weight and value; capacity is limited. Each item can be taken **at most once**. The DP table `dp[i][w]` stores the maximum value obtainable using the first `i` items with capacity at most `w`. After filling the table, we **backtrack** from `dp[n][W]` to recover the chosen items.

- **Time complexity:** `O(n × W)` where `n` = items, `W` = capacity  
- **Space complexity:** `O(n × W)` (table)

### 2. Merge Sort — Divide & Conquer

Recursively split the list in half until trivially sortable, then **merge** two sorted halves by comparing the chosen key (`weight` or `value`). Implemented **without** Python’s `list.sort()` or `sorted()`. The API sorts in **descending** order (highest key first).

- **Time complexity:** `O(n log n)`  
- **Space complexity:** `O(n)` for merge buffers

### 3. Linear Search

Walk the list from the start; return the **first** item whose `name` **contains** the query string (**case-insensitive**).

- **Time complexity:** `O(n)`  
- **Space complexity:** `O(1)` extra space

## Project structure

```
game-inventory-optimizer/
├── backend/
│   ├── app.py                 # Flask app and routes
│   ├── algorithms/
│   │   ├── __init__.py
│   │   ├── knapsack.py        # 0/1 Knapsack DP + backtracking
│   │   ├── merge_sort.py      # Merge sort (no built-in sort)
│   │   └── linear_search.py   # Substring linear search
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── main.js
└── README.md
```

## Setup

### Backend (Flask — `http://127.0.0.1:5001`)

```bash
cd backend
pip install -r requirements.txt
python app.py
```

CORS is enabled for browser clients. The API listens on port **5001** by default (port **5000** is often reserved on Windows and can error with “socket … forbidden by its access permissions”). To use another port: `set PORT=8000` then `python app.py` (PowerShell: `$env:PORT=8000`).

### Frontend

**Option A — open the file (simplest)**  
Open `frontend/index.html` in a modern browser.  
**Note:** Some browsers restrict `file://` requests to `localhost`. If API calls fail, use Option B.

**Option B — local static server (recommended)**

```bash
cd frontend
python -m http.server 8080
```

Then visit `http://127.0.0.1:8080`. Ensure the backend is running so `main.js` can reach `http://127.0.0.1:5001` (change `API_BASE` in `frontend/main.js` if you use a custom `PORT`).

The UI preloads sample items (Excalibur, Dragon Shield, etc.) and default capacity **10 kg**.

## API reference

Base URL: `http://127.0.0.1:5001`

### `GET /health`

**Response:** `{ "status": "ok" }`

---

### `POST /optimize`

**Body (JSON):**

```json
{
  "capacity": 10,
  "items": [
    { "name": "Sword", "weight": 5, "value": 100 }
  ]
}
```

**Rules:** `capacity` must be a **whole number** `> 0`. `items` must be non-empty. Each item needs `name` (string), `weight`, `value` (non-negative numbers). For knapsack DP, **weights must be whole numbers**.

**Response:**

```json
{
  "selected_items": [...],
  "total_weight": 10,
  "total_value": 150
}
```

**Errors:** `400` with `{ "error": "message" }` for missing fields, invalid numbers, empty list, etc.

---

### `POST /sort`

**Body (JSON):**

```json
{
  "items": [...],
  "key": "value"
}
```

`key` is `"value"` or `"weight"`. Items must be non-empty and valid like `/optimize` (without whole-number weight requirement for sort).

**Response:** `{ "sorted_items": [...] }` (descending by `key`).

---

### `POST /search`

**Body (JSON):**

```json
{
  "items": [...],
  "name": "scroll"
}
```

**Response:** `{ "result": { "name", "weight", "value" } }` or `{ "result": null }` if not found.

---

All routes use `try/except`; unexpected server errors return `500` with `{ "error": "..." }`.

## Tech stack

- **Backend:** Python 3, Flask, Flask-CORS; algorithms in pure Python (no algorithm libraries).  
- **Frontend:** HTML, CSS, JavaScript (no UI framework); dark RPG-style glassmorphism; **Cinzel** + **Rajdhani** (Google Fonts).

## License / academic use

Built for coursework demonstration. Adapt freely for your lab submission with proper attribution to the team.
