import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load the shapefile
shapefile_path = 'data/punesubdis.shp'  # Replace with your shapefile path
shapefile_data = gpd.read_file(shapefile_path)

# Step 2: Create the sample rainfall data
data = {
    'TEHSIL': ['Ambegaon', 'Baramati', 'Bhor', 'Daund', 'Haveli', 'Indapur', 'Junnar', 
               'Khed', 'Mawal', 'Mulshi-Paud', 'Saswad-Purandhar', 'Shirur', 'Velhe'],
    'Rainfall_mm': [800, 700, 850, 600, 750, 550, 900, 950, 1100, 1200, 650, 600, 1000]
}
rainfall_data = pd.DataFrame(data)

# Step 3: Merge the shapefile GeoDataFrame with the rainfall data
# Assume the column 'TEHSIL' in the shapefile corresponds to 'TEHSIL' in the rainfall data
merged_data = shapefile_data.merge(rainfall_data, on='TEHSIL')

# Step 4: Plot the map with rainfall data
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
merged_data.plot(column='Rainfall_mm', cmap='Blues', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)

# Add labels for the tehsils
for x, y, label in zip(merged_data.geometry.centroid.x, merged_data.geometry.centroid.y, merged_data['TEHSIL']):
    ax.text(x, y, label, fontsize=8, ha='center', va='center')

# Set plot title and display
plt.title("Rainfall Distribution by Tehsil in Pune District")
plt.show()
