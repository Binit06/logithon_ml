# Load required library
library(readr)

# Read the first CSV file (route fares)
fare_data <- read_csv("new_data/filtered_data.csv")

# Read the second CSV file (fare matrix with zeros)
fare_matrix <- read_csv("new_data/air_cost_new.csv")

# Get airport codes from the fare matrix
airport_codes <- colnames(fare_matrix)

# Ensure row names match column names
rownames(fare_matrix) <- airport_codes

# Update the fare matrix with the fares from fare_data
for (i in 1:nrow(fare_data)) {
  start_airport <- fare_data$startingAirport[i]
  end_airport <- fare_data$destinationAirport[i]
  total_fare <- fare_data$totalFare[i]
  
  # Check if both airports exist in the matrix
  fare_matrix[start_airport, end_airport] <- fare_matrix[start_airport, end_airport] + total_fare
}

# Write the updated matrix to a new CSV file
write_csv(fare_matrix, "updated_matrix.csv")