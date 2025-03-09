import pyreadr
import optimise
import math
import pandas as pd

node_coords = pyreadr.read_r("data/node_coords.rds")[None]
routes = pyreadr.read_r("data/routes.rds")[None]
paths = pyreadr.read_r("data/paths.rds")[None]
ports = pyreadr.read_r("data/ports.rds")[None]
trucks = pyreadr.read_r("data/trucks.rds")[None]

print(routes)

origin_location = "Shanghai Port"
destination_location = "Chongqing Port"
cargo_value = 5000
cargo_weight = 20
cargo_volume = 100
order_qty = 50

origin_v2 = node_coords.loc[node_coords["V1"] == origin_location, "V2"].values
destination_v2 = node_coords.loc[node_coords["V1"] == destination_location, "V2"].values

print(origin_v2)
def duration():
    return 360


optimised_result = optimise.optimise(origin_v2[0], destination_v2[0], duration(), cargo_value, cargo_weight, cargo_volume, order_qty)

cost = optimised_result[0]
route = optimised_result[1]
time = optimised_result[2]
color_of_path = optimised_result[3]

number_of_40_containers = math.floor(cargo_volume/67)
number_of_20_containers = math.ceil((cargo_volume % 67) / 33)

path_frame = pd.DataFrame(route)
rownum = path_frame.shape[0]
path_frame = pd.DataFrame(
    list(zip(path_frame.iloc[:rownum-1, 0], path_frame.iloc[1:rownum, 0])),
    columns=["From", "To"]
)

costlist = []
durationlist = []

for p in range(1, rownum - 1):
    currow = path_frame.iloc[p]
    V1, V2 = str(currow["V1"]), str(currow["V2"])
    rowmatch = paths[(paths["from_name"] == currow["V1"]) and (paths["to_name"] == currow["V2"])]

    if (len(rowmatch) == 0):
        dur = trucks.loc[trucks["X"] == currow["V1"], str(currow['V2'])]
        currcost = 6.9463*cargo_volume*dur
        currduation = dur

        nextnode = ports.loc[ports["name"] == currow["V2"]]

        if (ports.loc[ports["name"] == currow["V1"], "country"].values[0] != nextnode["country"]):
            currcost = currcost + cargo_value*nextnode["tax"]
    else:
        currcost = rowmatch["cost_air"]*50*cargo_volume + rowmatch["cost_train_20"]*33*number_of_20_containers + rowmatch["cost_train_40"]*67*number_of_40_containers + rowmatch["cost_ship_20"]*33*number_of_20_containers + rowmatch["cost_ship_40"]*67*number_of_40_containers
        currduation = rowmatch["duration"]

        if (rowmatch["to_country"] != rowmatch["from_country"]):
            currcost = currcost + cargo_value*(ports.loc[ports["name"] == currow["V2"]]["tax"])
            