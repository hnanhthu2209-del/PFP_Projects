from currency import format_vnd


class Component:
    def __init__(self, component_id, name, category, price, stock, description="", compatible_with=None):
        self.component_id = component_id
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock
        self.description = description
        self.compatible_with = compatible_with if compatible_with is not None else []

    def __str__(self):
        return (f"[{self.component_id}] {self.name} | Category: {self.category} "
                f"| Price: {format_vnd(self.price)} | Stock: {self.stock}")

    def detail_str(self, series_resolver=None):
        lines = [str(self)]
        if self.description:
            lines.append(f"    Description : {self.description}")
        if self.compatible_with:
            if series_resolver:
                names = []
                for sid in self.compatible_with:
                    s = series_resolver(sid)
                    names.append(str(s) if s else f"[ID {sid}]")
                lines.append(f"    Compatible PC series:\n" +
                             "\n".join(f"      - {n}" for n in names))
            else:
                lines.append(f"    Compatible series IDs: {self.compatible_with}")
        return "\n".join(lines)
