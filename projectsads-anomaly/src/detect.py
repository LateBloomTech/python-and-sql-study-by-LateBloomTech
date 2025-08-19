import sqlite3, pandas as pd
import matplotlib.pyplot as plt

DB_PATH = "projectsads-anomaly/ads.db"
IMG_OUT = "reports/anomalies.png"

con = sqlite3.connect(DB_PATH)
df = pd.read_sql("SELECT Date, Cost FROM v_daily", con, parse_dates=["Date"])
con.close()

df["ma7"] = df["Cost"].rolling(7, min_periods=3).mean()
df["sd7"] = df["Cost"].rolling(7, min_periods=3).std().fillna(0)
df["upper"] = df["ma7"] + 3*df["sd7"]
df["anomaly"] = df["Cost"] > df["upper"]

plt.figure(figsize=(10,5))
plt.plot(df["Date"], df["Cost"], label="Cost")
plt.plot(df["Date"], df["ma7"], label="MA7")
plt.plot(df["Date"], df["upper"], "--", label="Upper 3σ")
plt.scatter(df.loc[df["anomaly"],"Date"], df.loc[df["anomaly"],"Cost"],
            marker="x", s=80, label="anomaly")
plt.title("Daily Ad Cost with 3σ Band"); plt.legend(); plt.tight_layout()
plt.savefig(IMG_OUT, dpi=150)
print("OK:", IMG_OUT)
