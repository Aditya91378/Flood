import numpy as np
import rasterio
import matplotlib.pyplot as plt

# 1. Load the DEM
dem_file_path = 'data/puneDem.tif'
with rasterio.open(dem_file_path) as dem:
    # Read the elevation data
    dem_data = dem.read(1, resampling=rasterio.enums.Resampling.bilinear)  # Read the first band

# 2. Handle Negative Values
dem_data[dem_data < 0] = 0  # Set negative values to 0 or a small positive value

# 3. Calculate the Slope
x_gradient, y_gradient = np.gradient(dem_data)
slope = np.arctan(np.sqrt(x_gradient**2 + y_gradient**2)) * (180 / np.pi)  # Convert to degrees

# Set negative slopes to NaN for masking in visualization
slope[slope < 0] = np.nan

# 4. Visualize the Slope with Negative Values as White
plt.figure(figsize=(10, 10))

# Create a masked array to display NaN values as white
masked_slope = np.ma.masked_invalid(slope)

# Use a colormap where white represents NaN values
plt.imshow(masked_slope, cmap='terrain', origin='upper', interpolation='nearest')
plt.colorbar(label='Slope (degrees)')
plt.title('Slope Analysis from DEM (Negative Values in White)')
plt.show()
