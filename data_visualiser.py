import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load normalized feasibility data
normalized_df = pd.read_csv("new_data/air_feasibility.csv", index_col=0)

# Convert -1 values back to NaN for visualization (optional)
normalized_df.replace(-1, np.nan, inplace=True)

# Set up the heatmap
plt.figure(figsize=(12, 8))  # Adjust figure size
sns.heatmap(normalized_df, cmap="coolwarm", annot=False, fmt=".2f", linewidths=0.5, cbar=True)

# Customize the plot
plt.title("Feasibility Matrix Heatmap")
plt.xlabel("Destination")
plt.ylabel("Source")

# Show the heatmap
plt.show()
