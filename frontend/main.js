/**
 * Game Inventory Optimizer — frontend SPA
 * API: http://127.0.0.1:5001 (5000 is often blocked on Windows)
 */

const API_BASE = "https://game-inventory-optimizer.onrender.com";

const SAMPLE_ITEMS = [
  { name: "Excalibur", weight: 5, value: 100 },
  { name: "Dragon Shield", weight: 8, value: 80 },
  { name: "Health Potion", weight: 2, value: 40 },
  { name: "Magic Scroll", weight: 3, value: 60 },
  { name: "Iron Helmet", weight: 6, value: 70 },
];

const DEFAULT_CAPACITY = 10;

let items = [];

function itemEquals(a, b) {
  return (
    a.name === b.name &&
    Number(a.weight) === Number(b.weight) &&
    Number(a.value) === Number(b.value)
  );
}

function showToast(message) {
  const c = document.getElementById("toast-container");
  const t = document.createElement("div");
  t.className = "toast";
  t.textContent = message;
  c.appendChild(t);
  setTimeout(() => {
    t.style.opacity = "0";
    t.style.transition = "opacity 0.3s";
    setTimeout(() => t.remove(), 320);
  }, 4500);
}

function setLoading(on) {
  const el = document.getElementById("loading");
  el.classList.toggle("hidden", !on);
}

async function apiPost(path, body) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const msg = data.error || `Request failed (${res.status})`;
    throw new Error(msg);
  }
  return data;
}

function renderTable() {
  const body = document.getElementById("items-body");
  const empty = document.getElementById("empty-hint");
  body.innerHTML = "";
  if (items.length === 0) {
    empty.classList.remove("hidden");
    return;
  }
  empty.classList.add("hidden");
  items.forEach((it, idx) => {
    const tr = document.createElement("tr");
    tr.dataset.idx = String(idx);
    tr.innerHTML = `
      <td>${escapeHtml(it.name)}</td>
      <td>${it.weight}</td>
      <td>${it.value}</td>
      <td><button type="button" class="btn btn--small" data-remove="${idx}">Remove</button></td>
    `;
    body.appendChild(tr);
  });
  body.querySelectorAll("[data-remove]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const i = parseInt(btn.getAttribute("data-remove"), 10);
      items.splice(i, 1);
      renderTable();
      updateTotals();
      clearRowHighlights();
    });
  });
}

function escapeHtml(s) {
  const d = document.createElement("div");
  d.textContent = s;
  return d.innerHTML;
}

function updateTotals() {
  document.getElementById("total-count").textContent = String(items.length);
  const tw = items.reduce((a, x) => a + Number(x.weight), 0);
  const tv = items.reduce((a, x) => a + Number(x.value), 0);
  document.getElementById("total-weight-sum").textContent = String(tw);
  document.getElementById("total-value-sum").textContent = String(tv);
}

function clearRowHighlights() {
  document.querySelectorAll("#items-body tr").forEach((tr) => {
    tr.classList.remove("row--selected", "row--search-hit");
  });
}

function highlightSelected(selectedList) {
  document.querySelectorAll("#items-body tr").forEach((tr) => {
    const idx = parseInt(tr.dataset.idx, 10);
    const it = items[idx];
    const on = it && selectedList.some((s) => itemEquals(it, s));
    tr.classList.toggle("row--selected", !!on);
  });
}

function highlightSearchHit(hit) {
  clearRowHighlights();
  if (!hit) return;
  const idx = items.findIndex((it) => itemEquals(it, hit));
  if (idx < 0) return;
  const tr = document.querySelector(`#items-body tr[data-idx="${idx}"]`);
  if (tr) tr.classList.add("row--search-hit");
}

function showResults(html) {
  document.getElementById("results-content").innerHTML = `<div class="results-inner">${html}</div>`;
}

function validateItemsForRequest() {
  if (items.length === 0) {
    showToast("Add at least one item first.");
    return false;
  }
  return true;
}

document.getElementById("add-form").addEventListener("submit", (e) => {
  e.preventDefault();
  const name = document.getElementById("item-name").value.trim();
  const weight = Number(document.getElementById("item-weight").value);
  const value = Number(document.getElementById("item-value").value);
  if (!name) {
    showToast("Item name is required.");
    return;
  }
  if (!Number.isFinite(weight) || weight < 0 || !Number.isInteger(weight)) {
    showToast("Weight must be a non-negative whole number.");
    return;
  }
  if (!Number.isFinite(value) || value < 0 || !Number.isInteger(value)) {
    showToast("Value must be a non-negative whole number.");
    return;
  }
  items.push({ name, weight, value });
  e.target.reset();
  renderTable();
  updateTotals();
  clearRowHighlights();
});

