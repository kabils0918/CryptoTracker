"""
Cryptocurrency Price Tracker - Selenium Version (Scrape -> CSV -> 2 PNGs)
Author: Kabilan S | Hardened by Fab
Produces:
 - outputs/crypto_prices.csv
 - outputs/top10_prices.png
 - outputs/price_changes_24h.png
"""
import os
import time
from datetime import datetime
import sys
import pandas as pd
import matplotlib.pyplot as plt

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ---- Config ----
URL = "https://coinmarketcap.com/"
OUT_DIR = "outputs"
CSV_PATH = os.path.join(OUT_DIR, "crypto_prices.csv")
PNG_PRICE = os.path.join(OUT_DIR, "top10_prices.png")
PNG_CHANGE = os.path.join(OUT_DIR, "price_changes_24h.png")
WAIT_TIMEOUT = 20
TOP_N = 10
HEADLESS = False  # set True for background run once stable

# ---- Helpers ----
def create_driver(headless=HEADLESS):
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1920,1080")
    opts.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    )
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)
    driver.implicitly_wait(2)
    return driver

def _text_or_none(elem):
    try:
        t = elem.text
        return t.strip() if t else None
    except Exception:
        return None

def parse_price_str(s):
    """Convert price like '$89,619.55' to float (None if fails)."""
    if pd.isna(s):
        return None
    try:
        t = str(s).strip().replace("$", "").replace(",", "").split()[0]
        return float(t)
    except Exception:
        return None

def parse_percent_str(s):
    """Convert percent like '-1.23%' to float (None if fails)."""
    if pd.isna(s):
        return None
    try:
        t = str(s).strip().replace("%", "").replace(",", "")
        return float(t)
    except Exception:
        return None

