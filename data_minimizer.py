import pandas as pd
import numpy as np

# Load CSV files and replace NaN values with -1
cost_df = pd.read_csv("new_data/air_cost.csv", index_col=0).fillna(-1)
duration_df = pd.read_csv("new_data/air_duration.csv", index_col=0).fillna(-1)

# Convert DataFrames to NumPy arrays
cost_matrix = cost_df.to_numpy()
duration_matrix = duration_df.to_numpy()

# Mask invalid entries (-1 means missing data)
valid_entries = (duration_matrix > 0) & (cost_matrix > 0)

# Compute min & max for cost and duration, ignoring -1 values
finite_costs = cost_matrix[valid_entries]
finite_durations = duration_matrix[valid_entries]

if finite_costs.size > 0:
    min_cost, max_cost = np.min(finite_costs), np.max(finite_costs)
else:
    min_cost, max_cost = -1, -1  # No valid values

if finite_durations.size > 0:
    min_duration, max_duration = np.min(finite_durations), np.max(finite_durations)
else:
    min_duration, max_duration = -1, -1  # No valid values

# Compute feasibility: (Lower cost & duration should give higher feasibility)
feasibility_matrix = np.full_like(cost_matrix, -1, dtype=float)  # Default to -1
feasibility_matrix[valid_entries] = 1 / (cost_matrix[valid_entries] + duration_matrix[valid_entries])

# Normalize only valid feasibility values
finite_values = feasibility_matrix[valid_entries]
if finite_values.size > 0:
    min_val = np.min(finite_values)
    max_val = np.max(finite_values)

    # Avoid division by zero in normalization
    if max_val > min_val:
        normalized_matrix = np.full_like(feasibility_matrix, -1, dtype=float)  # Default to -1
        normalized_matrix[valid_entries] = (feasibility_matrix[valid_entries] - min_val) / (max_val - min_val)
    else:
        normalized_matrix = feasibility_matrix  # If all values are the same, no need to normalize
else:
    normalized_matrix = feasibility_matrix  # If all are -1, keep the same matrix

# Convert back to DataFrame
normalized_df = pd.DataFrame(normalized_matrix, index=cost_df.index, columns=cost_df.columns)

# Save normalized feasibility matrix
normalized_df.to_csv("feasibility.csv", na_rep="-1")

# Save min/max cost & duration separately
with open("min_max_values.txt", "w") as f:
    f.write(f"Min Cost: {min_cost}\n")
    f.write(f"Max Cost: {max_cost}\n")
    f.write(f"Min Duration: {min_duration}\n")
    f.write(f"Max Duration: {max_duration}\n")

print("Data Normalized")
print(f"Min Cost: {min_cost}, Max Cost: {max_cost}")
print(f"Min Duration: {min_duration}, Max Duration: {max_duration}")
