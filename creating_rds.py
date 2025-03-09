import pyreadr
import json

# Load the RDS file
result = pyreadr.read_r("data/paths.rds")

# Extract the dataframe (pyreadr returns a dictionary)
df = result[None]

# Convert dataframe to JSON
json_data = df.to_json(orient="records")

# Save to a JSON file
with open("data/paths.json", "w") as f:
    f.write(json_data)

print("Conversion complete: paths.rds -> paths.json")

tp = pyreadr.read_r("data/trucks.rds")

# Extract the dataframe
df = tp[None]

# Convert dataframe to JSON
json_data = df.to_json(orient="records")

# Save to a JSON file
with open("data/truck_paths.json", "w") as f:
    f.write(json_data)

print("Conversion complete: trucks.rds -> truck_paths.json")

port = pyreadr.read_r("data/ports.rds")

# Extract the dataframe
df = port[None]

# Convert dataframe to JSON
json_data = df.to_json(orient="records")

# Save to a JSON file
with open("data/ports.json", "w") as f:
    f.write(json_data)

print("Conversion complete: ports.rds -> ports.json")

routes = pyreadr.read_r("data/routes.rds")

# Extract the dataframe
df = port[None]

# Convert dataframe to JSON
json_data = df.to_json(orient="records")

# Save to a JSON file
with open("data/routes.json", "w") as f:
    f.write(json_data)

print("Conversion complete: routes.rds -> routes.json")


