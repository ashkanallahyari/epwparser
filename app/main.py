from volansarch import *
import os

# Loading environment variables
from dotenv import load_dotenv

data_update = EPWFilePreparator()

print(data_update.raw_data_file_names)

for i, file in enumerate(data_update.list_files_needed_update()):
    data_update.parse_file(file)
    print (f"File {i + 1} - {file}")


# # Select the nearest location sample
# sample_project = EPWFileselection(lat=43.0, lon=-94.0, max_distance=None, loc_numbers=1)
# print(sample_project.file_name)
