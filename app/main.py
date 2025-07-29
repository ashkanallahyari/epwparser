from volansarch import *
import os

# Loading environment variables
from dotenv import load_dotenv

data_update = EPWFilePreparator()

print(data_update.raw_data_file_names)

for i, file in enumerate(data_update.list_files_needed_update()):
    data_update.parse_file(file)
    print (f"File {i} - {file}")
