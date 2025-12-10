# scripts/generate_top_cities_chart.py
import os
import pandas as pd
import matplotlib.pyplot as plt

# Paths (adjust if your project structure differs)
INPUT_CSV = os.path.join('core', 'data', 'zomato_outlet_final.csv')
OUT_DIR = os.path.join('core', 'static', 'images')   # <-- output folder for templates' {% static 'images/...' %}
OUT_FILE = os.path.join(OUT_DIR, 'top_cities.png')

# Create output folder if missing
os.makedirs(OUT_DIR, exist_ok=True)

# Load data
df = pd.read_csv(INPUT_CSV)

# Use 'loc' column as location, and 'rest_name' as outlet identifier
df['loc'] = df.get('loc', df.columns[0]).fillna('Unknown')  # fallback safe-guard
df['rest_name'] = df.get('rest_name', df.columns[0]).fillna('Unknown')

# Compute top 10 locations by number of outlets
top_locations = df.groupby('loc')['rest_name'].count().sort_values(ascending=False).head(10)

# Plotting
plt.style.use('ggplot')  # simple base style; we'll override colors
fig, ax = plt.subplots(figsize=(10,6), facecolor='white')

# Bars: gold color to match theme
bars = ax.bar(top_locations.index, top_locations.values, color='#FFD700', edgecolor='#b8860b')

# Aesthetic adjustments for theme
ax.set_title('Top 10 Locations by Number of Outlets', fontsize=16, weight='bold')
ax.set_ylabel('Number of Outlets', fontsize=12)
ax.set_xticklabels(top_locations.index, rotation=45, ha='right', fontsize=10)
ax.set_facecolor('#ffffff')

# Add value labels on top of bars
for rect in bars:
    height = rect.get_height()
    ax.annotate(f'{int(height)}',
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 6),
                textcoords='offset points',
                ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig(OUT_FILE, dpi=150)
plt.close()

print("Saved chart to:", OUT_FILE)
