EPW Dataset Structure and Documentation
Overview
You can download raw data from https://climate.onebuilding.org/

The EnergyPlus Weather (EPW) file format is a standard format for weather data used in building energy simulation programs like EnergyPlus. It contains detailed meteorological data for a specific location, including hourly weather conditions, design conditions, and other metadata relevant for energy simulations. This documentation outlines the structure of the EPW dataset as parsed by the provided Python script.
File Structure
An EPW file is a comma-separated text file with the following sections:

Header (Lines 1-8): Contains metadata about the location, design conditions, typical/extreme periods, ground temperatures, holidays, comments, and data periods.
Weather Data (Line 9 onwards): Contains hourly weather observations for an entire year or a specified period.

Below is a detailed breakdown of each section.

Header Section
The header consists of eight lines, each beginning with a keyword indicating the type of data, followed by comma-separated values.
1. Location (Line 1)
Contains geographical and station-related metadata.



Field
Description
Type
Example



Keyword
Always "LOCATION"
String
LOCATION


City
City name
String
Chicago


State/Province
State or province name
String
IL


Country
Country name
String
USA


Data Source
Source of the weather data
String
TMY3


Station ID
Weather station identifier (e.g., WMO number)
String
725300


Latitude
Latitude of the location (degrees, positive north)
Float
41.78


Longitude
Longitude of the location (degrees, positive east)
Float
-87.75


Timezone
Time zone offset from GMT (hours)
Float
-6.0


Elevation
Elevation above sea level (meters)
Float
190.0


2. Design Conditions (Line 2)
Provides climatic design conditions for heating, cooling, and extreme conditions. The structure is dynamic, with subsections for "Heating," "Cooling," and "Extremes" identified by their respective keywords.



Field
Description
Type
Notes



Keyword
Always "DESIGN CONDITIONS"
String



Flag
Indicates if design conditions are present (1 = present, 0 = absent)
Integer



Source Description
Description of the data source
String
Optional


Heating Subsection
(If "Heating" keyword is present)




Identifier
Month identifier for heating season (e.g., 1 = January)
Integer



DB_99.6
99.6% heating dry-bulb temperature (°C)
Float



DB_99
99% heating dry-bulb temperature (°C)
Float



DB_Mean
Mean daily minimum dry-bulb temperature (°C)
Float



WS_99.6
Wind speed at 99.6% heating condition (m/s)
Float



MCW_99.6
Mean coincident wet-bulb temperature at 99.6% (°C)
Float



MCW_99
Mean coincident wet-bulb temperature at 99% (°C)
Float



MCW_Mean
Mean wind speed during heating conditions (m/s)
Float



DB_Range
Daily temperature range during heating conditions (°C)
Float



WS_Max
Maximum wind speed during heating conditions (m/s)
Float



WS_Mean2
Secondary mean wind speed (m/s)
Float



WS_Std
Standard deviation of wind speed (m/s)
Float



WS_Mean3
Tertiary mean wind speed (m/s)
Float



WS_Dir
Prevailing wind direction (degrees)
Float



WD_Primary
Primary wind direction (degrees)
Float



Clearness
Clearness number or humidity-related coefficient
Float



Cooling Subsection
(If "Cooling" keyword is present)




Identifier
Month identifier for cooling season (e.g., 7 = July)
Integer



Evap_DB
Evaporation dry-bulb temperature (°C)
Float



DB_0.4
0.4% cooling dry-bulb temperature (°C)
Float



MCW_0.4
Mean coincident wet-bulb temperature at 0.4% (°C)
Float



DB_1
1% cooling dry-bulb temperature (°C)
Float



MCW_1
Mean coincident wet-bulb temperature at 1% (°C)
Float



DB_2
2% cooling dry-bulb temperature (°C)
Float



MCW_2
Mean coincident wet-bulb temperature at 2% (°C)
Float



WB_0.4
0.4% wet-bulb temperature (°C)
Float



MCD_0.4
Mean coincident dry-bulb at 0.4% wet-bulb (°C)
Float



MCD_1
Mean coincident dry-bulb at 1% wet-bulb (°C)
Float



WB_1
1% wet-bulb temperature (°C)
Float



MCD_2
Mean coincident dry-bulb at 2% wet-bulb (°C)
Float



WB_2
2% wet-bulb temperature (°C)
Float



WS_0.4
Wind speed at 0.4% cooling condition (m/s)
Float



WD_Primary
Primary wind direction during cooling (degrees)
Float



