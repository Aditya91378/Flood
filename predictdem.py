import numpy as np
import rasterio
import matplotlib.pyplot as plt
import time  # Importing time module for timer functionality

# Dummy data for other factors
def generate_dummy_data(shape):
    # Creating dummy data for rainfall, land cover, population
    rainfall = np.random.uniform(100, 300, size=shape)  # Random rainfall values (in mm)
    land_cover = np.random.choice([0, 1], size=shape)  # Random binary land cover (0 = bare land, 1 = vegetation)
    population = np.random.uniform(0, 1000, size=shape)  # Random population density (people per sq. km)
    return rainfall, land_cover, population

# Flood risk calculation using weighted sum
def calculate_flood_risk(dem_data, rainfall, land_cover, population):
    # AHP-derived weights (adjustable)
    dem_weight = 0.4
    rainfall_weight = 0.3
    land_cover_weight = 0.2
    population_weight = 0.1

    # Normalize the DEM data between 0 and 1
    dem_normalized = (dem_data - np.min(dem_data)) / (np.max(dem_data) - np.min(dem_data))

    # Flood risk score (weighted sum of normalized factors)
    flood_risk = (dem_normalized * dem_weight +
                  rainfall * rainfall_weight +
                  land_cover * land_cover_weight +
                  population * population_weight)
    
    return flood_risk

# Function to estimate time for prediction
def estimate_time(shape):
    # Estimation logic based on the number of pixels
    # This can be a rough estimate, here we're using size as a factor
    num_pixels = shape[0] * shape[1]
    
    # Assume processing ~0.05 seconds per 1000 pixels (example speed)
    estimated_time = (num_pixels / 1000) * 0.05  # Time in seconds
    return estimated_time

# Function to process DEM input and predict flood risk
def predict_flood(dem_file_path):
    # Start time estimation
    start_time = time.time()
    
    # Open DEM file
    with rasterio.open(dem_file_path) as dem_dataset:
        dem_data = dem_dataset.read(1)
        shape = dem_data.shape
    
    # Estimate time for the prediction based on data size
    estimated_time = estimate_time(shape)
    print(f"Estimated time to predict flood risk: {estimated_time:.2f} seconds")
    
    # Sleep for 2 seconds to simulate a delay (you can remove this line if not needed)
    time.sleep(2)
    
    # Start actual prediction
    print("Starting flood risk prediction...")
    
    # Generate dummy data
    rainfall, land_cover, population = generate_dummy_data(shape)
    
    # Calculate flood risk
    flood_risk = calculate_flood_risk(dem_data, rainfall, land_cover, population)
    
    # End time and calculate actual time taken
    end_time = time.time()
    actual_time_taken = end_time - start_time
    print(f"Flood risk prediction completed in {actual_time_taken:.2f} seconds")
    
    # Plot DEM and Flood Risk
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

    ax1.set_title('DEM Data')
    cax1 = ax1.imshow(dem_data, cmap='terrain')
    fig.colorbar(cax1, ax=ax1)

    ax2.set_title('Predicted Flood Risk')
    cax2 = ax2.imshow(flood_risk, cmap='YlOrRd')
    fig.colorbar(cax2, ax=ax2, label='Flood Risk Score')
    
    plt.show()

# Example usage:
# Provide the path to the DEM file
dem_file_path = 'data/puneDem.tif'
predict_flood(dem_file_path)
