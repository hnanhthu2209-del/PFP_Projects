class Component:
    def __init__(self, component_id, name, category, price, stock):
        self.component_id = component_id
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock

    def __str__(self):
        return (f"[{self.component_id}] {self.name} | Category: {self.category} "
                f"| Price: ${self.price:.2f} | Stock: {self.stock}")
