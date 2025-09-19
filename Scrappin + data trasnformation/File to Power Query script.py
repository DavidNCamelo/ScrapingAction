# Sometimes, including new tables in Power BI isn’t possible due to restrictions on connecting directly to the data source on your device or professional cloud.
# Client environments may not always permit this type of connection. Additionally, implementing Python scripts might be impractical because Power BI service
# doesn’t allow scheduled refresh actions via this method on this kind of sources. To address this, the following script demonstrates a technique to read a
# local file and convert it into a Power Query source script. This script can then be saved as a .txt file, which you can copy and paste into your Power BI model.

# Generate power Query Script to create taxes sales table
import pandas as pd

# Read the original document
data = pd.read_excel("file.xlsx")

# clean last column
data = data.fillna(0)

# Create a list with retrieve data
registers = []

for index, row in data.iterrows():
    register = [
        (
            f'"{row[col]}"'
            if not pd.api.types.is_numeric_dtype(data[col])
            else str(row[col])
        )
        for col in data.columns
    ]
    registers.append("{" + ", ".join(register) + "}")

# Generate the Power Query format script
column_names = ", ".join([f'"{col}"' for col in data.columns])
script = f"let\n    Source = #table({{{column_names}}}, {{\n"
script += ",\n".join(registers)
script += "\n    })\nin\n    Source"

# Save document in .txt file
with open("file_script.txt", "w") as file:
    file.write(script)

print("Script generated and saved to file_script.txt")
