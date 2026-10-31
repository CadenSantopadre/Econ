import sys
import numpy as np
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, 
                             QVBoxLayout, QSlider, QLabel, QGroupBox)
from PyQt6.QtCore import Qt

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class SupplyDemandModel:
    def __init__(self, demand_intercept=100, demand_slope=-1, supply_intercept=10, supply_slope=1):
        self.d_int = demand_intercept
        self.d_slope = demand_slope  #Must be negative
        self.s_int = supply_intercept
        self.s_slope = supply_slope  #Must be positive

    def get_equilibrium(self):
        """Calculates exact equilibrium crossing: Qd = Qs"""
        q_eq = (self.d_int - self.s_int) / (self.s_slope - self.d_slope)
        p_eq = self.d_int + self.d_slope * q_eq
        return q_eq, p_eq

    def get_curves(self, max_q=100):
        """Generates continuous geometric paths for the curves."""
        q = np.linspace(0, max_q, 200)
        price_demand = self.d_int + self.d_slope * q
        price_supply = self.s_int + self.s_slope * q
        
        return q, np.clip(price_demand, 0, None), np.clip(price_supply, 0, None) #clip at 0 so they don't go below axis


class EconCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=5, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setup_econ_axes()

    def setup_econ_axes(self):
        """Formats the axes to match structural textbook representations."""
        self.axes.spines['top'].set_visible(False)
        self.axes.spines['right'].set_visible(False)
        self.axes.spines['left'].set_position('zero')
        self.axes.spines['bottom'].set_position('zero')
        self.axes.set_xlabel("Quantity (Q)", loc="right")
        self.axes.set_ylabel("Price (P)", loc="top", rotation=0)
        self.axes.set_xlim(0, 100)
        self.axes.set_ylim(0, 120)

    def draw_market(self, q, p_demand, p_supply, q_eq=None, p_eq=None):
        """Clears canvas bounds and draws fresh economics arrays."""
        self.axes.clear()
        self.setup_econ_axes()
        
        # Core Curves
        self.axes.plot(q, p_demand, label="Demand (D)", color="#1f77b4", linewidth=2.5)
        self.axes.plot(q, p_supply, label="Supply (S)", color="#d62728", linewidth=2.5)
        
        # Equilibrium Reference Guidelines (Dotted projection tracking to axes)
        if q_eq is not None and p_eq is not None and 0 <= q_eq <= 100:
            self.axes.axvline(x=q_eq, ymin=0, ymax=p_eq/120, color='gray', linestyle='--', linewidth=1.2)
            self.axes.axhline(y=p_eq, xmin=0, xmax=q_eq/100, color='gray', linestyle='--', linewidth=1.2)
            self.axes.plot(q_eq, p_eq, 'ko', markersize=6) # Focal crossing marker
            self.axes.text(q_eq + 2, p_eq + 2, f"E\n(Q={q_eq:.1f}\nP={p_eq:.1f})", weight='bold', fontsize=9)

        self.axes.legend(loc="upper right", frameon=False)
        self.draw()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interactive Economics Grapher Engine")
        self.setGeometry(100, 100, 950, 650)

        # Container Structure Splitter
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # Left Column Panel: Structural Control Sliders
        control_panel = QGroupBox("Market Curve Shifts")
        control_layout = QVBoxLayout(control_panel)
        control_panel.setFixedWidth(280)
        
        # Supply Intercept Configuration Slider
        control_layout.addWidget(QLabel("Supply Base Intercept (Shift S):"))
        self.supply_slider = QSlider(Qt.Orientation.Horizontal)
        self.supply_slider.setRange(0, 80)
        self.supply_slider.setValue(10) # Matches default model config
        control_layout.addWidget(self.supply_slider)

        # Demand Intercept Configuration Slider
        control_layout.addWidget(QLabel("Demand Base Intercept (Shift D):"))
        self.demand_slider = QSlider(Qt.Orientation.Horizontal)
        self.demand_slider.setRange(40, 120)
        self.demand_slider.setValue(100) # Matches default model config
        control_layout.addWidget(self.demand_slider)
        
        control_layout.addStretch() # Pushes layout content to top bounds
        main_layout.addWidget(control_panel)

        # Right Column Panel: Live Data Visualization View
        self.canvas = EconCanvas(self)
        main_layout.addWidget(self.canvas, stretch=1)


# =====================================================================
# 3. THE PRESENTER LAYER (Glues Math Inputs to Visual Re-rendering)
# =====================================================================
class GraphPresenter:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        
        # Connect front-end signal events directly to state mutation methods
        self.view.supply_slider.valueChanged.connect(self.handle_supply_shift)
        self.view.demand_slider.valueChanged.connect(self.handle_demand_shift)
        
        # Trigger explicit paint call on initial launch loop
        self.update_display()

    def handle_supply_shift(self, value):
        self.model.s_int = value 
        self.update_display()

    def handle_demand_shift(self, value):
        self.model.d_int = value
        self.update_display()

    def update_display(self):
        """Fetches calculated array values from data models and triggers canvas draws."""
        q, p_d, p_s = self.model.get_curves()
        q_eq, p_eq = self.model.get_equilibrium()
        
        # Pass the derived math vectors to the visual UI layer
        self.view.canvas.draw_market(q, p_d, p_s, q_eq, p_eq)


# =====================================================================
# 4. APPLICATION EXECUTION PROCESS ENTRY POINT
# =====================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Instantiate standalone operational contexts
    market_model = SupplyDemandModel()
    ui_window = MainWindow()
    
    # Presenter takes control management authority over model and view elements
    presenter = GraphPresenter(ui_window, market_model)
    
    ui_window.show()
    sys.exit(app.exec())
