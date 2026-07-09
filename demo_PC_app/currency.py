def format_vnd(amount):
    text = "{:,.0f}".format(amount)
    text = text.replace(",", ".")
    return text + " ₫"
