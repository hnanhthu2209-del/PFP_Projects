from currency import format_vnd


class Order:
    _next_id = 1

    def __init__(self, buyer_username, items):
        # items: list of (component_id, component_name, quantity, subtotal)
        self.order_id = Order._next_id
        Order._next_id += 1
        self.buyer_username = buyer_username
        self.items = items
        self.total_price = sum(subtotal for _, _, _, subtotal in items)

    def __str__(self):
        lines = [f"Order #{self.order_id} | Buyer: {self.buyer_username} | Total: {format_vnd(self.total_price)}"]
        for component_id, component_name, quantity, subtotal in self.items:
            lines.append(f"      - {component_name} x{quantity} = {format_vnd(subtotal)}")
        return "\n".join(lines)
