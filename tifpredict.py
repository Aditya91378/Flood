import tifffile as tiff
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

# Load the DEM image
image_path = 'data/puneDem.tif'
dem_data = tiff.imread(image_path).astype(float)  # Convert to float for NaN handling

# Create a mask for negative values
negative_mask = dem_data < 0

# Replace negative values with NaN
dem_data[negative_mask] = np.nan

# Apply Gaussian filter for smoothing (adjust sigma for more or less smoothing)
smoothed_data = gaussian_filter(dem_data, sigma=1)

# Define flood risk zones based on smoothed data directly
flood_risk_zones = np.zeros_like(smoothed_data)

# Set flood risk zones based on elevation thresholds (modified logic)
flood_risk_zones[(smoothed_data < 570) & (smoothed_data > 0)] = 3  # Low elevation, High flood risk
flood_risk_zones[(smoothed_data >= 570) & (smoothed_data < 700)] = 2  # Mid elevation, Moderate risk
flood_risk_zones[smoothed_data >= 700] = 1  # High elevation, Low flood risk

# Set areas where the original DEM was negative to NaN in flood risk zones
flood_risk_zones[negative_mask] = np.nan  # Set flood risk zones to NaN where DEM was negative

# Set up the plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Plot the elevation map on the left
cmap = plt.get_cmap('terrain')
img1 = ax1.imshow(smoothed_data, cmap=cmap, interpolation='bilinear', vmin=np.nanmin(smoothed_data), vmax=np.nanmax(smoothed_data))
ax1.set_title('Smoothed Elevation Visualization')
ax1.axis('off')
cbar1 = fig.colorbar(img1, ax=ax1, label='Elevation (m)', shrink=0.8)

# Plot the flood risk zones map on the right
# Define a colormap for flood risk zones (e.g., green=low, yellow=moderate, red=high)
risk_cmap = plt.get_cmap('RdYlGn_r')

# Display flood risk zones while handling NaNs
img2 = ax2.imshow(flood_risk_zones, cmap=risk_cmap, interpolation='nearest', vmin=1, vmax=3)
ax2.set_title('Flood Risk Zones')
ax2.axis('off')

# Create colorbar for flood risk zones and set labels
cbar2 = fig.colorbar(img2, ax=ax2, ticks=[1, 2, 3], label='Flood Risk', shrink=0.8)
cbar2.ax.set_yticklabels(['Low Risk', 'Moderate Risk', 'High Risk'])

plt.show()