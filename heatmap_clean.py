import pandas as pd

# Re-read file with correct header row
df = pd.read_csv('./data/crop_site_data.csv')

# List mandatory columns
mandatory_cols = ["latitude_north", "longitude_east", "crop", "Sample.ID"]

# Keep only relevant columns and drop any rows that have missing data from columns
df = df.dropna(subset=mandatory_cols)

# Drop any row with NA crop value
df = df[df['crop'] != 'NA']


# Convert coordinates from "degrees.minutes.seconds" to decimal degrees
def dms_to_dd(dms_str):
    if isinstance(dms_str, str) and dms_str[0] == "'":
        dms_str = dms_str[1:]
    try:
        parts = [float(p) for p in dms_str.split('.')]
        if len(parts) == 3:
            degrees, minutes, seconds = parts
            return degrees + minutes/60 + seconds/3600
        return float(dms_str)
    except:
        return None

df['latitude_north'] = df['latitude_north'].apply(dms_to_dd).round(4)
df['longitude_east'] = df['longitude_east'].apply(dms_to_dd).round(4)

# Crop grouping
vegetables = ['cabbage', 'carrot', 'potato', 'tomato', 'onion', 'spinach', 'komatsuna', 'celery', 'radish', 'eggplant', 'lettuce', 'broccoli']

def group_crop(crop):
    crop_clean = str(crop).strip().lower()  # remove spaces and lowercase

    crop = str(crop).lower()
    if any(x in crop_clean for x in ['rice', 'wheat', 'barley', 'corn']):
        return 'Grains'
    elif any(x in crop_clean for x in ['soybean', 'pea', 'lentil']):
        return 'Legumes'
    elif any(x in crop_clean for x in vegetables):
        return 'Vegetables'
    elif any(x in crop_clean for x in ['apple', 'citrus', 'nut', 'mandarin', 'strawberry']):
        return 'Fruits or Nuts'
    elif any(x in crop_clean for x in ['ginger']):
        return 'Spices'
    else:
        return 'Other'

df['crop_group'] = df['crop'].apply(group_crop)

df_veg = df[df['crop_group'] == 'Vegetables']
df_veg.to_csv("./data/veg_crops.csv", index=False)

# Save to CSV
output_path = "./data/crop_grouped_coordinates.csv"
df.to_csv(output_path, index=False)

output_path
