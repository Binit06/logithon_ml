import pandas as pd

# Load the fare data
fare_data = pd.read_csv("new_data/filtered_duration_data.csv")

# Get unique airports
airports = sorted(set(fare_data["startingAirport"]).union(set(fare_data["destinationAirport"])))

# Create an empty DataFrame with airports as both rows and columns
fare_matrix = pd.DataFrame('-', index=airports, columns=airports)

# Fill the DataFrame with the available fares
for _, row in fare_data.iterrows():
    start_airport = row["startingAirport"]
    end_airport = row["destinationAirport"]
    totalDuration = row["travelDuration"]
    
    fare_matrix.at[start_airport, end_airport] = totalDuration

# Save the fare matrix to a CSV file
fare_matrix.to_csv("fare_matrix.csv")

print("Fare matrix saved to fare_matrix.csv")
