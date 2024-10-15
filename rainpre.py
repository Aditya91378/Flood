import geopandas as gpd
import numpy as np
from scipy.spatial import cKDTree
import matplotlib.pyplot as plt

# 1. Load the Taluka Boundaries Shapefile (which already has the rainfall column)
taluka_gdf = gpd.read_file('data/punesubdis.shp')

# 2. Check if the rainfall column exists and inspect the data
print(taluka_gdf.head())

# 3. Identify talukas with non-null rainfall data
centroids_with_rainfall = taluka_gdf[~taluka_gdf['Rainfall'].isna()].centroid
rainfall_values = taluka_gdf[~taluka_gdf['Rainfall'].isna()]['Rainfall'].values

# 4. Identify talukas with missing (NaN) rainfall data
centroids_without_rainfall = taluka_gdf[taluka_gdf['Rainfall'].isna()].centroid

# Convert centroids to numpy arrays for interpolation
coords_with = np.array([(geom.x, geom.y) for geom in centroids_with_rainfall])
coords_without = np.array([(geom.x, geom.y) for geom in centroids_without_rainfall])

# 5. Use cKDTree for inverse distance weighting (IDW) interpolation
tree = cKDTree(coords_with)
distances, idx = tree.query(coords_without, k=3)  # Using 3 nearest neighbors

# Compute inverse distance weights
weights = 1 / distances
weights_sum = np.sum(weights, axis=1)
interpolated_values = np.sum(rainfall_values[idx] * weights, axis=1) / weights_sum

# 6. Assign interpolated values to the talukas with missing rainfall data
taluka_gdf.loc[taluka_gdf['Rainfall'].isna(), 'Rainfall'] = interpolated_values

# 8. Visualize the rainfall distribution (optional)
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
taluka_gdf.plot(column='Rainfall', cmap='Blues', legend=True, ax=ax)
plt.title('Rainfall Distribution in Pune District (With Interpolation)')
plt.show()
