import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load CSV data, treat 'puudu' as NaN
df = pd.read_csv('/Users/anderooovel/Downloads/finished_data.csv', na_values=['puudu'])

# Drop rows with missing critical data
df = df.dropna(subset=['kulunud aeg', 'Zoo buss algusaeg', 'kuupäev'])

# Convert elapsed time (HH:MM:SS) to total seconds
def time_to_seconds(t):
    h, m, s = map(int, t.split(':'))
    return h * 3600 + m * 60 + s

df['elapsed_seconds'] = df['kulunud aeg'].apply(time_to_seconds)

# Convert date column to datetime
df['date'] = pd.to_datetime(df['kuupäev'], format='%d.%m.%y')

# Convert elapsed seconds to minutes for readability
df['elapsed_minutes'] = df['elapsed_seconds'] / 60


# --- 1. Histogram of elapsed time ---
plt.figure(figsize=(10,5))
plt.hist(df['elapsed_minutes'], bins=20, color='skyblue', edgecolor='black')
plt.title('Distribution of Elapsed Time (minutes)')
plt.xlabel('Elapsed Time (minutes)')
plt.ylabel('Frequency')
plt.grid(axis='y', alpha=0.75)
plt.tight_layout()
plt.show()


# --- 2. Average elapsed time by date with weekday names and aligned grid ---

avg_by_date = df.groupby('date')['elapsed_minutes'].mean()

plt.figure(figsize=(12,5))
plt.plot(range(len(avg_by_date)), avg_by_date.values, marker='o', linestyle='-')
plt.title('Average Elapsed Time per Date')
plt.xlabel('Date (with Weekday)')
plt.ylabel('Average Elapsed Time (minutes)')

# Get weekday abbreviations for each date (e.g., Mon, Tue, Wed)
weekday_labels = avg_by_date.index.to_series().dt.strftime('%a')

# Format x-axis ticks as "day\nweekday"
x_labels = [f"{d.strftime('%d.%m')}\n{wd}" for d, wd in zip(avg_by_date.index, weekday_labels)]

# Set ticks as integer positions with custom labels
plt.xticks(ticks=range(len(avg_by_date)), labels=x_labels, rotation=0)

# Enable only horizontal grid lines aligned with y-axis ticks
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# --- 3. Grouped average elapsed time using your helper_index logic ---

# Create cyclic group index (0 to 7) per row
helper_index = 0
group_indices = []
for _ in range(len(df)):
    group_indices.append(helper_index)
    helper_index += 1
    if helper_index == 8:
        helper_index = 0

df['group'] = group_indices

# Calculate average elapsed time per group
grouped = df.groupby('group')['elapsed_minutes'].mean()

# Your group labels as strings
group_labels = ['7:54', '8:05', '8:16', '8:28', '8:38', '8:48', '8:59', '9:11']

plt.figure(figsize=(10,5))
plt.bar(grouped.index, grouped.values, color='cornflowerblue', edgecolor='black')
plt.xlabel('Group Start Time')
plt.ylabel('Average Elapsed Time (minutes)')
plt.title('Average Elapsed Time by Group (Start Times)')
plt.xticks(grouped.index, group_labels)
plt.ylim(12, 17)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()


