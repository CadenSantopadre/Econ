import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSlider, QGroupBox, QLabel
from PyQt6.QtCore import Qt

from mpl import EconCanvas
from presenter import GraphPresenter
from markets import SupplyDemandModel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Economics Graphing Engine")
        self.setGeometry(100,100,950,650)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        control_panel = QGroupBox("Market Curve Shifts")
        control_layout = QVBoxLayout(control_panel)
        control_panel.setFixedWidth(200)

        control_layout.addWidget(QLabel("Supply Base Intercept"))
        self.supply_slider = QSlider(Qt.Orientation.Horizontal) #Qt.Orientation.Horizontal makes it horizontal
        self.supply_slider.setRange(0, 80)
        self.supply_slider.setValue(10)
        control_layout.addWidget(self.supply_slider)

        control_layout.addWidget(QLabel("Demand Base Intercept"))
        self.demand_slider = QSlider(Qt.Orientation.Horizontal)
        self.demand_slider.setRange(40, 120)
        self.demand_slider.setValue(100)
        control_layout.addWidget(self.demand_slider)

        control_layout.addStretch() #Doesn't stretch them accross
        main_layout.addWidget(control_panel)

        self.canvas = EconCanvas(self)
        main_layout.addWidget(self.canvas, stretch=1)



if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create the model.
    market_model = SupplyDemandModel()

    # Create the view.
    ui_window = MainWindow()

    # Connect the model and view through the presenter.
    presenter = GraphPresenter(ui_window, market_model)

    # Display the application.
    ui_window.show()

    sys.exit(app.exec())