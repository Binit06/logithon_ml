import pyspark
from pyspark.sql import functions as F
from pyspark.sql.functions import col, count
from pyspark import SparkConf
from pyspark.sql import SparkSession
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import json
from pyspark.sql.types import (StructType,
                               StructField,
                               DateType,
                               BooleanType,
                               DoubleType,
                               IntegerType,
                               StringType,
                               TimestampType)
flight_schema = StructType([StructField("legId", StringType(), True),
                            StructField("searchDate", StringType(), True),
                            StructField("flightDate", DateType(), True),
                            StructField("startingAirport", StringType(), True),
                            StructField("destinationAirport", StringType(), True),
                            StructField("fareBasisCode", StringType(), True),
                            StructField("travelDuration", StringType(), True),
                            StructField("elapsedDays", IntegerType(), True ),
                            StructField("isBasicEconomy", BooleanType(), True),
                            StructField("isRefundable", BooleanType(), True),
                            StructField("isNonStop", BooleanType(), True),
                            StructField("baseFare", DoubleType(), True),
                            StructField("totalFare", DoubleType(), True),
                            StructField("seatsRemaining", IntegerType(), True),
                            StructField("totalTravelDistance", IntegerType(), True)
                            ])
data_path = "new_data/processed_data.csv"
sc = pyspark.SparkContext(appName="price_predict")
spark = SparkSession.builder.appName("intro_to_spark").config("spark.executor.memory", "32g").config("spark.driver.memory", "32g").getOrCreate()
data = spark.read.csv(data_path, header=True, escape="\"")

ac = pd.read_csv("new_data/air_cost.csv", index_col=0)
columns = list(ac.columns)
# ac.loc[:, :] = 0
ac = ac.apply(pd.to_numeric, errors='coerce').fillna(0)

for row in data.toLocalIterator():
    if row["startingAirport"] in ac.index and row["destinationAirport"] in ac.columns:
        ac.loc[row["startingAirport"], row["destinationAirport"]] += float(row["totalFare"])


print(ac)
ac.to_csv("new_data/air_cost.csv", index=True)
# for i in range(0, ac.shape[0] - 1):
#     rowname = columns[i]
#     for j in range(0, len(columns) - 1):
#         if (rowname == columns[j]):
#             ac.loc[rowname, rowname] = 0

# print(ac)
# ac.to_csv("new_data/air_cost.csv", index=True)


#AIR COST DATAFRAME CREATION
#read node_coords
# air_cost = pd.read_csv("new_data/node_coords.csv")
# #make df of same row and column
# air_cost["Country"]

# air_cost = air_cost.loc[~air_cost.eq("\\N").any(axis=1)]
# duplicates = air_cost[air_cost.duplicated(subset=["IATA"], keep=False)] #check for duplicates
# if (duplicates.shape[0] > 0):
#     air_cost= air_cost.drop_duplicates(subset=["IATA"], keep="first")

# new_df = pd.DataFrame(index=air_cost["IATA"], columns=air_cost["IATA"])
# new_df[:] = np.nan

# new_df.to_csv("new_data/air_cost.csv")
