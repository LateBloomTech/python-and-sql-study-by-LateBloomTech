import pandas as pd, sqlite3, os

os.makedirs("reports", exist_ok=True)
CSV_PATH = "data/google_ads_sample.csv"
DB_PATH  = "projectsads-anomaly/ads.db"

# 文字コードの想定（UTF-8推奨。Shift-JISなら encoding="cp932"）
df = pd.read_csv(CSV_PATH, parse_dates=["Date"])
df = df.sort_values(["Date"])

con = sqlite3.connect(DB_PATH)
df.to_sql("raw", con, if_exists="replace", index=False)
con.execute("""CREATE VIEW IF NOT EXISTS v_daily AS
  SELECT Date, SUM(Cost) AS Cost
  FROM raw GROUP BY Date ORDER BY Date
""")
con.commit(); con.close()
print("OK: ads.db + view v_daily")