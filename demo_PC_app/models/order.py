from currency import format_vnd


class Order:
    _next_id = 1

    def __init__(self, buyer_username, component_id, component_name, quantity, total_price):
        self.order_id = Order._next_id
        Order._next_id += 1
        self.buyer_username = buyer_username
        self.component_id = component_id
        self.component_name = component_name
        self.quantity = quantity
        self.total_price = total_price

    def __str__(self):
        return (f"Order #{self.order_id} | Buyer: {self.buyer_username} "
                f"| {self.component_name} x{self.quantity} | Total: {format_vnd(self.total_price)}")