DP_0.4
0.4% dew point temperature (°C)
Float



MCDP_0.4
Mean coincident dry-bulb at 0.4% dew point (°C)
Float



DP_1
1% dew point temperature (°C)
Float



MCDP_1
Mean coincident dry-bulb at 1% dew point (°C)
Float



DP_2
2% dew point temperature (°C)
Float



MCDP_2
Mean coincident dry-bulb at 2% dew point (°C)
Float



HR_0.4
Humidity ratio at 0.4% condition (g/kg)
Float



HR_1
Humidity ratio at 1% condition (g/kg)
Float



HR_2
Humidity ratio at 2% condition (g/kg)
Float



RH_0.4
Relative humidity at 0.4% condition (%)
Float



MCD_0.4_RH
Mean coincident dry-bulb at 0.4% relative humidity (°C)
Float



RH_1
Relative humidity at 1% condition (%)
Float



MCD_1_RH
Mean coincident dry-bulb at 1% relative humidity (°C)
Float



RH_2
Relative humidity at 2% condition (%)
Float



MCD_2_RH
Mean coincident dry-bulb at 2% relative humidity (°C)
Float



DB_Mean
Mean dry-bulb temperature during cooling (°C)
Float



Extremes Subsection
(If "Extremes" keyword is present)




Std_DB
Standard deviation of annual dry-bulb temperature (°C)
Float



Std_DB_2
Secondary standard deviation of dry-bulb temperature (°C)
Float



Std_DB_3
Tertiary standard deviation of dry-bulb temperature (°C)
Float



Min_DB_Annual
Annual minimum dry-bulb temperature (°C)
Float



Max_DB_Annual
Annual maximum dry-bulb temperature (°C)
Float



Std_WS
Standard deviation of wind speed (m/s)
Float



Std_WS_2
Secondary standard deviation of wind speed (m/s)
Float



Min_DB_5yr
5-year return minimum dry-bulb temperature (°C)
Float



Max_DB_5yr
5-year return maximum dry-bulb temperature (°C)
Float



Min_DB_10yr
10-year return minimum dry-bulb temperature (°C)
Float



Max_DB_10yr
10-year return maximum dry-bulb temperature (°C)
Float



Min_DB_20yr
20-year return minimum dry-bulb temperature (°C)
Float



Max_DB_20yr
20-year return maximum dry-bulb temperature (°C)
Float



Min_DB_50yr
50-year return minimum dry-bulb temperature (°C)
Float



Max_DB_50yr
50-year return maximum dry-bulb temperature (°C)
Float



3. Typical/Extreme Periods (Line 3)
Defines typical and extreme weather periods for simulation (e.g., summer maximum, winter minimum).



Field
Description
Type
Example



Keyword
Always "TYPICAL/EXTREME PERIODS"
String



Number_of_Periods
Number of periods defined
Integer
6


Period_1_Name
Name of the first period (e.g., Summer max temp)
String
Summer - Max Temp


Period_1_Type
Type of period (Typical or Extreme)
String
Extreme


Period_1_Start_Date
Start date of the first period (M/D)
String
7/15


Period_1_End_Date
End date of the first period (M/D)
String
7/21


...
(Fields repeat for Periods 2-6)




4. Ground Temperatures (Line 4)
Provides monthly ground temperatures at different depths.



Field
Description
Type
Notes



Keyword
Always "GROUND TEMPERATURES"
String



Number_of_Depths
Number of ground temperature depths
Integer
Optional


Depth_1_Value
Depth for ground temperature 1 (m)
Float
Optional


Depth_1_Conductivity
Soil thermal conductivity (W/m·K)
Float
Optional


Depth_1_Density
Soil density (kg/m³)
Float
Optional


Depth_1_Specific_Heat
Soil specific heat (J/kg·K)
Float
Optional


Depth_1_Jan
Avg ground temp for depth 1 in January (°C)
Float
Optional


...
(Monthly temperatures for Jan-Dec for Depth 1)
Float
Optional


Depth_2_Value
Depth for ground temperature 2 (m)
Float
Optional


...
(Fields repeat for Depths 2 and 3)




5. Holidays/Daylight Saving (Line 5)
Information about holidays and daylight saving time.



Field
Description
Type
Example



Keyword
Always "HOLIDAYS/DAYLIGHT SAVINGS"
String



Leap_Year_Observed
Indicates if leap year is observed ("Yes" or "No")
String
No


Daylight_Saving_Start_Day
Daylight saving start day (date or 0 if not observed)
Integer
0


