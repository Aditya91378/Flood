import geopandas as gpd
import numpy as np
import rasterio
from rasterio.mask import mask
from sklearn.preprocessing import MinMaxScaler

# Load Shapefiles
def load_shapefile(filepath):
    return gpd.read_file(filepath)

# Clip Raster with Shapefile
def clip_raster_with_shape(raster_path, shape):
    with rasterio.open(raster_path) as src:
        out_image, out_transform = mask(src, [shape.geometry.unary_union], crop=True)
        out_meta = src.meta
    return out_image, out_transform, out_meta

# Calculate Flood Risk Score
def calculate_risk_score(elevation, slope, proximity, rainfall):
    scaler = MinMaxScaler()
    normalized_elevation = scaler.fit_transform(elevation.reshape(-1, 1)).reshape(elevation.shape)
    normalized_slope = scaler.fit_transform(slope.reshape(-1, 1)).reshape(slope.shape)
    normalized_proximity = scaler.fit_transform(proximity.reshape(-1, 1)).reshape(proximity.shape)
    normalized_rainfall = scaler.fit_transform(rainfall.reshape(-1, 1)).reshape(rainfall.shape)
    
    # Custom formula to calculate risk
    flood_risk = (normalized_elevation * 0.3) + (normalized_slope * 0.2) + \
                 (normalized_proximity * 0.3) + (normalized_rainfall * 0.2)
    return flood_risk

# Load and Process GIS Data
def process_gis_data(elevation_tif, slope_tif, proximity_tif, rainfall_tif, boundary_shape):
    boundary = load_shapefile(boundary_shape)
    elevation, _, _ = clip_raster_with_shape(elevation_tif, boundary)
    slope, _, _ = clip_raster_with_shape(slope_tif, boundary)
    proximity, _, _ = clip_raster_with_shape(proximity_tif, boundary)
    rainfall, _, _ = clip_raster_with_shape(rainfall_tif, boundary)
    return elevation[0], slope[0], proximity[0], rainfall[0]

# Predict Flood Risk
def predict_flood_risk(elevation_tif, slope_tif, proximity_tif, rainfall_tif, boundary_shape):
    elevation, slope, proximity, rainfall = process_gis_data(elevation_tif, slope_tif, proximity_tif, rainfall_tif, boundary_shape)
    flood_risk = calculate_risk_score(elevation, slope, proximity, rainfall)
    return flood_risk

# Example Usage
elevation_tif = 'data/elevation.tif'
slope_tif = 'data/slope.tif'
proximity_tif = 'data/proximity_to_rivers.tif'
rainfall_tif = 'data/rainfall.tif'
boundary_shape = 'data/region_boundary.shp'

flood_risk = predict_flood_risk(elevation_tif, slope_tif, proximity_tif, rainfall_tif, boundary_shape)

# Output flood risk as an array
print(flood_risk)

# Save the flood risk as a new raster (optional)
def save_flood_risk_as_raster(flood_risk, reference_tif, output_tif):
    with rasterio.open(reference_tif) as src:
        out_meta = src.meta
        out_meta.update({"driver": "GTiff", "height": flood_risk.shape[0], "width": flood_risk.shape[1], "transform": src.transform})
        with rasterio.open(output_tif, "w", **out_meta) as dest:
            dest.write(flood_risk, 1)

output_tif = 'data/flood_risk.tif'
save_flood_risk_as_raster(flood_risk, elevation_tif, output_tif)
