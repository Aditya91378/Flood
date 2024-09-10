import sys
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QLineEdit
from PyQt5.QtCore import Qt

class FloodPredictionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Flood Risk Prediction')
        self.setGeometry(100, 100, 400, 300)

        # Layout
        layout = QVBoxLayout()

        # Shapefile Input
        self.label_shapefile = QLabel("Select Shapefile for Study Area:")
        layout.addWidget(self.label_shapefile)
        
        self.file_input = QLineEdit(self)
        layout.addWidget(self.file_input)

        self.browse_button = QPushButton('Browse', self)
        self.browse_button.clicked.connect(self.browse_shapefile)
        layout.addWidget(self.browse_button)

        # Predict Button
        self.predict_button = QPushButton('Predict Flood Risk', self)
        self.predict_button.clicked.connect(self.predict_flood_risk)
        layout.addWidget(self.predict_button)

        # Result Label
        self.result_label = QLabel("", self)
        self.result_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def browse_shapefile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        shapefile, _ = QFileDialog.getOpenFileName(self, "Select Shapefile", "", "Shapefiles (*.shp);;All Files (*)", options=options)
        if shapefile:
            self.file_input.setText(shapefile)

    import sys
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QLineEdit
from PyQt5.QtCore import Qt

class FloodPredictionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Flood Risk Prediction')
        self.setGeometry(100, 100, 400, 300)

        # Layout
        layout = QVBoxLayout()

        # Shapefile Input
        self.label_shapefile = QLabel("Select Shapefile for Study Area:")
        layout.addWidget(self.label_shapefile)
        
        self.file_input = QLineEdit(self)
        layout.addWidget(self.file_input)

        self.browse_button = QPushButton('Browse', self)
        self.browse_button.clicked.connect(self.browse_shapefile)
        layout.addWidget(self.browse_button)

        # Predict Button
        self.predict_button = QPushButton('Predict Flood Risk', self)
        self.predict_button.clicked.connect(self.predict_flood_risk)
        layout.addWidget(self.predict_button)

        # Result Label
        self.result_label = QLabel("", self)
        self.result_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def browse_shapefile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        shapefile, _ = QFileDialog.getOpenFileName(self, "Select Shapefile", "", "Shapefiles (*.shp);;All Files (*)", options=options)
        if shapefile:
            self.file_input.setText(shapefile)

    def predict_flood_risk(self):
        shapefile_path = self.file_input.text()
        if not shapefile_path:
            self.result_label.setText("Please select a shapefile!")
            return

        try:
            # Load the shapefile
            gdf = gpd.read_file(shapefile_path)

            # Sample Data for each sub-district (replace with actual data or add more fields for user input)
            flood_risk_data = {
                "elevation": np.random.randint(500, 650, len(gdf)),  # Example random data
                "slope": np.random.randint(1, 20, len(gdf)),
                "proximity_to_rivers": np.random.randint(50, 500, len(gdf)),
                "land_cover": np.random.randint(1, 3, len(gdf)),
                "rainfall": np.random.randint(900, 1300, len(gdf)),
                "historical_floods": np.random.randint(0, 2, len(gdf))
            }

            # AHP Weights
            criteria_weights = {
                "elevation": 0.2,
                "slope": 0.15,
                "proximity_to_rivers": 0.3,
                "land_cover": 0.1,
                "rainfall": 0.2,
                "historical_floods": 0.05
            }

            # Calculate flood risk
            flood_risk_scores = np.zeros(len(gdf))
            for criterion, weight in criteria_weights.items():
                flood_risk_scores += np.array(flood_risk_data[criterion]) * weight

            gdf['flood_risk'] = flood_risk_scores

            # Plot the results
            fig, ax = plt.subplots(1, 1, figsize=(10, 8))
            gdf.plot(column='flood_risk', ax=ax, legend=True, cmap='Reds')
            plt.title('Flood Risk Prediction Map')
            plt.xlabel('Longitude')
            plt.ylabel('Latitude')
            plt.show()

            self.result_label.setText("Flood risk prediction completed!")

        except Exception as e:
            self.result_label.setText(f"Error: {str(e)}")

# Run the Application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FloodPredictionApp()
    ex.show()
    sys.exit(app.exec_())
