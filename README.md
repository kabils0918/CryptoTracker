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

## 📂 Project Structure
CryptoTracker/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── src/
│ ├── tracker_selenium.py # Selenium scraper
│ └── plot_from_selenium_csv_debug.py # Plot generator
│
└── outputs/
├── crypto_prices.csv # Generated after scraping
├── top10_prices.png # Price plot
└── price_changes_24h.png # 24h change plot

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
git clone https://github.com/kabils0918/CryptoTracker.git
cd CryptoTracker

### 2️⃣ Create and activate a virtual environment (recommended)
python -m venv venv

**On Windows (PowerShell):**
.\venv\Scripts\Activate.ps1

**On macOS / Linux:**
source venv/bin/activat

### 3️⃣ Install dependencies
pip install -r requirements.txt

---

## ▶️ Run the Live Selenium Scraper
python src/tracker_selenium.py

What this does:

- Launches Chrome (visible or headless based on configuration)  
- Loads CoinMarketCap and scrapes the Top 10 coins  
- Prints a formatted table of data in the terminal  
- Saves/updates `outputs/crypto_prices.csv` with the latest snapshot

---

## 🎨 Generate the Plots

After you have run the scraper at least once (so that `crypto_prices.csv` exists):
python src/plot_from_selenium_csv_debug.py

This will generate/update:

- `outputs/top10_prices.png`  
- `outputs/price_changes_24h.png`

You can embed these images directly in your mini‑project report or PPT.

---

## 📊 Sample Outputs

- **Top 10 Crypto Prices (Live):**  
  Horizontal bar chart showing each coin’s current price in USD.

- **24h Price Changes:**  
  Horizontal bar chart showing 24‑hour percentage change for the same coins (ideal for volatility analysis).

---

## 🚧 Possible Enhancements

Some ideas you can build on top of this project:

- Add a scheduler to run scraping automatically every X minutes/hour  
- Build a FastAPI or Flask backend and expose the data as an API  
- Store data in SQLite/PostgreSQL for long‑term analysis  
- Create a Streamlit dashboard for interactive visualization  
- Add alert logic (e.g., notify when price change exceeds a threshold)  
- Log errors and scraping status for production‑






