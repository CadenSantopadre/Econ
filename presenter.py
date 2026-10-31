class GraphPresenter:
    def __init__(self, view, model):
        self.view = view
        self.model = model

        # Connect UI events to presenter methods.
        self.view.supply_slider.valueChanged.connect(
            self.handle_supply_shift
        )

        self.view.demand_slider.valueChanged.connect(
            self.handle_demand_shift
        )

        # Draw the initial market.
        self.update_graph()

    def handle_supply_shift(self, value):
        self.model.set_supply_intercept(value)
        self.update_graph()

    def handle_demand_shift(self, value):
        self.model.set_demand_intercept(value)
        self.update_graph()

    def update_graph(self):
        q, p_demand, p_supply, q_eq, p_eq = (
            self.model.calculate_market()
        )

        self.view.canvas.draw_market(
            q,
            p_demand,
            p_supply,
            q_eq,
            p_eq
        )