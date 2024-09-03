import numpy as np
import matplotlib.pyplot as plt

# Sample Data Dictionary
flood_risk_data = {
    "elevation": [
        [200, 220, 250],
        [210, 230, 240],
        [220, 210, 230]
    ],
    "slope": [
        [5, 10, 15],
        [10, 20, 25],
        [15, 10, 5]
    ],
    "proximity_to_rivers": [
        [500, 300, 100],
        [400, 200, 50],
        [600, 450, 300]
    ],
    "land_cover": [
        ["forest", "urban", "agriculture"],
        ["urban", "agriculture", "forest"],
        ["agriculture", "forest", "urban"]
    ],
    "rainfall": [
        [1000, 1200, 1100],
        [900, 1300, 1000],
        [950, 1150, 1050]
    ],
    "historical_floods": [
        [1, 0, 1],
        [0, 1, 0],
        [1, 0, 0]
    ]
}

# Example Weights for AHP
criteria_weights = {
    "elevation": 0.2,
    "slope": 0.1,
    "proximity_to_rivers": 0.3,
    "land_cover": 0.15,
    "rainfall": 0.15,
    "historical_floods": 0.1
}

# Initialize an empty grid for flood risk
flood_risk = np.zeros((3, 3))

# Convert categorical data (land cover) to numerical for analysis
land_cover_mapping = {
    "forest": 1,
    "urban": 3,
    "agriculture": 2
}
numerical_land_cover = np.array([[land_cover_mapping[land] for land in row] for row in flood_risk_data["land_cover"]])

# Update the flood risk data dictionary with numerical land cover data
flood_risk_data["land_cover"] = numerical_land_cover

# Loop through each criterion and apply the weights
for criterion, weight in criteria_weights.items():
    flood_risk += np.array(flood_risk_data[criterion]) * weight

# Display the Flood Risk Assessment Map
print("Flood Risk Assessment Map:")
print(flood_risk)

# Visualize the Flood Risk Map
plt.imshow(flood_risk, cmap='Reds', interpolation='none')
plt.colorbar(label='Flood Risk Score')
plt.title('Flood Risk Assessment Map')
plt.xticks(ticks=np.arange(3), labels=['Location 1', 'Location 2', 'Location 3'])
plt.yticks(ticks=np.arange(3), labels=['Location A', 'Location B', 'Location C'])
plt.show()
