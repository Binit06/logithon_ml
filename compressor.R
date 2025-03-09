# Load required library
library(data.table)

# Read only the required columns from processed_data.csv
data <- fread("new_data/processed_data.csv", header = TRUE, quote = "\"",
              select = c("startingAirport", "destinationAirport", "travelDuration"))

# Function to convert ISO 8601 duration to hours
convert_to_hours <- function(duration) {
  hours <- as.numeric(gsub(".*PT(\\d+)H.*", "\\1", duration))
  minutes <- as.numeric(gsub(".*H(\\d+)M.*", "\\1", duration))
  
  # Handle cases where hours or minutes may not exist
  hours[is.na(hours)] <- 0
  minutes[is.na(minutes)] <- 0
  
  return(hours + minutes / 60)
}

# Apply the function to convert travelDuration
data[, travelDuration := convert_to_hours(travelDuration)]

# Save the filtered data to a new CSV file
fwrite(data, "new_data/filtered_duration_data.csv", row.names = FALSE)

# Print the first 10 rows to verify
print(head(data, 10))
