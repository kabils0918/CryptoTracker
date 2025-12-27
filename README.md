# 🚀 CryptoTracker – Real-Time Cryptocurrency Price Tracker

**Selenium‑powered live web scraper with automated data visualization**

CryptoTracker is a mini‑project that tracks the **Top 10 cryptocurrencies from CoinMarketCap in real time** using Selenium browser automation.  
It extracts key market metrics, stores them in a CSV file, and generates two clean, presentation‑ready plots for analysis and reports.

Designed for **AI & Data Science students, crypto learners, automation enthusiasts, and analysts** who want a practical, end‑to‑end Python project.

---

## 🎯 Key Features

### 1️⃣ Live Web Scraping (Selenium)

The scraper opens **CoinMarketCap** in Chrome, waits for the dynamic table to load, and then extracts for the Top 10 coins:

- Rank  
- Coin Name  
- Symbol  
- Price (USD)  
- 24h Price Change (%)  
- Market Cap  

All values are captured in real time directly from the live webpage.

---

### 2️⃣ CSV Export with Timestamp

Every run creates or updates:

- `outputs/crypto_prices.csv`

Each row includes a **timestamp**, so you can:

- Track how prices change over time  
- Build your own analytics or dashboards later  
- Re‑use the data for ML or time‑series experiments

---

### 3️⃣ Automated Data Visualization

From the CSV, the plotting script generates **two core visual outputs**:

| File                          | Description                                             |
|-------------------------------|---------------------------------------------------------|
| `outputs/top10_prices.png`    | Horizontal bar chart of live prices (Top 10 coins)     |
| `outputs/price_changes_24h.png` | Horizontal bar chart of 24h percentage price changes |

These plots are suitable for:

- Mini‑project reports  
- PPT / viva presentations  
- Quick visual understanding of market movement

---

### 4️⃣ Headless Browser Support

CryptoTracker can run in **headless mode**, so:

- No browser window is shown  
- Suitable for background jobs, CI, cron scheduling, or server execution  
- Ideal if you want to run it periodically and only inspect the CSV/plots

(Headless mode can be toggled in the Selenium driver configuration inside `tracker_selenium.py`.)

---

### 5️⃣ Clean, Modular Code Structure

Logic is separated into focused Python modules:

- `src/tracker_selenium.py` – Scrapes CoinMarketCap using Selenium and saves data to CSV  
- `src/plot_from_selenium_csv_debug.py` – Reads the CSV and generates both plots

This makes the code:

- Easier to understand  
- Easier to extend (e.g., add alerts, more charts, or a GUI)  
- Better for academic evaluation and code reviews

---

## 🧠 Tech Stack

| Tool / Library      | Purpose                          |
|---------------------|-----------------------------------|
| Python 3.x          | Core programming language         |
| Selenium            | Dynamic web scraping & automation |
| Chrome WebDriver    | Controls the Chrome browser       |
| `webdriver-manager` | Auto‑downloads/updates WebDriver  |
| `pandas`            | Data cleaning & CSV operations    |
| `matplotlib`        | Plotting and visualization        |

