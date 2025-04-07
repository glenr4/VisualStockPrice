import csv
from datetime import datetime
import file_handling as fh
import os

data_dir = os.path.join(os.path.dirname(__file__), 'data')
input_dir = os.path.join(data_dir, 'unformatted')

for input_file in os.listdir(input_dir):
    if not input_file.endswith('.csv'):
        continue
        
    input_path = os.path.join(input_dir, input_file)
    output_file = os.path.join(data_dir, os.path.splitext(input_file)[0] + "_formatted.csv")

    # Read all rows first
    rows = []
    with open(input_path, 'r', encoding='utf-8-sig') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            # Clean up numeric values
            row = {key: value.replace(",", "") if key in ["Price", "Open", "High", "Low"] else value for key, value in row.items()}
            
            formatted_date = datetime.strptime(row["Date"], "%m/%d/%Y").strftime("%Y-%m-%d")
            
            formatted_row = {
                "Date": formatted_date,
                "Close": row["Price"],
                "High": row["High"],
                "Low": row["Low"],
                "Open": row["Open"],
            }
            rows.append(formatted_row)

    # Sort rows by date in chronological order
    rows.sort(key=lambda x: x["Date"])

    # Write the sorted data
    with open(output_file, 'w', newline='') as outfile:
        fieldnames = ["Date", "Close", "High", "Low", "Open"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(rows)
