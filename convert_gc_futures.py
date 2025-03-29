import csv
from datetime import datetime
import file_handling as fh
import os

# Converts from: "Date","Price","Open","High","Low","Vol.","Change %"
# "12/30/1999","289.60","292.70","292.90","289.30","30.70K","-0.96%"
# To: "Date","Close","High","Low","Open","Volume"
# "1999-12-30","289.60","292.90","289.30","292.70","30700"

# Select the input file dynamically
input_file = fh.browse_file('data')
output_file = os.path.splitext(input_file)[0] + "_formatted.csv"

# Open the input file and process the data
with open(input_file, 'r', encoding='utf-8-sig') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = ["Date", "Close", "High", "Low", "Open", "Volume"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()

    for row in reader:
        # Remove commas from numeric values and ensure they are not enclosed in quotes
        row = {key: value.replace(",", "") if key in ["Price", "Open", "High", "Low", "Vol."] else value for key, value in row.items()}
        
        formatted_date = datetime.strptime(row["Date"], "%m/%d/%Y").strftime("%Y-%m-%d")
        volume = row["Vol."]
        if "K" in volume:
            volume = str(int(float(volume.replace("K", "")) * 1000))
        writer.writerow({
            "Date": formatted_date,
            "Close": row["Price"],
            "High": row["High"],
            "Low": row["Low"],
            "Open": row["Open"],
            "Volume": volume if volume else ""
        })