# ---- Scraping ----
def parse_row_structural(row, idx):
    """Try to extract row data using the table structure (td indexes)."""
    tds = row.find_elements(By.TAG_NAME, "td")
    if len(tds) < 4:
        raise ValueError("Not enough td cells")

    # NAME/SYMBOL
    name = None
    symbol = None
    try:
        name_cell = tds[2]
        # try anchor first then paragraph
        try:
            name = _text_or_none(name_cell.find_element(By.CSS_SELECTOR, "a"))
        except:
            name = _text_or_none(name_cell.find_element(By.TAG_NAME, "p"))
        # symbol fallback
        spans = name_cell.find_elements(By.TAG_NAME, "span")
        if spans:
            # often last small span is symbol
            symbol = _text_or_none(spans[-1])
    except Exception:
        pass

    # PRICE
    price = None
    try:
        price_cell = tds[3]
        # anchor or span containing $...
        try:
            price = _text_or_none(price_cell.find_element(By.TAG_NAME, "a"))
        except:
            price = _text_or_none(price_cell.find_element(By.TAG_NAME, "span"))
    except Exception:
        # fallback: search for any $ span in row
        for s in row.find_elements(By.TAG_NAME, "span"):
            txt = _text_or_none(s)
            if txt and txt.strip().startswith("$"):
                price = txt
                break

    # 24H CHANGE
    change_24h = None
    try:
        change_cell = tds[4]
        change_24h = _text_or_none(change_cell.find_element(By.TAG_NAME, "span"))
    except Exception:
        for s in row.find_elements(By.TAG_NAME, "span"):
            txt = _text_or_none(s)
            if txt and "%" in txt:
                change_24h = txt
                break

    # MARKET CAP
    market_cap = None
    try:
        market_cap = _text_or_none(tds[-1].find_element(By.TAG_NAME, "span"))
        if not market_cap:
            # fallback: search for last $ span
            for s in reversed(row.find_elements(By.TAG_NAME, "span")):
                txt = _text_or_none(s)
                if txt and txt.startswith("$"):
                    market_cap = txt
                    break
    except Exception:
        market_cap = None

    if not (name and price):
        raise ValueError("Missing name or price")

    return {
        "rank": idx,
        "name": name,
        "symbol": symbol or "",
        "price": price,
        "price_num": parse_price_str(price),
        "change_24h": change_24h or "",
        "change_num": parse_percent_str(change_24h),
        "market_cap": market_cap or "",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

def scrape_top_n(driver, top_n=TOP_N):
    print("🔄 Opening", URL)
    driver.get(URL)
    wait = WebDriverWait(driver, WAIT_TIMEOUT)
    try:
        rows = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr")))
    except Exception as e:
        print("❌ Timeout waiting for table rows:", e)
        return []

    rows = rows[:top_n]
    out = []
    for i, row in enumerate(rows, start=1):
        try:
            rec = parse_row_structural(row, i)
            out.append(rec)
        except Exception as e:
            # fallback parse using generic anchors/spans; if fails, print innerHTML trimmed for debug
            try:
                name_elem = None
                try:
                    name_elem = row.find_element(By.CSS_SELECTOR, "a[href*='/currencies/']")
                except:
                    anchors = row.find_elements(By.TAG_NAME, "a")
                    if anchors:
                        name_elem = anchors[0]
                name = _text_or_none(name_elem) if name_elem else None

                price = None
                for s in row.find_elements(By.TAG_NAME, "span"):
                    txt = _text_or_none(s)
                    if txt and txt.startswith("$"):
                        price = txt
                        break

                change_24h = None
                for s in row.find_elements(By.TAG_NAME, "span"):
                    txt = _text_or_none(s)
                    if txt and "%" in txt:
                        change_24h = txt
                        break

                market_cap = None
                for s in reversed(row.find_elements(By.TAG_NAME, "span")):
                    txt = _text_or_none(s)
                    if txt and txt.startswith("$"):
                        market_cap = txt
                        break

                if not name or not price:
                    inner = row.get_attribute("innerHTML")
                    raise ValueError(f"Fallback parse failed. row innerHTML (trimmed):\n{inner[:800]}")

                rec = {
                    "rank": i,
                    "name": name,
                    "symbol": "",
                    "price": price,
                    "price_num": parse_price_str(price),
                    "change_24h": change_24h or "",
                    "change_num": parse_percent_str(change_24h),
                    "market_cap": market_cap or "",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                out.append(rec)
            except Exception as e2:
                print(f"⚠️ Row {i} parse error: {e2}")
                continue
    return out

# ---- Save CSV & plots ----
def save_csv(records, path=CSV_PATH):
    os.makedirs(OUT_DIR, exist_ok=True)
    df = pd.DataFrame(records)
    # Keep only snapshot columns (no history) - overwrite file each run
    df_to_save = df[["rank", "name", "symbol", "price", "price_num", "change_24h", "change_num", "market_cap", "timestamp"]]
    df_to_save.to_csv(path, index=False)
    print(f"✅ CSV saved: {path} ({len(df_to_save)} rows)")

def plot_top10_prices(df, top_n=TOP_N, out_path=PNG_PRICE):
    df2 = df.dropna(subset=["price_num"]).sort_values("price_num", ascending=False).head(top_n)
    if df2.empty:
        print("⚠️ No price data to plot.")
        return
    plt.figure(figsize=(12,8))
    bars = plt.barh(df2["name"].iloc[::-1], df2["price_num"].iloc[::-1])
    plt.xlabel("Price (USD)")
    plt.title(f"🏆 Top {len(df2)} Cryptocurrencies by Price (Live Data)")
    plt.tight_layout()
    # add labels on bars
    for i, val in enumerate(df2["price_num"].iloc[::-1]):
        plt.text(val, i, f' ${val:,.2f}', va='center', fontweight='bold')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Saved price plot: {out_path}")

def plot_price_changes_24h(df, top_n=TOP_N, out_path=PNG_CHANGE):
    df2 = df.dropna(subset=["change_num"]).sort_values("change_num", ascending=True).head(top_n)  # ascending to show negatives left
    if df2.empty:
        print("⚠️ No 24h change data to plot.")
        return
    plt.figure(figsize=(12,8))
    # colors: green for positive, red for negative
    colors = ['green' if x > 0 else 'red' for x in df2["change_num"].iloc[::-1]]
    bars = plt.barh(df2["name"].iloc[::-1], df2["change_num"].iloc[::-1], color=colors)
    plt.xlabel("24h Price Change (%)")
    plt.title("📈 24h Price Changes - Top Cryptocurrencies")
    plt.axvline(0, color='black', linewidth=0.6)
    plt.tight_layout()
    for i, val in enumerate(df2["change_num"].iloc[::-1]):
        plt.text(val, i, f' {val:.2f}%', va='center', fontweight='bold')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Saved 24h change plot: {out_path}")

# ---- Main ----
def main():
    driver = create_driver(headless=HEADLESS)
    try:
        records = scrape_top_n(driver, top_n=TOP_N)
        if not records:
            print("❌ No data scraped.")
            return
        # Save CSV
        save_csv(records)
        df = pd.DataFrame(records)
        # Make plots
        plot_top10_prices(df, top_n=TOP_N)
        plot_price_changes_24h(df, top_n=TOP_N)
        # Print top table
        print("\n🏆 TOP 10 CRYPTO (latest snapshot):")
        print(df[["rank","name","symbol","price","change_24h"]].to_string(index=False))
    finally:
        driver.quit()
        print("\n🛑 Browser closed. Script finished.")

if __name__ == "__main__":
    main()
