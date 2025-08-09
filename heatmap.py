import pandas as pd
import folium
from folium.plugins import HeatMap

# Load cleaned dataset
df = pd.read_csv("./data/crop_grouped_coordinates.csv")

# Center the map roughly on Japan
m = folium.Map(location=[36.2048, 138.2529], zoom_start=5, tiles='CartoDB positron')

# Choose which crop group to map
crop_groups = ['Grains', 'Legumes', 'Vegetables', 'Fruit or Nuts', 'Spices']  # change to "Grains", "Legumes", etc.

for group in crop_groups:
    # Filter only that crop group
    df_group = df[df['crop_group'] == group]

    # Prepare heatmap data (lat, lon)
    heat_data = df_group[['latitude_north', 'longitude_east']].values.tolist()

    # Add heatmap layer
    HeatMap(heat_data, radius=10, blur=15, max_zoom=8).add_to(m)

    # Save map to HTML file

    m.save(f"./created_content/{group.lower()}_heatmap.html")
    print(f"Heatmap saved as {group.lower()}_heatmap.html")
