from flask import Flask, flash, redirect, render_template, request, session, url_for

import data.store as store
from currency import format_vnd
from models.component import Component
from models.order import Order

app = Flask(__name__)
app.secret_key = "dev-secret-key"
app.jinja_env.filters["vnd"] = format_vnd


# ── AUTH ─────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    if "username" in session:
        if session["role"] == "admin":
            return redirect(url_for("admin_menu"))
        else:
            return redirect(url_for("buyer_menu"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        user = store.find_user(username)
        if user is None or user.password != password:
            flash("Invalid username or password.", "danger")
            return render_template("login.html")
        session["username"] = user.username
        session["role"] = user.role
        if user.role == "admin":
            return redirect(url_for("admin_menu"))
        else:
            return redirect(url_for("buyer_menu"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ── ADMIN: MENU ──────────────────────────────────────────────────────────────

@app.route("/admin")
def admin_menu():
    if "username" not in session or session["role"] != "admin":
        return redirect(url_for("login"))
    return render_template("admin/menu.html")


# ── ADMIN: COMPONENTS ────────────────────────────────────────────────────────

@app.route("/admin/components")
def admin_components():
    if "username" not in session or session["role"] != "admin":
        return redirect(url_for("login"))

    query = request.args.get("q", "").strip().lower()
    components = []
    for c in store.components:
        if query == "" or query in c.name.lower() or query in c.category.lower():
            components.append(c)
    return render_template("admin/components.html", components=components, query=query)


@app.route("/admin/components/add", methods=["GET", "POST"])
def admin_add_component():
    if "username" not in session or session["role"] != "admin":
        return redirect(url_for("login"))

    if request.method == "POST":
        try:
            name = request.form["name"].strip()
            category = request.form["category"].strip()
            price = int(float(request.form["price"]))
            stock = int(request.form["stock"])
            description = request.form.get("description", "").strip()
            component = Component(store.get_next_component_id(), name, category, price, stock, description)
            store.components.append(component)
            store.save_components()
            flash("Component added: " + component.name, "success")
            return redirect(url_for("admin_components"))
        except ValueError:
            flash("Invalid input. Component not added.", "danger")
    return render_template("admin/component_form.html")


@app.route("/admin/components/<int:component_id>")
def admin_component_detail(component_id):
    if "username" not in session or session["role"] != "admin":
        return redirect(url_for("login"))

    component = store.find_component_by_id(component_id)
    if component is None:
        flash("Component not found.", "danger")
        return redirect(url_for("admin_components"))

    compatible = []
    for series_id in component.compatible_with:
        compatible.append((series_id, store.find_series_by_id(series_id)))

    available = []
    for s in store.pc_model_series:
        if s.series_id not in component.compatible_with:
            available.append(s)

    return render_template("admin/component_detail.html",
                            component=component, compatible=compatible, available=available)


@app.route("/admin/components/<int:component_id>/compatible/add", methods=["POST"])
def admin_add_compatible(component_id):
    if "username" not in session or session["role"] != "admin":
        return redirect(url_for("login"))

    component = store.find_component_by_id(component_id)
    if component is not None:
        try:
            series_id = int(request.form["series_id"])
            series = store.find_series_by_id(series_id)
            if series is None:
                flash("Series not found.", "danger")
            elif series_id in component.compatible_with:
                flash("That series is already linked.", "danger")
            else:
                component.compatible_with.append(series_id)
                store.save_components()
                flash("Compatible series added.", "success")
        except ValueError:
            flash("Invalid series.", "danger")
    return redirect(url_for("admin_component_detail", component_id=component_id))


@app.route("/admin/components/<int:component_id>/compatible/remove/<int:series_id>", methods=["POST"])
def admin_remove_compatible(component_id, series_id):
    if "username" not in session or session["role"] != "admin":
        return redirect(url_for("login"))

    component = store.find_component_by_id(component_id)
    if component is not None and series_id in component.compatible_with:
        component.compatible_with.remove(series_id)
        store.save_components()
        flash("Compatible series removed.", "success")
    return redirect(url_for("admin_component_detail", component_id=component_id))


@app.route("/admin/components/<int:component_id>/compatible/clear", methods=["POST"])
def admin_clear_compatible(component_id):
    if "username" not in session or session["role"] != "admin":
        return redirect(url_for("login"))

    component = store.find_component_by_id(component_id)
    if component is not None:
        component.compatible_with.clear()
        store.save_components()
        flash("All compatible series cleared.", "success")
    return redirect(url_for("admin_component_detail", component_id=component_id))


# ── ADMIN: ORDERS ────────────────────────────────────────────────────────────

@app.route("/admin/orders")
def admin_orders():
    if "username" not in session or session["role"] != "admin":
        return redirect(url_for("login"))

    query = request.args.get("q", "").strip().lower()
    orders = []
    for o in store.orders:
        if query == "" or query in o.buyer_username.lower() or query in o.component_name.lower():
            orders.append(o)
    return render_template("admin/orders.html", orders=orders, query=query)


@app.route("/admin/orders/add", methods=["GET", "POST"])
def admin_add_order():
    if "username" not in session or session["role"] != "admin":
        return redirect(url_for("login"))

    if request.method == "POST":
        try:
            buyer = request.form["buyer"].strip()
            component = store.find_component_by_id(int(request.form["component_id"]))
            qty = int(request.form["quantity"])
            if component is None:
                flash("Component not found.", "danger")
            elif qty <= 0 or qty > component.stock:
                flash("Invalid quantity.", "danger")
            else:
                total = qty * component.price
                order = Order(buyer, component.component_id, component.name, qty, total)
                store.orders.append(order)
                component.stock -= qty
                store.save_orders()
                store.save_components()
                flash("Order added: " + str(order), "success")
                return redirect(url_for("admin_orders"))
        except ValueError:
            flash("Invalid input.", "danger")
    return render_template("admin/order_form.html", components=store.components)


# ── BUYER: MENU ──────────────────────────────────────────────────────────────

@app.route("/buyer")
def buyer_menu():
    if "username" not in session or session["role"] != "buyer":
        return redirect(url_for("login"))
    return render_template("buyer/menu.html")


@app.route("/buyer/search")
def buyer_search():
    if "username" not in session or session["role"] != "buyer":
        return redirect(url_for("login"))

    query = request.args.get("q", "").strip().lower()
    components = []
    if query != "":
        for c in store.components:
            if query in c.name.lower() or query in c.category.lower():
                components.append(c)
    return render_template("buyer/search.html", components=components, query=query)


@app.route("/buyer/components/<int:component_id>")
def buyer_component_detail(component_id):
    if "username" not in session or session["role"] != "buyer":
        return redirect(url_for("login"))

    component = store.find_component_by_id(component_id)
    if component is None:
        flash("Component not found.", "danger")
        return redirect(url_for("buyer_search"))

    compatible = []
    for series_id in component.compatible_with:
        compatible.append((series_id, store.find_series_by_id(series_id)))

    return render_template("buyer/component_detail.html", component=component, compatible=compatible)


@app.route("/buyer/components/<int:component_id>/buy", methods=["POST"])
def buyer_buy(component_id):
    if "username" not in session or session["role"] != "buyer":
        return redirect(url_for("login"))

    component = store.find_component_by_id(component_id)
    if component is None:
        flash("Component not found.", "danger")
        return redirect(url_for("buyer_search"))

    try:
        qty = int(request.form["quantity"])
        if component.stock <= 0:
            flash("Out of stock.", "danger")
        elif qty <= 0 or qty > component.stock:
            flash("Invalid quantity.", "danger")
        else:
            total = qty * component.price
            order = Order(session["username"], component.component_id, component.name, qty, total)
            store.orders.append(order)
            component.stock -= qty
            store.save_orders()
            store.save_components()
            flash("Order placed! " + str(order), "success")
    except ValueError:
        flash("Invalid input.", "danger")
    return redirect(url_for("buyer_component_detail", component_id=component_id))


@app.route("/buyer/orders")
def buyer_orders():
    if "username" not in session or session["role"] != "buyer":
        return redirect(url_for("login"))

    orders = []
    for o in store.orders:
        if o.buyer_username == session["username"]:
            orders.append(o)
    return render_template("buyer/orders.html", orders=orders)


if __name__ == "__main__":
    app.run(debug=True)
