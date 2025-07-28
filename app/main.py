from epwparser import *
import os

# Loading environment variables
from dotenv import load_dotenv

epw_files = [
    "IRN_TE_Abali.IRN105_TMYx.2009-2023.epw",
    "NLD_FL_Lelystad.AP.062690_TMYx.2009-2023.epw",
    "USA_IA_Algona.Muni.AP.725457_TMYx.2009-2023.epw",
    "ITA_LB_Bonifati.163370_TMYx.2009-2023.epw",
    "DEU_HH_Hamburg.Finkenwerder.AP.101490_TMYx.2009-2023.epw",
    "DEU_BY_Altenstadt.AP.109540_TMYx.2009-2023.epw",
    "IRN_TE_Abali.IRN105_TMYx.2009-2023.epw",
    "IRN_BK_Qasr-e.Shirin.407650_TMYx.epw",
]

data_update = EPWFilePreparator()
print(data_update.raw_data_file_names)
for i, file in enumerate(data_update.raw_data_file_names):
    data_update.parse_file(file)
    print (i)
