# ⚔️ Game Inventory Optimizer

> A web app that lets you manage a game inventory and run classic algorithms on it — built for **Design and Analysis of Algorithms (DAA)**, Sem IV, B. Tech AIML.

---

## 👥 Team

| Name | Roll No. |
|------|----------|
| Rashi Karule | C1_A3_45 |
| Vishakha Adtani | C1_A4_56 |
| Sankalp Jain | C1_A3_43 |

🔗 **GitHub:** [github.com/Rohit-998/DAA_Project](https://github.com/Rohit-998/DAA_Project)

---

## ⚡ What It Does

Add items (name, weight, value) to your inventory and run 3 algorithms on them:

| Feature | Algorithm | What it does |
|---------|-----------|--------------|
| ⚡ Optimize | 0/1 Knapsack (DP) | Picks best items within a weight limit |
| ↕ Sort | Merge Sort | Sorts items by weight or value |
| 🔍 Search | Linear Search | Finds an item by name |

---

## 🛠️ Tech Stack

- **Backend** — Python + Flask (REST API)
- **Frontend** — HTML, CSS, JavaScript (dark RPG theme)
- **Algorithms** — implemented from scratch, no libraries

---

## 🚀 How to Run

> You need **Python** installed. That's it.

### Step 1 — Download the project

Click the green **Code** button on GitHub → **Download ZIP** → Extract it

---

### Step 2 — Start the backend

Open a terminal in the project folder and run:

```bash
cd backend
pip install -r requirements.txt
python app.py
```

✅ You should see: `Running on http://127.0.0.1:5001`

> Keep this terminal open.

---

### Step 3 — Start the frontend

Open a **second terminal** and run:

```bash
cd frontend
python -m http.server 8080
```

---

### Step 4 — Open the app

Go to your browser and visit:

```
http://127.0.0.1:8080
```

🎮 App is live!

---

## 📁 Folder Structure

```
game-inventory-optimizer/
├── backend/
│   ├── app.py                  ← Flask server
│   ├── requirements.txt
│   └── algorithms/
│       ├── knapsack.py         ← 0/1 Knapsack (DP)
│       ├── merge_sort.py       ← Merge Sort
│       └── linear_search.py   ← Linear Search
└── frontend/
    ├── index.html
    ├── style.css
    └── main.js
```

---

## 🔌 API Endpoints

Base URL: `http://127.0.0.1:5001`

| Method | Endpoint | What it does |
|--------|----------|--------------|
| POST | `/optimize` | Runs Knapsack on items |
| POST | `/sort` | Sorts items by key |
| POST | `/search` | Searches item by name |
| GET | `/health` | Check if server is running |

---

## 🧠 Algorithms

**0/1 Knapsack** — Fills a DP table of size n×W, then backtracks to find selected items. Time: `O(n × W)`

**Merge Sort** — Recursively splits and merges. No built-in sort used. Time: `O(n log n)`

**Linear Search** — Scans each item, case-insensitive match. Time: `O(n)`

---

## ⚠️ Common Issues

**Port 5000 blocked on Windows?**
The app uses port `5001` by default to avoid this. If 5001 is also blocked:
```powershell
$env:PORT = "8000"
python app.py
```
Then update `API_BASE` in `frontend/main.js` to match.

---

*Built with Flask + vanilla JS · DAA Lab Project*
