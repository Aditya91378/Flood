import sys
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from io import BytesIO
from PIL import Image

class FloodPredictionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Flood Risk Prediction')
        self.setGeometry(100, 100, 600, 500)  # Adjusted size for better view of the image

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

        # Image Display
        self.image_label = QLabel(self)
        layout.addWidget(self.image_label)

        self.setLayout(layout)

    def browse_shapefile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        shapefile, _ = QFileDialog.getOpenFileName(self, "Select Shapefile", "", "Shapefiles (*.shp);;All Files (*)", options=options)
        if shapefile:
            self.file_input.setText(shapefile)

    def calculate_ahp_weights(self, matrix):
        """Calculate AHP weights and Consistency Ratio (CR)."""
        # Normalize the matrix
        norm_matrix = matrix / matrix.sum(axis=0)
        # Calculate the priority vector
        weights = norm_matrix.mean(axis=1)
        # Calculate the weighted sum vector
        weighted_sum = np.dot(matrix, weights)
        # Calculate lambda_max
        lambda_max = weighted_sum.mean() / weights.mean()
        # Calculate CI
        n = matrix.shape[0]
        CI = (lambda_max - n) / (n - 1)
        # Random Index (RI) values for matrix sizes
        RI = {1: 0.0, 2: 0.0, 3: 0.58, 4: 0.9, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
        RI_value = RI.get(n, 1.49)  # Default to 1.49 if matrix size not in RI table
        # Calculate CR
        CR = CI / RI_value
        return weights, CR

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

            # Example pairwise comparison matrix
            pairwise_matrix = np.array([
                [1, 3, 0.5, 2],
                [1/3, 1, 1/7, 1/3],
                [2, 7, 1, 5],
                [0.5, 3, 1/5, 1]
            ])

            # Calculate AHP weights and CR
            weights, cr = self.calculate_ahp_weights(pairwise_matrix)
            print("AHP Weights:", weights)
            print("Consistency Ratio (CR):", cr)

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

            # Convert plot to a QPixmap to display in PyQt5 GUI
            buf = BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            img = Image.open(buf)
            img = img.convert("RGB")

            # Convert to QImage for QPixmap
            data = img.tobytes("raw", "RGB")
            qimg = QImage(data, img.size[0], img.size[1], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimg)

            # Display the image in the QLabel
            self.image_label.setPixmap(pixmap)
            self.image_label.setScaledContents(True)  # Ensure the image fits the label
            self.result_label.setText("Flood risk prediction completed!")

        except Exception as e:
            self.result_label.setText(f"Error: {str(e)}")

# Run the Application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FloodPredictionApp()
    ex.show()
    sys.exit(app.exec_())
