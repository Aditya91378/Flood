import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load the Pune Tehsil Shapefile
shapefile_path = 'data/punesubdis.shp'  # Replace with your shapefile path
shapefile_data = gpd.read_file(shapefile_path)

# Step 2: Create Sample Flood Risk Data
# Assigning arbitrary flood risk levels to each tehsil
data = {
   'TEHSIL': ['Ambegaon', 'Baramati', 'Bhor', 'Daund', 'Haveli', 'Indapur', 'Junnar', 
               'Khed', 'Mawal', 'Mulshi-Paud', 'Saswad-Purandhar', 'Shirur', 'Velhe'],
   'Flood_Risk': ['Medium', 'Low', 'High', 'Low', 'Medium', 'Low', 'High', 
                   'High', 'High', 'High', 'Medium', 'Low', 'High']
}
flood_risk_data = pd.DataFrame(data)

# Step 3: Merge the Shapefile GeoDataFrame with the Flood Risk Data
merged_data = shapefile_data.merge(flood_risk_data, on='TEHSIL')

# Step 4: Define a Color Map for Flood Risk Levels
risk_colors = {
    'Low': '#56B4E9',    # Light Blue
    'Medium': '#F0E442', # Yellow
    'High': '#D55E00'    # Red
}

# Apply the color map to the merged data
merged_data['color'] = merged_data['Flood_Risk'].map(risk_colors)

# Step 5: Plot the Map with Flood Risk Levels
fig, ax = plt.subplots(1, 1, figsize=(12, 12))
merged_data.plot(color=merged_data['color'], linewidth=0.8, ax=ax, edgecolor='0.8')

# Add labels for the tehsils
for x, y, label in zip(merged_data.geometry.centroid.x, merged_data.geometry.centroid.y, merged_data['TEHSIL']):
    ax.text(x, y, label, fontsize=8, ha='center', va='center')

# Add a custom legend
import matplotlib.patches as mpatches
legend_patches = [mpatches.Patch(color=risk_colors[risk], label=risk) for risk in risk_colors]
ax.legend(handles=legend_patches, loc='upper left', title="Flood Risk Levels")

# Set plot title and display
plt.title("Flood Risk Map of Pune Tehsils")
plt.show()
