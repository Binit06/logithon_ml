import joblib
import numpy as np

model = joblib.load("feasibility_model.pkl")

def predict_feasibility(cost, duration):
    input_data = np.array([[cost, duration]])
    prediction = model.predict(input_data)[0]
    return prediction

test_cases = [
    (500, 10),
    (1000, 20),
    (50, 5),
]

for cost, duration in test_cases:
    feasibility = predict_feasibility(cost, duration)
    print(f"Cost: {cost}, Duration: {duration} -> Predicted Feasibility: {feasibility:.4f}")
