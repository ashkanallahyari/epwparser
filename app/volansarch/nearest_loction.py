# Finding N nearest locations
import pandas as pd
import numpy as np
import os
import json
from math import radians, sin, cos, sqrt, atan2
# Loading environment variables
from dotenv import load_dotenv

class EPWFileselection:
    def __init__(self, lat, lon, max_distance=None, loc_numbers=1):
        load_dotenv()
        self.settings = {
            "EPW_PATH": os.getenv("EPW_RAW_PATH"),
            "EPW_PARSED_PATH": os.getenv("EPW_PARSED_PATH"),
            "EPW_COMBINED_PATH": os.getenv("EPW_COMBINED_PATH"),
            "EPW_COMBINED_INDEX_NAME": os.getenv("EPW_COMBINED_INDEX_NAME"),
        }
        self.lat = lat
        self.lon = lon
        self.max_distance = max_distance
        self.loc_numbers = loc_numbers
        self.n_nearest_locations = self.find_nearest_location()
        self.file_name = self.loading_datasets(self.n_nearest_locations, "file_name")
        self.metadata = self.loading_datasets(self.n_nearest_locations, "metadata")
        self.data = self.loading_datasets(self.n_nearest_locations, "weather_data")

    # Haversine distance function
    def haversine(self, lat1, lon1, lat2, lon2):
        R = 6371  # Radius of Earth in km
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        return R * c
    
    # Function finding n nearest location
    def find_nearest_location(self):
        settings = self.settings

        index_path = os.path.join(settings["EPW_COMBINED_PATH"], settings["EPW_COMBINED_INDEX_NAME"])
        df = pd.read_csv(index_path)

        # Keep only the most recent year_end per location (latitude + longitude)
        df_latest = df.sort_values("year_end", ascending=False)
        df_latest = df_latest.drop_duplicates(subset=["latitude", "longitude"], keep="first")

        # Calculate distance for each remaining station
        df_latest["distance_km"] = df_latest.apply(
            lambda row: self.haversine(self.lat, self.lon, row["latitude"], row["longitude"]), axis=1
        )

        # Sort by distance
        df_sorted = df_latest.sort_values(by="distance_km", ascending=True)
        nearest_distance = df_sorted.iloc[0]["distance_km"]

        # Optionally filter by max_distance
        if self.max_distance is not None:
            df_sorted = df_sorted[df_sorted["distance_km"] <= nearest_distance+self.max_distance]
            n_nearest_locations = df_sorted.head(self.loc_numbers).reset_index(drop=True)
        else:
            n_nearest_locations = df_sorted.head(self.loc_numbers).reset_index(drop=True)

        return n_nearest_locations


    def loading_datasets(self, dataframe, field):
        settings = self.settings

        file_name_list = dataframe["file_name"].tolist()

        data_dict = {}

        for i, file_name in enumerate(file_name_list):
            base_name = os.path.splitext(file_name)[0]
            file_name = base_name + ".json"
            data_path = os.path.join(settings["EPW_PARSED_PATH"], file_name)
           
            # Load the JSON file
            with open(data_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                data_dict[field + "_" + str(i)] = data[field]

        return data_dict


