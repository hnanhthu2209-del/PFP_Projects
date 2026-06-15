class PCModelSeries:
    def __init__(self, series_id, brand, name, category):
        self.series_id = series_id
        self.brand = brand
        self.name = name
        self.category = category  # e.g. Laptop, Desktop, Workstation

    def __str__(self):
        return f"[{self.series_id}] {self.brand} {self.name} ({self.category})"
