import geopandas as gpd
import matplotlib.pyplot as plt
import rasterio
from rasterio.plot import show

# Load the shapefile
shapefile_path = 'data/punesubdis.shp'  # Replace with your shapefile path
shapefile_data = gpd.read_file(shapefile_path)

# Plot the shapefile (commented out)
# ax = shapefile_data.plot()
# 
# # Add sub-district names
# for x, y, label in zip(shapefile_data.geometry.centroid.x, shapefile_data.geometry.centroid.y, shapefile_data['TEHSIL']):  # Replace 'TEHSIL' with the actual column name in your shapefile
#     ax.text(x, y, label, fontsize=8, ha='center', va='center')
# 
# # Set title and show plot
# plt.title("Shapefile Display with Sub-District Names")
# plt.show()

# Load and display raster image
raster_path = 'data/PuneSlope.tif'  # Replace with your raster file path
with rasterio.open(raster_path) as src:
    plt.figure(figsize=(10, 10))
    show(src, title="Raster Image Display")
    plt.show()
