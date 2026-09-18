import requests
import pandas as pd
from io import StringIO
from pathlib import Path

# Bengaluru coordinates
latitude = 12.9716
longitude = 77.5946

# Date range
start_date = "20200101"
end_date = "20241231"

# NASA POWER parameters
parameters = [
    "PRECTOTCORR",
    "T2M",
    "ALLSKY_SFC_SW_DWN",
    "RH2M",
    "WS10M"
]

url = (
    "https://power.larc.nasa.gov/api/temporal/daily/point"
    f"?parameters={','.join(parameters)}"
    f"&community=AG"
    f"&longitude={longitude}"
    f"&latitude={latitude}"
    f"&start={start_date}"
    f"&end={end_date}"
    f"&format=CSV"
)

print("Downloading NASA POWER data...")

response = requests.get(url, timeout=60)
response.raise_for_status()

# Split response into lines
lines = response.text.splitlines()

# Find the actual CSV header
header_index = None

for index, line in enumerate(lines):
    if line.strip().startswith("YEAR,DOY"):
        header_index = index
        break

if header_index is None:
    print("CSV header was not found.")
    print(response.text[:1500])
    raise ValueError("Invalid NASA POWER CSV response.")

# Keep only the actual CSV table
csv_text = "\n".join(lines[header_index:])

# Read CSV
df = pd.read_csv(StringIO(csv_text))

print("Original columns:")
print(df.columns.tolist())

# Rename columns
df = df.rename(columns={
    "YEAR": "year",
    "DOY": "day_of_year",
    "PRECTOTCORR": "rainfall",
    "T2M": "temperature",
    "ALLSKY_SFC_SW_DWN": "solar_radiation",
    "RH2M": "relative_humidity",
    "WS10M": "wind_speed"
})

# Convert year and day-of-year into a date
df["date"] = (
    pd.to_datetime(
        df["year"].astype(str),
        format="%Y"
    )
    + pd.to_timedelta(
        df["day_of_year"] - 1,
        unit="D"
    )
)

# Add location information
df["latitude"] = latitude
df["longitude"] = longitude

# Select useful columns
final_columns = [
    "date",
    "latitude",
    "longitude",
    "rainfall",
    "temperature",
    "solar_radiation",
    "relative_humidity",
    "wind_speed"
]

df = df[final_columns]

# Create output folder
output_folder = Path("data/raw")
output_folder.mkdir(parents=True, exist_ok=True)

# Save data
output_path = output_folder / "weather_bengaluru_2020_2024.csv"

df.to_csv(output_path, index=False)

print("Data downloaded successfully!")
print("Saved to:", output_path)
print("Dataset shape:", df.shape)
print(df.head())
print(df.tail())