document.getElementById("btn-optimize").addEventListener("click", async () => {
  if (!validateItemsForRequest()) return;
  const cap = Number(document.getElementById("capacity").value);
  if (!Number.isFinite(cap) || cap <= 0 || !Number.isInteger(cap)) {
    showToast("Max capacity must be a whole number greater than 0.");
    return;
  }
  clearRowHighlights();
  setLoading(true);
  try {
    const data = await apiPost("/optimize", { capacity: cap, items });
    const sel = data.selected_items || [];
    const pct = cap > 0 ? Math.min(100, (data.total_weight / cap) * 100) : 0;
    highlightSelected(sel);
    showResults(`
      <div class="result-block">
        <h3>⚡ Knapsack (DP) — optimal loadout</h3>
        <div class="stat-line">
          <span>Total value: <strong>${data.total_value}</strong></span>
          <span>Total weight: <strong>${data.total_weight}</strong> / ${cap} kg</span>
        </div>
        <div class="bar-wrap" title="Capacity used">
          <div class="bar-fill" style="width: ${pct}%"></div>
        </div>
        <p class="results-placeholder" style="margin-top:0.75rem;font-size:0.9rem;color:var(--muted)">
          Selected rows are highlighted in the table above.
        </p>
      </div>
    `);
  } catch (err) {
    showToast(err.message);
    showResults(`<p class="results-placeholder" style="color:var(--danger)">${escapeHtml(err.message)}</p>`);
  } finally {
    setLoading(false);
  }
});

document.getElementById("btn-sort").addEventListener("click", async () => {
  if (!validateItemsForRequest()) return;
  const key = document.getElementById("sort-key").value;
  setLoading(true);
  try {
    const data = await apiPost("/sort", { items, key });
    const sorted = data.sorted_items || [];
    const rows = sorted
      .map(
        (it, i) => `
      <tr>
        <td class="sort-rank">#${i + 1}</td>
        <td>${escapeHtml(it.name)}</td>
        <td>${it.weight}</td>
        <td>${it.value}</td>
      </tr>
    `
      )
      .join("");
    showResults(`
      <div class="result-block">
        <h3>↕ Merge sort — by ${key} (descending)</h3>
        <div class="table-wrap">
          <table class="inv-table">
            <thead><tr><th>Rank</th><th>Name</th><th>Weight</th><th>Value</th></tr></thead>
            <tbody>${rows}</tbody>
          </table>
        </div>
      </div>
    `);
  } catch (err) {
    showToast(err.message);
    showResults(`<p class="results-placeholder" style="color:var(--danger)">${escapeHtml(err.message)}</p>`);
  } finally {
    setLoading(false);
  }
});

document.getElementById("btn-search").addEventListener("click", async () => {
  if (!validateItemsForRequest()) return;
  const term = document.getElementById("search-term").value;
  if (typeof term !== "string" || term.trim() === "") {
    showToast("Enter a search term.");
    return;
  }
  setLoading(true);
  try {
    const data = await apiPost("/search", { items, name: term });
    const hit = data.result;
    if (hit) {
      highlightSearchHit(hit);
      showResults(`
        <div class="result-block">
          <h3>🔍 Linear search — first match</h3>
          <div class="search-card">
            <div><strong>${escapeHtml(hit.name)}</strong></div>
            <div>Weight: ${hit.weight} · Value: ${hit.value}</div>
          </div>
        </div>
      `);
    } else {
      clearRowHighlights();
      showResults(`
        <div class="result-block">
          <h3>🔍 Linear search</h3>
          <div class="search-card not-found">Not Found</div>
        </div>
      `);
    }
  } catch (err) {
    showToast(err.message);
    showResults(`<p class="results-placeholder" style="color:var(--danger)">${escapeHtml(err.message)}</p>`);
  } finally {
    setLoading(false);
  }
});

function init() {
  items = SAMPLE_ITEMS.map((x) => ({ ...x }));
  document.getElementById("capacity").value = String(DEFAULT_CAPACITY);
  renderTable();
  updateTotals();
}

init();
