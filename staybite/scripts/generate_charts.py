import os
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, 'core', 'data', 'zomato_outlet_final.csv')
CHARTS_DIR = os.path.join(BASE_DIR, 'core', 'static', 'charts')

# Folder to save charts (inside static folder)
CHARTS_DIR = os.path.join(BASE_DIR, 'core', 'static', 'images')
os.makedirs(CHARTS_DIR, exist_ok=True)

# Load CSV
df = pd.read_csv(CSV_PATH)
print("Data loaded successfully!")
print(df.head())

# -------------------------
# Example Chart 1: Cuisine Distribution
# -------------------------
plt.figure(figsize=(10, 6))
df['Cuisines'].value_counts().head(10).plot(kind='bar', color='skyblue')
plt.title("Top 10 Cuisines")
plt.ylabel("Number of Restaurants")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, 'top_cuisines.png'))
plt.close()

# -------------------------
# Example Chart 2: Average Rating by City
# -------------------------
if 'City' in df.columns and 'Aggregate rating' in df.columns:
    plt.figure(figsize=(10, 6))
    df.groupby('City')['Aggregate rating'].mean().sort_values(ascending=False).head(10).plot(
        kind='bar', color='orange'
    )
    plt.title("Top 10 Cities by Average Rating")
    plt.ylabel("Average Rating")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, 'top_cities_ratings.png'))
    plt.close()

# -------------------------
# Example Chart 3: Price Range Distribution
# -------------------------
if 'Price range' in df.columns:
    plt.figure(figsize=(6, 6))
    df['Price range'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['#FFD700', '#FF6347', '#90EE90', '#87CEEB'])
    plt.title("Price Range Distribution")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, 'price_range.png'))
    plt.close()

print(f"Charts saved to: {CHARTS_DIR}")
