import pandas as pd
import matplotlib.pyplot as plt

# Load the datasets
df_10 = pd.read_csv('/mnt/data/results_10_stats.csv')
df_100 = pd.read_csv('/mnt/data/results_100_stats.csv')
df_1000 = pd.read_csv('/mnt/data/results_1000_stats.csv')
df_10000 = pd.read_csv('/mnt/data/results_10000_stats.csv')

# Extract relevant metrics for comparison
batch_sizes = ['10', '100', '1000', '10000']
median_response_times = [
    df_10['Median Response Time'].iloc[0],
    df_100['Median Response Time'].iloc[0],
    df_1000['Median Response Time'].iloc[0],
    df_10000['Median Response Time'].iloc[0]
]
average_response_times = [
    df_10['Average Response Time'].iloc[0],
    df_100['Average Response Time'].iloc[0],
    df_1000['Average Response Time'].iloc[0],
    df_10000['Average Response Time'].iloc[0]
]
# Load the new datasets for the orjson library
df_orjson_10 = pd.read_csv('/mnt/data/results_10_stats.csv')
df_orjson_100 = pd.read_csv('/mnt/data/results_100_stats.csv')
df_orjson_1000 = pd.read_csv('/mnt/data/results_1000_stats.csv')
df_orjson_10000 = pd.read_csv('/mnt/data/results_10000_stats.csv')

# Extract relevant metrics for comparison with orjson
median_response_times_orjson = [
    df_orjson_10['Median Response Time'].iloc[0],
    df_orjson_100['Median Response Time'].iloc[0],
    df_orjson_1000['Median Response Time'].iloc[0],
    df_orjson_10000['Median Response Time'].iloc[0]
]



# Plotting old vs new results in a horizontal bar chart
plt.figure(figsize=(14, 8))

# Define positions
y_positions = range(len(batch_sizes))
bar_height = 0.35

# Plot for original json library
plt.barh([y - bar_height/2 for y in y_positions], median_response_times, height=bar_height, label='Original JSON', color='lightblue')

# Plot for orjson library
plt.barh([y + bar_height/2 for y in y_positions], median_response_times_orjson, height=bar_height, label='orjson', color='lightgreen')

plt.xlabel('Median Response Time (ms)')
plt.title('Comparison of Median Response Times by Payload Size and JSON Library')

plt.yticks([y for y in y_positions], batch_sizes)
plt.legend()
plt.grid(True)

plt.show()
