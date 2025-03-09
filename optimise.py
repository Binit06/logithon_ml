import math
import pyreadr

def optimise(origin, destination, duration_to_deliver, cargo_value, cargo_weight, cargo_volume, order_qty):
    num_of_40_containers = math.floor(cargo_volume/67)
    num_of_20_containers = math.ceil((cargo_volume % 67)/33)

    routes = pyreadr.read_r("data/routes.rds")[None]
    ports = pyreadr.read_r("data/ports.rds")[None]
    paths = pyreadr.read_r("data/paths.rds")[None]
    trucks = pyreadr.read_r("data/trucks.rds")[None]

    routes = routes[
        ((routes["A"].isna()) | (routes["A"] != origin)) &
        ((routes["A"].isna()) | (routes["A"] != destination)) &
        ((routes["B"].isna()) | (routes["B"] != origin)) &
        ((routes["B"].isna()) | (routes["B"] != destination))
    ]

    cost_result = math.pow(10, 26)
    duration_result = 0
    path_result = ""

    for _, row in routes.iterrows():
        route = row.dropna().astype(str).tolist()
        route = [origin] + route + [destination]

        print(route)

        total_cost = 0
        total_duration = 0
        mylength = len(routes)

        for j in range(1, mylength - 1):
            if ((total_duration > duration_to_deliver) or (total_cost > cost_result)):
                break
            curr = ports.loc[ports['name'] == route[j]]

            if (len(curr) == 0):
                continue
            else:
                total_cost = total_cost + curr['handling_cost']*cargo_weight + curr['custom_cost']*order_qty
                total_duration = total_duration + curr['handling_duration'] + curr['custom_duration']
            
            my_path = paths.loc[(paths['from_name'] == route[j - 1]) & (paths['to_name'] == route[j])]

            if len(my_path) == 0:
                total_duration = total_duration + trucks.loc[trucks["X"] == route[j - 1]][route[j]]
                total_cost = total_cost + 6.4963*cargo_volume*trucks.loc[(trucks["X"] == route[j - 1])][route[j]]

                next_node = ports.loc[(ports["name"] == route[j])]
                if(ports.loc[(ports["name"] == route[j - 1]),]["country"] != next_node["country"]):
                    total_cost = total_cost + cargo_value*next_node["tax"]
            else:
                if(my_path["to_country"].item() != my_path["from_country"].item()):
                    total_cost = total_cost + cargo_value*ports[(ports["name"] == my_path["to_name"]),]["tax"]
                to_last = route[j - 1][-2:]

                if (to_last == " S"):
                    total_cost = total_cost + my_path["cost_ship_20"].item()*33*num_of_20_containers + my_path["cost_ship_40"].item()*67*num_of_40_containers
                elif (to_last == " T"):
                    total_cost = total_cost + my_path["cost_train_20"].item()*33*num_of_20_containers + my_path["cost_train_20"].item()*67*num_of_40_containers
                else:
                    total_cost = total_cost + my_path["cost_air"].item()*50*cargo_volume
                
                total_duration = total_duration + my_path["duration"].item()
            print(total_duration, duration_to_deliver, total_cost, cost_result)
            print(total_duration <= duration_to_deliver) 
            print(total_cost < cost_result)

            print(total_cost.item())
            print(total_duration)
            print(route)
            if ((total_duration <= duration_to_deliver).all() and (total_cost < cost_result).all()):
                print(total_cost.item())
                cost_result = total_cost.item()
                duration_result = total_duration.item()
                path_result = route
            
            print(cost_result)
            path_type_order = []

            if path_result:
                for i in range(len(path_result) - 1):
                    from_last = path_result[i][-2:]
                    to_last = path_result[i + 1][-2:]

                    temp_path = paths[
                        (paths["from_name"] == path_result[i]) & (paths["to_name"] == path_result[i + 1])
                    ]

                    if temp_path.empty:
                        path_type_order.append(4)
                    else:
                        if from_last == "A":
                            path_type_order.append(1)
                        elif from_last == " S":
                            path_type_order.append(2)
                        else:
                            path_type_order.append(3)
            print([cost_result, path_result, duration_result, path_type_order])
            return [cost_result, path_result, duration_result, path_type_order]

