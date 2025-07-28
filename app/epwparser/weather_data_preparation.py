import pandas as pd
import os
import json
import zipfile
from datetime import datetime

# Loading environment variables
from dotenv import load_dotenv

class EPWFilePreparator:
    def __init__(self):
        load_dotenv()
        self.settings = {
            "EPW_RAW_PATH": os.getenv("EPW_RAW_PATH"),
            "EPW_PARSED_PATH": os.getenv("EPW_PARSED_PATH"),
            "EPW_COMBINED_PATH": os.getenv("EPW_COMBINED_PATH"),
            "EPW_COMBINED_INDEX_NAME": os.getenv("EPW_COMBINED_INDEX_NAME"),
        }
        self.raw_data_file_names = self.list_files_in_directory(self.settings["EPW_RAW_PATH"])
        self.parsed_data_file_names = self.list_files_in_directory(self.settings["EPW_PARSED_PATH"])

    def parse_file(self, file_name):
        settings = self.settings
        # Creating the loading path
        file_path = os.path.join(settings["EPW_RAW_PATH"], file_name)

        # Opening file depending the format
        if os.path.splitext(file_name)[-1] == ".zip":
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                # Filter for .epw files
                epw_file = next((f for f in zip_ref.namelist() if f.endswith('.epw')), None)

                with zip_ref.open(epw_file) as file:
                    lines = [line.decode('utf-8') for line in file.readlines()]

        elif os.path.splitext(file_name)[-1] == ".epw":
            with open(file_path, 'r') as file:
                lines = file.readlines()

        else:
            raise ValueError("Unsupported file format. Only .zip and .epw files are allowed.")

        # Parsing data
        data = {}

        # File name
        data["file_name"] = file_path.split("\\")[-1]

        # Extracting location data
        location_row = lines[0].split(",")

        data["location"] = {
            "city": location_row[1],
            "state_province": location_row[2],
            "country": location_row[3],
            "data_source": location_row[4],
            "station_id": location_row[5],
            "latitude": float(location_row[6]),
            "longitude": float(location_row[7]),
            "timezone": float(location_row[8]),
            "elevation_meters": float(location_row[9]),
        }

        # Metadata
        # 1. DESIGN CONDITIONS
        design_conditions_row = lines[1].split(",")

        try:
            heating_index = design_conditions_row.index("Heating")
        except ValueError:
            heating_index = None

        try:
            cooling_index = design_conditions_row.index("Cooling")
        except ValueError:
            cooling_index = None
            
        try:
            extreme_index = design_conditions_row.index("Extremes")
        except ValueError:
            extreme_index = None

        data["metadata"] = {}
        
        data["metadata"]["design_conditions"] = {
            "flag": int(design_conditions_row[1]),
            "source_description": design_conditions_row[2] if len(design_conditions_row) > 2 else None,
            "heating": {
                "Identifier": int(design_conditions_row[heating_index + 1]),    # Identifier for the heating season (likely a month, e.g., 1 = January).
                "DB_99.6": float(design_conditions_row[heating_index + 2]),     # 99.6% heating dry-bulb temperature (°C).
                "DB_99.6": float(design_conditions_row[heating_index + 3]),   # 99% heating dry-bulb temperature (°C).
                "DB_Mean": float(design_conditions_row[heating_index + 4]),   # Mean daily minimum dry-bulb temperature (°C).
                "WS_99.6": float(design_conditions_row[heating_index + 5]),   # Wind speed at 99.6% heating condition (m/s).
                "MCW_99.6": float(design_conditions_row[heating_index + 6]),   # Mean coincident wet-bulb temperature at 99.6% condition (°C).
                "MCW_99": float(design_conditions_row[heating_index + 7]),   # Mean coincident wet-bulb temperature at 99% condition (°C).
                "MCW_Mean": float(design_conditions_row[heating_index + 8]),   # Mean wind speed during heating conditions (m/s).
                "DB_Range": float(design_conditions_row[heating_index + 9]),   # Daily temperature range during heating conditions (°C).
                "WS_Max": float(design_conditions_row[heating_index + 10]),   # Maximum wind speed during heating conditions (m/s).
                "WS_Mean2": float(design_conditions_row[heating_index + 11]),   # Secondary mean wind speed or related metric (m/s).
                "WS_Std": float(design_conditions_row[heating_index + 12]),   # Standard deviation of wind speed (m/s).
                "WS_Mean3": float(design_conditions_row[heating_index + 13]),   # Tertiary mean wind speed or related metric (m/s).
                "WS_Dir": float(design_conditions_row[heating_index + 14]),   # Prevailing wind direction (degrees).
                "WD_Primary": float(design_conditions_row[heating_index + 15]),   # Primary wind direction (degrees).
                "Clearness": float(design_conditions_row[heating_index + 16]),   # Clearness number or humidity-related coefficient.
            } if heating_index else None,
            "cooling": {
                "Identifier": int(design_conditions_row[cooling_index + 1]),    # Identifier for the cooling season (likely a month, e.g., 1 = January).
                "Evap_DB": float(design_conditions_row[cooling_index + 2]),     # Evaporation dry-bulb temperature (°C).
                "DB_0.4": float(design_conditions_row[cooling_index + 3]),     # 0.4% cooling dry-bulb temperature (°C).
                "MCW_0.4": float(design_conditions_row[cooling_index + 4]),     # Mean coincident wet-bulb temperature at 0.4% condition (°C).
                "DB_1": float(design_conditions_row[cooling_index + 5]),     # 1% cooling dry-bulb temperature (°C).
                "MCW_1": float(design_conditions_row[cooling_index + 6]),     # Mean coincident wet-bulb temperature at 1% condition (°C).
                "DB_2": float(design_conditions_row[cooling_index + 7]),     # 2% cooling dry-bulb temperature (°C).
                "MCW_2": float(design_conditions_row[cooling_index + 8]),     # Mean coincident wet-bulb temperature at 2% condition (°C).
                "WB_0.4": float(design_conditions_row[cooling_index + 9]),     # 0.4% wet-bulb temperature (°C).
                "MCD_0.4": float(design_conditions_row[cooling_index + 10]),     # Mean coincident dry-bulb temperature at 0.4% wet-bulb (°C).
                "MCD_1": float(design_conditions_row[cooling_index + 11]),     # Mean coincident dry-bulb temperature at 1% wet-bulb (°C).
                "WB_1": float(design_conditions_row[cooling_index + 12]),     # 1% wet-bulb temperature (°C).
                "MCD_2": float(design_conditions_row[cooling_index + 13]),     # Mean coincident dry-bulb temperature at 2% wet-bulb (°C).
                "WB_2": float(design_conditions_row[cooling_index + 14]),     # 2% wet-bulb temperature (°C).
                "WS_0.4": float(design_conditions_row[cooling_index + 15]),     # Wind speed at 0.4% cooling condition (m/s).
                "WD_Primary": float(design_conditions_row[cooling_index + 16]),     # Primary wind direction during cooling conditions (degrees).
                "DP_0.4": float(design_conditions_row[cooling_index + 17]),     # 0.4% dew point temperature (°C).
                "MCDP_0.4": float(design_conditions_row[cooling_index + 18]),     # Mean coincident dry-bulb at 0.4% dew point (°C).
                "DP_1": float(design_conditions_row[cooling_index + 19]),     # 1% dew point temperature (°C).
                "MCDP_1": float(design_conditions_row[cooling_index + 20]),     # Mean coincident dry-bulb at 1% dew point (°C).
                "DP_2": float(design_conditions_row[cooling_index + 21]),     # 2% dew point temperature (°C).
                "MCDP_2": float(design_conditions_row[cooling_index + 22]),     # Mean coincident dry-bulb at 2% dew point (°C).
                "HR_0.4": float(design_conditions_row[cooling_index + 23]),     # Humidity ratio at 0.4% condition (g/kg).
                "HR_1": float(design_conditions_row[cooling_index + 24]),     # Humidity ratio at 1% condition (g/kg).
                "HR_2": float(design_conditions_row[cooling_index + 25]),     # Humidity ratio at 2% condition (g/kg).
                "RH_0.4": float(design_conditions_row[cooling_index + 26]),     # Relative humidity at 0.4% condition (%).
                "MCD_0.4_RH": float(design_conditions_row[cooling_index + 27]),     # Mean coincident dry-bulb at 0.4% relative humidity (°C).
                "RH_1": float(design_conditions_row[cooling_index + 28]),     # Relative humidity at 1% condition (%).
                "MCD_1_RH": float(design_conditions_row[cooling_index + 29]),     # Mean coincident dry-bulb at 1% relative humidity (°C).
                "RH_2": float(design_conditions_row[cooling_index + 30]),     # Relative humidity at 2% condition (%).
                "MCD_2_RH": float(design_conditions_row[cooling_index + 31]),     # Mean coincident dry-bulb at 2% relative humidity (°C).
                "DB_Mean": float(design_conditions_row[cooling_index + 32]),     # Mean dry-bulb temperature during cooling conditions (°C).
            } if cooling_index else None,
            "extreme": {
                "Std_DB": float(design_conditions_row[extreme_index + 1]),     # Standard deviation of annual dry-bulb temperature (°C).
                "Std_DB_2": float(design_conditions_row[extreme_index + 2]),     # Secondary standard deviation of dry-bulb temperature (°C).
                "Std_DB_3": float(design_conditions_row[extreme_index + 3]),     # Tertiary standard deviation of dry-bulb temperature (°C).
                "Min_DB_Annual": float(design_conditions_row[extreme_index + 4]),     # Annual minimum dry-bulb temperature (°C).
                "Max_DB_Annual": float(design_conditions_row[extreme_index + 5]),     # Annual maximum dry-bulb temperature (°C).
                "Std_WS": float(design_conditions_row[extreme_index + 6]),     # Standard deviation of wind speed (m/s).
                "Std_WS_2": float(design_conditions_row[extreme_index + 7]),     # Secondary standard deviation of wind speed (m/s).
                "Min_DB_5yr": float(design_conditions_row[extreme_index + 8]),     # 5-year return minimum dry-bulb temperature (°C).
                "Max_DB_5yr": float(design_conditions_row[extreme_index + 9]),     # 5-year return maximum dry-bulb temperature (°C).
                "Min_DB_10yr": float(design_conditions_row[extreme_index + 10]),     # 10-year return minimum dry-bulb temperature (°C).
                "Max_DB_10yr": float(design_conditions_row[extreme_index + 11]),     # 10-year return maximum dry-bulb temperature (°C).
                "Min_DB_20yr": float(design_conditions_row[extreme_index + 12]),     # 20-year return minimum dry-bulb temperature (°C).
                "Max_DB_20yr": float(design_conditions_row[extreme_index + 13]),     # 20-year return maximum dry-bulb temperature (°C).
                "Min_DB_50yr": float(design_conditions_row[extreme_index + 14]),     # 50-year return minimum dry-bulb temperature (°C).
                "Max_DB_50yr": float(design_conditions_row[extreme_index + 15]),     # 50-year return maximum dry-bulb temperature (°C).
            } if extreme_index else None,
        }

        # 2. TYPICAL/EXTREME PERIODS
        typical_extreme_periods_row = lines[2].split(",")

        data["metadata"]["typical_extreme_periods"] = {
            "Number_of_Periods": int(typical_extreme_periods_row[1]),         # Number of periods.
            "Period_1_Name": typical_extreme_periods_row[2].strip(),                    # Name of the first period (Summer max temp).
            "Period_1_Type": typical_extreme_periods_row[3].strip(),                    # Type of the first period (Typical or Extreme).
            "Period_1_Start_Date": typical_extreme_periods_row[4].strip(),              # Start date of the first period (M/D).
            "Period_1_End_Date": typical_extreme_periods_row[5].strip(),                # End date of the first period (M/D).
            "Period_2_Name": typical_extreme_periods_row[6].strip(),                    # Name of the second period (Summer avg temp).
            "Period_2_Type": typical_extreme_periods_row[7].strip(),                    # Type of the second period (Typical or Extreme).
            "Period_2_Start_Date": typical_extreme_periods_row[8].strip(),              # Start date of the second period (M/D).
            "Period_2_End_Date": typical_extreme_periods_row[9].strip(),                # End date of the second period (M/D).
            "Period_3_Name": typical_extreme_periods_row[10].strip(),                   # Name of the third period (Winter min temp).
            "Period_3_Type": typical_extreme_periods_row[11].strip(),                    # Type of the third period (Typical or Extreme).
            "Period_3_Start_Date": typical_extreme_periods_row[12].strip(),              # Start date of the third period (M/D).
            "Period_3_End_Date": typical_extreme_periods_row[13].strip(),                # End date of the third period (M/D).
            "Period_4_Name": typical_extreme_periods_row[14].strip(),                   # Name of the fourth period (Winter avg temp).
            "Period_4_Type": typical_extreme_periods_row[15].strip(),                    # Type of the fourth period (Typical or Extreme).
            "Period_4_Start_Date": typical_extreme_periods_row[16].strip(),              # Start date of the fourth period (M/D).
            "Period_4_End_Date": typical_extreme_periods_row[17].strip(),                # End date of the fourth period (M/D).
            "Period_5_Name": typical_extreme_periods_row[18].strip(),                   # Name of the fifth period (Autumn avg temp).
            "Period_5_Type": typical_extreme_periods_row[19].strip(),                    # Type of the fifth period (Typical or Extreme).
            "Period_5_Start_Date": typical_extreme_periods_row[20].strip(),              # Start date of the fifth period (M/D).
            "Period_5_End_Date": typical_extreme_periods_row[21].strip(),                # End date of the fifth period (M/D).
            "Period_6_Name": typical_extreme_periods_row[22].strip(),                   # Name of the sixth period (Spring avg temp).
            "Period_6_Type": typical_extreme_periods_row[23].strip(),                    # Type of the sixth period (Typical or Extreme).
            "Period_6_Start_Date": typical_extreme_periods_row[24].strip(),              # Start date of the sixth period (M/D).
            "Period_6_End_Date": typical_extreme_periods_row[25].strip(),                # End date of the sixth period (M/D).
        }

        # 3. GROUND TEMPERATURES
        ground_temperatures_row = lines[3].split(",")

        data["metadata"]["ground_temperatures"] = {
            "Number_of_Depths": int(ground_temperatures_row[1]) if ground_temperatures_row[1] != "" else None,              # Number of ground temperature depths.
            "Depth_1_Value": float(ground_temperatures_row[2]) if ground_temperatures_row[2] != "" else None,               # Depth value for ground temperature 1 (m).
            "Depth_1_Conductivity": float(ground_temperatures_row[3]) if ground_temperatures_row[3] != "" else None,       # Soil thermal conductivity (W/m·K)
            "Depth_1_Density":	float(ground_temperatures_row[4]) if ground_temperatures_row[4] != "" else None,            # Soil density (kg/m³)
            "Depth_1_Specific_Heat": float(ground_temperatures_row[5]) if ground_temperatures_row[5] != "" else None,    # Soil specific heat (J/kg·K)
            "Depth_1_Jan": float(ground_temperatures_row[6]) if ground_temperatures_row[6] != "" else None,                 # Avg ground temp for depth 1 in January (°C).
            "Depth_1_Feb": float(ground_temperatures_row[7]) if ground_temperatures_row[7] != "" else None,                 # Avg ground temp for depth 1 in February (°C).
            "Depth_1_Mar": float(ground_temperatures_row[8]) if ground_temperatures_row[8] != "" else None,                 # Avg ground temp for depth 1 in March (°C).
            "Depth_1_Apr": float(ground_temperatures_row[9]) if ground_temperatures_row[9] != "" else None,                 # Avg ground temp for depth 1 in April (°C).
            "Depth_1_May": float(ground_temperatures_row[10]) if ground_temperatures_row[10] != "" else None,                # Avg ground temp for depth 1 in May (°C).
            "Depth_1_Jun": float(ground_temperatures_row[11]) if ground_temperatures_row[11] != "" else None,                # Avg ground temp for depth 1 in June (°C).
            "Depth_1_Jul": float(ground_temperatures_row[12]) if ground_temperatures_row[12] != "" else None,                # Avg ground temp for depth 1 in July (°C).
            "Depth_1_Aug": float(ground_temperatures_row[13]) if ground_temperatures_row[13] != "" else None,                # Avg ground temp for depth 1 in August (°C).
            "Depth_1_Sep": float(ground_temperatures_row[14]) if ground_temperatures_row[14] != "" else None,                # Avg ground temp for depth 1 in September (°C).
            "Depth_1_Oct": float(ground_temperatures_row[15]) if ground_temperatures_row[15] != "" else None,                # Avg ground temp for depth 1 in October (°C).
            "Depth_1_Nov": float(ground_temperatures_row[16]) if ground_temperatures_row[16] != "" else None,                # Avg ground temp for depth 1 in November (°C).
            "Depth_1_Dec": float(ground_temperatures_row[17]) if ground_temperatures_row[17] != "" else None,                # Avg ground temp for depth 1 in December (°C).
            "Depth_2_Value": float(ground_temperatures_row[18]) if ground_temperatures_row[18] != "" else None,               # Depth value for ground temperature 2 (m).
            "Depth_2_Conductivity": float(ground_temperatures_row[19]) if ground_temperatures_row[19] != "" else None,       # Soil thermal conductivity (W/m·K)
            "Depth_2_Density":	float(ground_temperatures_row[20]) if ground_temperatures_row[20] != "" else None,            # Soil density (kg/m³)
            "Depth_2_Specific_Heat": float(ground_temperatures_row[21]) if ground_temperatures_row[21] != "" else None,    # Soil specific heat (J/kg·K)
            "Depth_2_Jan": float(ground_temperatures_row[22]) if ground_temperatures_row[22] != "" else None,                 # Avg ground temp for depth 2 in January (°C).
            "Depth_2_Feb": float(ground_temperatures_row[23]) if ground_temperatures_row[23] != "" else None,                 # Avg ground temp for depth 2 in February (°C).
            "Depth_2_Mar": float(ground_temperatures_row[24]) if ground_temperatures_row[24] != "" else None,                 # Avg ground temp for depth 2 in March (°C).
            "Depth_2_Apr": float(ground_temperatures_row[25]) if ground_temperatures_row[25] != "" else None,                 # Avg ground temp for depth 2 in April (°C).
            "Depth_2_May": float(ground_temperatures_row[26]) if ground_temperatures_row[26] != "" else None,                # Avg ground temp for depth 2 in May (°C).
            "Depth_2_Jun": float(ground_temperatures_row[27]) if ground_temperatures_row[27] != "" else None,                # Avg ground temp for depth 2 in June (°C).
            "Depth_2_Jul": float(ground_temperatures_row[28]) if ground_temperatures_row[28] != "" else None,                # Avg ground temp for depth 2 in July (°C).
            "Depth_2_Aug": float(ground_temperatures_row[29]) if ground_temperatures_row[29] != "" else None,                # Avg ground temp for depth 2 in August (°C).
            "Depth_2_Sep": float(ground_temperatures_row[30]) if ground_temperatures_row[30] != "" else None,                # Avg ground temp for depth 2 in September (°C).
            "Depth_2_Oct": float(ground_temperatures_row[31]) if ground_temperatures_row[31] != "" else None,                # Avg ground temp for depth 2 in October (°C).
            "Depth_2_Nov": float(ground_temperatures_row[32]) if ground_temperatures_row[32] != "" else None,                # Avg ground temp for depth 2 in November (°C).
            "Depth_2_Dec": float(ground_temperatures_row[33]) if ground_temperatures_row[33] != "" else None,                # Avg ground temp for depth 2 in December (°C).
            "Depth_3_Value": float(ground_temperatures_row[34]) if ground_temperatures_row[34] != "" else None,               # Depth value for ground temperature 3 (m).
            "Depth_3_Conductivity": float(ground_temperatures_row[35]) if ground_temperatures_row[35] != "" else None,       # Soil thermal conductivity (W/m·K)
            "Depth_3_Density":	float(ground_temperatures_row[36]) if ground_temperatures_row[36] != "" else None,            # Soil density (kg/m³)
            "Depth_3_Specific_Heat": float(ground_temperatures_row[37]) if ground_temperatures_row[37] != "" else None,    # Soil specific heat (J/kg·K)
            "Depth_3_Jan": float(ground_temperatures_row[38]) if ground_temperatures_row[38] != "" else None,                 # Avg ground temp for depth 3 in January (°C).
            "Depth_3_Feb": float(ground_temperatures_row[39]) if ground_temperatures_row[39] != "" else None,                 # Avg ground temp for depth 3 in February (°C).
            "Depth_3_Mar": float(ground_temperatures_row[40]) if ground_temperatures_row[40] != "" else None,                 # Avg ground temp for depth 3 in March (°C).
            "Depth_3_Apr": float(ground_temperatures_row[41]) if ground_temperatures_row[41] != "" else None,                 # Avg ground temp for depth 3 in April (°C).
            "Depth_3_May": float(ground_temperatures_row[42]) if ground_temperatures_row[42] != "" else None,                # Avg ground temp for depth 3 in May (°C).
            "Depth_3_Jun": float(ground_temperatures_row[43]) if ground_temperatures_row[43] != "" else None,                # Avg ground temp for depth 3 in June (°C).
            "Depth_3_Jul": float(ground_temperatures_row[44]) if ground_temperatures_row[44] != "" else None,                # Avg ground temp for depth 3 in July (°C).
            "Depth_3_Aug": float(ground_temperatures_row[45]) if ground_temperatures_row[45] != "" else None,                # Avg ground temp for depth 3 in August (°C).
            "Depth_3_Sep": float(ground_temperatures_row[46]) if ground_temperatures_row[46] != "" else None,                # Avg ground temp for depth 3 in September (°C).
            "Depth_3_Oct": float(ground_temperatures_row[47]) if ground_temperatures_row[47] != "" else None,                # Avg ground temp for depth 3 in October (°C).
            "Depth_3_Nov": float(ground_temperatures_row[48]) if ground_temperatures_row[48] != "" else None,                # Avg ground temp for depth 3 in November (°C).
            "Depth_3_Dec": float(ground_temperatures_row[49]) if ground_temperatures_row[49] != "" else None,                # Avg ground temp for depth 3 in December (°C).
        }

        # 4. HARDCODED DATA
        holidays_daylight_saving_row = lines[4].split(",")

        data["metadata"]["holidays_daylight_saving"] = {
            "Leap_Year_Observed": holidays_daylight_saving_row[1].strip(),             # Indicates if leap year is observed ("Yes" or "No").
            "Daylight_Saving_Start_Day": int(holidays_daylight_saving_row[2]),         # Daylight saving start day (date format or "0" if not observed).
            "Daylight_Saving_End_Day": int(holidays_daylight_saving_row[3]),           # Daylight saving end day (date format or "0" if not observed).
            "Number_of_Holidays": int(holidays_daylight_saving_row[4]),                # Number of holidays defined (integer).
        }

        # 5. Comments
        data["metadata"]["comments"] = {
            "Comments_1": lines[5].strip(),
            "Comments_2": lines[6].strip(),
        }

        # 6. Data Period
        data_period_row = lines[7].split(",")

        data["metadata"]["data_period"] = {
            "Number_of_Data_Periods": int(data_period_row[1]),           # Total number of data periods in the file (integer).
            "Data_Period_1_Start_Date": int(data_period_row[2]),         # Index of the current data period (integer, starts from 1).
            "Data_Period_1_End_Date": data_period_row[3].strip(),        # Name of the data period (string).
            "Start_Day_of_Week": data_period_row[4].strip(),             # Day of the week on which the data period starts (string).
            "Data_Period_2_Start_Date": data_period_row[5].strip(),      # Start date of the data period in "M/D" format (string).
            "Data_Period_2_End_Date": data_period_row[6].strip(),        # End date of the data period (M/D format) (string).
        }

        # Main data
        weather_data = []

        for i in range(8, len(lines)):
            data_row = lines[i].split(",")

            weather_data.append({
                "Year": int(data_row[0]),                                # Year of the data (e.g., 2019).
                "Month": int(data_row[1]),                               # Month of the data (1-12).
                "Day": int(data_row[2]),                                 # Day of the month (1-31).
                "Hour": int(data_row[3]),                                # Hour of the day (1-24, where 1 is 00:00:01-01:00:00).
                "Minute": int(data_row[4]),                              # Minute of the hour (0-59, typically 0 or 30).
                "Data_Source_Uncertainty_Flags": data_row[5].strip(),    # String indicating data source and uncertainty.
                "Dry_Bulb_Temperature": float(data_row[6]),               # Dry bulb temperature (°C).
                "Dew_Point_Temperature": float(data_row[7]),              # Dew point temperature (°C).
                "Relative_Humidity": float(data_row[8]),                   # Relative humidity (0-100%).
                "Atmospheric_Station_Pressure": float(data_row[9]),         # Atmospheric pressure at the station (Pa).
                "Extraterrestrial_Horizontal_Radiation": float(data_row[10]), # Extraterrestrial horizontal radiation (Wh/m²).
                "Extraterrestrial_Direct_Normal_Radiation": float(data_row[11]), # Extraterrestrial direct normal radiation (Wh/m²).
                "Horizontal_Infrared_Radiation_Intensity": float(data_row[12]), # Horizontal infrared radiation intensity (Wh/m²).
                "Global_Horizontal_Radiation": float(data_row[13]), # Global horizontal radiation (Wh/m²).
                "Direct_Normal_Radiation": float(data_row[14]), # Direct normal radiation (Wh/m²).
                "Diffuse_Horizontal_Radiation": float(data_row[15]), # Diffuse horizontal radiation (Wh/m²).
                "Global_Horizontal_Illuminance": float(data_row[16]), # Global horizontal illuminance (lux).
                "Direct_Normal_Illuminance": float(data_row[17]), # Direct normal illuminance (lux).
                "Diffuse_Horizontal_Illuminance": float(data_row[18]), # Diffuse horizontal illuminance (lux).
                "Zenith_Luminance": float(data_row[19]), # Zenith luminance (cd/m²).
                "Wind_Direction": float(data_row[20]), # Wind direction (degrees, 0-360).
                "Wind_Speed": float(data_row[21]), # Wind speed (m/s).
                "Total_Sky_Cover": float(data_row[22]), # Total sky cover (%).
                "Opaque_Sky_Cover": float(data_row[23]), # Opaque sky cover (%).
                "Visibility": float(data_row[24]), # Visibility (km).
                "Ceiling_Height": float(data_row[25]), # Ceiling height (m).
                "Present_Weather_Observation": float(data_row[26]), # Present weather observation code.
                "Present_Weather_Codes": float(data_row[27]), # Additional present weather codes.
                "Precipitable_Water": float(data_row[28]), # Precipitable water (mm).
                "Aerosol_Optical_Depth": float(data_row[29]), # Aerosol optical depth (unitless).
                "Snow_Depth": float(data_row[30]), # Snow depth (cm).
                "Days_Since_Last_Snowfall": float(data_row[31]), # Number of days since last snowfall.
                "Albedo": float(data_row[32]), # Albedo (unitless).
                "Liquid_Precipitation_Depth": float(data_row[33]), # Liquid precipitation depth (mm).
                "Liquid_Precipitation_Quantity": float(data_row[34]), # Liquid precipitation quantity (mm).
            })

        data["weather_data"] = weather_data

        # Adding data period to the weather data
        years = [row["Year"] for row in data["weather_data"]]
        data["metadata"]["year_start"] = min(years)
        data["metadata"]["year_end"] = max(years)

        # Saving the data to a csv file
        # Creating the save path
        # Change the file extension to .json
        base_name = os.path.splitext(file_name)[0]
        save_name = base_name + ".json"
        save_path = os.path.join(settings["EPW_PARSED_PATH"], save_name)

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "w") as file:
            json.dump(data, file, indent=4)

        # Updating the combined index file
        EPW_COMBINED_PATH = os.path.join(settings["EPW_COMBINED_PATH"], settings["EPW_COMBINED_INDEX_NAME"])

        if os.path.exists(EPW_COMBINED_PATH):
            summary_df = pd.read_csv(EPW_COMBINED_PATH)
        else:
            summary_df = pd.DataFrame(columns=[
                "file_name", "city", "state_province", "country",
                "latitude", "longitude", "elevation_meters",
                "year_start", "year_end"
            ])

        # Extract info from parsed data
        loc = data["location"]
        meta = data["metadata"]

        new_entry = {
            "file_name": data["file_name"],
            "city": loc.get("city"),
            "state_province": loc.get("state_province"),
            "country": loc.get("country"),
            "latitude": loc.get("latitude"),
            "longitude": loc.get("longitude"),
            "elevation_meters": loc.get("elevation_meters"),
            "year_start": meta.get("year_start"),
            "year_end": meta.get("year_end")
        }

        # Drop any existing entry for this file (in case of re-parse)
        summary_df = summary_df[summary_df["file_name"] != data["file_name"]]

        # Append the new entry
        summary_df = pd.concat([summary_df, pd.DataFrame([new_entry])], ignore_index=True)
        
        # Save back
        os.makedirs(os.path.dirname(EPW_COMBINED_PATH), exist_ok=True)
        summary_df.to_csv(EPW_COMBINED_PATH, index=False)

        return data

    def list_files_in_directory(self, directory_path):
        if os.path.isdir(directory_path):
            files = [file for file in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file))]
        else:
            files = None

        return files


    def list_files_needed_update(self):
        settings = self.settings
        # Creating the loading path
        path_raw = settings["EPW_RAW_PATH"]
        path_parsed = settings["EPW_PARSED_PATH"]

        raw_files = [file for file in os.listdir(path_raw) if os.path.isfile(os.path.join(path_raw, file))]
        raw_files_format_removed = [os.path.splitext(filename)[0] for filename in raw_files]

        parsed_files = [file for file in os.listdir(path_parsed) if os.path.isfile(os.path.join(path_parsed, file))]
        parsed_files_format_removed = [os.path.splitext(filename)[0] for filename in parsed_files]

        # Remove items in list1 that are also in list2
        filtered_list = [item for item in raw_files_format_removed if item not in parsed_files_format_removed]
        filtered_list_zip = [item + ".zip" for item in filtered_list]

        return filtered_list_zip

