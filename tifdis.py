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

# Create a colormap for visualization (e.g., 'viridis', 'plasma', or 'terrain')
cmap = plt.get_cmap('terrain')

# Plotting the smoothed elevation data with continuous colors
plt.figure(figsize=(8, 6))
plt.gcf().patch.set_facecolor('white')

# Display the smoothed image, setting NaNs to be transparent and setting clim directly
img = plt.imshow(smoothed_data, cmap=cmap, interpolation='bilinear', vmin=np.nanmin(smoothed_data), vmax=np.nanmax(smoothed_data))

# Overlay negative values with white color (set alpha=0 to ignore negatives)
plt.imshow(np.where(negative_mask, 1, smoothed_data), cmap='gray', alpha=0)  # White for NaNs

# Add a color bar that reflects the correct range of values
cbar = plt.colorbar(img, label='Elevation (m)', shrink=0.8)

plt.title('Smoothed Elevation Visualization')
plt.axis('off')

plt.show()
