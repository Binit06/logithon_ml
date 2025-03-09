import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

feasibility_df = pd.read_csv("new_data/air_feasibility.csv", index_col=0)

feasibility_matrix = feasibility_df.to_numpy()

cost_df = pd.read_csv("new_data/air_cost.csv", index_col=0)
duration_df = pd.read_csv("new_data/air_duration.csv", index_col=0)

cost_matrix = cost_df.to_numpy()
duration_matrix = duration_df.to_numpy()

X = np.column_stack((cost_matrix.flatten(), duration_matrix.flatten()))
y = feasibility_matrix.flatten()

valid_indices = np.isfinite(y)
X = X[valid_indices]
y = y[valid_indices]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("Mean Absolute Error:", mean_absolute_error(y_test, y_pred))
print("R² Score:", r2_score(y_test, y_pred))

joblib.dump(model, "feasibility_model.pkl")
print("Model trained and saved!")
