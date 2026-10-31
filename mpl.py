from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class EconCanvas(FigureCanvas):
    def __init__(self, parent=None, width=6, height=6, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi) #instance variable
        self.axes = self.fig.add_subplot(111) #We need a 1 subplot to be declared
        super().__init__(self.fig)
        self.setup_econ_axes()

    def setup_econ_axes(self):
        self.axes.spines['top'].set_visible(False) #Set spines to be invisible
        self.axes.spines['right'].set_visible(False)
        self.axes.set_xlabel("Quantity (Q)")
        self.axes.set_ylabel("Price (P)")
        self.axes.set_xlim(0, None) #Make sure it starts at 0
        self.axes.set_ylim(0, None)

    def draw_market(self, q, p_demand, p_supply, q_eq=None, p_eq=None):
        self.axes.clear()
         
        self.axes.plot(q, p_demand, label="Demand", color="blue", linewidth=2) #Make it a little bolder
        self.axes.plot(q, p_supply, label="Supply", color="red", linewidth=2)
        
        if q_eq is not None and p_eq is not None: #If we can calculate an equilibrium, add one
            self.axes.axvline(x=q_eq, ymin=0, ymax=p_eq/self.axes.get_ylim()[1], color='gray', linestyle='--')
            self.axes.axhline(y=p_eq, xmin=0, xmax=q_eq/self.axes.get_xlim()[1], color='gray', linestyle='--')
            self.axes.plot(q_eq, p_eq, 'ko') #Black dot at intersection
            self.axes.text(q_eq + 1, p_eq + 1, f"E ({q_eq:.1f}, {p_eq:.1f})", weight='bold')

        self.axes.legend()
        self.draw()