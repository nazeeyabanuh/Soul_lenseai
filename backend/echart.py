import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to database
conn = sqlite3.connect("soullens.db")

# Read analysis table
df = pd.read_sql(
    "SELECT * FROM analysis",
    conn
)

print("Database Records:")
print(df.head())

# Count emotions
emotion_counts = (
    df["emotion"]
    .value_counts()
)

print("\nEmotion Counts:")
print(emotion_counts)

# Create chart
emotion_counts.plot(
    kind="bar"
)

plt.title(
    "SoulLens Emotion Distribution"
)

plt.xlabel("Emotion")
plt.ylabel("Count")

# Save chart
plt.savefig(
    "emotion_chart.png"
)

print("\nChart saved as emotion_chart.png")