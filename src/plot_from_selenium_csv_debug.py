# src/plot_from_selenium_csv_debug.py
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

# Config
OUT_DIR = "outputs"
CSV_CANDIDATES = [
    os.path.join(OUT_DIR, "selenium_crypto_prices.csv"),
    os.path.join(OUT_DIR, "crypto_prices.csv"),
]
OUT_PRICE = os.path.join(OUT_DIR, "top10_prices.png")
OUT_CHANGE = os.path.join(OUT_DIR, "price_changes_24h.png")
TOP_N = 10

def parse_price(s):
    try:
        if pd.isna(s): return None
        t = str(s).strip().replace("$","").replace(",","").split()[0]
        return float(t)
    except Exception:
        return None

def parse_pct(s):
    try:
        if pd.isna(s): return None
        return float(str(s).strip().replace("%","").replace(",",""))
    except Exception:
        return None

def find_csv():
    for p in CSV_CANDIDATES:
        if os.path.exists(p):
            print("🔎 Using CSV:", p)
            return p
    print("❌ No CSV found. Checked:", CSV_CANDIDATES)
    return None

def main():
    csv_path = find_csv()
    if not csv_path:
        print("Make sure your scraper produced .\\outputs\\selenium_crypto_prices.csv or .\\outputs\\crypto_prices.csv")
        sys.exit(1)

    print("📥 Loading CSV...")
    df = pd.read_csv(csv_path)
    print("Columns:", list(df.columns))
    print("First 5 rows:\n", df.head(5).to_string(index=False))

    # Normalize column names
    if "price" not in df.columns and "price_usd" in df.columns:
        df["price"] = df["price_usd"]
    if "change_24h" not in df.columns and "price_change_24h" in df.columns:
        df["change_24h"] = df["price_change_24h"]

    # parse numbers
    df["price_num"] = df["price"].apply(parse_price) if "price" in df.columns else None
    df["change_num"] = df["change_24h"].apply(parse_pct) if "change_24h" in df.columns else None

    print("\nParsed price_num sample:")
    if "price_num" in df.columns:
        print(df[["name","price","price_num"]].head(10).to_string(index=False))
    else:
        print("price column missing.")

    print("\nParsed change_num sample:")
    if "change_num" in df.columns:
        print(df[["name","change_24h","change_num"]].head(10).to_string(index=False))
    else:
        print("change_24h column missing.")

    # Price plot
    if "price_num" in df.columns and df["price_num"].dropna().any():
        p = df.dropna(subset=["price_num"]).sort_values("price_num", ascending=False).head(TOP_N)
        plt.figure(figsize=(12,8))
        plt.barh(p["name"].iloc[::-1], p["price_num"].iloc[::-1])
        plt.xlabel("Price (USD)")
        plt.title(f"Top {len(p)} Cryptocurrencies by Price (Latest)")
        for i, val in enumerate(p["price_num"].iloc[::-1]):
            plt.text(val, i, f' ${val:,.2f}', va='center', fontweight='bold')
        plt.tight_layout()
        plt.savefig(OUT_PRICE, dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Saved price plot:", OUT_PRICE)
    else:
        print("⚠️ No numeric price data to plot. Check price parsing.")

    # 24h change plot
    if "change_num" in df.columns and df["change_num"].dropna().any():
        c = df.dropna(subset=["change_num"]).sort_values("change_num", ascending=True).head(TOP_N)
        plt.figure(figsize=(12,8))
        colors = ['green' if x>0 else 'red' for x in c["change_num"].iloc[::-1]]
        plt.barh(c["name"].iloc[::-1], c["change_num"].iloc[::-1], color=colors)
        plt.xlabel("24h Price Change (%)")
        plt.title("24h Price Changes - Top Cryptocurrencies")
        plt.axvline(0, color='black', linewidth=0.6)
        for i, val in enumerate(c["change_num"].iloc[::-1]):
            plt.text(val, i, f' {val:.2f}%', va='center', fontweight='bold')
        plt.tight_layout()
        plt.savefig(OUT_CHANGE, dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Saved 24h change plot:", OUT_CHANGE)
    else:
        print("⚠️ No numeric 24h change data to plot. Check change parsing.")

if __name__ == "__main__":
    main()
