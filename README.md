# ⚔️ Game Inventory Optimizer

A full-stack web application that lets you manage a game inventory and run classic Design and Analysis of Algorithms (DAA) techniques on it — now fully deployed and accessible online.

🌐 **Live App:** https://game-inventory-optimizer.vercel.app/

---

## 👥 Team

| Name            | Roll No. |
| --------------- | -------- |
| Rashi Karule    | C1_A3_45 |
| Vishakha Adtani | C1_A4_56 |
| Sankalp Jain    | C1_A3_43 |

🔗 GitHub: https://github.com/Rashi-Karule/game-inventory-optimizer

---

## ⚡ Features

Add items (name, weight, value) and apply powerful algorithms:

| Feature    | Algorithm                          | Description                            |
| ---------- | ---------------------------------- | -------------------------------------- |
| ⚡ Optimize | 0/1 Knapsack (Dynamic Programming) | Selects best items within weight limit |
| ↕ Sort     | Merge Sort                         | Sorts items by weight or value         |
| 🔍 Search  | Linear Search                      | Finds item by name                     |

---

## 🛠️ Tech Stack

* **Frontend:** HTML, CSS, JavaScript (Dark RPG UI)
* **Backend:** Python (Flask REST API)
* **Algorithms:** Implemented from scratch (No libraries)
* **Deployment:**

  * Frontend → Vercel
  * Backend → Render

---

## 🚀 Live Architecture

```text
Frontend (Vercel) → API Calls → Backend (Render) → Algorithms
```

---

## 📁 Folder Structure

```
game-inventory-optimizer/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── algorithms/
│       ├── knapsack.py
│       ├── merge_sort.py
│       └── linear_search.py
└── frontend/
    ├── index.html
    ├── style.css
    └── main.js
```

---

## 🔌 API Endpoints

Base URL: https://game-inventory-optimizer.onrender.com

| Method | Endpoint  | Description            |
| ------ | --------- | ---------------------- |
| GET    | /health   | Check server status    |
| POST   | /optimize | Run Knapsack algorithm |
| POST   | /sort     | Sort items             |
| POST   | /search   | Search item by name    |

---

## 🧠 Algorithms Used

### 1. 0/1 Knapsack (Dynamic Programming)

* Time Complexity: **O(n × W)**
* Uses DP table and backtracking to select optimal items

### 2. Merge Sort

* Time Complexity: **O(n log n)**
* Divide and conquer sorting (no built-in sort used)

### 3. Linear Search

* Time Complexity: **O(n)**
* Sequential search with case-insensitive matching

---

## 🧪 Running Locally

### Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend

```bash
cd frontend
python -m http.server 8080
```

Open in browser:

```
http://127.0.0.1:8080
```

---

## ⚠️ Common Issues

* **Port issues (Windows):**

  * App uses port 5001 by default
* **CORS errors:**

  * Handled using Flask-CORS
* **Slow first load:**

  * Backend hosted on free tier (Render sleeps)

---

## 🎯 Project Purpose

This project demonstrates practical implementation of core DAA concepts in a real-world web application, combining algorithmic efficiency with user interaction.

---

## 📜 License

MIT License

---

## 💡 Future Improvements

* Add authentication system
* Use advanced search (Binary Search / Hashing)
* Add database (MongoDB / PostgreSQL)
* Visualize algorithm steps

---

## 🚀 Final Note

This project showcases how classic algorithms can be integrated into modern full-stack applications to solve real-world problems efficiently.