Daylight_Saving_End_Day
Daylight saving end day (date or 0 if not observed)
Integer
0


Number_of_Holidays
Number of holidays defined
Integer
0


6. Comments (Lines 6-7)
Free-text comments about the dataset.



Field
Description
Type
Example



Comments_1
First comment line
String
Source: TMY3


Comments_2
Second comment line
String
Generated by NREL


7. Data Period (Line 8)
Defines the time period covered by the weather data.



Field
Description
Type
Example



Keyword
Always "DATA PERIODS"
String



Number_of_Data_Periods
Total number of data periods
Integer
1


Data_Period_1_Start_Date
Index of the current data period
Integer
1


Data_Period_1_End_Date
Name of the data period
String
Data


Start_Day_of_Week
Day of the week the period starts
String
Sunday


Data_Period_2_Start_Date
Start date of the data period (M/D)
String
1/1


Data_Period_2_End_Date
End date of the data period (M/D)
String
12/31



Weather Data Section
Starting from line 9, each row represents an hourly weather observation with 35 fields.



Field
Description
Type
Units



Year
Year of the data
Integer
e.g., 2019


Month
Month of the data
Integer
1-12


Day
Day of the month
Integer
1-31


Hour
Hour of the day (1 = 00:00:01-01:00:00)
Integer
1-24


Minute
Minute of the hour
Integer
0 or 30


Data_Source_Uncertainty_Flags
Indicates data source and uncertainty
String
e.g., ?0?0?0


Dry_Bulb_Temperature
Dry bulb temperature
Float
°C


Dew_Point_Temperature
Dew point temperature
Float
°C


Relative_Humidity
Relative humidity
Float
0-100%


Atmospheric_Station_Pressure
Atmospheric pressure at the station
Float
Pa


Extraterrestrial_Horizontal_Radiation
Extraterrestrial horizontal radiation
Float
Wh/m²


Extraterrestrial_Direct_Normal_Radiation
Extraterrestrial direct normal radiation
Float
Wh/m²


Horizontal_Infrared_Radiation_Intensity
Horizontal infrared radiation intensity
Float
Wh/m²


Global_Horizontal_Radiation
Global horizontal radiation
Float
Wh/m²


Direct_Normal_Radiation
Direct normal radiation
Float
Wh/m²


Diffuse_Horizontal_Radiation
Diffuse horizontal radiation
Float
Wh/m²


Global_Horizontal_Illuminance
Global horizontal illuminance
Float
lux


Direct_Normal_Illuminance
Direct normal illuminance
Float
lux


Diffuse_Horizontal_Illuminance
Diffuse horizontal illuminance
Float
lux


Zenith_Luminance
Zenith luminance
Float
cd/m²


Wind_Direction
Wind direction (0-360)
Float
degrees


Wind_Speed
Wind speed
Float
m/s


Total_Sky_Cover
Total sky cover
Float
%


Opaque_Sky_Cover
Opaque sky cover
Float
%


Visibility
Visibility
Float
km


Ceiling_Height
Ceiling height
Float
m


Present_Weather_Observation
Present weather observation code
Float



Present_Weather_Codes
Additional weather codes
Float



Precipitable_Water
Precipitable water
Float
mm


Aerosol_Optical_Depth
Aerosol optical depth
Float
unitless


Snow_Depth
Snow depth
Float
cm


Days_Since_Last_Snowfall
Days since last snowfall
Float
days


Albedo
Albedo
Float
unitless


Liquid_Precipitation_Depth
Liquid precipitation depth
Float
mm


Liquid_Precipitation_Quantity
Liquid precipitation quantity
Float
mm



Notes

File Format: EPW files are comma-separated text files. Ensure proper handling of missing or empty fields, which may be represented as empty strings.
Data Source: Common sources include TMY (Typical Meteorological Year), AMY (Actual Meteorological Year), or other weather station data.
Uncertainty Flags: The Data_Source_Uncertainty_Flags field in the weather data section provides information about the reliability and source of each data point.
Usage: The parsed data is structured into a Python dictionary with a weather_data key containing a pandas DataFrame for the hourly weather data, and other keys for metadata sections.
Error Handling: The provided Python script includes checks for optional fields (e.g., empty strings for ground temperatures) and conditional subsections (e.g., heating/cooling/extremes in design conditions).

This documentation can be used as a reference for understanding the structure of the EPW dataset and how it is processed by the epw_file_preparator function.