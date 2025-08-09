import pandas as pd

# Re-read file with correct header row
df = pd.read_csv('./data/crop_site_data.csv')

# Keep only relevant columns
df = df[['Sample.ID', 'latitude_north', 'longitude_east', 'crop']]

# Convert coordinates from "degrees.minutes.seconds" to decimal degrees
def dms_to_dd(dms_str):
    try:
        parts = [float(p) for p in dms_str.split('.')]
        if len(parts) == 3:
            degrees, minutes, seconds = parts
            return degrees + minutes/60 + seconds/3600
        return float(dms_str)
    except:
        return None

df['latitude_north'] = df['latitude_north'].apply(dms_to_dd)
df['longitude_east'] = df['longitude_east'].apply(dms_to_dd)

# Crop grouping
def group_crop(crop):
    crop = str(crop).lower()
    if any(x in crop for x in ['rice', 'wheat', 'barley', 'corn']):
        return 'Grains'
    elif any(x in crop for x in ['soybean', 'pea', 'lentil']):
        return 'Legumes'
    elif any(x in crop for x in ['cabbage', 'carrot', 'potato']):
        return 'Vegetables'
    elif any(x in crop for x in ['apple', 'citrus', 'nut']):
        return 'Fruit/Nuts'
    else:
        return 'Other'

df['crop_group'] = df['crop'].apply(group_crop)

# Save to CSV
output_path = "./data/crop_grouped_coordinates.csv"
df.to_csv(output_path, index=False)

output_path
