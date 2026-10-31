import numpy as np


class SupplyDemandModel:
    def __init__(self):
        self.supply_intercept = 10
        self.demand_intercept = 100

        self.supply_slope = 0.5
        self.demand_slope = 0.5

    def set_supply_intercept(self, value):
        self.supply_intercept = value

    def set_demand_intercept(self, value):
        self.demand_intercept = value

    def calculate_market(self):
        # Generate the quantity values for plotting.
        q = np.linspace(0, 100, 500)

        # Calculate the two curves.
        p_demand = self.demand_intercept - self.demand_slope * q
        p_supply = self.supply_intercept + self.supply_slope * q

        # Solve for equilibrium.
        denominator = self.supply_slope + self.demand_slope

        q_eq = (
            self.demand_intercept - self.supply_intercept
        ) / denominator

        p_eq = (
            self.demand_intercept
            - self.demand_slope * q_eq
        )

        # Only display an equilibrium within the positive market.
        if q_eq < 0 or p_eq < 0:
            q_eq = None
            p_eq = None

        return q, p_demand, p_supply, q_eq, p_eq